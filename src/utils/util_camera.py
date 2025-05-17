import bpy

def add_camera(self, height, width, blur_strength, shape):
    cam_data = bpy.data.cameras.new("Camera")
    cam_ob = bpy.data.objects.new(name="Camera", object_data=cam_data)
    bpy.context.scene.collection.objects.link(cam_ob)  # instance the camera object in the scene
    bpy.context.scene.camera = cam_ob       # set the active camera
    cam_ob.location = (0.0, 0.0, height)
    cam_ob.rotation_euler[0] = 1.5708
    if (shape == "Sky" or shape == "Mountains" or shape == "Forest"):
        cam_ob.data.clip_end = 100000000
    else:
        cam_ob.data.lens = 10
        cam_ob.scale[0] = 1.5
        cam_ob.scale[2] = 1.5
    cam_ob.data.type = 'PANO'
    cam_ob.data.panorama_type = 'EQUIRECTANGULAR'
    if (blur_strength != 0):
        cam_ob.data.dof.use_dof = True
        cam_ob.data.dof.focus_distance = width/20
        cam_ob.data.dof.aperture_fstop = 1.1 - blur_strength/10