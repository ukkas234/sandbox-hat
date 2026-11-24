#!/usr/bin/env python3
"""Render the kabuto alone, close-up, front 3/4 + side + top (Blender)."""
import bpy
import math
from mathutils import Vector

D = "/home/hatch/workspace/sandbox-hat/round2/neon-ronin"
bpy.ops.wm.open_mainfile(filepath=f"{D}/neon-ronin-kabuto.blend")
hat = bpy.data.objects["NeonRoninKabuto"]

s = bpy.context.scene
s.render.engine = 'CYCLES'
s.cycles.device = 'CPU'
s.cycles.samples = 32
s.cycles.use_denoising = True
s.render.resolution_x = 720
s.render.resolution_y = 720
s.render.film_transparent = True
w = bpy.data.worlds["World"]
w.use_nodes = True
bg = w.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.85, 0.87, 0.90, 1.0)
bg.inputs["Strength"].default_value = 0.6
bpy.ops.object.light_add(type='SUN', location=(2, -3, 4))
sun = bpy.context.active_object
sun.data.energy = 2.5
sun.rotation_euler = (math.radians(50), 0, math.radians(30))
bpy.ops.object.light_add(type='AREA', location=(-2, 2, 2))
fill = bpy.context.active_object
fill.data.energy = 80.0
fill.data.size = 3.0

def render_to(path, cam_loc, target, lens=50):
    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.active_object
    direction = (Vector(target) - Vector(cam_loc))
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = lens
    s.camera = cam
    s.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("RENDERED:", path)
    bpy.data.objects.remove(cam, do_unlink=True)

P = f"{D}/previews"
# front is -Y: camera at -Y looking +Y sees the maedate
render_to(f"{P}/kabuto-front.png", (0.35, -0.55, 0.28), (0, 0, 0.12), lens=55)
render_to(f"{P}/kabuto-side.png", (0.55, 0.05, 0.22), (0, 0, 0.12), lens=55)
render_to(f"{P}/kabuto-top.png", (0.0, -0.15, 0.7), (0, 0, 0.05), lens=55)
print("DONE")
