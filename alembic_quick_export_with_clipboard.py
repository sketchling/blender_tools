import bpy
import os 

def set_clipboard_text(text):
    bpy.context.window_manager.clipboard = text

def export_geo(file_name = 'projection_geo.abc'):
    
    #Set path to match current file    
    file_path = os.path.join(os.path.dirname(bpy.data.filepath, file_name)
    
    # Get the selected objects
    selected_objects = bpy.context.selected_objects
    
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    
    # Get the meshes and curves
    meshes_curves_cams = [obj for obj in selected_objects if obj.type in ['MESH', 'CURVE','CAMERA']]
    # Set the export file path and name
    for obj in meshes_curves_cams:
        obj.select_set(True)

    # Set the export operator properties
    bpy.ops.wm.alembic_export(
        filepath=file_path,
        selected=True,
        visible_objects_only=True,
        #flatten=True,
        curves_as_mesh=True,
        start=1,
        end=1
    )
    for obj in selected_objects:
        obj.select_set(True)

    return file_path

set_clipboard_text(export_geo())
