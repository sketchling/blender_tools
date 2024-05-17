import bpy

selected_objects = bpy.context.selected_objects

use_existing_camera = False
projcam_object = None

# Check for existing camera
for obj in selected_objects:
    if obj.type == 'CAMERA':
        projcam_object = obj
        projcam_object.data.lens_unit = 'FOV'
        use_existing_camera = True
        break

if not projcam_object:
    # Create a new camera if none exists
    projcam_data = bpy.data.cameras.new(name='projcam')
    projcam_object = bpy.data.objects.new("projcam", projcam_data)
    scene = bpy.context.scene
    scene.collection.objects.link(projcam_object)

mat = bpy.data.materials.new(name="Projection_Shader")
mat.use_nodes = True
projection_shader = mat.node_tree
mat.blend_method = 'HASHED'
mat.shadow_method = 'HASHED'

# Clear existing nodes
for node in projection_shader.nodes:
    projection_shader.nodes.remove(node)

# Create the camera projection nodes
"""Create the nodes within the material 'projection_shader'."""
nodes_y_offset = 200

# Create a frame for organization
frame = projection_shader.nodes.new("NodeFrame")
frame.label = "Projection Camera Setup"

# Create nodes
image_texture = projection_shader.nodes.new("ShaderNodeTexImage")
image_texture.interpolation = 'Linear'
image_texture.projection = 'FLAT'
image_texture.extension = 'EXTEND'
image_texture.parent = frame

texture_coordinate = projection_shader.nodes.new("ShaderNodeTexCoord")
texture_coordinate.object = projcam_object
texture_coordinate.parent = frame



"""Create the Camera Projection Node Group."""

cam_proj_group = bpy.data.node_groups.new(name='Cam_Proj_Group', type='ShaderNodeTree')

# Create input and output nodes for the node group
#group_inputs = cam_proj_group.nodes.new('NodeGroupInput')
#group_inputs.location = (-200, 0)
#group_outputs = cam_proj_group.nodes.new('NodeGroupOutput')
#group_outputs.location = (200, 0)

#As of blender 4x THIS HAS CHANGED so this next part is conditional 
# Get the Blender version
version = bpy.app.version
if version[0] >= 4:
    # Code for Blender versions before 4.0

  
    # Add input sockets to the group
    vector_socket = cam_proj_group.interface.new_socket(name='Vector', in_out='INPUT', socket_type='NodeSocketVector')
    fov_socket = cam_proj_group.interface.new_socket(name='FOV', in_out='INPUT', socket_type='NodeSocketFloat')
    width_socket = cam_proj_group.interface.new_socket(name='Width', in_out='INPUT', socket_type='NodeSocketFloat')
    height_socket = cam_proj_group.interface.new_socket(name='Height', in_out='INPUT', socket_type='NodeSocketFloat')

    # Set default values for input sockets
    vector_socket.default_value = (0.0, 0.0, 0.0)
    vector_socket.min_value = -10000.0
    vector_socket.max_value = 10000.0

    fov_socket.default_value = 0.5
    fov_socket.min_value = -10000.0
    fov_socket.max_value = 10000.0

    width_socket.default_value = 0.0
    width_socket.min_value = -3.402
    width_socket.max_value = 3.402

    height_socket.default_value = 0.0
    height_socket.min_value = -3.402
    height_socket.max_value = 3.402

    # Add an output socket to the group
    output_socket = cam_proj_group.interface.new_socket(name='OutputValue', in_out='OUTPUT', socket_type='NodeSocketFloat')    
    
    
else: #For older, pre v4x Blender...
    print('Pre blender 4 detected')
    cam_proj_group= bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "Cam_Proj_Group")
    #cam_proj_group inputs
    #input Vector
    cam_proj_group.inputs.new('NodeSocketVector', "Vector")
    cam_proj_group.inputs[0].default_value = (0.0, 0.0, 0.0)
    cam_proj_group.inputs[0].min_value = -10000.0
    cam_proj_group.inputs[0].max_value = 10000.0
    cam_proj_group.inputs[0].attribute_domain = 'POINT'

    #input FOV
    cam_proj_group.inputs.new('NodeSocketFloat', "FOV")
    cam_proj_group.inputs[1].default_value = 0.5
    cam_proj_group.inputs[1].min_value = -10000.0
    cam_proj_group.inputs[1].max_value = 10000.0
    cam_proj_group.inputs[1].attribute_domain = 'POINT'

    #input Width
    cam_proj_group.inputs.new('NodeSocketFloat', "Width")
    cam_proj_group.inputs[2].default_value = 0.0
    cam_proj_group.inputs[2].min_value = -3.402
    cam_proj_group.inputs[2].max_value = 3.402
    cam_proj_group.inputs[2].attribute_domain = 'POINT'

    #input Height
    cam_proj_group.inputs.new('NodeSocketFloat', "Height")
    cam_proj_group.inputs[3].default_value = 0.0
    cam_proj_group.inputs[3].min_value = -3.402
    cam_proj_group.inputs[3].max_value = 3.402
    cam_proj_group.inputs[3].attribute_domain = 'POINT'
    
      #cam_proj_group outputs
    #output Vector
    cam_proj_group.outputs.new('NodeSocketVector', "Vector")
    cam_proj_group.outputs[0].default_value = (0.0, 0.0, 0.0)
    cam_proj_group.outputs[0].min_value = -3.402
    cam_proj_group.outputs[0].max_value = 3.402
    cam_proj_group.outputs[0].attribute_domain = 'POINT'


# Initialize cam_proj_group nodes
nodes = {
    "g_input" :  cam_proj_group.nodes.new("NodeGroupInput"),
    "divide_03": cam_proj_group.nodes.new("ShaderNodeMath"),
    "tangent_01": cam_proj_group.nodes.new("ShaderNodeMath"),
    "divide_04": cam_proj_group.nodes.new("ShaderNodeMath"),
    "divide_05": cam_proj_group.nodes.new("ShaderNodeMath"),
    "divide_02": cam_proj_group.nodes.new("ShaderNodeMath"),
    "separate_xyz": cam_proj_group.nodes.new("ShaderNodeSeparateXYZ"),
    "mult_01": cam_proj_group.nodes.new("ShaderNodeMath"),
    "divide_06": cam_proj_group.nodes.new("ShaderNodeMath"),
    "divide_01": cam_proj_group.nodes.new("ShaderNodeMath"),
    "mult_02": cam_proj_group.nodes.new("ShaderNodeMath"),
    "combine_xyz": cam_proj_group.nodes.new("ShaderNodeCombineXYZ"),
    "v_add_01": cam_proj_group.nodes.new("ShaderNodeVectorMath"),
    "v_mult_01": cam_proj_group.nodes.new("ShaderNodeVectorMath"),
    "g_output": cam_proj_group.nodes.new("NodeGroupOutput"),
}

# Set node operations and default values
nodes["divide_03"].operation = 'DIVIDE'
nodes["divide_03"].inputs[1].default_value = 2.0
nodes["divide_03"].inputs[2].default_value = 0.5

nodes["tangent_01"].operation = 'TANGENT'
nodes["tangent_01"].inputs[1].default_value = 0.5
nodes["tangent_01"].inputs[2].default_value = 0.5

nodes["divide_04"].operation = 'DIVIDE'
nodes["divide_04"].inputs[2].default_value = 0.5

nodes["divide_05"].operation = 'DIVIDE'
nodes["divide_05"].inputs[2].default_value = 0.5

nodes["divide_02"].operation = 'DIVIDE'
nodes["divide_02"].inputs[2].default_value = 0.5

nodes["mult_01"].operation = 'MULTIPLY'
nodes["mult_01"].inputs[1].default_value = -1.0
nodes["mult_01"].inputs[2].default_value = 0.5

nodes["divide_06"].operation = 'DIVIDE'
nodes["divide_06"].inputs[2].default_value = 0.5

nodes["divide_01"].operation = 'DIVIDE'
nodes["divide_01"].inputs[2].default_value = 0.5

nodes["mult_02"].operation = 'MULTIPLY'
nodes["mult_02"].inputs[2].default_value = 0.5

nodes["combine_xyz"].inputs[2].default_value = 0.0

nodes["v_add_01"].operation = 'ADD'
nodes["v_add_01"].inputs[1].default_value = (1.0, 1.0, 1.0)
nodes["v_add_01"].inputs[2].default_value = (0.0, 0.0, 0.0)
nodes["v_add_01"].inputs[3].default_value = 1.0

nodes["v_mult_01"].operation = 'MULTIPLY'
nodes["v_mult_01"].inputs[1].default_value = (0.5, 0.5, 0.0)
nodes["v_mult_01"].inputs[2].default_value = (0.0, 0.0, 0.0)
nodes["v_mult_01"].inputs[3].default_value = 1.0

# Set locations
locations = {
    "g_input": (-357, 250),
    "divide_03": (313, -212),
    "tangent_01": (490, -209),
    "divide_04": (747, 207),
    "divide_05": (755, -68),
    "divide_02": (351, 57),
    "separate_xyz": (-147, 249),
    "mult_01": (16, 77),
    "divide_06": (1300, -123),
    "divide_01": (352, 236),
    "mult_02": (1469, 14),
    "combine_xyz": (1917, 221),
    "v_add_01": (2117, 174),
    "v_mult_01": (2343, 231),
    "g_output": (2560, 224),
}

for node_name, location in locations.items():
    if node_name in nodes:
        nodes[node_name].location = location
    else:
        locals()[node_name].location = location

# Create links between nodes
links = [
    (nodes['g_input'].outputs[0], nodes['separate_xyz'].inputs[0]),
    (nodes['separate_xyz'].outputs[2], nodes['mult_01'].inputs[0]),
    (nodes['mult_01'].outputs[0], nodes['divide_01'].inputs[1]),
    (nodes['mult_01'].outputs[0], nodes['divide_02'].inputs[1]),
    (nodes['separate_xyz'].outputs[0], nodes['divide_01'].inputs[0]),
    (nodes['divide_03'].outputs[0], nodes['tangent_01'].inputs[0]),
    (nodes['divide_02'].outputs[0], nodes['divide_05'].inputs[0]),
    (nodes['tangent_01'].outputs[0], nodes['divide_05'].inputs[1]),
    (nodes['divide_01'].outputs[0], nodes['divide_04'].inputs[0]),
    (nodes['tangent_01'].outputs[0], nodes['divide_04'].inputs[1]),
    (nodes['divide_05'].outputs[0], nodes['mult_02'].inputs[0]),
    (nodes['divide_06'].outputs[0], nodes['mult_02'].inputs[1]),
    (nodes['divide_04'].outputs[0], nodes['combine_xyz'].inputs[0]),
    (nodes['mult_02'].outputs[0], nodes['combine_xyz'].inputs[1]),
    (nodes['combine_xyz'].outputs[0], nodes['v_add_01'].inputs[0]),
    (nodes['v_add_01'].outputs[0], nodes['v_mult_01'].inputs[0]),
    (nodes['v_mult_01'].outputs[0], nodes['g_output'].inputs[0]),
    (nodes['separate_xyz'].outputs[1], nodes['divide_02'].inputs[0]),
    (nodes['g_input'].outputs['Width'], nodes['divide_06'].inputs[0]),
    (nodes['g_input'].outputs['Height'], nodes['divide_06'].inputs[1]),
    (nodes['g_input'].outputs['FOV'], nodes['divide_03'].inputs[0]),
]

for link in links:
    cam_proj_group.links.new(*link)

#----------------------------------------------
cam_proj_group_group = projection_shader.nodes.new("ShaderNodeGroup")
cam_proj_group_group.label = "Projection Camera Nodegroup"
cam_proj_group_group.node_tree = cam_proj_group
cam_proj_group_group.parent = frame

if use_existing_camera:
    # Set existing camera properties
    cam_proj_group_group.inputs['FOV'].default_value = projcam_object.data.angle
    cam_proj_group_group.inputs['Width'].default_value = bpy.context.scene.render.resolution_x
    cam_proj_group_group.inputs['Height'].default_value = bpy.context.scene.render.resolution_y
else:
    # Set default properties for the node group
    cam_proj_group_group.inputs['FOV'].default_value = 1
    cam_proj_group_group.inputs['Width'].default_value = 4096
    cam_proj_group_group.inputs['Height'].default_value = 4096

# Additional nodes
emission = projection_shader.nodes.new("ShaderNodeEmission")
n_trans_bsdf = projection_shader.nodes.new("ShaderNodeBsdfTransparent")
n_geometry = projection_shader.nodes.new("ShaderNodeNewGeometry")
n_mult = projection_shader.nodes.new("ShaderNodeMath")
n_mult.operation = 'MULTIPLY'
n_mix_shader = projection_shader.nodes.new("ShaderNodeMixShader")
n_invert = projection_shader.nodes.new("ShaderNodeInvert")
material_output = projection_shader.nodes.new("ShaderNodeOutputMaterial")

# Set node locations
locations = {
    "frame": (-184, 50 + nodes_y_offset),
    "n_geometry": (100, 600 + nodes_y_offset),
    "n_invert": (300, 600 + nodes_y_offset),
    "n_mult": (450, 600 + nodes_y_offset),
    "n_trans_bsdf": (450, 400 + nodes_y_offset),
    "emission": (450, 250 + nodes_y_offset),
    "n_mix_shader": (650, 400 + nodes_y_offset),
    "image_texture": (158, 0 + nodes_y_offset),
    "texture_coordinate": (-203, 0 + nodes_y_offset),
    "cam_proj_group_group": (-32, 0 + nodes_y_offset),
    "material_output": (900, 400 + nodes_y_offset),
}

for node_name, location in locations.items():
    locals()[node_name].location = location

# Create links between nodes
links = [
    (texture_coordinate.outputs['Object'], cam_proj_group_group.inputs['Vector']),
    (cam_proj_group_group.outputs[0], image_texture.inputs['Vector']),
    (image_texture.outputs['Color'], emission.inputs['Color']),
    (n_geometry.outputs['Backfacing'], n_invert.inputs['Color']),
    (n_invert.outputs['Color'], n_mult.inputs['Value']),
    (image_texture.outputs['Alpha'], n_mult.inputs[1]),
    (n_trans_bsdf.outputs['BSDF'], n_mix_shader.inputs['Shader']),
    (n_mult.outputs['Value'], n_mix_shader.inputs['Fac']),
    (emission.outputs['Emission'], n_mix_shader.inputs[2]),
    (n_mix_shader.outputs['Shader'], material_output.inputs['Surface']),
]

for link in links:
    projection_shader.links.new(*link)




# Assign the material to all selected objects
for obj in selected_objects:
    if obj.type == 'MESH':
        obj.data.materials.clear()
        obj.data.materials.append(mat)
