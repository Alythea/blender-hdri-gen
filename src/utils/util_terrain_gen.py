import bpy
import os

def mountain_node_group(seed, multiply):
    geometry_nodes = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Geometry Nodes")
    
    geometry_nodes.is_modifier = True
    
    geometry_socket = geometry_nodes.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'

    geometry_socket_1 = geometry_nodes.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'


    group_input = geometry_nodes.nodes.new("NodeGroupInput")
    group_output = geometry_nodes.nodes.new("NodeGroupOutput")
    group_output.is_active_output = True

    subdivision_surface = geometry_nodes.nodes.new("GeometryNodeSubdivisionSurface")
    subdivision_surface.boundary_smooth = 'PRESERVE_CORNERS'
    subdivision_surface.uv_smooth = 'PRESERVE_BOUNDARIES'
    subdivision_surface.inputs[1].default_value = 10
    subdivision_surface.inputs[2].default_value = 0.0
    subdivision_surface.inputs[3].default_value = 0.0
    subdivision_surface.inputs[4].default_value = True

    set_position = geometry_nodes.nodes.new("GeometryNodeSetPosition")
    set_position.inputs[1].default_value = True
    set_position.inputs[2].default_value = (0.0, 0.0, 0.0)

    set_shade_smooth = geometry_nodes.nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.domain = 'FACE'
    set_shade_smooth.inputs[1].default_value = True
    set_shade_smooth.inputs[2].default_value = True

    noise_texture = geometry_nodes.nodes.new("ShaderNodeTexNoise")
    noise_texture.noise_dimensions = '4D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = True
    #W = seed
    noise_texture.inputs[1].default_value = seed
    noise_texture.inputs[2].default_value = 5.0
    noise_texture.inputs[3].default_value = 10.0
    noise_texture.inputs[4].default_value = 0.5
    noise_texture.inputs[5].default_value = 2.0
    noise_texture.inputs[8].default_value = 0.0

    math = geometry_nodes.nodes.new("ShaderNodeMath")
    math.operation = 'MULTIPLY'
    math.use_clamp = False
    math.inputs[1].default_value = multiply

    vector_math = geometry_nodes.nodes.new("ShaderNodeVectorMath")
    vector_math.operation = 'SCALE'

    normal = geometry_nodes.nodes.new("GeometryNodeInputNormal")
    normal.legacy_corner_normals = False

    geometry_nodes.links.new(group_input.outputs[0], subdivision_surface.inputs[0])
    geometry_nodes.links.new(set_shade_smooth.outputs[0], set_position.inputs[0])
    geometry_nodes.links.new(noise_texture.outputs[0], math.inputs[0])
    geometry_nodes.links.new(math.outputs[0], vector_math.inputs[3])
    geometry_nodes.links.new(normal.outputs[0], vector_math.inputs[0])
    geometry_nodes.links.new(vector_math.outputs[0], set_position.inputs[3])
    geometry_nodes.links.new(subdivision_surface.outputs[0], set_shade_smooth.inputs[0])
    geometry_nodes.links.new(set_position.outputs[0], group_output.inputs[0])
    return geometry_nodes


def generate_mountain_terrain(self, scale, seed, mountain_mat):
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.ops.object.shade_smooth()
    bpy.context.object.scale[0] = 20000
    bpy.context.object.scale[1] = 20000
    bpy.context.object.scale[2] = scale
    obj = bpy.context.view_layer.objects.active
    node_group = mountain_node_group(seed, 100)
    modifier = obj.modifiers.new('Mountain Modifier', 'NODES')
    modifier.node_group = node_group
    
    dg = bpy.context.evaluated_depsgraph_get()
    object_eval = obj.evaluated_get(dg)
    mesh_eval = object_eval.data
    
    center_vertex = [v for v in mesh_eval.vertices if (abs(v.co.x)-0.0001<0 and abs(v.co.y)-0.0001<0)]
    center_z = center_vertex[0].co.z * scale
    obj.location[2] = -center_z
    if (mountain_mat != None):
        obj.data.materials.append(mountain_mat)
     
        
def generate_forest_terrain(self, forest_floor_seed, forest_floor_mat, forest_floor_scale, seed_tree, amount, tree_size, random_size, tree_type):
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.ops.object.shade_smooth()
    bpy.context.object.scale[0] = 1000
    bpy.context.object.scale[1] = 1000
    bpy.context.object.scale[2] = forest_floor_scale
    obj = bpy.context.view_layer.objects.active
    node_group = mountain_node_group(forest_floor_seed, 20)
    modifier = obj.modifiers.new('Mountain Modifier', 'NODES')
    modifier.node_group = node_group
    
    dg = bpy.context.evaluated_depsgraph_get()
    object_eval = obj.evaluated_get(dg)
    mesh_eval = object_eval.data
    
    center_vertex = [v for v in mesh_eval.vertices if (abs(v.co.x)-0.0001<0 and abs(v.co.y)-0.0001<0)]
    center_z = center_vertex[0].co.z * forest_floor_scale
    obj.location[2] = -center_z
    if (forest_floor_mat != None):
        obj.data.materials.append(forest_floor_mat)        
    
    script_file = os.path.realpath(__file__)
    directory = os.path.dirname(script_file)
    filepath = os.path.join(directory, "imports", "import.blend")
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        if "HDRI_Gen_Tree_Collection" in data_from.collections:
            data_to.collections = ["HDRI_Gen_Tree_Collection"]
        else:
            print("Collection not found in import.blend")                                
    mod = obj.modifiers.new("psys name", 'PARTICLE_SYSTEM')
    mod.particle_system.seed =  seed_tree
    settings = mod.particle_system.settings
    settings.type = 'HAIR'
    settings.count = amount
    settings.particle_size = tree_size
    settings.size_random = random_size
    settings.use_rotations = True
    settings.rotation_mode = 'GLOB_X'
    if (tree_type == "random"):
        settings.render_type = 'COLLECTION'
        settings.use_collection_pick_random = True
        settings.instance_collection = bpy.data.collections["HDRI_Gen_Tree_Collection"]
    else:
        tree_name = "HDRI_Gen_Tree_" + str(tree_type)
        settings.render_type = 'OBJECT'
        settings.instance_object = bpy.data.collections["HDRI_Gen_Tree_Collection"].objects[tree_name]