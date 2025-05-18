import bpy
import tempfile
import string
import random
import os
import shutil
import math
from ..utils.util_enum_population import populate_enum_mountain

class MountainNode (bpy.types.ShaderNodeCustomGroup):
    """ Node that offers settings for a mountain HDR render. It uses the render of the scene as an enviromental texture.
    """
    bl_name = 'Mountain HDRI Node'
    bl_label = 'Mountain HDRI Node'
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
        
        #mountain
        mountain_box = layout.box()
        mountain_box.label(text="Mountain settings")
        mountain_col = mountain_box.column(align=True)
        mountain_col.prop(self, "mountain_seed")
        mountain_col.prop(self, "mountain_scale")
        mountain_col.prop(self, "mountain_mat")
        
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
        op.mountain_seed = self.mountain_seed
        op.mountain_scale = self.mountain_scale
        op.mountain_mat = self.mountain_mat
        op.height = 1000
        op.blur_strength = self.blur_strength
        op.width = 80
        op.shape = "Mountains"
        
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