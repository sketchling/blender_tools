import bpy


scene = bpy.context.scene
scene.use_nodes = True
#scene.node_tree.nodes.clear()

node_tree = scene.node_tree

#set up the file- out node
file_out =  node_tree.nodes.new("CompositorNodeOutputFile")


#If the current render directory is still at default but has been saved, set it inside the current blend files directory
#**********maybe add a render directory bit here in future******************
if bpy.data.scenes['Scene'].render.filepath == '/tmp\\' and bpy.data.is_saved:
    bpy.data.scenes['Scene'].render.filepath = bpy.path.abspath('//')

file_out.base_path = bpy.data.scenes['Scene'].render.filepath


file_out.format.file_format = 'PNG'
file_out.format.color_depth = '16'
file_out.format.color_mode = 'RGBA'


y = 0
x = 0
x_offset = 0


file_out.location.x = x+400
file_out.location.y = 600
 
#remove the first, unused slot
file_out.file_slots.remove(file_out.inputs[0])

#set up all the view layers as a 'render layer' node each
for i, view_layer in enumerate(bpy.data.scenes['Scene'].view_layers):
    x = 0 
    render_layers =  node_tree.nodes.new("CompositorNodeRLayers")
    render_layers.layer = view_layer.name
    
    
    
    #Then attatch these to the file out
    for output in render_layers.outputs:
        if output.enabled and ('Crypto' not in output.name) and ('Alpha' not in output.name) and ('Noisy' not in output.name) :
            if 'SO_' in view_layer.name:
                x_offset = -350
                if 'Image' in output.name:
                    slot = file_out.file_slots.new(view_layer.name)
                    node_tree.links.new(output, slot)
            else:
                slot = file_out.file_slots.new(output.name)
                node_tree.links.new(output, slot)
                y+= 100
                x_offset = 0
            
    #set secondary passes off to the side and down
    if i == 1:
        y -= 300
        
    render_layers.location.x = x + x_offset
    render_layers.location.y = y
    

    y -= 50
    
    #use offset to determine if it should be hidden
    if x_offset != 0:
        render_layers.hide = True
        
