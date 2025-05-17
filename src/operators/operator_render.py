import bpy
import tempfile
import string
import random
import os
import shutil
import math
from ..utils.util_abstract_gen import *
from ..utils.util_enum_population import *
from ..utils.util_camera import *
from ..utils.util_get_data import *
from ..utils.util_sky_gen import *
from ..utils.util_terrain_gen import *

class RenderImage(bpy.types.Operator):
    """ Sets up the scene, renders an HDR image out of it and loads it into this node.
    """
    bl_idname = "hdri.render"
    bl_label = "Render HDRI"
    
    
    fileName : bpy.props.StringProperty(
    name="Name of the image",
    description="This image is used to store the render",
    default="")
    
    shape : bpy.props.StringProperty(
        name="Shape",
        description="Holds the information of the shape of the room between classes",
        default="Cube"
    )
    
    subdivisions : bpy.props.IntProperty(
        name="Subdivisions",
        description="Sets the subdivision parameter for the resulting icosphere render",
        min=1,
        default=1
    )
    
    width : bpy.props.FloatProperty(
        name="Width",
        description="Sets width of the rendered room",
        min=1,
        default=1
    )
    
    height : bpy.props.FloatProperty(
        name="Height",
        description="Sets height of the rendered room",
        min=1,
        default=1
    )
    
    blur_strength : bpy.props.IntProperty(
        name="Blur Strength",
        description="Sets the blur strength of the rendered picture",
        min=0,
        max=10,
        default=0
    ) 
    
    enum_floor_mat : bpy.props.EnumProperty(
        name="Floor Material",
        description="Sets the floor material",
        items=populate_enum_reflective
    )
    
    enum_ceiling_mat : bpy.props.EnumProperty(
        name="Ceiling Material",
        description="Sets the ceiling material",
        items=populate_enum_reflective
    )
    
    enum_fwall_mat : bpy.props.EnumProperty(
        name="Front Wall Material",
        description="Sets the front wall material",
        items=populate_enum_reflective
    )
    
    enum_rwall_mat : bpy.props.EnumProperty(
        name="Right Wall Material",
        description="Sets the right wall material",
        items=populate_enum_reflective
    )
    
    enum_lwall_mat : bpy.props.EnumProperty(
        name="Left Wall Material",
        description="Sets the left wall material",
        items=populate_enum_reflective
    )
    
    enum_bwall_mat : bpy.props.EnumProperty(
        name="Back Wall Material",
        description="Sets the back wall material",
        items=populate_enum_reflective
    )
    
    cloud_seed : bpy.props.FloatProperty(
        name="Clouds Seed",
        description="Seed for the rendered clouds.",
        default=0
    )
    
    sun_size : bpy.props.FloatProperty(
        name="Sun Size",
        subtype='ANGLE',
        description="Size of the sun disc.",
        default=math.radians(2),
        min=0
    )
    
    sun_elevation : bpy.props.FloatProperty(
        name="Sun Elevation",
        subtype='ANGLE',
        description="Sun elevation from the horizon.",
        default=math.radians(10),
        min=0
    )
    
    altitude : bpy.props.FloatProperty(
        name="Altitude",
        unit='LENGTH',
        description="Height from sea level",
        default=0,
        min=0
    )
    
    air : bpy.props.FloatProperty(
        name="Air",
        description="Density of air molecules.\\n \\u2022 0 - No air \\n \\u2022 1 - Clear day atmosphere \\n \\u2022 2 - Highly polluted day",
        default=1,
        min=0,
        max=10
    )
    
    dust : bpy.props.FloatProperty(
        name="Dust",
        description="Density of dust molecules and water droplets.\\n \\u2022 0 - No dust \\n \\u2022 1 - Clear day atmosphere \\n \\u2022 5 - City like atmosphere \\n \\u2022 10 - Hazy day",
        default=1,
        min=0,
        max=10
    )
    
    ozone : bpy.props.FloatProperty(
        name="Ozone",
        description="Density of ozone layer.\\n \\u2022 0 - No ozone \\n \\u2022 1 - Clear day atmosphere \\n \\u2022 2 - City like atmosphere",
        default=1,
        min=0,
        max=10
    )
    
    mountain_scale :bpy.props.IntProperty(
        name="Mountain Scale",
        description="Scale of mountains in the render",
        min=1,
        default=10
    ) 
    
    mountain_seed : bpy.props.FloatProperty(
        name="Mountain Seed",
        description="Seed for the rendered mountains.",
        default=10
    )
    
    mountain_mat : bpy.props.EnumProperty(
        name="Mountain Material",
        description="Sets the mountain material",
        items=populate_enum_mountain
    )
    
    forest_floor_seed : bpy.props.FloatProperty(
        name="Forest Floor Seed",
        description="Seed for rendered forest floor.",
        default=10
    )
    
    forest_floor_mat : bpy.props.EnumProperty(
        name="Forest Floor Material",
        description="Sets the forest floor material",
        items=populate_enum_forest_floor
    )
    
    forest_floor_scale : bpy.props.IntProperty(
        name="Forest Floor Displacement Scale",
        description="Sets how much the forest floor gets displaced.",
        default=10,
        min=1
    )
    
    tree_seed : bpy.props.IntProperty(
        name="Tree Seed",
        description="Seed for the rendered trees.",
        default=0
    )
    
    tree_scale : bpy.props.FloatProperty(
        name="Tree Scale",
        description="scale rendered trees.",
        default=3,
        min=0.01
    )
    
    tree_amount : bpy.props.IntProperty(
        name="Tree Amount",
        description="Amount of trees rendered.",
        default=100,
        min=1
    )
    
    tree_random_size : bpy.props.FloatProperty(
        name="Tree Random Scale",
        description="Randomizes scale of trees 0 - none 1 - max.",
        default=1,
        min=0,
        max=1
    )
    
    tree_enum_type : bpy.props.EnumProperty(
        name="Tree Type",
        description="Sets the tree type for the scene from one of preset trees",
        items=[('1', "Type 1",""),
                ('2', "Type 2",""),
                ('3', "Type 3",""),
                ('random', "Random","")  
        ],
    )    
     
    def invoke(self, context, event):
        previous_scene = bpy.context.scene
        if self.shape == "Ico_Sphere" or self.shape == "Cube":
            mat_floor = get_material(self.enum_floor_mat)
            mat_ceiling = get_material(self.enum_ceiling_mat)
            light_list = previous_scene.light_list
            object_list = previous_scene.object_list
            mat_object = []
            custom_object = []
            custom_collection = []
            for i in range(len(object_list)):
                mat_object.append(get_material(object_list[i].enum_object_mat))
                if object_list[i].object_shape == "custom":
                    custom_object.append(get_object(object_list[i].custom_object))
                else:        
                    custom_object.append(None)
                if object_list[i].object_shape == "collection":
                    custom_collection.append(get_collection(object_list[i].custom_collection))
                else:        
                    custom_collection.append(None)
        if self.shape == "Cube":
            mat_fwall = get_material(self.enum_fwall_mat)
            mat_rwall = get_material(self.enum_rwall_mat)
            mat_lwall = get_material(self.enum_lwall_mat)  
            mat_bwall = get_material(self.enum_bwall_mat)
        if self.shape == "Mountains":
            mat_mountain = get_material(self.mountain_mat)
        if self.shape == "Forest":
            mat_forest_floor = get_material(self.forest_floor_mat)
        
            
        bpy.ops.scene.new(type='NEW')
        add_camera(self, self.height/4, self.width, self.blur_strength, self.shape)
        match self.shape:
            case "Ico_Sphere":  
                ico_sphere = make_scene_ico_sphere(self, self.subdivisions, self.height, mat_ceiling)
                make_floor(self, self.height, 2*self.height, mat_floor, mat_object, object_list, custom_object, custom_collection)
                add_lights(light_list, self.height, self.height, self.shape, ico_sphere)
            case "Cube":
                make_floor(self, self.height, self.width, mat_floor, mat_object, object_list, custom_object, custom_collection)           
                make_scene_cube(self, self.height, self.width, mat_ceiling, mat_fwall, mat_rwall, mat_lwall, mat_bwall)
                add_lights(light_list, self.width, self.height, self.shape, None)
            case "Sky":
                make_sky_material(self, self.cloud_seed, 2000)
                create_sky_background(self, self.sun_size, self.sun_elevation, self.altitude, self.air,self.dust, self.ozone)
            case "Mountains":
                make_sky_material(self, self.cloud_seed, 2000)
                create_sky_background(self, self.sun_size, self.sun_elevation, self.altitude, self.air,self.dust, self.ozone)
                generate_mountain_terrain(self, self.mountain_scale*5, self.mountain_seed, mat_mountain)
            case "Forest":
                make_sky_material(self, self.cloud_seed, 2000)
                create_sky_background(self, self.sun_size, self.sun_elevation, self.altitude, self.air,self.dust, self.ozone)
                generate_forest_terrain(self, self.forest_floor_seed, mat_forest_floor, self.forest_floor_scale, self.tree_seed, self.tree_amount, self.tree_scale,  self.tree_random_size, self.tree_enum_type)
                
        
        renderInfo = context.scene.render 
        renderInfo.image_settings.file_format = "OPEN_EXR"
        renderInfo.engine = 'CYCLES' 
        bpy.context.scene.cycles.device = 'GPU'
        bpy.context.scene.cycles.samples = 100
        renderInfo.resolution_x = 2048
        renderInfo.resolution_y = 1024
        renderInfo.filepath = self.fileName
        
        bpy.ops.render.render(write_still=True)
        image = bpy.data.images.get(self.fileName, None)
        image.source = 'FILE'
        image.filepath = self.fileName
        image.reload()
        image.update()
        
        scene = bpy.context.scene
        for object in scene.objects:
            bpy.data.objects.remove(object, do_unlink=True)
        bpy.data.scenes.remove(scene, do_unlink=True)
        bpy.context.window.scene = previous_scene
        return {"FINISHED"}