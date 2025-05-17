import bpy

from .node_cuberoom import CubeRoomNode
from .node_forest import ForestNode
from .node_icosphere import IcoSphereNode
from .node_mountain import MountainNode
from .node_sky import SkyNode
from .node_category import testNodeDrawInNew, NODE_MT_category_shader_HDRI

_classes = [
    CubeRoomNode,
    ForestNode,
    IcoSphereNode,
    MountainNode,
    SkyNode
]


def register():
    bpy.utils.register_class(NODE_MT_category_shader_HDRI)
    bpy.types.NODE_MT_shader_node_add_all.append(testNodeDrawInNew)
    for cls in _classes:
        bpy.utils.register_class(cls)

def unregister():
    bpy.types.NODE_MT_shader_node_add_all.remove(testNodeDrawInNew)
    bpy.utils.unregister_class(NODE_MT_category_shader_HDRI)
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls) 