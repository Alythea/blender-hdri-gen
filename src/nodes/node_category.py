import bpy
from bl_ui import node_add_menu

class NODE_MT_category_shader_HDRI(bpy.types.Menu):
    bl_idname = "NODE_MT_category_shader_HDRI"
    bl_label = "HDRI Nodes"

    def draw(self, context):
        layout = self.layout
        node_add_menu.add_node_type(layout, "IcoSphereNode")
        node_add_menu.add_node_type(layout, "CubeRoomNode")
        node_add_menu.add_node_type(layout, "SkyNode")
        node_add_menu.add_node_type(layout, "MountainNode")
        node_add_menu.add_node_type(layout, "ForestNode")
        node_add_menu.draw_assets_for_catalog(layout, self.bl_label)
        
def testNodeDrawInNew(self, context):
    layout = self.layout
    layout.menu("NODE_MT_category_shader_HDRI")