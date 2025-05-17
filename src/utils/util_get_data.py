import bpy
import os
import time

def import_base_material(mat_name):
    script_file = os.path.realpath(__file__)
    directory = os.path.dirname(script_file)
    filepath = os.path.join(directory, "imports", "import.blend")
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        if mat_name in data_from.materials:
            data_to.materials = [mat_name]
        else:
            print(f"Material '{mat_name}' not found in {filepath}")

def get_material(mat_name):
    if (mat_name == "Default_Mountain_Material" or mat_name == "Default_Emission_Material" or mat_name == "Default_Reflective_Material" or mat_name == "Default_Leaves_Material" or mat_name == "Default_Terrain_Material" or mat_name == "Default_Tree_Material") and mat_name not in bpy.data.materials:
        import_base_material(mat_name)
        time.sleep(5)
        return bpy.data.materials[mat_name]
    if mat_name in bpy.data.materials:
        return bpy.data.materials[mat_name]
    else:
        return None
    
def get_object(object_name):
    if object_name in bpy.data.objects:
        return bpy.data.objects[object_name]
    else:
        return None
    
def get_collection(collection_name):
    if collection_name in bpy.data.collections:
        return bpy.data.collections[collection_name]
    else:
        return None