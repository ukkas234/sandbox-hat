#!/usr/bin/env python3
"""Render the NEON RONIN set on a stylised manikin (Blender).

Same manikin + UV mapping as round-1 render_set.py (identical garment
footprints), but with the voxel kabuto + ronin textures. Renders:
  previews/ronin-set-front.png   full outfit + kabuto, 3/4 front
  previews/ronin-set-back.png    full outfit + kabuto, 3/4 back
  previews/ronin-top-front.png   torso close-up, front
  previews/ronin-top-back.png    torso close-up, back
  previews/ronin-bottom.png      legs close-up, front
  previews/ronin-footwear.png    feet close-up, low 3/4

Run: blender --background --python render_ronin.py
"""
import bpy
import math
import os
from mathutils import Vector

D = "/home/hatch/workspace/sandbox-hat/round2/neon-ronin"
TOP = f"{D}/neon-ronin-top.png"
BOT = f"{D}/neon-ronin-bottom.png"
SHOE = f"{D}/neon-ronin-footwear.png"
os.makedirs(f"{D}/previews", exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=f"{D}/neon-ronin-kabuto.blend")
hat = bpy.data.objects["NeonRoninKabuto"]
hat.location = (0, 0, 1.73)   # origin = top of head

def uv_rect(x0, y0, x1, y1):
    return ((x0 / 1024.0, x1 / 1024.0),
            (1.0 - y1 / 1024.0, 1.0 - y0 / 1024.0))

def make_textured_mat(name, img_path):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    tex = m.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(img_path)
    tex.extension = 'CLIP'
    m.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.75
    return m

def make_plain_mat(name, rgb, rough=0.6):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1.0)
    b.inputs["Roughness"].default_value = rough
    return m

def box(name, loc, dims, mat):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    return o

def set_face_uv(obj, normal, u_fn, v_fn):
    mesh = obj.data
    if not mesh.uv_layers:
        mesh.uv_layers.new()
    uv = mesh.uv_layers.active.data
    for poly in mesh.polygons:
        n = poly.normal
        if (abs(n.x - normal[0]) < 0.5 and abs(n.y - normal[1]) < 0.5
                and abs(n.z - normal[2]) < 0.5):
            for li in poly.loop_indices:
                vtx = mesh.vertices[mesh.loops[li].vertex_index].co
                uv[li].uv = (u_fn(vtx), v_fn(vtx))

def face_uv_box(obj, normal, u_range, v_range, u_axis, v_axis,
                u_min, u_max, v_min, v_max, flip_u=False, flip_v=False):
    def u_fn(vtx):
        c = getattr(vtx, u_axis)
        t = (c - u_min) / (u_max - u_min) if u_max > u_min else 0.0
        if flip_u:
            t = 1.0 - t
        return u_range[0] + t * (u_range[1] - u_range[0])
    def v_fn(vtx):
        c = getattr(vtx, v_axis)
        t = (c - v_min) / (v_max - v_min) if v_max > v_min else 0.0
        if flip_v:
            t = 1.0 - t
        return v_range[0] + t * (v_range[1] - v_range[0])
    set_face_uv(obj, normal, u_fn, v_fn)

def plain_patch(obj, normal):
    mesh = obj.data
    if not mesh.uv_layers:
        mesh.uv_layers.new()
    uv = mesh.uv_layers.active.data
    for poly in mesh.polygons:
        n = poly.normal
        if (abs(n.x - normal[0]) < 0.5 and abs(n.y - normal[1]) < 0.5
                and abs(n.z - normal[2]) < 0.5):
            for li in poly.loop_indices:
                uv[li].uv = (0.61, 0.67)

mat_top = make_textured_mat("TopTex", TOP)
mat_bot = make_textured_mat("BottomTex", BOT)
mat_shoe = make_textured_mat("ShoeTex", SHOE)
mat_skin = make_plain_mat("Skin", (0.72, 0.55, 0.42), 0.7)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=(0, 0, 1.62))
head = bpy.context.active_object
head.name = "Head"
head.data.materials.append(mat_skin)

torso = box("Torso", (0, 0, 1.20), (0.42, 0.24, 0.55), mat_top)
face_uv_box(torso, (0, -1, 0), *uv_rect(312, 26, 712, 500),
            'x', 'z', -0.21, 0.21, -0.275, 0.275)
face_uv_box(torso, (0, 1, 0), *uv_rect(312, 538, 712, 1012),
            'x', 'z', -0.21, 0.21, -0.275, 0.275, flip_u=True)
for n in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)):
    plain_patch(torso, n)

for side, sx in (("L", -1), ("R", 1)):
    arm = box(f"Arm{side}", (sx * 0.27, 0, 1.20), (0.11, 0.13, 0.55), mat_top)
    fx0, fx1 = (24, 312) if side == "L" else (712, 1000)
    flip = (side == "R")
    face_uv_box(arm, (0, -1, 0), *uv_rect(fx0, 36, fx1, 168),
                'z', 'x', -0.275, 0.275, -0.055, 0.055, flip_u=flip)
    face_uv_box(arm, (0, 1, 0), *uv_rect(fx0, 548, fx1, 680),
                'z', 'x', -0.275, 0.275, -0.055, 0.055, flip_u=flip)
    for n in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)):
        plain_patch(arm, n)

for side, sx in (("L", -1), ("R", 1)):
    leg = box(f"Leg{side}", (sx * 0.10, 0, 0.475), (0.16, 0.18, 0.85), mat_bot)
    fx0, fx1 = (24, 250) if side == "L" else (262, 488)
    bx0, bx1 = (536, 762) if side == "L" else (774, 1000)
    face_uv_box(leg, (0, -1, 0), *uv_rect(fx0, 24, fx1, 1000),
                'x', 'z', -0.08, 0.08, -0.425, 0.425)
    face_uv_box(leg, (0, 1, 0), *uv_rect(bx0, 24, bx1, 1000),
                'x', 'z', -0.08, 0.08, -0.425, 0.425, flip_u=True)
    for n in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)):
        plain_patch(leg, n)

for side, sx in (("L", -1), ("R", 1)):
    foot = box(f"Foot{side}", (sx * 0.10, -0.06, 0.05), (0.17, 0.30, 0.10),
               mat_shoe)
    face_uv_box(foot, (0, -1, 0), *uv_rect(60, 140, 520, 560),
                'x', 'z', -0.085, 0.085, -0.05, 0.05)
    face_uv_box(foot, (0, 1, 0), *uv_rect(60, 140, 520, 560),
                'x', 'z', -0.085, 0.085, -0.05, 0.05)
    face_uv_box(foot, (0, 0, 1), *uv_rect(60, 140, 520, 560),
                'x', 'y', -0.085, 0.085, -0.15, 0.15, flip_v=True)
    for n in ((1, 0, 0), (-1, 0, 0), (0, 0, -1)):
        plain_patch(foot, n)

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
    cam.name = "Cam"
    direction = (Vector(target) - Vector(cam_loc))
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = lens
    s.camera = cam
    s.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("RENDERED:", path)
    bpy.data.objects.remove(cam, do_unlink=True)

P = f"{D}/previews"
# kabuto is 0.25 m tall (fedora was 0.13 m): pull the camera back so the
# horns stay in frame
render_to(f"{P}/ronin-set-front.png", (1.0, -2.4, 1.7), (0, 0, 0.95))
render_to(f"{P}/ronin-set-back.png", (-1.0, 2.4, 1.7), (0, 0, 0.95))
render_to(f"{P}/ronin-top-front.png", (0, -1.5, 1.4), (0, 0, 1.3), lens=55)
render_to(f"{P}/ronin-top-back.png", (0, 1.5, 1.4), (0, 0, 1.3), lens=55)
render_to(f"{P}/ronin-bottom.png", (0, -1.3, 0.5), (0, 0, 0.45), lens=55)
render_to(f"{P}/ronin-footwear.png", (0.35, -0.95, 0.3), (0, -0.05, 0.08), lens=55)

bpy.ops.wm.save_as_mainfile(filepath=f"{D}/ronin-preview.blend")
print("DONE")
