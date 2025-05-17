import bpy

from .operator_list import Object_List_NewItem, Object_List_DeleteItem, Light_List_NewItem, Light_List_DeleteItem
from .operator_render import RenderImage

_classes = [
    Object_List_NewItem, 
    Object_List_DeleteItem, 
    Light_List_NewItem, 
    Light_List_DeleteItem,
    RenderImage
]


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls) 