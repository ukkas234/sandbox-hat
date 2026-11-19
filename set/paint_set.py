#!/usr/bin/env python3
"""Paint the Sandbox 'Midnight Gold' set textures (Top / Bottom / Footwear).

Layout reference: official Sandbox Studio docs
  - https://studio-docs.sandbox.game/avatars/how-to-paint-avatar-clothing.md
    * Skin = 2D textures: Top, Bottom, Shoes. Template textures are 1024x1024.
    * Top:    front = upper half, back = lower half.
    * Bottom: front = left half,  back = right half.
    * Shoes:  upper shoe shape = right shoe, lower shoe shape = left shoe,
              soles are separate islands beside them.
  - Template screenshots (docs) confirm the garment footprints used below.

Palette matches the finished fedora (charcoal felt #1A1A1F + gold #D4AD33).
Output: 1024x1024 RGB PNG, black outside the garment (UV-unused area).
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "/home/hatch/workspace/sandbox-hat/set"

# ---------- palette ----------
CHAR_DARK = (16, 16, 20)      # near-black leather / deep shadow
CHAR = (26, 26, 31)           # fedora charcoal felt
CHAR_MID = (32, 32, 40)
CHAR_LIGHT = (44, 44, 54)     # lighter charcoal panel
CHAR_PALE = (58, 58, 70)      # highlight fabric
GOLD = (212, 173, 51)         # #D4AD33 fedora gold
GOLD_LT = (240, 216, 120)
GOLD_DK = (138, 109, 31)
GOLD_DEEP = (96, 74, 18)
BLACK = (0, 0, 0)

try:
    SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
except Exception:
    SERIF_B = SANS_B = None


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def add_fabric(img, mask, weave=6, noise_amp=7, seed=7):
    """Subtle cloth weave + noise, only where mask is True."""
    rng = np.random.default_rng(seed)
    a = np.asarray(img).astype(np.int16)
    n = rng.integers(-noise_amp, noise_amp + 1, size=(H, W, 1))
    # faint horizontal weave lines
    yy = np.arange(H)[:, None, None]
    weave_pat = ((yy % weave) == 0) * 5
    a = a + n + weave_pat
    a = np.clip(a, 0, 255).astype(np.uint8)
    m = np.asarray(mask)
    base = np.asarray(img)
    out = np.where(m[..., None], a, base)
    return Image.fromarray(out)


def mask_of(layer):
    return np.asarray(layer.convert("L")) > 8


def gold_button(d, cx, cy, r):
    """A gold button: dark rim, gold face, light highlight."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD_DK)
    d.ellipse([cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2], fill=GOLD)
    d.ellipse([cx - r + 4, cy - r + 5, cx - r + 8, cy - r + 9], fill=GOLD_LT)
    # 4 thread holes
    for dx, dy in ((-4, -4), (4, -4), (-4, 4), (4, 4)):
        d.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2],
                  fill=GOLD_DEEP)


def gold_piping(d, xy, width=4):
    """Metallic gold line: dark edge, gold core, light centre."""
    d.line(xy, fill=GOLD_DK, width=width + 2)
    d.line(xy, fill=GOLD, width=width)
    d.line(xy, fill=GOLD_LT, width=max(1, width - 2))


def monogram(d, cx, cy, s=1.0, text="MG"):
    """Gold diamond outline with MG monogram."""
    r = int(26 * s)
    pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    d.polygon(pts, outline=GOLD, width=max(2, int(3 * s)))
    d.polygon([(cx, cy - r + 7 * s), (cx + r - 7 * s, cy),
               (cx, cy + r - 7 * s), (cx - r + 7 * s, cy)],
              outline=GOLD_DK, width=1)
    f = font(SERIF_B, int(20 * s))
    tb = d.textbbox((0, 0), text, font=f)
    d.text((cx - (tb[2] - tb[0]) / 2, cy - (tb[3] - tb[1]) / 2 - 2),
           text, font=f, fill=GOLD_LT)


# =====================================================================
# TOP — tailored coat, front upper half / back lower half
# =====================================================================
def paint_top():
    layer = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(layer)

    def torso(y0):
        # front/back torso: shoulders wide, slight taper to hem
        d.polygon([(312, y0 + 26), (712, y0 + 26), (706, y0 + 180),
                   (700, y0 + 474), (324, y0 + 474), (318, y0 + 180)],
                  fill=CHAR)
        # sleeves (long): horizontal, slightly tapered
        d.polygon([(24, y0 + 36), (312, y0 + 36), (312, y0 + 150),
                   (24, y0 + 168)], fill=CHAR)
        d.polygon([(712, y0 + 36), (1000, y0 + 36), (1000, y0 + 168),
                   (712, y0 + 150)], fill=CHAR)

    torso(0)      # front
    torso(512)    # back
    img = add_fabric(layer, mask_of(layer), seed=11)

    d = ImageDraw.Draw(img)
    # ---- front details ----
    # neckline shadow + collar band
    d.ellipse([442, 6, 582, 52], fill=CHAR_DARK)
    d.arc([442, 6, 582, 52], 0, 180, fill=GOLD_DK, width=3)
    # notched lapels
    d.polygon([(512, 34), (440, 60), (470, 170), (512, 120)], fill=CHAR_LIGHT)
    d.polygon([(512, 34), (584, 60), (554, 170), (512, 120)], fill=CHAR_LIGHT)
    gold_piping(d, [(512, 34), (440, 60), (470, 170)], width=3)
    gold_piping(d, [(512, 34), (584, 60), (554, 170)], width=3)
    # centre placket + gold buttons
    d.rectangle([496, 34, 528, 500], fill=CHAR_MID)
    gold_piping(d, [(496, 40), (496, 498)], width=2)
    gold_piping(d, [(528, 40), (528, 498)], width=2)
    for y in (96, 186, 276, 366, 452):
        gold_button(d, 512, y, 13)
    # side piping
    gold_piping(d, [(330, 44), (330, 492)], width=3)
    gold_piping(d, [(694, 44), (694, 492)], width=3)
    # flap pockets with gold buttons
    for x0 in (352, 556):
        d.polygon([(x0, 384), (x0 + 116, 384), (x0 + 116, 424),
                   (x0 + 58, 440), (x0, 424)], fill=CHAR_LIGHT)
        gold_piping(d, [(x0, 424), (x0 + 58, 440), (x0 + 116, 424)], width=3)
        gold_button(d, x0 + 58, 404, 9)
    # sleeve gold edges + cuff bands
    gold_piping(d, [(24, 164), (312, 146)], width=3)
    gold_piping(d, [(712, 146), (1000, 164)], width=3)
    d.rectangle([24, 40, 58, 164], fill=GOLD_DK)
    d.rectangle([28, 40, 58, 164], fill=GOLD)
    d.rectangle([966, 40, 1000, 164], fill=GOLD_DK)
    d.rectangle([966, 40, 996, 164], fill=GOLD)
    # chest emblem (gold diamond + MG) on wearer's left chest
    monogram(d, 618, 116, s=1.0)
    # subtle shoulder shading
    d.polygon([(312, 26), (712, 26), (712, 60), (312, 60)], fill=CHAR_PALE)

    # ---- back details (y + 512) ----
    # centre back seam with gold stitch dashes
    d.line([(512, 540), (512, 1000)], fill=CHAR_DARK, width=4)
    for y in range(556, 996, 28):
        d.line([(512, y), (512, y + 14)], fill=GOLD, width=2)
    # yoke line across shoulders
    gold_piping(d, [(330, 566), (694, 566)], width=3)
    # back emblem
    monogram(d, 512, 660, s=1.3)
    # side piping
    gold_piping(d, [(330, 556), (330, 1004)], width=3)
    gold_piping(d, [(694, 556), (694, 1004)], width=3)
    # centre back vent with gold trim
    gold_piping(d, [(498, 900), (498, 1000)], width=3)
    gold_piping(d, [(526, 900), (526, 1000)], width=3)
    d.polygon([(498, 900), (526, 900), (512, 930)], fill=GOLD_DK)
    # sleeve gold edges + cuffs (back)
    gold_piping(d, [(24, 676), (312, 658)], width=3)
    gold_piping(d, [(712, 658), (1000, 676)], width=3)
    d.rectangle([24, 552, 58, 676], fill=GOLD_DK)
    d.rectangle([28, 552, 58, 676], fill=GOLD)
    d.rectangle([966, 552, 1000, 676], fill=GOLD_DK)
    d.rectangle([966, 552, 996, 676], fill=GOLD)

    img.save(f"{OUT}/sandbox-top.png")
    print("saved sandbox-top.png")


# =====================================================================
# BOTTOM — tailored trousers, front left half / back right half
# =====================================================================
def paint_bottom():
    layer = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(layer)

    # front legs (x 0..512) and back legs (x 512..1024)
    for x0 in (0, 512):
        d.polygon([(x0 + 24, 24), (x0 + 250, 24), (x0 + 250, 1000),
                   (x0 + 24, 1000)], fill=CHAR)          # left leg
        d.polygon([(x0 + 262, 24), (x0 + 488, 24), (x0 + 488, 1000),
                   (x0 + 262, 1000)], fill=CHAR)          # right leg
        d.rectangle([x0 + 24, 24, x0 + 488, 84], fill=CHAR_MID)  # waistband
    img = add_fabric(layer, mask_of(layer), seed=23)
    # front panels a touch lighter than back
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([24, 84, 488, 1000], fill=(14, 14, 18, 90))
    d = ImageDraw.Draw(img)

    # ---- front details ----
    # waistband: gold button + belt loops
    gold_button(d, 256, 54, 12)
    for x in (64, 150, 256, 362, 452):
        d.rectangle([x - 8, 24, x + 8, 96], fill=CHAR_DARK)
        gold_piping(d, [(x - 8, 26), (x - 8, 94)], width=2)
        gold_piping(d, [(x + 8, 26), (x + 8, 94)], width=2)
    gold_piping(d, [(24, 84), (488, 84)], width=3)
    # double gold pinstripe down outer side of each front leg
    for x in (32, 44, 468, 480):
        gold_piping(d, [(x, 96), (x, 932)], width=3)
    # centre crease per leg
    for x in (137, 375):
        d.line([(x, 100), (x, 930)], fill=CHAR_PALE, width=3)
        d.line([(x + 3, 100), (x + 3, 930)], fill=CHAR_DARK, width=2)
    # slash pockets, gold trimmed
    gold_piping(d, [(62, 96), (140, 156)], width=4)
    d.polygon([(62, 96), (140, 156), (140, 170), (62, 110)], fill=CHAR_DARK)
    gold_piping(d, [(450, 96), (372, 156)], width=4)
    d.polygon([(450, 96), (372, 156), (372, 170), (450, 110)], fill=CHAR_DARK)
    # monogram on right front thigh
    monogram(d, 375, 280, s=0.9)
    # gold hem line + darker cuff
    for x0, x1 in ((24, 250), (262, 488)):
        gold_piping(d, [(x0, 940), (x1, 940)], width=3)
        d.rectangle([x0, 948, x1, 1000], fill=CHAR_DARK)

    # ---- back details ----
    gold_button(d, 768, 54, 12)
    for x in (576, 662, 768, 874, 964):
        d.rectangle([x - 8, 24, x + 8, 96], fill=CHAR_DARK)
    gold_piping(d, [(536, 84), (1000, 84)], width=3)
    # welt pockets with gold trim
    for x0 in (584, 828):
        d.rectangle([x0, 150, x0 + 116, 192], fill=CHAR_DARK)
        gold_piping(d, [(x0, 150), (x0 + 116, 150)], width=3)
        gold_button(d, x0 + 58, 172, 8)
    monogram(d, 886, 172, s=0.8)
    # centre back seam
    d.line([(768, 96), (768, 220)], fill=CHAR_DARK, width=4)
    # outer seam piping (subtler)
    for x in (544, 992):
        d.line([(x, 96), (x, 932)], fill=GOLD_DK, width=3)
    # hem
    for x0, x1 in ((536, 762), (774, 1000)):
        gold_piping(d, [(x0, 940), (x1, 940)], width=3)
        d.rectangle([x0, 948, x1, 1000], fill=CHAR_DARK)

    img.save(f"{OUT}/sandbox-bottom.png")
    print("saved sandbox-bottom.png")


# =====================================================================
# FOOTWEAR — dress boots, uppers + soles
# =====================================================================
def paint_footwear(v2=False):
    out_name = "sandbox-footwear-v2.png" if v2 else "sandbox-footwear.png"
    layer = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(layer)

    def upper_poly(cx, cy):
        """A shoe upper as a true U (horseshoe): arms up = ankle opening,
        bottom = toe. Points trace outer edge then inner edge."""
        ox, oy = cx - 290, cy - 400   # right shoe is the reference (290,400)
        pts = [(30, 190), (30, 430), (80, 550), (290, 600), (500, 550),
               (550, 430), (550, 190), (430, 190), (430, 380), (390, 450),
               (290, 470), (190, 450), (150, 380), (150, 190)]
        return [(x + ox, y + oy) for (x, y) in pts]

    def sole(x0, y0, x1, y1):
        # footprint: heel (top) + toe (bottom), waisted middle
        d.polygon([(x0 + 20, y0), (x1 - 20, y0), (x1, y0 + 60),
                   (x1 - 8, (y0 + y1) // 2), (x1 - 18, y1 - 60),
                   (x1 - 30, y1), (x0 + 30, y1), (x0 + 18, y1 - 60),
                   (x0 + 8, (y0 + y1) // 2), (x0, y0 + 60)], fill=CHAR_DARK)

    d.polygon(upper_poly(290, 400), fill=CHAR)   # right shoe (upper region)
    d.polygon(upper_poly(700, 790), fill=CHAR)   # left shoe (lower region)
    sole(635, 102, 819, 451)   # sole, upper right
    sole(51, 614, 195, 983)    # sole, lower left
    # top strip (ankle collar)
    d.rectangle([102, 10, 963, 82], fill=CHAR)
    # insole ovals (separate small islands)
    d.ellipse([222, 200, 358, 268], fill=CHAR_DARK)
    d.ellipse([632, 668, 768, 736], fill=CHAR_DARK)

    img = add_fabric(layer, mask_of(layer), seed=31, noise_amp=5)
    d = ImageDraw.Draw(img)

    def upper_details(cx, cy):
        ox, oy = cx - 290, cy - 400
        # polished toe cap (bottom of the U)
        d.polygon([(80 + ox, 500 + oy), (500 + ox, 500 + oy),
                   (480 + ox, 590 + oy), (100 + ox, 590 + oy)],
                  fill=CHAR_LIGHT)
        d.polygon([(150 + ox, 520 + oy), (430 + ox, 520 + oy),
                   (420 + ox, 585 + oy), (160 + ox, 585 + oy)],
                  fill=CHAR_MID)
        # gold stitching around the outer edge of the upper
        outer = [(30, 190), (30, 430), (80, 550), (290, 600), (500, 550),
                 (550, 430), (550, 190)]
        gold_piping(d, [(x + ox, y + oy) for (x, y) in outer], width=3)
        # gold trim around the ankle opening (inner edge)
        inner = [(150, 190), (150, 380), (190, 450), (290, 470),
                 (390, 450), (430, 380), (430, 190)]
        gold_piping(d, [(x + ox, y + oy) for (x, y) in inner], width=3)
        # tongue in the opening, with monogram
        d.ellipse([cx - 105, cy - 60, cx + 105, cy + 60], fill=CHAR_LIGHT)
        gold_piping(d, [(cx - 105, cy - 10), (cx + 105, cy - 10)], width=2)
        monogram(d, cx, cy - 30, s=1.0)
        # gold buckle strap across the vamp (above the toe cap)
        # v2: slimmer strap — the wide bar read as a sandal strap in preview
        if v2:
            d.rectangle([cx - 130, cy + 80, cx + 130, cy + 102], fill=GOLD_DK)
            d.rectangle([cx - 130, cy + 83, cx + 130, cy + 99], fill=GOLD)
            d.rectangle([cx - 16, cy + 76, cx + 16, cy + 106],
                        outline=GOLD_LT, width=3)
        else:
            d.rectangle([cx - 150, cy + 70, cx + 150, cy + 112], fill=GOLD_DK)
            d.rectangle([cx - 150, cy + 74, cx + 150, cy + 108], fill=GOLD)
            d.rectangle([cx - 24, cy + 66, cx + 24, cy + 116],
                        outline=GOLD_LT, width=4)

    upper_details(290, 400)
    upper_details(700, 790)

    def sole_details(x0, y0, x1, y1):
        # thin gold heel edge + tread grooves
        # v2: fewer, thinner, single dark-gold lines — the double bright
        # grooves dominated the sole view in preview
        d.line([(x0 + 20, y0 + 4), (x1 - 20, y0 + 4)], fill=GOLD, width=2)
        step = 64 if v2 else 42
        for yy in range(y0 + 50, y1 - 20, step):
            d.line([(x0 + 14, yy), (x1 - 14, yy)], fill=GOLD_DK, width=2)
            if not v2:
                d.line([(x0 + 14, yy + 5), (x1 - 14, yy + 5)], fill=GOLD, width=2)

    sole_details(635, 102, 819, 451)
    sole_details(51, 614, 195, 983)

    # top strip: dark ankle collar with a single gold centre line
    d.rectangle([102, 10, 963, 82], fill=CHAR_MID)
    d.line([(102, 14), (963, 14)], fill=GOLD_DK, width=2)
    d.line([(102, 46), (963, 46)], fill=GOLD, width=3)
    d.line([(102, 78), (963, 78)], fill=GOLD_DK, width=2)
    # insole monograms (small, on the footbed islands)
    monogram(d, 290, 234, s=0.6)
    monogram(d, 700, 702, s=0.6)

    img.save(f"{OUT}/{out_name}")
    print(f"saved {out_name}")


if __name__ == "__main__":
    paint_top()
    paint_bottom()
    paint_footwear()
    paint_footwear(v2=True)
    print("ALL TEXTURES DONE")
