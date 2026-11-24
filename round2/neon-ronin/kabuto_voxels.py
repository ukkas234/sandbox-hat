#!/usr/bin/env python3
"""Design the NEON RONIN kabuto as a voxel model (32 voxels / metre).

Grid: voxel size 1/32 m. ix = right (+x), iy = front is NEGATIVE y
(manikin faces -Y in the preview scene), iz = up from the top of the head
(z=0 = Hat socket attachment point, same convention as build_fedora.py).

The model is a hollow stepped dome (rings) + curved kuwagata horns +
front maedate crest plate + side fukigaeshi turn-backs + front peak.
All geometry is blocky/stepped on purpose: voxel look, NOT smooth mesh.

Outputs:
  kabuto.vox.json  - {"voxel_size_m": 1/32, "colors": {...}, "voxels": [[ix,iy,iz,key], ...]}
  kabuto.vox       - MagicaVoxel .vox (py-vox-io) for Goxel/VoxEdit, if writable
"""
import json, os

OUT = "/home/hatch/workspace/sandbox-hat/round2/neon-ronin"

COLORS = {
    "PLATE": (18, 18, 22),      # near-black plate
    "CHAR":  (38, 38, 46),      # charcoal
    "CYAN":  (0, 240, 255),     # neon cyan #00F0FF
    "MAG":   (255, 45, 150),    # thin magenta accent
}

vox = {}

def put(ix, iy, iz, key):
    vox[(ix, iy, iz)] = key

def ring(x0, x1, y0, y1, iz, key):
    """Hollow rectangular ring outline at height iz."""
    for ix in range(x0, x1 + 1):
        for iy in (y0, y1):
            put(ix, iy, iz, key)
    for iy in range(y0 + 1, y1):
        for ix in (x0, x1):
            put(ix, iy, iz, key)

def solid(x0, x1, y0, y1, z0, z1, key):
    for ix in range(x0, x1 + 1):
        for iy in range(y0, y1 + 1):
            for iz in range(z0, z1 + 1):
                put(ix, iy, iz, key)

# ---------- bowl: stepped hollow dome ----------
ring(-4, 3, -4, 3, 0, "PLATE")   # base ring
ring(-4, 3, -4, 3, 1, "CHAR")
ring(-3, 2, -3, 2, 2, "PLATE")
ring(-3, 2, -3, 2, 3, "CHAR")
solid(-2, 1, -2, 1, 4, 4, "CHAR")  # top cap
solid(-1, 0, -1, 0, 5, 5, "PLATE")  # top knob (tehen)

# ---------- kuwagata horns — ASYMMETRIC (BOLD v2) ----------
# Left horn: taller + longer, sweeps outward. Right horn: shorter, leans
# forward more. NOT mirrored pairs — dynamic silhouette.
# Each entry: (ix, iy, iz, cells) where cells are (dx, dy) offsets.
_left_steps = [
    (-3, -4, 2, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)], "CHAR"),
    (-4, -4, 3, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)], "CHAR"),
    (-5, -5, 4, [(0, 0), (0, 1), (1, 0), (1, 1)], "CHAR"),
    (-6, -5, 5, [(0, 0), (0, 1)], "CHAR"),
    (-6, -6, 6, [(0, 0), (0, 1)], "CHAR"),
    (-7, -6, 7, [(0, 0), (0, 1)], "CYAN"),
    (-7, -7, 8, [(0, 0), (0, 1)], "CYAN"),
]
_right_steps = [
    (2, -4, 2, [(0, 0), (0, 1), (1, 0), (1, 1)], "CHAR"),
    (3, -4, 3, [(0, 0), (0, 1), (1, 0), (1, 1)], "CHAR"),
    (4, -5, 4, [(0, 0), (0, 1)], "CHAR"),
    (5, -6, 5, [(0, 0), (0, 1)], "CHAR"),
    (5, -6, 6, [(0, 0), (0, 1)], "CYAN"),
    (6, -7, 7, [(0, 0), (0, 1)], "CYAN"),
]
for (ix, iy, iz, offs, key) in _left_steps + _right_steps:
    for (dx, dy) in offs:
        put(ix + dx, iy + dy, iz, key)

# ---------- glowing visor slit: front rows of the iz=0/1 rings ----------
for ix in range(-4, 3):
    put(ix, -4, 1, "CYAN")
for ix in range(-3, 2):
    put(ix, -4, 0, "CYAN")

# ---------- cyan crest ridge along the dome top (slightly off-centre) ----------
solid(-1, 0, -2, 1, 6, 6, "CYAN")
solid(-1, 0, -1, 0, 7, 7, "CYAN")

# ---------- maedate: wider front crest plate, OFFSET left, big magenta jewel ----------
solid(-2, 1, -5, -5, 1, 5, "PLATE")
for iz in (1, 2, 3, 4, 5):
    put(-2, -5, iz, "CYAN")
    put(1, -5, iz, "CYAN")
for iz in (2, 3):
    put(-1, -5, iz, "CYAN")
    put(0, -5, iz, "CYAN")
put(-1, -5, 4, "MAG")
put(0, -5, 4, "MAG")
put(-1, -5, 5, "MAG")
put(0, -5, 5, "MAG")

# ---------- fukigaeshi: side turn-backs — LEFT bigger than right ----------
solid(-5, -4, -2, 0, 0, 1, "CHAR")
solid(3, 3, -2, 0, 0, 1, "CHAR")
for iy in (-2, -1, 0):
    put(-5, iy, 1, "CYAN")
    put(-4, iy, 1, "CYAN")

# ---------- front peak (visor shade) with glowing front edge ----------
solid(-4, 3, -5, -5, 0, 0, "PLATE")
for ix in range(-4, 4):
    put(ix, -5, 0, "CYAN")

data = {
    "name": "neon-ronin-kabuto",
    "voxel_size_m": 1 / 32,
    "front": "-Y",
    "colors": {k: list(v) for k, v in COLORS.items()},
    "voxels": [[ix, iy, iz, key] for (ix, iy, iz), key in sorted(vox.items())],
}
with open(f"{OUT}/kabuto.vox.json", "w") as f:
    json.dump(data, f, indent=1)
print(f"voxels: {len(vox)}")
print(f"bbox x [{min(k[0] for k in vox)}..{max(k[0] for k in vox)}] "
      f"y [{min(k[1] for k in vox)}..{max(k[1] for k in vox)}] "
      f"z [{min(k[2] for k in vox)}..{max(k[2] for k in vox)}]")

# ---------- .vox via py-vox-io (best effort) ----------
try:
    from pyvox.models import Vox, Voxel, Model, Size, Color
    from pyvox.writer import VoxWriter
    xs = [k[0] for k in vox]; ys = [k[1] for k in vox]; zs = [k[2] for k in vox]
    sx, sy, sz = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1, max(zs) - min(zs) + 1
    palette = {}
    voxels = []
    for (ix, iy, iz), key in sorted(vox.items()):
        if key not in palette:
            palette[key] = len(palette) + 1
        voxels.append(Voxel(-min(xs) + ix, -min(ys) + iy,
                            -min(zs) + iz, palette[key]))
    pal = [Color(0, 0, 0, 0)] + [Color(*COLORS[k], 255) for k in palette]
    model = Model(Size(sx, sy, sz), voxels)
    VoxWriter(f"{OUT}/kabuto.vox", Vox([model], palette=pal)).write()
    print("wrote kabuto.vox")
except Exception as e:
    print("VOX export skipped:", type(e).__name__, e)
