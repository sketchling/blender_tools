import bpy
import math

def set_clipboard_text(text):
    bpy.context.window_manager.clipboard = text

def convert_cam_for_nuke(name = 'Camera'):
    
    cam_obj = bpy.data.objects[name]
    lens = bpy.data.cameras[name].lens
    
    # Convert from Blender's camera rotation format to Nuke's
    euler_radians = (cam_obj.rotation_euler[0], cam_obj.rotation_euler[2],  cam_obj.rotation_euler[1])
    cam_rotation = (90-math.degrees(euler_radians[0]),
                    math.degrees(euler_radians[1]) ,
                    math.degrees(euler_radians[2])*-1)
        
    #format the data into the nuke 'set cut paste format'
    cam_text = ('Camera {\n'
    ' translate {'
    f'{cam_obj.location[0]} {cam_obj.location[2]} {cam_obj.location[1] *-1}'
    '}\n'
    ' rot_order XYZ'
    ' rotate {'
    f'{-cam_rotation[0] } {cam_rotation[1]}  {cam_rotation[2] }'
    '}\n'
    ' scaling {1.0 1.0 1.0}\n'
    f'focal {lens}\n'

    ' haperture 36\n'
    ' vaperture 24\n'
    ' near 1\n'
    ' far 1000\n'
    ' focal_point 30\n'
    ' fstop 2.799999952\n'
    ' name proj_cam\n'
    '}\n')
    return cam_text



cams = [obj for obj in bpy.context.selected_objects if obj.type == 'CAMERA']
converted_cams = ''
for cam in cams:
    converted_cams = converted_cams + '\n' + convert_cam_for_nuke(cam.name)
# Example usage:
set_clipboard_text()


#bpy.data.objects["Camera"].location[0]

