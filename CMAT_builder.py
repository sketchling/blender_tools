import bpy

'''
Creates a series of useful concept art shaders
DIFFUSE LIGHT - Just an alpha for any light - simplifies light to shapes for painting
FRESNEL - Facing ratio mask
EDGE MATT - A slightly wonky alpha for any sharp edges in the geometry
DIRTY OCCLUSION - an imperfect mask for occlusion to compliment the standard variety.

'''

#First set up the current view layer with quick render settings and passes 
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.cycles.samples = 8
bpy.context.scene.cycles.adaptive_threshold = 1
bpy.context.scene.cycles.use_denoising = True

current_view = bpy.context.window.view_layer
view = bpy.context.scene.view_layers[current_view.name]

view.use_pass_mist= True
view.use_pass_position= True
view.use_pass_normal= True
view.use_pass_diffuse_direct= True
view.use_pass_diffuse_color= True
view.use_pass_glossy_direct= True
view.use_pass_ambient_occlusion= True
view.use_pass_transmission_color= True

#Then make the environment backdrop to black

#bpy.context.scene.render.film_transparent = True
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)



#node spacing variable
spacing = 300
wide_spacing = spacing + 100

def mat_to_override(material):
    #shader overrides have to be done in Cycles 
    bpy.context.scene.render.engine = 'CYCLES'

    shader_name = material.name
    #pre-pend 'SO_' so that the render output passes can know only to include the combined channel from these layers
    current_view = bpy.context.view_layer
    new_view =  bpy.context.scene.view_layers.new('SO_' + shader_name)
    new_view.material_override = material
    #return to the existing View Layer
    bpy.context.window.view_layer= current_view


#---------------------------------BW DIFFUSE LIGHT SHADER --------------

mat = bpy.data.materials.new(name = 'CMAT_JUST_BW_LIGHT')
mat.use_nodes = True
mat_single_light = mat.node_tree
for node in mat_single_light.nodes:
        mat_single_light.nodes.remove(node)

#MAKE NODES
light_path = mat_single_light.nodes.new(type ="ShaderNodeLightPath")
col_ramp = mat_single_light.nodes.new(type ="ShaderNodeValToRGB")
bsdf = mat_single_light.nodes.new(type ="ShaderNodeBsdfPrincipled")
output = mat_single_light.nodes.new(type ="ShaderNodeOutputMaterial")

#POSITION THE NODES

light_path.location.y = 0
col_ramp.location.y = 0
bsdf.location.y = 0
output.location.y = 0
light_path.location.x = 100
col_ramp.location.x = spacing
bsdf.location.x =spacing *2
output.location.x = spacing *3

#LINK THEM
mat_single_light.links.new(light_path.outputs[2], col_ramp.inputs[0])
mat_single_light.links.new(col_ramp.outputs['Color'], bsdf.inputs[0])
mat_single_light.links.new( bsdf.outputs['BSDF'], output.inputs['Surface'])


#Now make a new shader override view layer for this shader
mat_to_override(mat)


#--------------------------------------CHEAP ID PASS SHADER --------------

mat = bpy.data.materials.new(name = 'CMAT_CHEAP_ID_PASS')
mat.use_nodes = True
mat_single_light = mat.node_tree
for node in mat_single_light.nodes:
        mat_single_light.nodes.remove(node)

#MAKE NODES
id_mat = mat_single_light.nodes.new(type ="ShaderNodeObjectInfo")
normalize = mat_single_light.nodes.new(type ="ShaderNodeVectorMath")
output = mat_single_light.nodes.new(type ="ShaderNodeOutputMaterial")

#POSITION THE NODES

id_mat.location.y = 0
normalize.location.y = 0
output.location.y = 0
id_mat.location.x = 100
normalize.location.x = spacing
output.location.x = spacing *2 -100

normalize.operation = 'NORMALIZE'

#LINK THEM
mat_single_light.links.new(id_mat.outputs[0], normalize.inputs['Vector'])
mat_single_light.links.new(normalize.outputs['Vector'], output.inputs['Surface'])


#Now make a new shader override view layer for this shader
mat_to_override(mat)

#---------------------------------------------BW FRESNEL SHADER --------------

mat = bpy.data.materials.new(name = 'CMAT_FRESNEL')
mat.use_nodes = True
mat_single_light = mat.node_tree
for node in mat_single_light.nodes:
        mat_single_light.nodes.remove(node)

#MAKE NODES
layer_weight = mat_single_light.nodes.new(type ="ShaderNodeLayerWeight")
output = mat_single_light.nodes.new(type ="ShaderNodeOutputMaterial")

#SET NODE INFO
layer_weight.inputs[0].default_value = 0.1

#POSITION THE NODES

layer_weight.location.y = 0
output.location.y = 0
layer_weight.location.x = 100
output.location.x = spacing


#LINK THEM
mat_single_light.links.new(layer_weight.outputs[0], output.inputs['Surface'])

#Now make a new shader override view layer for this shader
mat_to_override(mat)

#---------------------------------------BW EDGE BEVEL SHADER --------------

mat = bpy.data.materials.new(name = 'CMAT_WONKY_EDGES')
mat.use_nodes = True
mat_node_tree = mat.node_tree
for node in mat_node_tree.nodes:
        mat_node_tree.nodes.remove(node)

#MAKE NODES
geo = mat_node_tree.nodes.new(type ="ShaderNodeNewGeometry")
noise = mat_node_tree.nodes.new(type ="ShaderNodeTexNoise")
col_ramp1 = mat_node_tree.nodes.new(type ="ShaderNodeValToRGB")
bevel =  mat_node_tree.nodes.new(type ="ShaderNodeBevel")
dot_product =  mat_node_tree.nodes.new(type ="ShaderNodeVectorMath")
col_ramp2 = mat_node_tree.nodes.new(type ="ShaderNodeValToRGB")
output = mat_node_tree.nodes.new(type ="ShaderNodeOutputMaterial")

#SET NODE INFO

noise.inputs['Scale'].default_value = 2
noise.inputs['Detail'].default_value = 1
noise.inputs['Roughness'].default_value = 1

col_ramp1.color_ramp.elements[1].color = (0.049,0.049,0.049,1)
col_ramp1.color_ramp.elements[0].position = 0.236
col_ramp2.color_ramp.elements[0].color = (1,1,1,1)
col_ramp2.color_ramp.elements[1].color = (0,0,0,1)


dot_product.operation = 'DOT_PRODUCT'


#POSITION THE NODES

geo.location.y = -20
noise.location.y = -spacing
col_ramp1.location.y = -spacing
bevel.location.y = -spacing
dot_product.location.y = 0
col_ramp2.location.y =0
output.location.y = 0

geo.location.x = 0
noise.location.x = spacing
col_ramp1.location.x = spacing *2
bevel.location.x = spacing *3 +100
dot_product.location.x = spacing*4
col_ramp2.location.x =spacing *5
output.location.x = spacing *6 + 100


#LINK THEM
mat_node_tree.links.new(geo.outputs['Position'], noise.inputs['Vector']) 
mat_node_tree.links.new(geo.outputs['Normal'], dot_product.inputs[0])
mat_node_tree.links.new(noise.outputs['Fac'], col_ramp1.inputs['Fac'])
mat_node_tree.links.new(col_ramp1.outputs['Color'], bevel.inputs['Radius'])
mat_node_tree.links.new(bevel.outputs['Normal'], dot_product.inputs[1])
mat_node_tree.links.new(dot_product.outputs['Value'], col_ramp2.inputs['Fac'])
mat_node_tree.links.new(col_ramp2.outputs['Color'], output.inputs['Surface'])



#Now make a new shader override view layer for this shader
mat_to_override(mat)

#-----------------------------------------BW DIRTY OCCLUSION SHADER --------------

mat = bpy.data.materials.new(name = 'CMAT_DIRTY_OCCLUSION')
mat.use_nodes = True
mat_node_tree = mat.node_tree
for node in mat_node_tree.nodes:
        mat_node_tree.nodes.remove(node)

#MAKE NODES
tex_coord = mat_node_tree.nodes.new(type ="ShaderNodeTexCoord")
mapping = mat_node_tree.nodes.new(type ="ShaderNodeMapping")
noise1 = mat_node_tree.nodes.new(type ="ShaderNodeTexNoise")
noise2 = mat_node_tree.nodes.new(type ="ShaderNodeTexNoise")
voronoi = mat_node_tree.nodes.new(type ="ShaderNodeTexVoronoi")

col_ramp1 = mat_node_tree.nodes.new(type ="ShaderNodeValToRGB")
mix =  mat_node_tree.nodes.new(type ="ShaderNodeMix")

ambient_occ1 =  mat_node_tree.nodes.new(type ="ShaderNodeAmbientOcclusion")
ambient_occ2 =  mat_node_tree.nodes.new(type ="ShaderNodeAmbientOcclusion")

col_ramp2 = mat_node_tree.nodes.new(type ="ShaderNodeValToRGB")

mult =  mat_node_tree.nodes.new(type ="ShaderNodeMath")
output = mat_node_tree.nodes.new(type ="ShaderNodeOutputMaterial")



#SET NODE INFO

mapping.inputs['Scale'].default_value = (12.6,16.6,12.6)



noise1.inputs['Scale'].default_value = 10
noise1.inputs['Detail'].default_value = 0
noise1.inputs['Roughness'].default_value = 1
noise1.inputs['Distortion'].default_value = 9.47


noise2.inputs['Scale'].default_value = -2.43
noise2.inputs['Detail'].default_value = 15
noise2.inputs['Roughness'].default_value = 1
noise2.inputs['Distortion'].default_value = 3.15

voronoi.inputs['Scale'].default_value = -2.71
voronoi.feature = 'DISTANCE_TO_EDGE'

mix.inputs[0].default_value = 0.408

col_ramp1.color_ramp.elements[0].position = 0.2
col_ramp1.color_ramp.elements[1].position = 0.3

ambient_occ2.inputs['Distance'].default_value= 1.09

mult.operation = 'MULTIPLY'


col_ramp2.color_ramp.elements[0].color = (1,1,1,1)
col_ramp2.color_ramp.elements[0].position = 0.073
col_ramp2.color_ramp.elements[1].position = 0.773
col_ramp2.color_ramp.elements[1].color = (0,0,0,1)

#POSITION THE NODES

tex_coord.location.y = 0
mapping.location.y = 0
noise1.location.y = 0 

noise2.location.y = 120
voronoi.location.y = 120

col_ramp1.location.y = 0
mix.location.y = 0
ambient_occ1.location.y = 0
ambient_occ2.location.y = -120
col_ramp2.location.y = 0
mult.location.y = 0
output.location.y = 0

#-------now x
tex_coord.location.x = 0
mapping.location.x = spacing
noise1.location.x = spacing*2

noise2.location.x = spacing*3
voronoi.location.x = spacing*4

mix.location.x = spacing*5
col_ramp1.location.x = spacing*6
ambient_occ1.location.x = wide_spacing + spacing*6
ambient_occ2.location.x = ambient_occ1.location.x

mult.location.x = spacing*7 + wide_spacing
col_ramp2.location.x = spacing*8 + wide_spacing

output.location.x = spacing*8 + wide_spacing*2



#LINK THEM
mat_node_tree.links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
mat_node_tree.links.new(mapping.outputs['Vector'], noise1.inputs['Vector'])
mat_node_tree.links.new(noise1.outputs['Fac'], mix.inputs[2])
mat_node_tree.links.new(noise1.outputs['Color'], ambient_occ2.inputs['Color'])

mat_node_tree.links.new(noise2.outputs['Fac'], voronoi.inputs['Vector'])
mat_node_tree.links.new(voronoi.outputs['Distance'], mix.inputs['B'])

mat_node_tree.links.new(mix.outputs['Result'], col_ramp1.inputs['Fac'])
mat_node_tree.links.new(col_ramp1.outputs['Color'], ambient_occ1.inputs['Distance'])
mat_node_tree.links.new(ambient_occ1.outputs['AO'], mult.inputs[0])
mat_node_tree.links.new(ambient_occ2.outputs['AO'], mult.inputs[1])
mat_node_tree.links.new(mult.outputs['Value'], col_ramp2.inputs['Fac'])
mat_node_tree.links.new(col_ramp2.outputs['Color'], output.inputs['Surface'])

mat_to_override(mat)
