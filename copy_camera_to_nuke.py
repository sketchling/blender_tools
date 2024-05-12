import bpy
import math

def set_clipboard_text(text):
    bpy.context.window_manager.clipboard = text


cam_obj = bpy.data.objects["Camera"]

#Convert Euler angles from Blender (RHS, X-Y-Z order) to Nuke (LHS, Z-Y-X order)


# Convert from Blender's camera rotation format to Nuke's
euler_radians = (cam_obj.rotation_euler[0], cam_obj.rotation_euler[2],  cam_obj.rotation_euler[1])
cam_rotation = (90-math.degrees(euler_radians[0]),
                math.degrees(euler_radians[1]) ,
                math.degrees(euler_radians[2])*-1)
    

cam = ('Camera {\n'
' translate {'
f'{cam_obj.location[0]} {cam_obj.location[2]} {cam_obj.location[1] *-1}'
'}\n'
' rot_order XYZ'
' rotate {'
f'{-cam_rotation[0] } {cam_rotation[1]}  {cam_rotation[2] }'
'}\n'
' scaling {1.000000014 0.9999999806 1.000000009}\n'


' haperture 36\n'
' vaperture 24\n'
' near 0.1000000015\n'
' far 100\n'
' focal_point 10\n'
' fstop 2.799999952\n'
' name proj_cam\n'
'}\n')

# Example usage:
set_clipboard_text(cam)


#bpy.data.objects["Camera"].location[0]

