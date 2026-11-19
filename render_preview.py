import bpy
import math

# ---------- load the hat ----------
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/sandbox-hat/sandbox-fedora.blend")
hat = bpy.data.objects["SandboxFedora"]

# ---------- render settings: Cycles CPU ----------
s = bpy.context.scene
s.render.engine = 'CYCLES'
s.cycles.device = 'CPU'
s.cycles.samples = 64
s.cycles.use_denoising = True
s.render.resolution_x = 900
s.render.resolution_y = 900
s.render.film_transparent = True
s.render.filepath = "/home/hatch/workspace/sandbox-hat/preview.png"

# ---------- world: soft light background ----------
w = bpy.data.worlds["World"]
w.use_nodes = True
bg = w.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.85, 0.87, 0.90, 1.0)
bg.inputs["Strength"].default_value = 0.6

# ---------- lights ----------
bpy.ops.object.light_add(type='SUN', location=(2, -3, 4))
sun = bpy.context.active_object
sun.data.energy = 2.0
sun.rotation_euler = (math.radians(50), 0, math.radians(30))

bpy.ops.object.light_add(type='AREA', location=(-2, 2, 2))
fill = bpy.context.active_object
fill.data.energy = 80.0
fill.data.size = 3.0

# ---------- camera: 3/4 view, hat centered ----------
bpy.ops.object.camera_add(location=(0.45, -0.55, 0.28))
cam = bpy.context.active_object
cam.name = "Cam"
# look at hat center (0,0,0.08)
target = (0, 0, 0.08)
direction = (target[0] - cam.location.x, target[1] - cam.location.y,
             target[2] - cam.location.z)
from mathutils import Vector
cam.rotation_euler = Vector(direction).to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 50
s.camera = cam

# ---------- render ----------
bpy.ops.render.render(write_still=True)
print("RENDERED:", s.render.filepath)
