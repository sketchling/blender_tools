import bpy

current_view = bpy.context.window.view_layer

view = bpy.context.scene.view_layers[current_view.name]

view.use_pass_mist= True
view.use_pass_position= True
view.use_pass_normal= True
view.use_pass_diffuse_direct= True
view.use_pass_glossy_direct= True
view.use_pass_ambient_occlusion= True
view.use_pass_transmission_color= True



