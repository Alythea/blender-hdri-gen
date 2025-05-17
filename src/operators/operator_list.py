import bpy

class Object_List_NewItem(bpy.types.Operator): 
    """Add a new item to the list.""" 
    bl_idname = "object_list.new_item" 
    bl_label = "Add a new item" 
    
    def execute(self, context): 
        context.scene.object_list.add() 
        return{'FINISHED'}

class Object_List_DeleteItem(bpy.types.Operator): 
    """Delete the selected item from the list.""" 
    bl_idname = "object_list.delete_item" 
    bl_label = "Deletes an item" 

    @classmethod 
    def poll(cls, context): 
        return context.scene.object_list
    
    def execute(self, context): 
        object_list = context.scene.object_list 
        index = context.scene.object_list_index 
        object_list.remove(index) 
        context.scene.light_list_index = min(max(0, index - 1), len(object_list) - 1) 
        return{'FINISHED'}
                
class Light_List_NewItem(bpy.types.Operator): 
    """Add a new item to the list.""" 
    bl_idname = "light_list.new_item" 
    bl_label = "Add a new item" 
    
    def execute(self, context): 
        context.scene.light_list.add() 
        return{'FINISHED'}

class Light_List_DeleteItem(bpy.types.Operator): 
    """Delete the selected item from the list.""" 
    bl_idname = "light_list.delete_item" 
    bl_label = "Deletes an item" 

    @classmethod 
    def poll(cls, context): 
        return context.scene.light_list
    
    def execute(self, context): 
        light_list = context.scene.light_list 
        index = context.scene.light_list_index 
        light_list.remove(index) 
        context.scene.light_list_index = min(max(0, index - 1), len(light_list) - 1) 
        return{'FINISHED'}