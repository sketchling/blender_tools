#This script sets the mist pass start and end to match the closest and furthest mesh object
#If nothing is selected all mesh objects are considered. 
#If one mesh selected, that and the camera are compared.
#If multiple meshes are selected it will set the Start to the closest and the end to the furthest.


import bpy
import mathutils

def get_distance(obj, camera):
    """Calculate the distance between an object and the camera."""
    return (camera.location - obj.location).length

def main():
    scene = bpy.context.scene
    camera = scene.camera

    if not camera:
        print("No active camera found in the scene.")
        return

    # Get selected objects or all mesh objects if none are selected
    selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    objects = selected_objects if selected_objects else [obj for obj in scene.objects if obj.type == 'MESH']

    if not objects:
        print("No mesh objects found in the scene.")
        return

    # Ensure there are at least two objects for comparison
    if len(objects) == 1:
        objects.append(camera)

    # Calculate distances from the camera to each object
    distances = [get_distance(obj, camera) for obj in objects]
    
    min_distance = min(distances)
    max_distance = max(distances)
    
    # Adjust max distance to ensure the furthest object is still slightly darker than white
    mist_factor = 0.95  # Adjust this factor to control how much darker the furthest object will be
    mist_end = max_distance * mist_factor
    
    # Set mist settings
    if not scene.world:
        scene.world = bpy.data.worlds.new("World")

    world = scene.world
    if not world.mist_settings:
        world.mist_settings = world

    world.mist_settings.use_mist = True
    world.mist_settings.start = min_distance
    world.mist_settings.depth = mist_end - min_distance

    print(f"Mist Start: {min_distance}")
    print(f"Mist End: {mist_end}")

# Run the main function
main()
