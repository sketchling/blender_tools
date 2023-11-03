#This sets up a view layer with an override for the current shader

import bpy
for object in bpy.context.selected_objects:
    if object.type == "MESH":
        #obj = bpy.data.objects[bpy.context.selected_objects[0].name]
        material = object.active_material

        #Duplicate shader to save it from accidental edits in the main view layer & make it a better name
        new_material = material.copy()
        new_material.name = 'C_' + material.name
        shader_name = new_material.name
        #pre-pend 'SO_' so that the render output passes can know only to include the combined channel from these layers
        new_view =  bpy.context.scene.view_layers.new('SO_' + shader_name)
        new_view.material_override = new_material
        break
