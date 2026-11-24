#!/usr/bin/env python3
"""Build the ROYAL PEACOCK crown .glb from crown.vox.json (Blender script).

Same pattern as build_kabuto.py (Neon Ronin): 32 voxels/metre, only
exposed faces, one material per voxel colour, origin at world (0,0,0)
= top of head (Hat socket). Exports GLB (metres, Y-up, transforms
applied), no armature/modifiers.

Run:  blender --background --python build_crown.py
"""
import json
import bpy
import bmesh

D = "/home/hatch/workspace/sandbox-hat/round2/royal-peacock"
with open(f"{D}/crown.vox.json") as f:
    data = json.load(f)

S = data["voxel_size_m"]
COLORS = {k: tuple(v) for k, v in data["colors"].items()}
VOX = {}
for ix, iy, iz, key in data["voxels"]:
    VOX[(ix, iy, iz)] = key

# centre x/y on bbox centre so the model is symmetric about the origin
xs = [k[0] for k in VOX]; ys = [k[1] for k in VOX]
cx = (min(xs) + max(xs) + 1) / 2.0
cy = (min(ys) + max(ys) + 1) / 2.0

# ---------- clear scene ----------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for m in list(bpy.data.meshes):
    bpy.data.meshes.remove(m)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 1.0

# ---------- materials (one per colour) ----------
def make_mat(name, rgb, metallic=0.0, roughness=0.6, emission=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*[c / 255.0 for c in rgb], 1.0)
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = roughness
    if emission > 0:
        b.inputs["Emission Color"].default_value = (*[c / 255.0 for c in rgb], 1.0)
        b.inputs["Emission Strength"].default_value = emission
    return m

MAT_DEFS = {
    "GOLD":    ("PeacockGold",   (212, 175, 55),  0.5, 0.35, 0.0),
    "GOLD_LT": ("PeacockGoldLt", (240, 216, 120), 0.5, 0.3,  0.0),
    "GOLD_DK": ("PeacockGoldDk", (138, 109, 31),  0.5, 0.45, 0.0),
    "TEAL":    ("PeacockTeal",   (0, 150, 140),   0.0, 0.4,  0.25),
    "PEACOCK": ("PeacockBlue",   (0, 90, 180),    0.0, 0.4,  0.25),
    "EMERALD": ("PeacockEmerald",(0, 110, 85),    0.0, 0.45, 0.2),
    "DARK":    ("PeacockDark",   (14, 20, 16),    0.1, 0.75, 0.0),
}
mats = {}
for key, (name, rgb, met, rough, emis) in MAT_DEFS.items():
    mats[key] = make_mat(name, rgb, met, rough, emis)
mat_index = {k: i for i, k in enumerate(MAT_DEFS)}

# ---------- exposed faces ----------
FACES = [
    ((1, 0, 0),  [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)]),
    ((-1, 0, 0), [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)]),
    ((0, 1, 0),  [(0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0)]),
    ((0, -1, 0), [(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)]),
    ((0, 0, 1),  [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]),
    ((0, 0, -1), [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)]),
]

mesh = bpy.data.meshes.new("CrownMesh")
obj = bpy.data.objects.new("RoyalPeacockCrown", mesh)
bpy.context.collection.objects.link(obj)
for key in MAT_DEFS:
    mesh.materials.append(mats[key])

bm = bmesh.new()
for (ix, iy, iz), key in sorted(VOX.items()):
    for (dx, dy, dz), corners in FACES:
        if (ix + dx, iy + dy, iz + dz) in VOX:
            continue  # hidden face
        vs = []
        for ox, oy, oz in corners:
            vs.append(bm.verts.new((
                (ix + ox - cx) * S,
                (iy + oy - cy) * S,
                (iz + oz) * S,
            )))
        face = bm.faces.new(vs)
        face.material_index = mat_index[key]
bm.to_mesh(mesh)
bm.free()

print("VOXELS:", len(VOX))
print("FACES:", len(mesh.polygons))
print("TRIS:", sum(len(p.vertices) - 2 for p in mesh.polygons))
xs2 = [v.co.x for v in mesh.vertices]
ys2 = [v.co.y for v in mesh.vertices]
zs2 = [v.co.z for v in mesh.vertices]
print("BOUNDS X:", min(xs2), max(xs2))
print("BOUNDS Y:", min(ys2), max(ys2))
print("BOUNDS Z:", min(zs2), max(zs2))

# origin at (0,0,0) = top of head
bpy.context.scene.cursor.location = (0, 0, 0)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

out = f"{D}/royal-peacock-crown.glb"
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB',
                          export_yup=True, export_apply=True)
print("EXPORTED:", out)
bpy.ops.wm.save_as_mainfile(filepath=f"{D}/royal-peacock-crown.blend")
print("SAVED BLEND")
