#!/usr/bin/env python3
"""
BandCraft 2D - asset generator  (needs:  pip install pillow)
Run from the project root:   python tools/make_assets.py

It draws the static art used by src/pages/game/game.ux into src/common/generated/.
The numbers below are the SAME numbers used in game.ux (look for "LAYOUT" there).
If you change a number here, change it in game.ux too (or just leave both alone).
"""
from PIL import Image, ImageDraw, ImageFont
import os, random

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'common')
A = os.path.join(ROOT, 'assets', 'game')      # original Minecraft textures
OUT = os.path.join(ROOT, 'generated')
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ LAYOUT (px, screen is 192x490)
W, H       = 192, 490
BLOCK      = 32            # one world block = 32x32 px (textures are 16x16, drawn 2x, NO gaps)
COLS       = 6             # 6 blocks * 32 = 192 = full screen width
SURFACE_Y  = 186           # top of the grass row (Steve's feet stand here)
ROWS       = 3             # grass, dirt, stone
PANEL_Y    = SURFACE_Y + ROWS * BLOCK   # 282: dark panel (hotbar + buttons) starts here
SLOT       = 38            # hotbar slot size (item is 32x32 inside = 2x texture)
SLOT_X     = [8, 54, 100, 146]          # 4 columns
SLOT_Y     = [290, 334]                 # 2 rows -> 8 slots
BTN_W, BTN_H = 60, 48
BTN_X      = [4, 66, 128]
BTN_Y      = [384, 436]                 # row 1: left/jump/right   row 2: mine/place/craft
PLAYER_W, PLAYER_H = 24, 60             # Steve on screen (zombie is 36x60, same height)
CRAFT = dict(x=8, y=96, w=176, h=140)   # crafting panel

def tex(path, size=None):
    im = Image.open(os.path.join(A, path)).convert('RGBA')
    return im.resize((size, size), Image.NEAREST) if size else im

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

# ------------------------------------------------------------------ fonts
try:
    FONT = ImageFont.load_default(size=13)
except TypeError:
    FONT = ImageFont.load_default()

# ------------------------------------------------------------------ pieces
def slot_frame(d, x, y, s):
    d.rectangle((x, y, x + s - 1, y + s - 1), fill=(34, 34, 34))
    d.rectangle((x + 2, y + 2, x + s - 3, y + s - 3), fill=(78, 78, 78))
    d.rectangle((x + 2, y + s - 4, x + s - 3, y + s - 3), fill=(118, 118, 118))   # bottom light
    d.rectangle((x + s - 4, y + 2, x + s - 3, y + s - 3), fill=(118, 118, 118))   # right light
    d.rectangle((x + 2, y + 2, x + s - 5, y + 3), fill=(46, 46, 46))              # top dark
    d.rectangle((x + 2, y + 2, x + 3, y + s - 5), fill=(46, 46, 46))              # left dark

def button(im, x, y, w, h):
    d = ImageDraw.Draw(im)
    d.rectangle((x, y, x + w - 1, y + h - 1), fill=(20, 20, 20))
    d.rectangle((x + 1, y + 1, x + w - 2, y + h - 2), fill=(126, 126, 126))
    d.rectangle((x + 1, y + 1, x + w - 2, y + 3), fill=(196, 196, 196))
    d.rectangle((x + 1, y + 1, x + 3, y + h - 2), fill=(196, 196, 196))
    d.rectangle((x + 1, y + h - 4, x + w - 2, y + h - 2), fill=(72, 72, 72))
    d.rectangle((x + w - 4, y + 1, x + w - 2, y + h - 2), fill=(72, 72, 72))

def arrow(d, cx, cy, kind):
    pts = {'left':  [(cx + 10, cy - 15), (cx - 13, cy), (cx + 10, cy + 15)],
           'right': [(cx - 10, cy - 15), (cx + 13, cy), (cx - 10, cy + 15)],
           'up':    [(cx - 15, cy + 10), (cx, cy - 13), (cx + 15, cy + 10)]}[kind]
    d.polygon(pts, fill=(238, 238, 238), outline=(25, 25, 25))
    d.line(pts + [pts[0]], fill=(25, 25, 25), width=2)

def pickaxe(im, cx, cy):
    d = ImageDraw.Draw(im)
    d.line((cx - 12, cy + 13, cx + 6, cy - 5), fill=(25, 25, 25), width=7)
    d.line((cx - 12, cy + 13, cx + 6, cy - 5), fill=(150, 100, 50), width=4)
    head = [(cx - 9, cy - 10), (cx + 4, cy - 15), (cx + 15, cy - 4), (cx + 10, cy + 9), (cx + 8, cy - 1), (cx + 1, cy - 8)]
    d.polygon(head, fill=(205, 215, 220), outline=(25, 25, 25))
    d.line(head + [head[0]], fill=(25, 25, 25), width=2)

def place_icon(im, cx, cy):
    t = tex('blocks/oak-planks.png', 26)
    d = ImageDraw.Draw(im)
    d.rectangle((cx - 15, cy - 15, cx + 14, cy + 14), fill=(25, 25, 25))
    im.alpha_composite(t, (cx - 13, cy - 13))
    d.rectangle((cx + 4, cy - 15, cx + 15, cy - 4), fill=(25, 25, 25))
    d.rectangle((cx + 9, cy - 13, cx + 10, cy - 6), fill=(120, 255, 120))
    d.rectangle((cx + 6, cy - 10, cx + 13, cy - 9), fill=(120, 255, 120))

def craft_icon(im, cx, cy):
    d = ImageDraw.Draw(im)
    for dx in (-15, 1):
        for dy in (-15, 1):
            d.rectangle((cx + dx, cy + dy, cx + dx + 13, cy + dy + 13), fill=(25, 25, 25))
            d.rectangle((cx + dx + 2, cy + dy + 2, cx + dx + 11, cy + dy + 11), fill=(215, 215, 215))
            d.rectangle((cx + dx + 2, cy + dy + 9, cx + dx + 11, cy + dy + 11), fill=(150, 150, 150))

# ------------------------------------------------------------------ scene.png  (sky + terrain + HUD + hotbar + buttons)
def make_scene(variant=0):
    # variant 0 = plains, 1 = forest (trees are decoration only), 2 = desert (sand instead of grass/dirt)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(im)
    # sky
    for y in range(SURFACE_Y):
        d.line((0, y, W, y), fill=lerp((92, 164, 236), (172, 216, 255), y / SURFACE_Y))
    # sun
    d.rectangle((146, 38, 169, 61), fill=(255, 244, 170)); d.rectangle((150, 42, 165, 57), fill=(255, 252, 215))
    # clouds (blocky)
    for cx, cy in ((14, 78), (96, 118), (122, 84)):
        for r in ((0, 6, 38, 8), (6, 0, 24, 8), (14, 12, 22, 6)):
            d.rectangle((cx + r[0], cy + r[1], cx + r[0] + r[2], cy + r[1] + r[3]), fill=(255, 255, 255))
    # terrain: every texture is scaled 2x to fill its 32x32 cell -> blocks touch each other
    rows = ['blocks/grass-block-side.png', 'blocks/dirt.png', 'blocks/stone.png']
    if variant == 2: rows = ['blocks/sand.png', 'blocks/sand.png', 'blocks/stone.png']
    for r, p in enumerate(rows):
        t = tex(p, BLOCK)
        for c in range(COLS):
            im.alpha_composite(t, (c * BLOCK, SURFACE_Y + r * BLOCK))
    if variant == 1:                       # two oak trees standing on the grass (behind Steve)
        log, leaves = tex('blocks/oak-log.png', BLOCK), tex('blocks/oak-leaves.png', BLOCK)
        for tc in (1, 4):
            for k in (1, 2): im.alpha_composite(log, (tc * BLOCK, SURFACE_Y - k * BLOCK))
            for k in (3, 4):
                for lc in (tc - 1, tc, tc + 1): im.alpha_composite(leaves, (lc * BLOCK, SURFACE_Y - k * BLOCK))
    coal = tex('blocks/coal-ore.png', BLOCK)
    for c in (1, 4):                       # a few coal ores in the stone row
        im.alpha_composite(coal, (c * BLOCK, SURFACE_Y + 2 * BLOCK))
    # dark panel (stone texture, darkened)
    st = tex('blocks/stone.png', BLOCK)
    for y in range(PANEL_Y, H, BLOCK):
        for x in range(0, W, BLOCK):
            im.paste(st, (x, y))
    shade = Image.new('RGBA', (W, H - PANEL_Y), (0, 0, 0, 175))
    im.alpha_composite(shade, (0, PANEL_Y))
    d.rectangle((0, PANEL_Y, W, PANEL_Y + 1), fill=(15, 15, 15))
    d.rectangle((0, PANEL_Y + 2, W, PANEL_Y + 3), fill=(95, 95, 95))
    # hotbar: 8 slots (2 rows x 4), item 2x inside the slot
    items = ['blocks/grass-block-side.png', 'blocks/dirt.png', 'blocks/stone.png', 'blocks/sand.png',
             'blocks/oak-planks.png', 'blocks/coal-ore.png', 'blocks/torch.png', 'items/stick.png']
    n = 0
    for sy in SLOT_Y:
        for sx in SLOT_X:
            slot_frame(d, sx, sy, SLOT)
            im.alpha_composite(tex(items[n], 32), (sx + 3, sy + 3))
            n += 1
    # status bars (hearts left, hunger right): icons come from the original 32x32 art
    def icon16(name):
        return Image.open(os.path.join(A, 'ui', name)).convert('RGBA').resize((16, 16), Image.LANCZOS)
    heart, hunger = icon16('heart.png'), icon16('hunger.png')
    for i in range(5):
        im.alpha_composite(heart, (4 + i * 18, 5))
        im.alpha_composite(hunger, (W - 4 - 16 - (4 - i) * 18, 5))
    # control buttons
    labels = [('left', 'up', 'right'), ('mine', 'place', 'craft')]
    for r, row in enumerate(labels):
        for c, kind in enumerate(row):
            x, y = BTN_X[c], BTN_Y[r]
            button(im, x, y, BTN_W, BTN_H)
            cx, cy = x + BTN_W // 2, y + BTN_H // 2
            dd = ImageDraw.Draw(im)
            if kind in ('left', 'right', 'up'): arrow(dd, cx, cy, kind)
            elif kind == 'mine': pickaxe(im, cx, cy)
            elif kind == 'place': place_icon(im, cx, cy)
            else: craft_icon(im, cx, cy)
    im.convert('RGBA').save(os.path.join(OUT, 'scene%d.png' % variant), optimize=True)

# ------------------------------------------------------------------ small overlay pieces
def make_overlays():
    # hole = what you see after mining the grass block (plain sky colour, same as horizon)
    Image.new('RGBA', (BLOCK, BLOCK), (172, 216, 255, 255)).save(os.path.join(OUT, 'hole.png'))
    # placeable blocks, 2x, one file each (hotbar slots 0..5)
    for name, p in (('grass', 'blocks/grass-block-side.png'), ('dirt', 'blocks/dirt.png'), ('stone', 'blocks/stone.png'),
                    ('sand', 'blocks/sand.png'), ('planks', 'blocks/oak-planks.png'), ('coal', 'blocks/coal-ore.png')):
        tex(p, BLOCK).save(os.path.join(OUT, 'b-%s.png' % name), optimize=True)
    # hotbar selection frame (42x42, drawn around the slot)
    s = SLOT + 4
    sel = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(sel)
    d.rectangle((0, 0, s - 1, s - 1), outline=(20, 20, 20), width=1)
    d.rectangle((1, 1, s - 2, s - 2), outline=(255, 255, 255), width=3)
    sel.save(os.path.join(OUT, 'sel.png'))
    # target marker (outline of the block Steve will mine / place on)
    t = Image.new('RGBA', (BLOCK, BLOCK), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rectangle((0, 0, BLOCK - 1, BLOCK - 1), outline=(0, 0, 0), width=1)
    d.rectangle((1, 1, BLOCK - 2, BLOCK - 2), outline=(255, 255, 255), width=2)
    t.save(os.path.join(OUT, 'target.png'))
    # Steve: original is 16x40 -> 24x60 (same height as the zombie). Mirror copy for facing left.
    st = Image.open(os.path.join(A, 'player', 'right', 'idle.png')).convert('RGBA').resize((PLAYER_W, PLAYER_H), Image.NEAREST)
    st.save(os.path.join(OUT, 'steve-r.png'), optimize=True)
    st.transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(OUT, 'steve-l.png'), optimize=True)

# ------------------------------------------------------------------ craft.png
def make_craft():
    c = CRAFT
    im = Image.new('RGBA', (c['w'], c['h']), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, c['w'] - 1, c['h'] - 1), fill=(14, 14, 14))
    d.rectangle((2, 2, c['w'] - 3, c['h'] - 3), fill=(52, 52, 52), outline=(140, 140, 140), width=2)
    d.text((10, 8), 'Crafting', font=FONT, fill=(235, 235, 235))
    # close button (top-right 24x20)  -> hit area in game.ux: craftClose
    d.rectangle((c['w'] - 30, 6, c['w'] - 8, 26), fill=(150, 40, 40), outline=(20, 20, 20), width=2)
    d.line((c['w'] - 24, 11, c['w'] - 14, 21), fill=(255, 255, 255), width=3)
    d.line((c['w'] - 24, 21, c['w'] - 14, 11), fill=(255, 255, 255), width=3)
    for gx in (12, 54):
        for gy in (40, 82):
            slot_frame(d, gx, gy, SLOT)
    # arrow + output
    d.polygon([(98, 79), (110, 79), (110, 71), (122, 85), (110, 99), (110, 91), (98, 91)], fill=(200, 200, 200), outline=(20, 20, 20))
    slot_frame(d, 130, 66, 40)
    im.save(os.path.join(OUT, 'craft.png'), optimize=True)

if __name__ == '__main__':
    for v in (0, 1, 2): make_scene(v)
    make_overlays(); make_craft()
    # zombie decoration (unchanged art)
    Image.open(os.path.join(A, 'mobs', 'zombie', 'right', 'idle.png')).convert('RGBA').save(os.path.join(OUT, 'zombie.png'), optimize=True)
    print('assets written to', OUT)
