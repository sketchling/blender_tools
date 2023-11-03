import bpy


use_existing_camera = False

selected_objects = bpy.context.selected_objects
if len(selected_objects) > 0:
    
    #First test if one of the objects is a camera
    for obj in selected_objects:
        if obj.type == 'CAMERA':
            projcam_object = obj
            projcam_object.data.lens_unit = 'FOV'
            use_existing_camera = True
             
            
        '''if use_existing_camera:
            #If there is an existing camera selected then set it up in the projection
            projcam.lens_unit -= 'FOV'
            projection_shader_1.inputs[1].default_value = projcam.angle
            projection_shader_1.inputs[2].default_value = bpy.context.scene.render.resolution_x
            projection_shader_1.inputs[3].default_value = bpy.context.scene.render.resolution_y
        else: 
            #Otherwise make a square projection stand in
            projection_shader_1.inputs[1].default_value = 1
            projection_shader_1.inputs[2].default_value = 4096
            projection_shader_1.inputs[3].default_value = 4096
            
            break #It uses the first camera it finds as the proj camera'''
            
        if 'projcam_object' not in locals():
            
            projcam_data = bpy.data.cameras.new(name = 'projcam')
            projcam_object = bpy.data.objects.new("projcam", projcam_data)
            scene = bpy.context.scene
            scene.collection.objects.link(projcam_object)
            
    mat = bpy.data.materials.new(name = "Projection_Shader")
    mat.use_nodes = True
    #initialize projection_shader node group
    projection_shader = mat.node_tree
    #start with a clean node tree
    for node in projection_shader.nodes:
        projection_shader.nodes.remove(node)
    #initialize projection_shader nodes
    #node Projection_Setup
    
    #projection_setup = projection_shader.nodes.new("NodeFrame")
    #projection_setup.label = "Projection Camera Setup"

    #node Frame
    frame = projection_shader.nodes.new("NodeFrame")
    frame.label = "Projection Camera Setup"

    #node Image Texture
    image_texture = projection_shader.nodes.new("ShaderNodeTexImage")
    image_texture.interpolation = 'Linear'
    image_texture.projection = 'FLAT'
    image_texture.extension = 'EXTEND'

    #node Texture Coordinate
    texture_coordinate = projection_shader.nodes.new("ShaderNodeTexCoord")
    #----------Make sure projcam in tex coordinates is set to whatever is created or selected at the start
    texture_coordinate.object = projcam_object

    #------------CAM PROJ NODE GROUP - Create a simple UI node for the complex undertech-----------------------
    cam_proj_group= bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "Cam_Proj_Group")

    #initialize cam_proj_group nodes
    #node Divide_03
    divide_03 = cam_proj_group.nodes.new("ShaderNodeMath")
    divide_03.operation = 'DIVIDE'
    divide_03.inputs[1].default_value = 2.0
    divide_03.inputs[2].default_value = 0.5

    #node Tangent_01
    tangent_01 = cam_proj_group.nodes.new("ShaderNodeMath")
    tangent_01.operation = 'TANGENT'
    tangent_01.inputs[1].default_value = 0.5
    tangent_01.inputs[2].default_value = 0.5

    #node Divide_04
    divide_04 = cam_proj_group.nodes.new("ShaderNodeMath")
    divide_04.operation = 'DIVIDE'
    divide_04.inputs[2].default_value = 0.5

    #node Divide_05
    divide_05 = cam_proj_group.nodes.new("ShaderNodeMath")
    divide_05.operation = 'DIVIDE'
    divide_05.inputs[2].default_value = 0.5

    
    #node Divide_02
    divide_02 = cam_proj_group.nodes.new("ShaderNodeMath")
    divide_02.operation = 'DIVIDE'
    divide_02.inputs[2].default_value = 0.5

    #node G_Input01
    g_input01 = cam_proj_group.nodes.new("NodeGroupInput")

    
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
    cam_proj_group.inputs[2].min_value = -3.4028234663852886e+38
    cam_proj_group.inputs[2].max_value = 3.4028234663852886e+38
    cam_proj_group.inputs[2].attribute_domain = 'POINT'

    #input Height
    cam_proj_group.inputs.new('NodeSocketFloat', "Height")
    cam_proj_group.inputs[3].default_value = 0.0
    cam_proj_group.inputs[3].min_value = -3.4028234663852886e+38
    cam_proj_group.inputs[3].max_value = 3.4028234663852886e+38
    cam_proj_group.inputs[3].attribute_domain = 'POINT'



    #node Separate XYZ
    separate_xyz = cam_proj_group.nodes.new("ShaderNodeSeparateXYZ")

    #node Mult_01
    mult_01 = cam_proj_group.nodes.new("ShaderNodeMath")
    mult_01.operation = 'MULTIPLY'
    #Value_001
    mult_01.inputs[1].default_value = -1.0
    #Value_002
    mult_01.inputs[2].default_value = 0.5

    #node G_Input02
    g_input02 = cam_proj_group.nodes.new("NodeGroupInput")

    #node Divide_06
    divide_06 = cam_proj_group.nodes.new("ShaderNodeMath")
    divide_06.operation = 'DIVIDE'
    #Value_002
    divide_06.inputs[2].default_value = 0.5

    #node Divide_01
    divide_01 = cam_proj_group.nodes.new("ShaderNodeMath")
    divide_01.operation = 'DIVIDE'
    #Value_002
    divide_01.inputs[2].default_value = 0.5

    #node Mult_02
    mult_02 = cam_proj_group.nodes.new("ShaderNodeMath")
    mult_02.operation = 'MULTIPLY'
    #Value_002
    mult_02.inputs[2].default_value = 0.5

    #node Combine XYZ
    combine_xyz = cam_proj_group.nodes.new("ShaderNodeCombineXYZ")
    #Z
    combine_xyz.inputs[2].default_value = 0.0

    #node V_Add_01
    v_add_01 = cam_proj_group.nodes.new("ShaderNodeVectorMath")
    v_add_01.operation = 'ADD'
    #Vector_001
    v_add_01.inputs[1].default_value = (1.0, 1.0, 1.0)
    #Vector_002
    v_add_01.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    v_add_01.inputs[3].default_value = 1.0

    #node V_Mult_01
    v_mult_01 = cam_proj_group.nodes.new("ShaderNodeVectorMath")
    v_mult_01.operation = 'MULTIPLY'
    #Vector_001
    v_mult_01.inputs[1].default_value = (0.5, 0.5, 0.0)
    #Vector_002
    v_mult_01.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    v_mult_01.inputs[3].default_value = 1.0

    #node G_Output
    g_output = cam_proj_group.nodes.new("NodeGroupOutput")
    
    
    #cam_proj_group outputs
    #output Vector
    cam_proj_group.outputs.new('NodeSocketVector', "Vector")
    cam_proj_group.outputs[0].default_value = (0.0, 0.0, 0.0)
    cam_proj_group.outputs[0].min_value = -3.4028234663852886e+38
    cam_proj_group.outputs[0].max_value = 3.4028234663852886e+38
    cam_proj_group.outputs[0].attribute_domain = 'POINT'

    #Set locations
    divide_03.location = (313, -212)
    tangent_01.location = (490, -209)
    divide_04.location = (747, 207)
    divide_05.location = (755,-68)

    divide_02.location = (351, 57)
    g_input01.location = (-357, 250)
    separate_xyz.location = (-147, 249)
    mult_01.location = (16, 77)
    g_input02.location = (1104, -159)
    divide_06.location = (1300, -123)
    divide_01.location = (352, 236)
    mult_02.location = (1469, 14)
    combine_xyz.location = (1917, 221)
    v_add_01.location = (2117, 174)
    v_mult_01.location = (2343, 231)
    g_output.location = (2560, 224)

    #Set dimensions
    divide_03.width, divide_03.height = 140.0, 100.0
    tangent_01.width, tangent_01.height = 140.0, 100.0
    divide_04.width, divide_04.height = 140.0, 100.0
    divide_05.width, divide_05.height = 140.0, 100.0
 
    divide_02.width, divide_02.height = 140.0, 100.0
    g_input01.width, g_input01.height = 140.0, 100.0
    separate_xyz.width, separate_xyz.height = 140.0, 100.0
    mult_01.width, mult_01.height = 140.0, 100.0
    g_input02.width, g_input02.height = 140.0, 100.0
    divide_06.width, divide_06.height = 140.0, 100.0
    divide_01.width, divide_01.height = 140.0, 100.0
    mult_02.width, mult_02.height = 140.0, 100.0
    combine_xyz.width, combine_xyz.height = 140.0, 100.0
    v_add_01.width, v_add_01.height = 140.0, 100.0
    v_mult_01.width, v_mult_01.height = 140.0, 100.0
    g_output.width, g_output.height = 140.0, 100.0

    #initialize cam_proj_group links
    #g_input01.Vector -> separate_xyz.Vector
    cam_proj_group.links.new(g_input01.outputs[0], separate_xyz.inputs[0])
    #separate_xyz.Z -> mult_01.Value
    cam_proj_group.links.new(separate_xyz.outputs[2], mult_01.inputs[0])
    #mult_01.Value -> divide_01.Value
    cam_proj_group.links.new(mult_01.outputs[0], divide_01.inputs[1])
    #mult_01.Value -> divide_02.Value
    cam_proj_group.links.new(mult_01.outputs[0], divide_02.inputs[1])
    #separate_xyz.X -> divide_01.Value
    cam_proj_group.links.new(separate_xyz.outputs[0], divide_01.inputs[0])

    #divide_03.Value -> tangent_01.Value
    cam_proj_group.links.new(divide_03.outputs[0], tangent_01.inputs[0])
    #divide_02.Value -> divide_05.Value
    cam_proj_group.links.new(divide_02.outputs[0], divide_05.inputs[0])
    #tangent_01.Value -> divide_05.Value
    cam_proj_group.links.new(tangent_01.outputs[0], divide_05.inputs[1])
    #divide_01.Value -> divide_04.Value
    cam_proj_group.links.new(divide_01.outputs[0], divide_04.inputs[0])
    #tangent_01.Value -> divide_04.Value
    cam_proj_group.links.new(tangent_01.outputs[0], divide_04.inputs[1])
    #divide_05.Value -> mult_02.Value
    cam_proj_group.links.new(divide_05.outputs[0], mult_02.inputs[0])
    #divide_06.Value -> mult_02.Value
    cam_proj_group.links.new(divide_06.outputs[0], mult_02.inputs[1])
    #divide_04.Value -> combine_xyz.X
    cam_proj_group.links.new(divide_04.outputs[0], combine_xyz.inputs[0])
    #mult_02.Value -> combine_xyz.Y
    cam_proj_group.links.new(mult_02.outputs[0], combine_xyz.inputs[1])
    #combine_xyz.Vector -> v_add_01.Vector
    cam_proj_group.links.new(combine_xyz.outputs[0], v_add_01.inputs[0])
    #v_add_01.Vector -> v_mult_01.Vector
    cam_proj_group.links.new(v_add_01.outputs[0], v_mult_01.inputs[0])
    #v_mult_01.Vector -> g_output.Vector
    cam_proj_group.links.new(v_mult_01.outputs[0], g_output.inputs[0])
    #separate_xyz.Y -> divide_02.Value
    cam_proj_group.links.new(separate_xyz.outputs[1], divide_02.inputs[0])
    #g_input02.Width -> divide_06.Value
    cam_proj_group.links.new(g_input02.outputs[2], divide_06.inputs[0])
    #g_input02.Height -> divide_06.Value
    cam_proj_group.links.new(g_input02.outputs[3], divide_06.inputs[1])
    #g_input01.FOV -> to_radians.Value
    cam_proj_group.links.new(g_input01.outputs[1], divide_03.inputs[0])
    
    
    #node cam_proj_group_Group
    cam_proj_group_group = projection_shader.nodes.new("ShaderNodeGroup")
    cam_proj_group_group.label = "Projection Camera Nodegroup"
    cam_proj_group_group.node_tree = bpy.data.node_groups["Cam_Proj_Group"]
    
    if use_existing_camera:
        #If there is an existing camera selected then set it up in the projection
        cam_proj_group_group.inputs[1].default_value = projcam_object.data.angle
        cam_proj_group_group.inputs[2].default_value = bpy.context.scene.render.resolution_x
        cam_proj_group_group.inputs[3].default_value = bpy.context.scene.render.resolution_y
    else: 
        #Otherwise make a square projection stand in
        cam_proj_group_group.inputs[1].default_value = 1
        cam_proj_group_group.inputs[2].default_value = 4096
        cam_proj_group_group.inputs[3].default_value = 4096
    

    #node Emission
    emission = projection_shader.nodes.new("ShaderNodeEmission")
    #Strength
    emission.inputs[1].default_value = 1.0
    #Weight
    emission.inputs[2].default_value = 0.0

    #node Material Output
    material_output = projection_shader.nodes.new("ShaderNodeOutputMaterial")
    material_output.target = 'ALL'
    #Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Thickness
    material_output.inputs[3].default_value = 0.0

    #Set parents
    #frame.parent = projection_setup
    image_texture.parent = frame
    texture_coordinate.parent = frame
    cam_proj_group_group.parent = frame

    #Set locations
    #projection_setup.location = (73.9127197265625, 467.888427734375)
    frame.location = (-184, -181)
    image_texture.location = (158, 79)
    texture_coordinate.location = (-203, 78)
    cam_proj_group_group.location = (-32, 67)
    emission.location = (432, 391)
    material_output.location = (673, 415)

    #Set dimensions
    #projection_setup.width, projection_setup.height = 721.0, 359.0
    frame.width, frame.height = 661.0, 299.0
    image_texture.width, image_texture.height = 240.0, 100.0
    texture_coordinate.width, texture_coordinate.height = 140.0, 100.0
    cam_proj_group_group.width, cam_proj_group_group.height = 140.0, 100.0
    emission.width, emission.height = 140.0, 100.0
    material_output.width, material_output.height = 140.0, 100.0

    #initialize projection_shader links
    #texture_coordinate.Object -> cam_proj_group_group.Vector
    projection_shader.links.new(texture_coordinate.outputs[3], cam_proj_group_group.inputs[0])
    #cam_proj_group_group.Vector -> image_texture.Vector
    projection_shader.links.new(cam_proj_group_group.outputs[0], image_texture.inputs[0])
    #image_texture.Color -> emission.Color
    projection_shader.links.new(image_texture.outputs[0], emission.inputs[0])
    #emission.Emission -> material_output.Surface
    projection_shader.links.new(emission.outputs[0], material_output.inputs[0])
    #node projection_shader

    # Assign the 'mat' material to all selected objects
    selected_objects = bpy.context.selected_objects
    for obj in selected_objects:
        if obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            #obj.data.materials.clear()  # Remove existing materials
            obj.data.materials.append(bpy.data.materials[mat.name])
            
            
