import bpy

def make_sky_material(self, seed, height):
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, height), scale=(1, 1, 1))
    obj = bpy.context.object
    obj.dimensions = (500000, 500000, 200)
    bpy.ops.object.transform_apply(scale=True)
    new_mat = bpy.data.materials.new(name = "sky_mat")
    new_mat.use_nodes = True
    nodes = new_mat.node_tree.nodes
    links = new_mat.node_tree.links
    node_to_delete =  nodes['Principled BSDF']
    nodes.remove( node_to_delete )
    nodes.new(type="ShaderNodeVolumeScatter")
    nodes["Volume Scatter"].inputs[2].default_value = 0.63
    nodes["Volume Scatter"].inputs[1].default_value = 0.006
    links.new(nodes["Volume Scatter"].outputs["Volume"], nodes["Material Output"].inputs["Volume"])
    nodes.new(type="ShaderNodeValToRGB")
    nodes["Color Ramp"].color_ramp.interpolation = 'CONSTANT'
    nodes["Color Ramp"].color_ramp.elements[1].position = 0.5
    links.new(nodes["Color Ramp"].outputs["Color"], nodes["Volume Scatter"].inputs["Color"])
    nodes.new(type="ShaderNodeTexNoise")
    nodes["Noise Texture"].noise_dimensions = '4D'
    nodes["Noise Texture"].inputs[3].default_value = 25
    nodes["Noise Texture"].inputs[4].default_value = 0.8
    nodes["Noise Texture"].inputs[2].default_value = 1
    nodes["Noise Texture"].inputs[1].default_value = seed
    links.new(nodes["Noise Texture"].outputs["Fac"], nodes["Color Ramp"].inputs["Fac"])
    nodes.new(type="ShaderNodeMapping")
    nodes["Mapping"].vector_type = 'TEXTURE'
    nodes["Mapping"].inputs[3].default_value[0] = 5000
    nodes["Mapping"].inputs[3].default_value[1] = 5000
    nodes["Mapping"].inputs[3].default_value[2] = 5000
    links.new(nodes["Mapping"].outputs["Vector"], nodes["Noise Texture"].inputs["Vector"])
    nodes.new(type="ShaderNodeTexCoord")
    links.new(nodes["Texture Coordinate"].outputs["Object"], nodes["Mapping"].inputs["Vector"])
    obj.data.materials.append(new_mat)
    

def create_sky_background(self, sun_size, sun_elevation, altitude, air, dust, ozone):
    new_world = bpy.data.worlds.new("New World")
    new_world.use_nodes = True
    bpy.context.scene.world = new_world
    sky_texture = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexSky")
    bg = bpy.context.scene.world.node_tree.nodes["Background"]
    bpy.context.scene.world.node_tree.links.new(bg.inputs["Color"], sky_texture.outputs["Color"])
    sky_texture.sky_type = 'NISHITA'
    sky_texture.sun_size = sun_size
    sky_texture.sun_elevation = sun_elevation 
    sky_texture.altitude = altitude
    sky_texture.air_density = air
    sky_texture.dust_density = dust
    sky_texture.ozone_density = ozone
    bg.inputs['Strength'].default_value = 0.1