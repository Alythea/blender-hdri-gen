import bpy
from .utils.util_enum_population import populate_enum_reflective, populate_enum_objects, populate_enum_collections

class ObjectListItem (bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(
        name="Name of item",
        default="Object"
    )
    
    object_number :bpy.props.IntProperty(
        name="Amount of Objects",
        description="Sets the number of randomly placed objects in the scene",
        min=0,
        default=0
    ) 
    
    enum_object_mat : bpy.props.EnumProperty(
        name="Object Material",
        description="Sets the object material",
        items=populate_enum_reflective
    )
    
    object_shape : bpy.props.EnumProperty(
        name="Object Shape",
        description="Sets the object shape",
        items=[('cube', "Cube",""),
                ('sphere', "Sphere",""),
                ('ico_sphere', "Ico Sphere",""),
                ('cylinder', "Cylinder",""),
                ('cone', "Cone",""),
                ('custom', "Custom",""),
                ('collection', "Collection",""),   
        ],
        default='cube'
    )
    
    custom_object : bpy.props.EnumProperty(
        name="Select object",
        description="Selects custom object",
        items=populate_enum_objects
    )
    
    custom_collection : bpy.props.EnumProperty(
        name="Select collection",
        description="Selects custom collection",
        items=populate_enum_collections
    )

    object_seed :bpy.props.IntProperty(
        name="Object in scene seed",
        description="Sets the seed for placing objects",
        min=0,
        default=0
    )
    

class LightListItem (bpy.types.PropertyGroup):
    
    name : bpy.props.StringProperty(
        name="Name of item",
        default="Light"
    )
    
    light_location_x : bpy.props.FloatProperty(
        name="Light Location X",
        description="Sets X coordinate of light",
        default=0
    )
    
    light_location_y : bpy.props.FloatProperty(
        name="Light Location Y",
        description="Sets Y coordinate of light",
        default=0
    )
    
    light_location_z : bpy.props.FloatProperty(
        name="Light Location Z",
        description="Sets Z coordinate of light",
        default=0
    )
    
    light_colour : bpy.props.FloatVectorProperty(
        name="Light Colour",
        description="Sets colour of light",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0)
    )
    
    light_strength : bpy.props.FloatProperty(
        name="Light Power",
        subtype="POWER",
        description="Sets power of light",
        default=1000,
        min=0
    )
    
def register():
    bpy.utils.register_class(LightListItem)
    bpy.utils.register_class(ObjectListItem)  
    bpy.types.Scene.light_list = bpy.props.CollectionProperty(type = LightListItem)
    bpy.types.Scene.light_list_index = bpy.props.IntProperty(name = "Index for light_list", default = 0)
    bpy.types.Scene.object_list = bpy.props.CollectionProperty(type = ObjectListItem)
    bpy.types.Scene.object_list_index = bpy.props.IntProperty(name = "Index for object_list", default = 0)
    
def unregister():
    del bpy.types.Scene.light_list_index
    del bpy.types.Scene.light_list
    del bpy.types.Scene.object_list_index
    del bpy.types.Scene.object_list
    bpy.utils.unregister_class(ObjectListItem)
    bpy.utils.unregister_class(LightListItem)