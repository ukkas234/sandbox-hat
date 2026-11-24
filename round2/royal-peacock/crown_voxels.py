#!/usr/bin/env python3
"""Design the ROYAL PEACOCK crown as a voxel model (32 voxels / metre).

Grid: voxel size 1/32 m. ix = right (+x), iy = front is NEGATIVE y
(manikin faces -Y), iz = up from the top of the head (z=0 = Hat socket).

The model: gold band (2 rings) + gold spikes + 5 feather fans rising
from the back arc, each feather tipped with a peacock eye-spot
(teal ring / blue centre / gold dot). Blocky/stepped on purpose.

Outputs: crown.vox.json + crown.vox (py-vox-io, best effort).
"""
import json

OUT = "/home/hatch/workspace/sandbox-hat/round2/royal-peacock"

COLORS = {
    "GOLD":  (212, 175, 55),    # #D4AF37
    "GOLD_LT": (240, 216, 120),
    "GOLD_DK": (138, 109, 31),
    "TEAL":  (0, 150, 140),     # feather body
    "PEACOCK": (0, 90, 180),    # eye-spot blue
    "EMERALD": (0, 110, 85),    # dark green accent
    "DARK":  (14, 20, 16),      # dark green-black base
}

vox = {}

def put(ix, iy, iz, key):
    vox[(ix, iy, iz)] = key

def ring(x0, x1, y0, y1, iz, key):
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

# ---------- gold band ----------
ring(-4, 3, -4, 3, 0, "GOLD")
ring(-4, 3, -4, 3, 1, "GOLD_DK")
# front jewel: emerald at the front centre of the band
put(-1, -4, 0, "EMERALD")
put(0, -4, 0, "EMERALD")
put(-1, -4, 1, "EMERALD")
put(0, -4, 1, "EMERALD")

# ---------- gold spikes on the band rim ----------
for (ix, iy) in [(-4, -4), (3, -4), (-4, 3), (3, 3),
                 (-1, -4), (0, -4), (-4, -1), (-4, 0),
                 (3, -1), (3, 0), (-1, 3), (0, 3)]:
    put(ix, iy, 2, "GOLD_LT")

# ---------- 5 feather fans (back arc), each with an eye-spot tip ----------
# (base_ix, base_iy, height, lean_dx) — lean shifts the top outward.
# v2: shorter stalks (5-7) + bigger 3-row eye fan so the eye dominates
# the silhouette instead of the stalk reading as a fence post.
feathers = [
    (-3, 1, 5, -1),
    (-2, 2, 6, 0),
    (0, 3, 7, 0),
    (2, 2, 6, 0),
    (3, 1, 5, 1),
]
for bx, by, h, lean in feathers:
    # stalk: vertical column, leaning at the top
    for iz in range(1, h + 1):
        dx = lean if iz >= h - 1 else 0
        put(bx + dx, by, iz, "TEAL")
    # eye-spot: 3-wide fan at the top, 3 tall (eye dominates the tip)
    top = h
    tx = bx + lean
    # upper eye row
    put(tx - 1, by, top, "TEAL")
    put(tx, by, top, "PEACOCK")
    put(tx + 1, by, top, "TEAL")
    # middle eye row (wide blue + gold centre)
    put(tx - 1, by, top - 1, "PEACOCK")
    put(tx, by, top - 1, "GOLD")
    put(tx + 1, by, top - 1, "PEACOCK")
    # lower eye row (emerald rim)
    put(tx - 1, by, top - 2, "TEAL")
    put(tx, by, top - 2, "EMERALD")
    put(tx + 1, by, top - 2, "TEAL")

data = {
    "name": "royal-peacock-crown",
    "voxel_size_m": 1 / 32,
    "front": "-Y",
    "colors": {k: list(v) for k, v in COLORS.items()},
    "voxels": [[ix, iy, iz, key] for (ix, iy, iz), key in sorted(vox.items())],
}
with open(f"{OUT}/crown.vox.json", "w") as f:
    json.dump(data, f, indent=1)
print(f"voxels: {len(vox)}")
print(f"bbox x [{min(k[0] for k in vox)}..{max(k[0] for k in vox)}] "
      f"y [{min(k[1] for k in vox)}..{max(k[1] for k in vox)}] "
      f"z [{min(k[2] for k in vox)}..{max(k[2] for k in vox)}]")

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
    VoxWriter(f"{OUT}/crown.vox", Vox([model], palette=pal)).write()
    print("wrote crown.vox")
except Exception as e:
    print("VOX export skipped:", type(e).__name__, e)
