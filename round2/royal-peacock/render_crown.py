#!/usr/bin/env python3
"""Render the crown alone, close-up, front 3/4 + side + top (Blender)."""
import bpy
import math
from mathutils import Vector

D = "/home/hatch/workspace/sandbox-hat/round2/royal-peacock"
bpy.ops.wm.open_mainfile(filepath=f"{D}/royal-peacock-crown.blend")
hat = bpy.data.objects["RoyalPeacockCrown"]

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
# front is -Y: camera at -Y looking +Y sees the front jewel
render_to(f"{P}/crown-front.png", (0.4, -0.62, 0.32), (0, 0, 0.15), lens=55)
render_to(f"{P}/crown-side.png", (0.62, 0.05, 0.26), (0, 0, 0.15), lens=55)
render_to(f"{P}/crown-top.png", (0.0, -0.18, 0.78), (0, 0, 0.06), lens=55)
print("DONE")
