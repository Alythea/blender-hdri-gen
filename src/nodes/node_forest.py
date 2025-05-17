import bpy
import tempfile
import string
import random
import os
import shutil
import math
from ..utils.util_enum_population import populate_enum_forest_floor

class ForestNode (bpy.types.ShaderNodeCustomGroup):
    """ Node that offers settings for a Forest HDR render. It uses the render of the scene as an enviromental texture.
    """
    bl_name = 'Forest HDRI Node'
    bl_label = 'Forest HDRI Node'
    bl_width_default = 500
    
    fileName : bpy.props.StringProperty(
    name="Name of the image",
    description="This image is used to store the render",
    default="")
    
    blur_strength : bpy.props.IntProperty(
        name="Blur Strength",
        description="Sets the blur strength of the rendered picture",
        min=0,
        max=10,
        default=0
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
    
    
    def init(self, context):
        self.node_tree = bpy.data.node_groups.new(self.bl_name, 'ShaderNodeTree')
        outputColor = self.node_tree.interface.new_socket(name="Color", description="Color output", in_out='OUTPUT', socket_type='NodeSocketColor')
        outputNode = self.node_tree.nodes.new(type='NodeGroupOutput')

        imageNode = self.node_tree.nodes.new("ShaderNodeTexEnvironment")
        self.fileName = str((''.join(random.choices(string.ascii_letters, k=5))) + ".exr")
        imageNode.name = 'resultImageNode'
        temp = tempfile.TemporaryDirectory().name 
        self.fileName = os.path.join(temp, self.fileName)
        for image in bpy.data.images:
            if image.name == self.fileName:
                bpy.data.images.remove(image)
        textureImage = bpy.data.images.new(self.fileName, 0, 0)
        imageNode.image = textureImage
        
        self.node_tree.links.new(imageNode.outputs[0], outputNode.inputs[0])
        return

    def draw_buttons(self, context, layout):  
        textureImage = bpy.data.images.get("TestImage", None)
        
        #sky
        sky_box = layout.box()
        sky_box.label(text="Sky settings")
        sky_col = sky_box.column(align=True)
        sky_col.prop(self, "cloud_seed")
        sky_col.prop(self, "sun_size")
        sky_col.prop(self, "sun_elevation")
        sky_col.prop(self, "altitude")
        sky_col.prop(self, "air")
        sky_col.prop(self, "dust")
        sky_col.prop(self, "ozone")
        
        #forest floor
        mountain_box = layout.box()
        mountain_box.label(text="Floor settings")
        mountain_col = mountain_box.column(align=True)
        mountain_col.prop(self, "forest_floor_seed")
        mountain_col.prop(self, "forest_floor_scale")
        mountain_col.prop(self, "forest_floor_mat")
        
        #trees
        tree_box = layout.box()
        tree_box.label(text="Tree settings")
        tree_col = tree_box.column(align=True)
        tree_col.prop(self, "tree_seed")
        tree_col.prop(self, "tree_scale")
        tree_col.prop(self, "tree_amount")
        tree_col.prop(self, "tree_random_size")
        tree_col.prop(self, "tree_enum_type")
        
        #filters
        filter_box = layout.box()
        filter_box.label(text="Filters")
        filter_col = filter_box.column(align=True)
        filter_col.prop(self, "blur_strength")
        
        #operator
        op_box = layout.box()
        op_row = op_box.row()
        op = op_row.operator("hdri.render", text="Render")
        op.fileName = self.fileName
        op.cloud_seed = self.cloud_seed
        op.sun_size = self.sun_size
        op.sun_elevation = self.sun_elevation
        op.altitude = self.altitude
        op.air = self.air
        op.dust = self.dust
        op.ozone = self.ozone
        op.forest_floor_seed = self.forest_floor_seed
        op.forest_floor_mat = self.forest_floor_mat
        op.forest_floor_scale = self.forest_floor_scale
        op.tree_seed = self.tree_seed
        op.tree_scale = self.tree_scale
        op.tree_amount = self.tree_amount
        op.tree_random_size = self.tree_random_size
        op.tree_enum_type = self.tree_enum_type
        op.height = 100
        op.width = 10
        op.shape = "Forest"
        
    def copy(self, node):
        self.init(bpy.context)
        return

    def free(self):
        bpy.data.node_groups.remove(self.node_tree, do_unlink=True)
        try:
            shutil.rmtree(os.path.dirname(self.fileName))
        except:
            pass    
        return