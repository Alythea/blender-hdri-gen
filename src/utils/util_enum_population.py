import bpy

def populate_enum_reflective(scene, context):
    items = [("Default_Reflective_Material","Default_Reflective_Material","","",0)]
    i = 1
    for material in bpy.data.materials:    
        items.append((material.name, material.name,"","",i),)
        i += 1
    return items

def populate_enum_mountain(scene, context):
    items = [("Default_Mountain_Material","Default_Mountain_Material","","",0)]
    i = 1
    for material in bpy.data.materials:    
        items.append((material.name, material.name,"","",i),)
        i += 1
    return items

def populate_enum_forest_floor(scene, context):
    items = [("Default_Terrain_Material","Default_Terrain_Material","","",0)]
    i = 1
    for material in bpy.data.materials:    
        items.append((material.name, material.name,"","",i),)
        i += 1
    return items

def populate_enum_objects(scene, context):
    items = []
    i = 0
    for object in bpy.data.objects:    
        items.append((object.name, object.name,"","",i),)
        i += 1
    return items

def populate_enum_collections(scene, context):
    items = []
    i = 0
    for collection in bpy.data.collections:    
        items.append((collection.name, collection.name,"","",i),)
        i += 1
    return items