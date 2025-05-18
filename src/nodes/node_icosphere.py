import bpy
import tempfile
import string
import random
import os
import shutil
from ..utils.util_enum_population import populate_enum_reflective

class IcoSphereNode (bpy.types.ShaderNodeCustomGroup):
    """ Node that offers settings for an icosphere shaped abstract room HDR render. It uses the render of the scene as an enviromental texture.
    """
    bl_name = 'Abstract Icosphere Room Node'
    bl_label = 'Abstract Icosphere Room Node'
    bl_width_default = 500
    
    fileName : bpy.props.StringProperty(
    name="Name of the image",
    description="This image is used to store the render",
    default="")
    
    subdivisions : bpy.props.IntProperty(
        name="Subdivisions",
        description="Sets the subdivision parameter for the resulting icosphere render",
        min=1,
        default=1
    )
           
    radius : bpy.props.FloatProperty(
        name="Radius",
        description="Sets the radius of the icosphere room",
        min=5,
        default=5
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
        
        if not bpy.context.scene.light_list:
             bpy.context.scene.light_list.add()
             bpy.context.scene.light_list[0].name = "Base Light"
             
        
        self.node_tree.links.new(imageNode.outputs[0], outputNode.inputs[0])
        return

    def draw_buttons(self, context, layout):
        scene = context.scene
        
        textureImage = bpy.data.images.get("TestImage", None)
        #size
        size_box = layout.box()
        size_box.label(text="Room settings")
        size_col = size_box.column(align=True)
        size_col.prop(self, "radius")
        size_col.prop(self, "subdivisions")
        
        #materials
        mat_box = layout.box()
        mat_box.label(text="Materials")
        mat_col = mat_box.column(align=True)
        mat_col.prop(self, "enum_floor_mat")
        mat_col.prop(self, "enum_ceiling_mat")
        
        #objects
        obj_box = layout.box()
        obj_box.label(text="Objects in scene")   
        name_row = obj_box.row()
        obj_row = obj_box.row()
        obj_row.template_list("UI_List", "The_List", scene, "object_list", scene, "object_list_index")
        obj_row1 = obj_box.row() 
        obj_row1.operator('object_list.new_item', text='New Object Set') 
        obj_row2 = obj_box.row()
        obj_row2.operator('object_list.delete_item', text='Remove Object Set')
        
        if scene.object_list_index >= 0 and scene.object_list: 
            item = scene.object_list[scene.object_list_index]
            obj_row6 = obj_box.row() 
            obj_row6.prop(item, "name") 
            obj_seed_row = obj_box.row()
            obj_seed_row.prop(item, "object_seed")
            obj_row3 = obj_box.row() 
            obj_row3.prop(item, "object_number")
            obj_row4 = obj_box.row() 
            obj_row4.prop(item, "enum_object_mat") 
            obj_row5 = obj_box.row() 
            obj_row5.prop(item, "object_shape")
            if (item.object_shape == "custom"): 
                obj_row7 = obj_box.row() 
                obj_row7.prop(item, "custom_object")
            if (item.object_shape == "collection"): 
                obj_row7 = obj_box.row() 
                obj_row7.prop(item, "custom_collection")
                
                
        
        #light
        list_box = layout.box()
        list_box.label(text="Lights in scene")
        name_row = list_box.row()
        list_row = list_box.row()
        list_row.template_list("UI_List", "The_List", scene, "light_list", scene, "light_list_index")
        list_row1 = list_box.row() 
        list_row1.operator('light_list.new_item', text='New Light') 
        list_row2 = list_box.row()
        list_row2.operator('light_list.delete_item', text='Remove Light')
        
        if scene.light_list_index >= 0 and scene.light_list: 
            item = scene.light_list[scene.light_list_index]
            list_row8 = list_box.row() 
            list_row8.prop(item, "name") 
            list_row3 = list_box.row() 
            list_row3.prop(item, "light_location_x")
            list_row4 = list_box.row() 
            list_row4.prop(item, "light_location_y") 
            list_row5 = list_box.row() 
            list_row5.prop(item, "light_location_z")
            list_row6 = list_box.row() 
            list_row6.prop(item, "light_colour")
            list_row7 = list_box.row() 
            list_row7.prop(item, "light_strength")
        
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
        op.height = self.radius
        op.width = self.radius
        op.subdivisions = self.subdivisions
        op.enum_floor_mat = self.enum_floor_mat
        op.enum_ceiling_mat = self.enum_ceiling_mat
        op.blur_strength = self.blur_strength
        op.shape = "Ico_Sphere"
        
        
    
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