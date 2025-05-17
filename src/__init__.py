bl_info = {
    "name": "HDRI Image Image Generator",
    "author": "Niki Ostatku",
    "blender": (4, 4, 3),
    "location": "Shading -> World Shader -> Add",
    "description": "Add-on containing nodes used to set up and generate HDRI imagery and be able to instantly use it. ",
    "category": "Node",
}

from . import (
    properties,
    operators,
    ui_lists,
    nodes
)

_register = [properties, operators, ui_lists, nodes]

def register():
    for module in _register:
        if hasattr(module, "register"):
            module.register()

def unregister():
    for module in reversed(_register):
        if hasattr(module, "unregister"):
            module.unregister()