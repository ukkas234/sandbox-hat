import bpy
import bmesh
import math

# ---------- clear scene ----------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for m in list(bpy.data.meshes):
    bpy.data.meshes.remove(m)

# ---------- units: metres ----------
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 1.0

# ---------- materials ----------
def make_mat(name, rgb, metallic, roughness):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1.0)
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = roughness
    return m

charcoal = make_mat("CharcoalFelt", (0.10, 0.10, 0.12), 0.05, 0.85)
gold = make_mat("GoldBand", (0.83, 0.68, 0.20), 0.9, 0.30)

# ---------- crown: lathe (spin) profile with a center dent ----------
# profile (radius, z): bottom-center -> base -> tapered side -> top edge
# -> flat top -> dent wall -> dent floor center
profile = [
    (0.000, 0.010),
    (0.110, 0.010),
    (0.110, 0.050),
    (0.104, 0.090),
    (0.094, 0.120),
    (0.088, 0.130),
    (0.060, 0.130),
    (0.056, 0.112),
    (0.000, 0.112),
]
mesh = bpy.data.meshes.new("CrownMesh")
crown = bpy.data.objects.new("Crown", mesh)
bpy.context.collection.objects.link(crown)
bm = bmesh.new()
verts = [bm.verts.new((r, 0.0, z)) for (r, z) in profile]
for i in range(len(verts) - 1):
    bm.edges.new((verts[i], verts[i + 1]))
bm.to_mesh(mesh)
bm.free()
mod = crown.modifiers.new("Screw", 'SCREW')
mod.axis = 'Z'
mod.angle = math.radians(360)
mod.steps = 64
mod.render_steps = 64
mod.use_merge_vertices = True
bpy.context.view_layer.objects.active = crown
bpy.ops.object.modifier_apply(modifier=mod.name)
# smooth shading for a clean lathe surface
for p in crown.data.polygons:
    p.use_smooth = True
crown.data.materials.append(charcoal)

# ---------- brim: disc, outer edge curved down ----------
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.19, depth=0.008,
                                    location=(0, 0, 0.014))
brim = bpy.context.active_object
brim.name = "Brim"
bm = bmesh.new()
bm.from_mesh(brim.data)
max_r = max((v.co.x ** 2 + v.co.y ** 2) ** 0.5 for v in bm.verts)
for v in bm.verts:
    r = (v.co.x ** 2 + v.co.y ** 2) ** 0.5
    if r > max_r - 1e-4:
        v.co.z -= 0.010
bm.to_mesh(brim.data)
bm.free()
brim.data.materials.append(charcoal)

# ---------- band: gold torus around crown base ----------
bpy.ops.mesh.primitive_torus_add(major_radius=0.109, minor_radius=0.011,
                                 major_segments=64, minor_segments=16,
                                 location=(0, 0, 0.028))
band = bpy.context.active_object
band.name = "Band"
band.data.materials.append(gold)

# ---------- join into ONE mesh ----------
bpy.ops.object.select_all(action='SELECT')
bpy.context.view_layer.objects.active = crown
bpy.ops.object.join()
hat = bpy.context.active_object
hat.name = "SandboxFedora"

# no armature, no modifiers: rigid accessory. Apply transforms.
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# origin MUST be at world (0,0,0) = top of head (Hat socket attachment point)
bpy.context.scene.cursor.location = (0, 0, 0)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

print("ORIGIN:", tuple(hat.location))
print("BOUNDS Z:", min(v.co.z for v in hat.data.vertices),
      max(v.co.z for v in hat.data.vertices))
print("TRIS:", len(hat.data.polygons))
print("MATERIALS:", [m.name if m else None for m in hat.data.materials])

# ---------- export GLB (metres, Y-up) ----------
out = "/home/hatch/workspace/sandbox-hat/sandbox-fedora.glb"
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB',
                          export_yup=True, export_apply=True)
print("EXPORTED:", out)

# ---------- save .blend ----------
bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/sandbox-hat/sandbox-fedora.blend")
print("SAVED BLEND")
