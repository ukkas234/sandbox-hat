#!/usr/bin/env python3
"""Paint the NEON RONIN set textures (Top / Bottom / Footwear).

Same garment footprints + layout rules as round 1 (paint_set.py), which
follow the official Sandbox Studio docs:
  - Top:    front = upper half, back = lower half.
  - Bottom: front = left half,  back = right half.
  - Shoes:  upper shoe shape = right shoe, lower shoe shape = left shoe,
            soles are separate islands beside them.
  - Footprint coordinates are copied from round-1 v2 (footwear v2 was the
    fixed layout; do not re-derive the shoe shape).

Palette: black/charcoal + neon cyan #00F0FF + thin magenta accent.
Motif: kimono wrap + diagonal sash + circuit traces (right-angle lines).
Output: 1024x1024 RGB PNG, black outside the garment.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "/home/hatch/workspace/sandbox-hat/round2/neon-ronin"

# ---------- palette ----------
BLK = (16, 16, 20)          # darkest shade — must stay > pure black (0,0,0)
                            # so UV-used pixels are never confused with the
                            # unused black background (round-1 lesson)
CHAR = (22, 22, 30)         # charcoal
CHAR_MID = (30, 30, 40)
CHAR_LT = (46, 46, 58)      # lighter panel
CHAR_PALE = (62, 62, 76)    # highlight fabric
CYAN = (0, 255, 255)        # #00FFFF full neon cyan (BOLD v2: was #00F0FF)
CYAN_LT = (150, 250, 255)
CYAN_DK = (0, 140, 165)
CYAN_DEEP = (0, 80, 100)
MAG = (255, 45, 150)        # thin magenta accent
SILVER = (150, 160, 170)
BLACK = (0, 0, 0)

try:
    SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
except Exception:
    SANS_B = None


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


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


def cyan_piping(d, xy, width=4):
    """Neon line: dark edge, cyan core, light centre."""
    d.line(xy, fill=CYAN_DK, width=width + 2)
    d.line(xy, fill=CYAN, width=width)
    d.line(xy, fill=CYAN_LT, width=max(1, width - 2))


def cyan_dot(d, cx, cy, r=5):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CYAN_DK)
    d.ellipse([cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2], fill=CYAN)
    d.ellipse([cx - r + 4, cy - r + 4, cx - r + 7, cy - r + 7], fill=CYAN_LT)


def ronin_emblem(d, cx, cy, s=1.0, color=CYAN):
    """Drawn emblem (no font): diamond outline + torii-like gate bar + dot.
    Represents the ronin mark; s scales it. color = outline/bar colour
    (BOLD v2: magenta variant for use on the cyan back crest)."""
    r = int(26 * s)
    pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    d.polygon(pts, outline=color, width=max(2, int(3 * s)))
    d.line([(cx - r + 8 * s, cy - 4 * s), (cx + r - 8 * s, cy - 4 * s)],
           fill=color, width=max(2, int(2 * s)))
    d.line([(cx, cy - r + 8 * s), (cx, cy + r - 8 * s)],
           fill=color, width=max(2, int(2 * s)))
    cyan_dot(d, cx, cy, max(3, int(5 * s)))


def circuit(d, x0, y0, x1, y1, n=3, seed=1):
    """Right-angle circuit traces inside rect (x0,y0)-(x1,y1): a few
    horizontal runs with vertical drops + endpoint dots."""
    import random
    rnd = random.Random(seed)
    for i in range(n):
        y = y0 + (y1 - y0) * (i + 1) / (n + 1)
        xa = x0 + rnd.randint(0, (x1 - x0) // 3)
        xb = x0 + rnd.randint((x1 - x0) // 2, x1 - x0)
        cyan_piping(d, [(xa, y), (xb, y)], width=3)
        drop = rnd.randint(8, 26) * (1 if rnd.random() > 0.5 else -1)
        cyan_piping(d, [(xb, y), (xb, y + drop)], width=3)
        cyan_dot(d, xb, y + drop, 5)
        cyan_dot(d, xa, y, 5)


# =====================================================================
# TOP — kimono/jacket, front upper half / back lower half
# =====================================================================
def paint_top():
    layer = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(layer)

    def torso(y0):
        d.polygon([(312, y0 + 26), (712, y0 + 26), (706, y0 + 180),
                   (700, y0 + 474), (324, y0 + 474), (318, y0 + 180)],
                  fill=CHAR)
        # wide kimono sleeves
        d.polygon([(24, y0 + 36), (312, y0 + 36), (312, y0 + 150),
                   (24, y0 + 168)], fill=CHAR)
        d.polygon([(712, y0 + 36), (1000, y0 + 36), (1000, y0 + 168),
                   (712, y0 + 150)], fill=CHAR)

    torso(0)
    torso(512)
    img = add_fabric(layer, mask_of(layer), seed=11)
    d = ImageDraw.Draw(img)

    # ---- BOLD v2 front: ASYMMETRIC wide panels + steep magenta sash ----
    # wide cyan side panels — LEFT wider than right (broken symmetry)
    d.rectangle([330, 30, 382, 470], fill=CYAN_DK)
    d.rectangle([334, 30, 378, 470], fill=CYAN)
    d.rectangle([346, 30, 354, 470], fill=CYAN_LT)
    d.rectangle([664, 30, 694, 470], fill=CYAN_DK)
    d.rectangle([668, 30, 690, 470], fill=CYAN)
    # fold shading: diagonal shadow bands + one light fold (jacket not flat)
    d.polygon([(400, 30), (414, 30), (348, 470), (334, 470)], fill=(10, 10, 14))
    d.polygon([(580, 30), (592, 30), (668, 470), (656, 470)], fill=(10, 10, 14))
    d.polygon([(486, 30), (494, 30), (556, 470), (548, 470)], fill=CHAR_PALE)
    # collar V (wrap): left panel over right, thicker cyan piping
    d.polygon([(442, 26), (582, 26), (560, 120), (512, 200), (464, 120)],
              fill=CHAR_MID)
    cyan_piping(d, [(442, 26), (512, 200)], width=5)
    cyan_piping(d, [(582, 26), (512, 200)], width=5)
    # STEEP magenta diagonal sash (obi) with cyan edges
    d.polygon([(330, 320), (700, 180), (700, 252), (330, 392)], fill=MAG)
    cyan_piping(d, [(330, 320), (700, 180)], width=4)
    cyan_piping(d, [(330, 392), (700, 252)], width=4)
    # flowing curved circuit arcs (not straight lines only)
    d.arc([400, 60, 580, 240], 200, 340, fill=CYAN, width=5)
    d.arc([520, 300, 680, 460], 180, 320, fill=CYAN, width=4)
    d.arc([380, 380, 520, 520], 270, 60, fill=CYAN_DK, width=4)
    cyan_dot(d, 580, 150, 6)
    cyan_dot(d, 600, 380, 6)
    # magenta hem band across the torso base
    d.rectangle([330, 448, 694, 474], fill=MAG)
    d.line([(330, 448), (694, 448)], fill=CYAN, width=4)
    # BIG torii emblem OFF-CENTRE (left chest) + small one right
    ronin_emblem(d, 400, 412, s=1.9)
    ronin_emblem(d, 640, 430, s=0.8)
    # sleeve cyan edges + WIDE cuff bands with magenta outer stripe
    cyan_piping(d, [(24, 164), (312, 146)], width=4)
    cyan_piping(d, [(712, 146), (1000, 164)], width=4)
    d.rectangle([24, 40, 78, 164], fill=CYAN_DK)
    d.rectangle([30, 40, 72, 164], fill=CYAN)
    d.rectangle([24, 40, 30, 164], fill=MAG)
    d.rectangle([946, 40, 1000, 164], fill=CYAN_DK)
    d.rectangle([952, 40, 994, 164], fill=CYAN)
    d.rectangle([994, 40, 1000, 164], fill=MAG)
    # shoulder band: bright cyan
    d.polygon([(312, 26), (712, 26), (712, 60), (312, 60)], fill=CYAN)
    d.line([(312, 60), (712, 60)], fill=CYAN_LT, width=4)

    # ---- BOLD v2 back: giant filled-cyan crest + diagonal sash + flame arc ----
    # wide cyan side panels (back) — LEFT wider than right
    d.rectangle([330, 542, 382, 982], fill=CYAN_DK)
    d.rectangle([334, 542, 378, 982], fill=CYAN)
    d.rectangle([346, 542, 354, 982], fill=CYAN_LT)
    d.rectangle([664, 542, 694, 982], fill=CYAN_DK)
    d.rectangle([668, 542, 690, 982], fill=CYAN)
    # fold shading: diagonal shadow bands (back)
    d.polygon([(400, 542), (414, 542), (348, 982), (334, 982)], fill=(10, 10, 14))
    d.polygon([(580, 542), (592, 542), (668, 982), (656, 982)], fill=(10, 10, 14))
    # back collar band
    d.rectangle([442, 538, 582, 570], fill=CHAR_MID)
    cyan_piping(d, [(442, 570), (582, 570)], width=4)
    # sweeping flame arc across the back (behind the crest)
    d.arc([340, 600, 700, 980], 300, 120, fill=CYAN_DK, width=10)
    d.arc([360, 620, 680, 960], 300, 120, fill=CYAN, width=5)
    # giant crest: outline rings + filled cyan core diamond
    cx, cy = 512, 760
    for r, w in ((190, 5), (150, 4)):
        d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)],
                  outline=CYAN, width=w)
    d.polygon([(cx, cy - 110), (cx + 110, cy), (cx, cy + 110), (cx - 110, cy)],
              fill=CYAN_DK)
    d.polygon([(cx, cy - 70), (cx + 70, cy), (cx, cy + 70), (cx - 70, cy)],
              fill=CYAN)
    # magenta emblem slightly OFF-CENTRE inside the crest
    ronin_emblem(d, 545, 745, s=2.2, color=MAG)
    # circuit spokes from the crest to the edges
    for (x0, y0, x1, y1) in ((362, 760, 330, 760), (662, 760, 694, 760),
                             (512, 610, 512, 566), (512, 910, 512, 990)):
        cyan_piping(d, [(x0, y0), (x1, y1)], width=3)
        cyan_dot(d, x1, y1, 5)
    # sash continues across the back waist — DIAGONAL magenta
    d.polygon([(330, 890), (700, 830), (700, 900), (330, 960)], fill=MAG)
    cyan_piping(d, [(330, 890), (700, 830)], width=4)
    cyan_piping(d, [(330, 960), (700, 900)], width=4)
    # sleeve edges + WIDE cuffs (back)
    cyan_piping(d, [(24, 676), (312, 658)], width=4)
    cyan_piping(d, [(712, 658), (1000, 676)], width=4)
    d.rectangle([24, 552, 78, 676], fill=CYAN_DK)
    d.rectangle([30, 552, 72, 676], fill=CYAN)
    d.rectangle([24, 552, 30, 676], fill=MAG)
    d.rectangle([946, 552, 1000, 676], fill=CYAN_DK)
    d.rectangle([952, 552, 994, 676], fill=CYAN)
    d.rectangle([994, 552, 1000, 676], fill=MAG)

    img.save(f"{OUT}/neon-ronin-top.png")
    print("saved neon-ronin-top.png")


# =====================================================================
# BOTTOM — hakama, front left half / back right half
# =====================================================================
def paint_bottom():
    layer = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(layer)

    for x0 in (0, 512):
        d.polygon([(x0 + 24, 24), (x0 + 250, 24), (x0 + 250, 1000),
                   (x0 + 24, 1000)], fill=CHAR)
        d.polygon([(x0 + 262, 24), (x0 + 488, 24), (x0 + 488, 1000),
                   (x0 + 262, 1000)], fill=CHAR)
        d.rectangle([x0 + 24, 24, x0 + 488, 84], fill=CHAR_MID)
    img = add_fabric(layer, mask_of(layer), seed=23)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([24, 84, 488, 1000], fill=(10, 10, 14, 90))
    d = ImageDraw.Draw(img)

    # ---- front: hakama pleats + cyan hem trim ----
    # belt: wide cyan band + big magenta buckle
    d.rectangle([24, 30, 488, 48], fill=CYAN)
    d.rectangle([216, 30, 296, 78], outline=MAG, width=6)
    d.rectangle([228, 42, 284, 66], fill=CYAN)
    for x in (64, 150, 362, 452):
        d.rectangle([x - 8, 24, x + 8, 96], fill=BLK)
    cyan_piping(d, [(24, 84), (488, 84)], width=3)
    # BOLD v2: wide cyan side stripes — LEFT leg wider than RIGHT leg
    d.rectangle([24, 96, 70, 932], fill=CYAN_DK)
    d.rectangle([28, 96, 66, 932], fill=CYAN)
    d.rectangle([40, 96, 48, 932], fill=CYAN_LT)
    d.rectangle([450, 96, 488, 932], fill=CYAN_DK)
    d.rectangle([454, 96, 484, 932], fill=CYAN)
    # fold shading: one diagonal shadow band per leg
    d.polygon([(150, 96), (164, 96), (120, 932), (106, 932)], fill=(10, 10, 14))
    d.polygon([(360, 96), (374, 96), (420, 932), (406, 932)], fill=(10, 10, 14))
    # pleat lines: 3 vertical folds per leg
    for x in (80, 137, 194, 318, 375, 432):
        d.line([(x, 96), (x, 930)], fill=CHAR_PALE, width=3)
        d.line([(x + 4, 96), (x + 4, 930)], fill=BLK, width=2)
    # curved circuit accent on the right front thigh
    d.arc([300, 220, 470, 360], 180, 360, fill=CYAN, width=4)
    d.arc([320, 240, 450, 340], 180, 360, fill=CYAN_DK, width=3)
    cyan_dot(d, 385, 290, 5)
    ronin_emblem(d, 375, 420, s=1.6)
    # BOLD v2 hem: wide magenta band (sloped — left higher than right)
    d.polygon([(24, 928), (250, 928), (250, 1000), (24, 1000)], fill=MAG)
    d.polygon([(262, 916), (488, 916), (488, 1000), (262, 1000)], fill=MAG)
    d.line([(24, 928), (250, 928)], fill=CYAN, width=5)
    d.line([(262, 916), (488, 916)], fill=CYAN, width=5)

    # ---- back ----
    d.rectangle([738, 30, 1000, 48], fill=CYAN)
    d.rectangle([728, 30, 808, 78], outline=MAG, width=6)
    d.rectangle([740, 42, 796, 66], fill=CYAN)
    for x in (576, 662, 874, 964):
        d.rectangle([x - 8, 24, x + 8, 96], fill=BLK)
    cyan_piping(d, [(536, 84), (1000, 84)], width=3)
    # BOLD v2: wide cyan side stripes (back) — RIGHT leg wider than LEFT
    d.rectangle([536, 96, 574, 932], fill=CYAN_DK)
    d.rectangle([540, 96, 570, 932], fill=CYAN)
    d.rectangle([962, 96, 1000, 932], fill=CYAN_DK)
    d.rectangle([966, 96, 996, 932], fill=CYAN)
    d.rectangle([976, 96, 984, 932], fill=CYAN_LT)
    # fold shading (back)
    d.polygon([(662, 96), (676, 96), (632, 932), (618, 932)], fill=(10, 10, 14))
    d.polygon([(872, 96), (886, 96), (932, 932), (918, 932)], fill=(10, 10, 14))
    for x in (592, 649, 706, 830, 887, 944):
        d.line([(x, 96), (x, 930)], fill=CHAR_PALE, width=3)
        d.line([(x + 4, 96), (x + 4, 930)], fill=BLK, width=2)
    # back waist tie (knot) at centre back — bigger, off-centre
    ronin_emblem(d, 790, 150, s=1.6)
    # centre back seam
    d.line([(768, 96), (768, 220)], fill=BLK, width=4)
    # curved accent on the left back thigh
    d.arc([580, 300, 740, 440], 180, 360, fill=CYAN, width=4)
    cyan_dot(d, 660, 370, 5)
    # BOLD v2 hem: wide magenta band (sloped opposite to front)
    d.polygon([(536, 916), (762, 916), (762, 1000), (536, 1000)], fill=MAG)
    d.polygon([(774, 928), (1000, 928), (1000, 1000), (774, 1000)], fill=MAG)
    d.line([(536, 916), (762, 916)], fill=CYAN, width=5)
    d.line([(774, 928), (1000, 928)], fill=CYAN, width=5)

    img.save(f"{OUT}/neon-ronin-bottom.png")
    print("saved neon-ronin-bottom.png")


# =====================================================================
# FOOTWEAR — tabi boots, uppers + soles (round-1 v2 footprints)
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
                   (x0 + 8, (y0 + y1) // 2), (x0, y0 + 60)], fill=BLK)

    d.polygon(upper_poly(290, 400), fill=CHAR)   # right shoe (upper region)
    d.polygon(upper_poly(700, 790), fill=CHAR)   # left shoe (lower region)
    sole(635, 102, 819, 451)   # sole, upper right
    sole(51, 614, 195, 983)    # sole, lower left
    d.rectangle([102, 10, 963, 82], fill=CHAR)
    d.ellipse([222, 200, 358, 268], fill=BLK)
    d.ellipse([632, 668, 768, 736], fill=BLK)

    img = add_fabric(layer, mask_of(layer), seed=31, noise_amp=5)
    d = ImageDraw.Draw(img)

    def upper_details(cx, cy, variant="A"):
        ox, oy = cx - 290, cy - 400
        # BOLD v2: big toe cap — variant A cyan, variant B magenta
        toe = CYAN if variant == "A" else MAG
        d.polygon([(80 + ox, 500 + oy), (500 + ox, 500 + oy),
                   (480 + ox, 590 + oy), (100 + ox, 590 + oy)],
                  fill=toe)
        d.line([(290 + ox, 500 + oy), (290 + ox, 590 + oy)], fill=BLK, width=6)
        # wide diagonal accent stripe across the vamp
        d.polygon([(120 + ox, 470 + oy), (460 + ox, 400 + oy),
                   (470 + ox, 440 + oy), (130 + ox, 500 + oy)],
                  fill=CYAN_DK if variant == "A" else MAG)
        # cyan stitching around the outer edge
        outer = [(30, 190), (30, 430), (80, 550), (290, 600), (500, 550),
                 (550, 430), (550, 190)]
        cyan_piping(d, [(x + ox, y + oy) for (x, y) in outer], width=4)
        # cyan trim around the ankle opening
        inner = [(150, 190), (150, 380), (190, 450), (290, 470),
                 (390, 450), (430, 380), (430, 190)]
        cyan_piping(d, [(x + ox, y + oy) for (x, y) in inner], width=4)
        # tongue with emblem (bigger on variant A)
        d.ellipse([cx - 105, cy - 60, cx + 105, cy + 60], fill=CHAR_LT)
        cyan_piping(d, [(cx - 105, cy - 10), (cx + 105, cy - 10)], width=3)
        ronin_emblem(d, cx, cy - 30, s=1.4 if variant == "A" else 1.0)
        # WIDE buckle strap across the vamp (swapped accent per variant)
        strap = CYAN if variant == "A" else MAG
        d.rectangle([cx - 130, cy + 78, cx + 130, cy + 108], fill=CYAN_DK)
        d.rectangle([cx - 130, cy + 82, cx + 130, cy + 104], fill=strap)
        d.rectangle([cx - 16, cy + 74, cx + 16, cy + 112],
                    outline=SILVER, width=3)

    upper_details(290, 400, "A")
    upper_details(700, 790, "B")

    def sole_details(x0, y0, x1, y1):
        # BOLD v2: wide magenta heel edge + thicker tread grooves
        d.line([(x0 + 20, y0 + 4), (x1 - 20, y0 + 4)], fill=MAG, width=6)
        for yy in range(y0 + 50, y1 - 20, 64):
            d.line([(x0 + 14, yy), (x1 - 14, yy)], fill=CYAN_DK, width=3)

    sole_details(635, 102, 819, 451)
    sole_details(51, 614, 195, 983)

    # top strip: ankle collar with wide cyan band + magenta edges
    d.rectangle([102, 10, 963, 82], fill=CHAR_MID)
    d.line([(102, 14), (963, 14)], fill=MAG, width=4)
    d.line([(102, 40), (963, 40)], fill=CYAN, width=10)
    d.line([(102, 78), (963, 78)], fill=MAG, width=4)
    # insole emblems
    ronin_emblem(d, 290, 234, s=0.6)
    ronin_emblem(d, 700, 702, s=0.6)

    img.save(f"{OUT}/neon-ronin-footwear.png")
    print("saved neon-ronin-footwear.png")


if __name__ == "__main__":
    paint_top()
    paint_bottom()
    paint_footwear()
    print("ALL RONIN TEXTURES DONE")
