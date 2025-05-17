import bpy
import math
from mathutils import Matrix, Vector

def origin_to_bottom(obj, matrix=Matrix()):
    mesh = obj.data
    mw = obj.matrix_world
    local_verts = [matrix @ Vector(v[:]) for v in obj.bound_box]
    avg_pos = sum(local_verts, Vector()) / 8
    avg_pos.z = min(v.z for v in local_verts)
    avg_pos = matrix.inverted() @ avg_pos
    mesh.transform(Matrix.Translation(-avg_pos))
    mw.translation = mw @ avg_pos
              

def make_floor(self, height, width, mat_floor, mat_object, object_list, custom_object, custom_collection):
    
    bpy.ops.mesh.primitive_plane_add(size=width)
    floor = bpy.context.active_object
    if (mat_floor != None):
        floor.data.materials.append(mat_floor)
    
    min_dimension = 0
    if (height > width):
        min_dimension = width
    else:
        min_dimension = height
        
    index = 0
    for object in object_list:     
        match object.object_shape:
                    case 'cube':
                        bpy.ops.mesh.primitive_cube_add(size=min_dimension/8, enter_editmode=False, align='WORLD', location=(width*10,width*10,height*10))
                    case 'sphere':
                        bpy.ops.mesh.primitive_uv_sphere_add(radius=min_dimension/8, enter_editmode=False, align='WORLD', location=(width*10,width*10,height*10))
                        bpy.ops.object.shade_smooth()
                    case 'ico_sphere':
                        bpy.ops.mesh.primitive_ico_sphere_add(radius=min_dimension/8, enter_editmode=False, align='WORLD', location=(width*10,width*10,height*10))
                    case 'cylinder':
                        bpy.ops.mesh.primitive_cylinder_add(radius=width/15, depth=height/5, enter_editmode=False, align='WORLD', location=(width*10,width*10,height*10))        
                    case 'cone':
                        bpy.ops.mesh.primitive_cone_add(radius1=width/15, radius2=0, depth=height/5, enter_editmode=False, align='WORLD', location=(width*10,width*10,height*10))
                   
        obj = bpy.context.active_object               
        origin_to_bottom(obj)
        if (mat_object[index] != None):
            obj.data.materials.append(mat_object[index])            
        mod = floor.modifiers.new("psys name", 'PARTICLE_SYSTEM')
        mod.particle_system.seed = object.object_seed
        settings = mod.particle_system.settings
        settings.type = 'HAIR'
        settings.count = object.object_number
        settings.render_type = 'OBJECT'
        match object.object_shape:
            case 'custom':
                obj = custom_object[index]
                settings.instance_object = bpy.data.objects[obj.name]
            case 'collection':
                obj = custom_collection[index]
                settings.render_type = 'COLLECTION'
                settings.use_collection_pick_random = True
                settings.instance_collection = bpy.data.collections[obj.name]
            case _:
                 settings.instance_object = bpy.data.objects[obj.name]
        settings.particle_size = 0.25
        settings.size_random = 0.5
        settings.use_rotations = True
        settings.rotation_mode = 'GLOB_X'
        index +=1




def make_scene_ico_sphere(self, subdivisions, radius, mat_ceiling):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=radius, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    if (mat_ceiling != None):
        bpy.context.object.data.materials.append(mat_ceiling)
    return (bpy.context.active_object)
    
    
def make_scene_cube(self, height, width, mat_ceiling, mat_fwall, mat_rwall, mat_lwall, mat_bwall):
    bpy.ops.mesh.primitive_plane_add(size=width, location=(0,0,height))
    if (mat_ceiling != None):
        bpy.context.object.data.materials.append(mat_ceiling)
    
    #front wall
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0,width/2,height/2), rotation=(1.5708,1.5708,0))
    bpy.context.object.scale[0] = height
    bpy.context.object.scale[1] = width
    if (mat_fwall != None):
        bpy.context.object.data.materials.append(mat_fwall)
    
    #right wall   
    bpy.ops.mesh.primitive_plane_add(size=1, location=(width/2,0,height/2), rotation=(0,1.5708,0))
    bpy.context.object.scale[0] = height
    bpy.context.object.scale[1] = width
    if (mat_rwall != None):
        bpy.context.object.data.materials.append(mat_rwall)
        
        
    #left wall
    bpy.ops.mesh.primitive_plane_add(size=1, location=(-width/2,0,height/2), rotation=(0,1.5708,0))
    bpy.context.object.scale[0] = height
    bpy.context.object.scale[1] = width
    if (mat_lwall != None):
        bpy.context.object.data.materials.append(mat_lwall)    
    
        
    #backwall
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0,-width/2,height/2), rotation=(1.5708,1.5708,0))
    bpy.context.object.scale[0] = height
    bpy.context.object.scale[1] = width
    if (mat_bwall != None):
        bpy.context.object.data.materials.append(mat_bwall)  


def add_lights(light_list, width, height, shape, object):
    for light in light_list:
        bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(light.light_location_x, light.light_location_y, light.light_location_z))
        bpy.context.object.data.color = light.light_colour
        bpy.context.object.data.energy = light.light_strength
        if shape == "Ico_Sphere":
            bpy.ops.object.constraint_add(type='LIMIT_DISTANCE')
            bpy.context.object.constraints["Limit Distance"].distance = 0.8 * width
            bpy.context.object.constraints["Limit Distance"].target = object
        if shape == "Cube":
            bpy.ops.object.constraint_add(type='LIMIT_LOCATION')
            bpy.context.object.constraints["Limit Location"].use_min_x = True
            bpy.context.object.constraints["Limit Location"].use_min_y = True
            bpy.context.object.constraints["Limit Location"].use_min_z = True
            bpy.context.object.constraints["Limit Location"].use_max_x = True
            bpy.context.object.constraints["Limit Location"].use_max_y = True
            bpy.context.object.constraints["Limit Location"].use_max_z = True
            
            bpy.context.object.constraints["Limit Location"].min_x = (-0.5 * width) + 0.01
            bpy.context.object.constraints["Limit Location"].min_y = (-0.5 * width) + 0.01
            bpy.context.object.constraints["Limit Location"].min_z = 0.01
            bpy.context.object.constraints["Limit Location"].max_x = (0.5 * width) - 0.01
            bpy.context.object.constraints["Limit Location"].max_y = (0.5 * width) - 0.01
            bpy.context.object.constraints["Limit Location"].max_z = height - 0.01