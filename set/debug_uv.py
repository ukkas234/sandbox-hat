import bpy
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/sandbox-hat/set/set-preview.blend")
for name in ("Torso", "LegL", "ArmR"):
    o = bpy.data.objects.get(name)
    if not o:
        print(name, "NOT FOUND"); continue
    mesh = o.data
    uv = mesh.uv_layers.active.data if mesh.uv_layers else None
    print("==", name, "mats:", [m.name if m else None for m in o.data.materials])
    if uv is None:
        print("  NO UV LAYER"); continue
    for poly in mesh.polygons:
        n = tuple(round(c, 2) for c in poly.normal)
        uvs = [tuple(round(c, 3) for c in uv[li].uv) for li in poly.loop_indices]
        print("  face normal", n, "uvs", uvs)
hat = bpy.data.objects.get("SandboxFedora")
print("hat:", hat.location if hat else "NOT FOUND", "hide_render:", hat.hide_render if hat else None)
print("objects:", [o.name for o in bpy.data.objects])
