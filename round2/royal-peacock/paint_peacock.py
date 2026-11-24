#!/usr/bin/env python3
"""Paint the ROYAL PEACOCK set textures (Top / Bottom / Footwear).

Same garment footprints + layout rules as round 1 (paint_set.py) and the
Neon Ronin painter; footprints copied from round-1 v2 (do not re-derive
the shoe shape).

Palette: gold #D4AF37 + emerald/teal + peacock blue.
Motif: peacock eye (concentric teal/blue/gold) + brocade swirls.
Output: 1024x1024 RGB PNG, black outside the garment.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "/home/hatch/workspace/sandbox-hat/round2/royal-peacock"

# ---------- palette ----------
GOLD = (212, 175, 55)       # #D4AF37
GOLD_LT = (240, 216, 120)
GOLD_DK = (138, 109, 31)
GOLD_DEEP = (96, 74, 18)
GOLD_PALE = (226, 196, 110)
TEAL = (0, 150, 140)
TEAL_DK = (0, 95, 90)
PEACOCK = (0, 90, 180)      # eye-spot blue
EMERALD = (0, 110, 85)
DARK = (16, 20, 18)         # darkest shade (> pure black)
BLACK = (0, 0, 0)


def add_fabric(img, mask, weave=6, noise_amp=7, seed=7):
    rng = np.random.default_rng(seed)
    a = np.asarray(img).astype(np.int16)
    n = rng.integers(-noise_amp, noise_amp + 1, size=(H, W, 1))
    yy = np.arange(H)[:, None, None]
    weave_pat = ((yy % weave) == 0) * 5
    a = a + n + weave_pat
    a = np.clip(a, 0, 255).astype(np.uint8)
    m = np.asarray(mask)
    base = np.asarray(img)
    return Image.fromarray(np.where(m[..., None], a, base))


def mask_of(layer):
    return np.asarray(layer.convert("L")) > 8


def gold_piping(d, xy, width=4):
    d.line(xy, fill=GOLD_DK, width=width + 2)
    d.line(xy, fill=GOLD, width=width)
    d.line(xy, fill=GOLD_LT, width=max(1, width - 2))


def teal_piping(d, xy, width=4):
    d.line(xy, fill=TEAL_DK, width=width + 2)
    d.line(xy, fill=TEAL, width=width)
    d.line(xy, fill=(120, 220, 210), width=max(1, width - 2))


def gold_button(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD_DK)
    d.ellipse([cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2], fill=GOLD)
    d.ellipse([cx - r + 4, cy - r + 5, cx - r + 8, cy - r + 9], fill=GOLD_LT)
    for dx, dy in ((-4, -4), (4, -4), (-4, 4), (4, 4)):
        d.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2],
                  fill=GOLD_DEEP)


def peacock_eye(d, cx, cy, r):
    """Concentric peacock eye: teal outer, blue middle, gold centre."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL_DK)
    d.ellipse([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4], fill=TEAL)
    r2 = int(r * 0.62)
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=PEACOCK)
    r3 = int(r * 0.30)
    d.ellipse([cx - r3, cy - r3, cx + r3, cy + r3], fill=GOLD)
    d.ellipse([cx - r3 + 2, cy - r3 + 2, cx - r3 + 6, cy - r3 + 6],
              fill=GOLD_LT)


def brocade_swirls(d, x0, y0, x1, y1, n=4, seed=3):
    """Brocade suggestion: arcs + dots in darker gold inside a rect."""
    import random
    rnd = random.Random(seed)
    for i in range(n):
        cx = x0 + (x1 - x0) * (i + 0.5) / n
        cy = (y0 + y1) // 2 + rnd.randint(-30, 30)
        r = rnd.randint(18, 30)
        d.arc([cx - r, cy - r, cx + r, cy + r], 0, 300, fill=GOLD_DK, width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=GOLD_DK)


# =====================================================================
# TOP — brocade jacket, front upper half / back lower half
# =====================================================================
def paint_top():
    layer = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(layer)

    def torso(y0):
        d.polygon([(312, y0 + 26), (712, y0 + 26), (706, y0 + 180),
                   (700, y0 + 474), (324, y0 + 474), (318, y0 + 180)],
                  fill=GOLD)
        d.polygon([(24, y0 + 36), (312, y0 + 36), (312, y0 + 150),
                   (24, y0 + 168)], fill=GOLD)
        d.polygon([(712, y0 + 36), (1000, y0 + 36), (1000, y0 + 168),
                   (712, y0 + 150)], fill=GOLD)

    torso(0)
    torso(512)
    img = add_fabric(layer, mask_of(layer), seed=11)
    d = ImageDraw.Draw(img)

    # ---- front ----
    # mandarin collar + teal trim
    d.ellipse([442, 6, 582, 52], fill=GOLD_DK)
    d.arc([442, 6, 582, 52], 0, 180, fill=TEAL, width=4)
    # centre placket + gold buttons
    d.rectangle([496, 34, 528, 500], fill=GOLD_PALE)
    gold_piping(d, [(496, 40), (496, 498)], width=2)
    gold_piping(d, [(528, 40), (528, 498)], width=2)
    for y in (96, 186, 276, 366, 452):
        gold_button(d, 512, y, 13)
    # peacock eyes on the chest (left + right of the placket)
    peacock_eye(d, 400, 150, 42)
    peacock_eye(d, 624, 150, 42)
    # brocade swirls on the lower front
    brocade_swirls(d, 340, 330, 690, 470, n=4, seed=5)
    # teal side piping
    teal_piping(d, [(330, 44), (330, 492)], width=3)
    teal_piping(d, [(694, 44), (694, 492)], width=3)
    # sleeve teal edges + gold cuff bands
    teal_piping(d, [(24, 164), (312, 146)], width=3)
    teal_piping(d, [(712, 146), (1000, 164)], width=3)
    d.rectangle([24, 40, 58, 164], fill=TEAL_DK)
    d.rectangle([28, 40, 58, 164], fill=TEAL)
    d.rectangle([966, 40, 1000, 164], fill=TEAL_DK)
    d.rectangle([966, 40, 996, 164], fill=TEAL)
    # shoulder shading
    d.polygon([(312, 26), (712, 26), (712, 60), (312, 60)], fill=GOLD_LT)
    # flap pockets with teal trim
    for x0 in (352, 556):
        d.polygon([(x0, 384), (x0 + 116, 384), (x0 + 116, 424),
                   (x0 + 58, 440), (x0, 424)], fill=GOLD_PALE)
        teal_piping(d, [(x0, 424), (x0 + 58, 440), (x0 + 116, 424)], width=3)

    # ---- back (y + 512) ----
    # large peacock eye as the back centrepiece
    peacock_eye(d, 512, 720, 110)
    # brocade swirls around it
    brocade_swirls(d, 340, 560, 690, 660, n=4, seed=7)
    brocade_swirls(d, 340, 850, 690, 960, n=4, seed=11)
    # centre back seam with teal stitch dashes
    d.line([(512, 540), (512, 1000)], fill=GOLD_DK, width=4)
    for y in range(556, 996, 28):
        d.line([(512, y), (512, y + 14)], fill=TEAL, width=2)
    # yoke line across shoulders
    teal_piping(d, [(330, 566), (694, 566)], width=3)
    # side piping (back)
    teal_piping(d, [(330, 556), (330, 1004)], width=3)
    teal_piping(d, [(694, 556), (694, 1004)], width=3)
    # sleeve edges + cuffs (back)
    teal_piping(d, [(24, 676), (312, 658)], width=3)
    teal_piping(d, [(712, 658), (1000, 676)], width=3)
    d.rectangle([24, 552, 58, 676], fill=TEAL_DK)
    d.rectangle([28, 552, 58, 676], fill=TEAL)
    d.rectangle([966, 552, 1000, 676], fill=TEAL_DK)
    d.rectangle([966, 552, 996, 676], fill=TEAL)

    img.save(f"{OUT}/royal-peacock-top.png")
    print("saved royal-peacock-top.png")


# =====================================================================
# BOTTOM — formal trousers, front left half / back right half
# =====================================================================
def paint_bottom():
    layer = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(layer)

    for x0 in (0, 512):
        d.polygon([(x0 + 24, 24), (x0 + 250, 24), (x0 + 250, 1000),
                   (x0 + 24, 1000)], fill=GOLD)
        d.polygon([(x0 + 262, 24), (x0 + 488, 24), (x0 + 488, 1000),
                   (x0 + 262, 1000)], fill=GOLD)
        d.rectangle([x0 + 24, 24, x0 + 488, 84], fill=EMERALD)
    img = add_fabric(layer, mask_of(layer), seed=23)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([24, 84, 488, 1000], fill=(20, 14, 6, 90))
    d = ImageDraw.Draw(img)

    # ---- front ----
    gold_button(d, 256, 54, 12)
    for x in (64, 150, 362, 452):
        d.rectangle([x - 8, 24, x + 8, 96], fill=DARK)
    teal_piping(d, [(24, 84), (488, 84)], width=3)
    # teal side stripes down each front leg
    for x in (32, 44, 468, 480):
        teal_piping(d, [(x, 96), (x, 932)], width=3)
    # centre crease per leg
    for x in (137, 375):
        d.line([(x, 100), (x, 930)], fill=GOLD_LT, width=3)
        d.line([(x + 3, 100), (x + 3, 930)], fill=GOLD_DK, width=2)
    # slash pockets, teal trimmed
    teal_piping(d, [(62, 96), (140, 156)], width=4)
    d.polygon([(62, 96), (140, 156), (140, 170), (62, 110)], fill=DARK)
    teal_piping(d, [(450, 96), (372, 156)], width=4)
    d.polygon([(450, 96), (372, 156), (372, 170), (450, 110)], fill=DARK)
    # peacock eye on right front thigh
    peacock_eye(d, 375, 280, 36)
    # hem
    for x0, x1 in ((24, 250), (262, 488)):
        teal_piping(d, [(x0, 940), (x1, 940)], width=3)
        d.rectangle([x0, 948, x1, 1000], fill=DARK)

    # ---- back ----
    gold_button(d, 768, 54, 12)
    for x in (576, 662, 874, 964):
        d.rectangle([x - 8, 24, x + 8, 96], fill=DARK)
    teal_piping(d, [(536, 84), (1000, 84)], width=3)
    # welt pockets with teal trim
    for x0 in (584, 828):
        d.rectangle([x0, 150, x0 + 116, 192], fill=DARK)
        teal_piping(d, [(x0, 150), (x0 + 116, 150)], width=3)
        gold_button(d, x0 + 58, 172, 8)
    peacock_eye(d, 886, 172, 26)
    # centre back seam
    d.line([(768, 96), (768, 220)], fill=GOLD_DK, width=4)
    for x in (544, 992):
        d.line([(x, 96), (x, 932)], fill=TEAL_DK, width=3)
    for x0, x1 in ((536, 762), (774, 1000)):
        teal_piping(d, [(x0, 940), (x1, 940)], width=3)
        d.rectangle([x0, 948, x1, 1000], fill=DARK)

    img.save(f"{OUT}/royal-peacock-bottom.png")
    print("saved royal-peacock-bottom.png")


# =====================================================================
# FOOTWEAR — formal shoes, uppers + soles (round-1 v2 footprints)
# =====================================================================
def paint_footwear():
    layer = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(layer)

    def upper_poly(cx, cy):
        ox, oy = cx - 290, cy - 400
        pts = [(30, 190), (30, 430), (80, 550), (290, 600), (500, 550),
               (550, 430), (550, 190), (430, 190), (430, 380), (390, 450),
               (290, 470), (190, 450), (150, 380), (150, 190)]
        return [(x + ox, y + oy) for (x, y) in pts]

    def sole(x0, y0, x1, y1):
        d.polygon([(x0 + 20, y0), (x1 - 20, y0), (x1, y0 + 60),
                   (x1 - 8, (y0 + y1) // 2), (x1 - 18, y1 - 60),
                   (x1 - 30, y1), (x0 + 30, y1), (x0 + 18, y1 - 60),
                   (x0 + 8, (y0 + y1) // 2), (x0, y0 + 60)], fill=DARK)

    d.polygon(upper_poly(290, 400), fill=GOLD)
    d.polygon(upper_poly(700, 790), fill=GOLD)
    sole(635, 102, 819, 451)
    sole(51, 614, 195, 983)
    d.rectangle([102, 10, 963, 82], fill=GOLD)
    d.ellipse([222, 200, 358, 268], fill=DARK)
    d.ellipse([632, 668, 768, 736], fill=DARK)

    img = add_fabric(layer, mask_of(layer), seed=31, noise_amp=5)
    d = ImageDraw.Draw(img)

    def upper_details(cx, cy):
        ox, oy = cx - 290, cy - 400
        # polished toe cap
        d.polygon([(80 + ox, 500 + oy), (500 + ox, 500 + oy),
                   (480 + ox, 590 + oy), (100 + ox, 590 + oy)],
                  fill=GOLD_LT)
        d.polygon([(150 + ox, 520 + oy), (430 + ox, 520 + oy),
                   (420 + ox, 585 + oy), (160 + ox, 585 + oy)],
                  fill=GOLD_PALE)
        # teal stitching around the outer edge
        outer = [(30, 190), (30, 430), (80, 550), (290, 600), (500, 550),
                 (550, 430), (550, 190)]
        teal_piping(d, [(x + ox, y + oy) for (x, y) in outer], width=3)
        # teal trim around the ankle opening
        inner = [(150, 190), (150, 380), (190, 450), (290, 470),
                 (390, 450), (430, 380), (430, 190)]
        teal_piping(d, [(x + ox, y + oy) for (x, y) in inner], width=3)
        # tongue with peacock eye
        d.ellipse([cx - 105, cy - 60, cx + 105, cy + 60], fill=GOLD_LT)
        teal_piping(d, [(cx - 105, cy - 10), (cx + 105, cy - 10)], width=2)
        peacock_eye(d, cx, cy - 30, 26)
        # gold buckle strap across the vamp (slim, v2-style)
        d.rectangle([cx - 130, cy + 80, cx + 130, cy + 102], fill=GOLD_DK)
        d.rectangle([cx - 130, cy + 83, cx + 130, cy + 99], fill=GOLD)
        d.rectangle([cx - 16, cy + 76, cx + 16, cy + 106],
                    outline=GOLD_LT, width=3)

    upper_details(290, 400)
    upper_details(700, 790)

    def sole_details(x0, y0, x1, y1):
        d.line([(x0 + 20, y0 + 4), (x1 - 20, y0 + 4)], fill=TEAL, width=2)
        for yy in range(y0 + 50, y1 - 20, 64):
            d.line([(x0 + 14, yy), (x1 - 14, yy)], fill=TEAL_DK, width=2)

    sole_details(635, 102, 819, 451)
    sole_details(51, 614, 195, 983)

    # top strip: ankle collar with teal centre line
    d.rectangle([102, 10, 963, 82], fill=EMERALD)
    d.line([(102, 14), (963, 14)], fill=TEAL_DK, width=2)
    d.line([(102, 46), (963, 46)], fill=TEAL, width=3)
    d.line([(102, 78), (963, 78)], fill=TEAL_DK, width=2)
    # insole eyes
    peacock_eye(d, 290, 234, 18)
    peacock_eye(d, 700, 702, 18)

    img.save(f"{OUT}/royal-peacock-footwear.png")
    print("saved royal-peacock-footwear.png")


if __name__ == "__main__":
    paint_top()
    paint_bottom()
    paint_footwear()
    print("ALL PEACOCK TEXTURES DONE")
