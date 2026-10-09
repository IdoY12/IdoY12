#!/usr/bin/env python3
"""
Generates the animated pixel-art banner used in the profile README:
  assets/hero.svg  - "Midnight Castle": a dark night march of knights, a wizard,
                     a robot, a war elephant, dragons and a UFO, each dressed in
                     the colours of a technology and carrying its name.

Everything is self-contained: no external fonts (GitHub strips them from
SVGs), every glyph is a 5x7 bitmap, and all motion is plain CSS keyframes,
which GitHub renders inside <img> tags.

Run: python3 scripts/make-hero.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 5x7 bitmap font. '1' = lit pixel.
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    " ": ["00000"] * 7,
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ",": ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    ">": ["10000", "01000", "00100", "00010", "00100", "01000", "10000"],
    "<": ["00001", "00010", "00100", "01000", "00100", "00010", "00001"],
    "_": ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "|": ["00100"] * 7,
    "@": ["01110", "10001", "10111", "10101", "10111", "10000", "01110"],
    "#": ["01010", "01010", "11111", "01010", "11111", "01010", "01010"],
    "{": ["00110", "01000", "01000", "11000", "01000", "01000", "00110"],
    "}": ["01100", "00010", "00010", "00011", "00010", "00010", "01100"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "?": ["01110", "10001", "00001", "00010", "00100", "00000", "00100"],
    "'": ["00100", "00100", "00000", "00000", "00000", "00000", "00000"],
    "=": ["00000", "00000", "11111", "00000", "11111", "00000", "00000"],
    "*": ["00000", "10101", "01110", "11111", "01110", "10101", "00000"],
    "$": ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
    "~": ["00000", "00000", "01000", "10101", "00010", "00000", "00000"],
    # custom glyphs
    "♥": ["01010", "11111", "11111", "11111", "01110", "00100", "00000"],  # heart
    "★": ["00100", "00100", "11111", "01110", "01110", "01010", "00000"],  # star
}


def text_width(text, px, gap=1):
    return len(text) * (5 + gap) * px - gap * px


def text_pixels(text, x, y, px, fill, gap=1, extra=""):
    """Returns SVG rects for `text`, top-left at (x, y), pixel size px."""
    out = []
    cx = x
    for ch in text.upper():
        glyph = FONT.get(ch, FONT["?"])
        for row, bits in enumerate(glyph):
            # merge horizontal runs into single rects to keep files small
            col = 0
            while col < 5:
                if bits[col] == "1":
                    start = col
                    while col < 5 and bits[col] == "1":
                        col += 1
                    out.append(
                        f'<rect x="{cx + start * px}" y="{y + row * px}" '
                        f'width="{(col - start) * px}" height="{px}" fill="{fill}"{extra}/>'
                    )
                else:
                    col += 1
        cx += (5 + gap) * px
    return "\n".join(out), cx


def sprite_pixels(rows, x, y, px, palette, extra=""):
    """rows: list of strings; each char maps to a color in palette ('.' = transparent)."""
    out = []
    for r, line in enumerate(rows):
        c = 0
        while c < len(line):
            ch = line[c]
            if ch == ".":
                c += 1
                continue
            start = c
            while c < len(line) and line[c] == ch:
                c += 1
            out.append(
                f'<rect x="{x + start * px}" y="{y + r * px}" width="{(c - start) * px}" '
                f'height="{px}" fill="{palette[ch]}"{extra}/>'
            )
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Scene: "Midnight Castle" - a dark pixel-art night march. Every character is
# dressed in the colours of a technology and carries its name on a banner.
# ---------------------------------------------------------------------------
import random

W, H = 1200, 480
PX = 4
SP = 5  # pixel size of the characters
GROUND = 440  # y of the marchers' feet
INK = "#07040f"
rnd = random.Random(22)


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>'


def banner(label, cx, bottom, bg, fg, pole_to=None):
    """Flag with the tech name; optional pole running down to y=pole_to."""
    px = 4 if len(label) <= 5 else 3
    w = text_width(label, px) + 4 * px
    h = 7 * px + 4 * px
    x, y = int(cx - w / 2), bottom - h
    out = []
    if pole_to is not None:
        out.append(rect(cx - 2, y - 6, 4, pole_to - y + 6, "#b9a37a"))
    out.append(rect(x - 3, y - 3, w + 6, h + 6, INK))
    out.append(rect(x, y, w, h, bg))
    t, _ = text_pixels(label, x + 2 * px, y + 2 * px, px, fg)
    out.append(t)
    return "".join(out)


# ---- sprites (facing right) -------------------------------------------------
# knight: p=plume k=armour v=visor c=caparison/cloak s=shield h=horse m=mane t=tail e=eye d=hoof
KNIGHT = [
    "..........pp............",
    ".........pkkk...........",
    ".........kkkk...........",
    ".........kvvk...........",
    ".........kkkk......mm...",
    "........cccccc....mhhh..",
    ".......scccccc...mhhhhh.",
    "......ssscccc...mmhhehh.",
    "......ssskkk...mmhhhhhhh",
    "..hhhhssshhhhhhmhhhh..hh",
    ".hhhcccccccccchhhhh.....",
    "thhhcsssssssschhhh......",
    "thhhcccccccccchhh.......",
    "t.hhcccccccccchhh.......",
    "t.hhhhhhhhhhhhhhh.......",
]
KNIGHT_A = ["...hh.hh....hh.hh", "...hh.hh....hh.hh", "..hh...hh..hh...hh", "..dd...dd..dd...dd"]
KNIGHT_B = ["...hh.hh....hh.hh", "....hhhh.....hhhh", "....hh.hh....hh.hh", "....dd.dd....dd.dd"]

# wizard: w=hat f=face e=eye b=beard r=robe l=robe trim o=orb y=staff
WIZARD = [
    "......w.........",
    ".....ww.........",
    ".....www....o...",
    "....wwww...ooo..",
    "...wwwwww...o...",
    "..llllllll..y...",
    "....ffff....y...",
    "....fefe....y...",
    "....bbbb....y...",
    "...rbbbbr...y...",
    "..rrrbbrrrffy...",
    "..rrrrrrrr..y...",
    "..rrlrrrrr..y...",
    "..rrlrrrrr..y...",
    ".rrrlrrrrrr.y...",
    ".rrrlrrrrrr.y...",
]
WIZARD_A = [".rrrlrrrrrr.y", ".llllllllll.y", "..dd....dd..."]
WIZARD_B = [".rrrlrrrrrr.y", ".llllllllll.y", "...dd..dd...."]

# robot: a=antenna g=shell e=eyes d=dark l=chest light
ROBOT = [
    "......l.......",
    "......a.......",
    "...gggggggg...",
    "...gddddddg...",
    "...gdeddedg...",
    "...gddddddg...",
    "...gggggggg...",
    ".....dddd.....",
    ".gggggggggggg.",
    ".ggddgllgddgg.",
    ".gg.gggggg.gg.",
    ".gg.gggggg.gg.",
    ".dd.gggggg.dd.",
]
ROBOT_A = ["....gg..gg....", "....gg..gg....", "...ddd..ddd..."]
ROBOT_B = ["....gg..gg....", "....gg...gg...", "...ddd...ddd.."]

# elephant: b=body E=ear e=eye w=tusk c=blanket d=toes
ELEPHANT = [
    "......bbbbbbbb...bbbb...",
    "...bbbbbbbbbbbbbbbbbbb..",
    "..bbbbccccccbbEEbbbbbbb.",
    ".bbbbbccccccbEEEEbbebbb.",
    ".bbbbbccccccbEEEEbbbbbb.",
    "bbbbbbccccccbEEEEbbbbbbb",
    "b.bbbbccccccbbEEbbbbwbbb",
    "b.bbbbbbbbbbbbbbbb.ww.bb",
    "..bbbbbbbbbbbbbbbb....bb",
    "..bbbbbbbbbbbbbbbb....bb",
]
ELEPHANT_A = ["..bbb.bbb...bbb.bbb...bb", "..bbb.bbb...bbb.bbb..bb.", "..ddd.ddd...ddd.ddd....."]
ELEPHANT_B = ["..bbb.bbb...bbb.bbb...bb", "...bbbbb.....bbbbb...bb.", "...ddddd.....ddddd......"]

# dragon: g=scales b=belly h=horn e=eye w=teeth t=tail c=claw
DRAGON = [
    "....................h.h.....",
    "...................hhhh.....",
    "..................ggggggg...",
    "..................ggeggggg..",
    "t.................gggggggg..",
    "tt...............ggg..www...",
    ".tt.....ggggggggggg.........",
    "..tt..ggggggggggggg.........",
    "...tgggggbbbbbbbggg.........",
    "....ggggbbbbbbbbgg..........",
    ".....ggg.bbbbbb.ggg.........",
    ".....gg..........gg.........",
    ".....cc..........cc.........",
]
WING = [
    "........dd....",
    ".......dddd...",
    "......dddddd..",
    "....dddddddd..",
    "..dddddddddd..",
    "dddddddddddd..",
    "..dd.ddddddd..",
    ".......ddddd..",
]

# ufo: d=dome l=glint p=hull y=lights m=legs
UFO = [
    "......dddd......",
    ".....dlldddd....",
    "....dlddddddd...",
    "..pppppppppppp..",
    "pppyppyppyppyppp",
    "..pppppppppppp..",
    "....mm....mm....",
]


def marcher(i, n, body, legs_a, legs_b, pal, label, bg, fg, pole_col, period=56):
    rows = len(body) + len(legs_a)
    y0 = GROUND - rows * SP
    yl = y0 + len(body) * SP
    cx = pole_col * SP + 2
    return (
        f'<g class="march" style="animation-delay:-{i * period / n:.2f}s"><g class="bob" '
        f'style="animation-delay:-{i * 0.13:.2f}s">'
        + banner(label, cx, y0 - 2, bg, fg, pole_to=y0 + 9 * SP)
        + sprite_pixels(body, 0, y0, SP, pal)
        + f'<g class="fa">{sprite_pixels(legs_a, 0, yl, SP, pal)}</g>'
        + f'<g class="fb">{sprite_pixels(legs_b, 0, yl, SP, pal)}</g>'
        + "</g></g>"
    )


def dragon(y, pal, label, bg, fg, delay, period=30):
    body = sprite_pixels(DRAGON, 0, y, SP, pal)
    up = sprite_pixels(WING, 5 * SP, y - 2 * SP, SP, pal)
    down = sprite_pixels(WING[::-1], 5 * SP, y + 7 * SP, SP, pal)
    fire = "".join(
        rect(27 * SP + k * 10, y + 5 * SP - (k % 2) * 5, 10, 10 + (k % 2) * 5, c)
        for k, c in enumerate(("#fff3a6", "#ffb703", "#fb5607", "#fb5607"))
    )
    return (
        f'<g class="fly" style="animation-duration:{period}s;animation-delay:-{delay}s"><g class="hover">'
        + banner(label, 13 * SP, y - 14, bg, fg)
        + body
        + f'<g class="fa">{up}</g><g class="fb">{down}</g>'
        + f'<g class="fire">{fire}</g>'
        + "</g></g>"
    )


def ufo(y, pal, label, bg, fg, delay, period=30):
    beam = "".join(
        rect(6 * SP - k * 4, y + 7 * SP + k * 8, 4 * SP + k * 8, 8, pal["p"], f' fill-opacity="{0.34 - k * 0.04:.2f}"')
        for k in range(7)
    )
    lights = sprite_pixels(["", "", "", "", "...y..y..y..y..."], 0, y, SP, {"y": "#ffffff"})
    return (
        f'<g class="fly" style="animation-duration:{period}s;animation-delay:-{delay}s"><g class="hover">'
        + f'<g class="beam">{beam}</g>'
        + banner(label, 8 * SP, y - 14, bg, fg)
        + sprite_pixels(UFO, 0, y, SP, pal)
        + f'<g class="fb">{lights}</g>'
        + "</g></g>"
    )


# ---- castle -----------------------------------------------------------------
C_BASE, C_ALT, C_DARK, C_LIP = "#35186a", "#4d2596", "#231047", "#6b3fc4"


def bricks(x, y, w, h):
    out = [rect(x, y, w, h, C_BASE)]
    row = 0
    for by in range(y, y + h, 8):
        off = 8 if row % 2 else 0
        for bx in range(x - off, x + w, 16):
            r = rnd.random()
            if r < 0.5:
                x0, x1 = max(bx, x), min(bx + 14, x + w)
                if x1 > x0:
                    out.append(rect(x0, by, x1 - x0, min(6, y + h - by), C_ALT if r < 0.3 else C_DARK))
        row += 1
    out.append(rect(x + w - 8, y, 8, h, C_DARK, ' fill-opacity=".6"'))  # shaded side
    return "".join(out)


def roof(cx, base_y, half_w, height, col, hi):
    out = []
    n = height // 4
    for i in range(n):
        hw = max(2, round(half_w * (1 - i / n) / 2) * 2)
        y = base_y - (i + 1) * 4
        out.append(rect(cx - hw, y, hw * 2, 4, col))
        out.append(rect(cx - hw, y, max(2, hw // 2), 4, hi))
    out.append(rect(cx - 2, base_y - height - 12, 4, 12, "#b9a37a"))
    out.append(rect(cx + 2, base_y - height - 12, 12, 8, "#e11d48", ' class="flag"'))
    return "".join(out)


def window(x, y, d):
    return (
        rect(x - 2, y - 2, 12, 20, INK)
        + rect(x, y + 4, 8, 12, "#ffd166", f' class="flick" style="animation-delay:-{d}s"')
        + rect(x + 2, y, 4, 4, "#ffd166", f' class="flick" style="animation-delay:-{d}s"')
    )


def tower(x, top, w, base, roof_h, roof_cols, wins=()):
    out = [bricks(x, top, w, base - top)]
    out.append(rect(x - 4, top, w + 8, 8, C_LIP))
    for bx in range(x - 4, x + w + 4, 12):  # battlements
        out.append(rect(bx, top - 6, 8, 6, C_LIP))
    out.append(roof(x + w // 2, top - 4, w // 2 + 6, roof_h, *roof_cols))
    for i, wy in enumerate(wins):
        out.append(window(x + w // 2 - 4, wy, (x + i * 7) % 5))
    return "".join(out)


def castle():
    base = GROUND - 44
    blue, teal = ("#262b78", "#474fc0"), ("#145a50", "#22a08a")
    out = []
    out.append(tower(1068, 150, 56, base, 76, blue, (176, 236)))  # tall back tower
    out.append(tower(872, 222, 44, base, 52, teal, (248,)))
    out.append(bricks(900, 262, 200, base - 262))  # keep
    out.append(rect(896, 262, 208, 8, C_LIP))
    for bx in range(896, 1104, 16):
        out.append(rect(bx, 254, 10, 8, C_LIP))
    out.append(tower(968, 190, 60, base, 64, blue, (216,)))  # central tower
    out.append(tower(828, 300, 48, base, 44, teal, (322,)))  # left gate tower
    out.append(tower(1108, 286, 52, base, 48, teal, (310,)))
    for i, wx in enumerate((916, 944, 1044, 1072)):
        out.append(window(wx, 286, i * 1.3))
    # gate
    gx, gy = 968, base - 76
    out.append(rect(gx - 6, gy + 6, 72, 70, C_DARK))
    out.append(rect(gx, gy + 12, 60, 64, INK))
    out.append(rect(gx + 8, gy + 4, 44, 8, INK))
    out.append(rect(gx + 6, gy + 34, 48, 42, "#ff7b54", ' class="glow" fill-opacity=".55"'))
    out.append(rect(gx + 16, gy + 48, 28, 28, "#ffd166", ' class="glow" fill-opacity=".6"'))
    for k in range(5):  # portcullis bars
        out.append(rect(gx + 6 + k * 12, gy + 12, 3, 30, C_DARK))
    return "".join(out)


def hills():
    out = []
    # far ridge
    x, y = 0, 330
    while x < 860:
        w = rnd.choice([24, 32, 48])
        y = max(292, min(356, y + rnd.choice([-12, -8, -4, 4, 8, 12])))
        out.append(rect(x, y, w, GROUND - y, "#0c1830"))
        x += w
    # near ridge with pines
    x, y = 0, 360
    while x < 840:
        w = rnd.choice([20, 28, 40])
        y = max(336, min(384, y + rnd.choice([-8, -4, 4, 8])))
        out.append(rect(x, y, w, GROUND - y, "#0b2a2c"))
        out.append(rect(x, y, w, 4, "#14524a"))
        if rnd.random() < 0.55:
            tx = x + w // 2
            for k in range(5):
                out.append(rect(tx - 2 - k * 2, y - 24 + k * 4, 4 + k * 4, 4, "#0f3d38" if k % 2 else "#16665a"))
            out.append(rect(tx - 2, y - 4, 4, 4, "#231047"))
        x += w
    return "".join(out)


def road():
    top = GROUND - 44
    out = [rect(0, top, W, 16, "#1a0f3a")]
    for bx in range(0, W, 24):  # low wall
        out.append(rect(bx, top, 20, 6, "#2e1a5e"))
        out.append(rect(bx + 12, top + 8, 20, 6, "#24134b"))
    out.append(rect(0, top + 16, W, H - top - 16, "#0a2f30"))
    y = top + 18
    row = 0
    while y < H:
        hgt = rnd.choice([8, 8, 12])
        x = -rnd.randrange(0, 24)
        while x < W:
            w = rnd.choice([16, 20, 28, 36])
            c = rnd.choices(["#11514b", "#1b7a6c", "#2bb39a", "#63e6c8"], weights=[5, 4, 2, 1])[0]
            out.append(rect(x, y, w - 4, hgt - 3, c))
            x += w
        y += hgt
        row += 1
    out.append(rect(0, GROUND + 2, W, 6, INK, ' fill-opacity=".25"'))
    return "".join(out)


def sky():
    out = [rect(0, 0, W, H, "url(#sky)")]
    for _ in range(46):  # crimson nebula blocks
        cx, cy = rnd.choice([(260, 150), (640, 210), (980, 70), (90, 60)])
        x = int(rnd.gauss(cx, 110) // 16 * 16)
        y = int(rnd.gauss(cy, 46) // 16 * 16)
        out.append(rect(x, y, 32, 16, "#7a1238", f' fill-opacity="{rnd.uniform(0.10, 0.26):.2f}"'))
    stars = []
    for _ in range(120):
        x, y = rnd.randrange(0, W, 4), rnd.randrange(0, 330, 4)
        s = rnd.choice([2, 2, 3, 4])
        c = rnd.choice(["#ffffff", "#ffffff", "#c4b5fd", "#99f6e4", "#fda4af"])
        stars.append(rect(x, y, s, s, c, f' style="animation-delay:-{rnd.uniform(0, 3):.2f}s"'))
    out.append('<g class="stars">' + "".join(stars) + "</g>")
    return "".join(out)


def build_hero():
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'shape-rendering="crispEdges" role="img" '
        f'aria-label="Hello there - Ido Yahav, full-stack developer. A night march of pixel knights, '
        f'dragons and other characters, each dressed as a technology.">'
    ]
    p.append(
        """<style>
@keyframes tw { 0%,100% { opacity:.25 } 50% { opacity:1 } }
@keyframes blink { 0%,49% { opacity:1 } 50%,100% { opacity:0 } }
@keyframes bob { 0%,49% { transform:translateY(0) } 50%,100% { transform:translateY(-4px) } }
@keyframes march { from { transform:translateX(-280px) } to { transform:translateX(1260px) } }
@keyframes fly { from { transform:translateX(-260px) } to { transform:translateX(1280px) } }
@keyframes hover { 0%,100% { transform:translateY(0) } 50% { transform:translateY(-12px) } }
@keyframes drift { 0%,100% { transform:translate(0,0) } 50% { transform:translate(120px,-8px) } }
@keyframes flick { 0%,100% { opacity:1 } 45% { opacity:.55 } 50% { opacity:.9 } 70% { opacity:.4 } }
@keyframes glow { 0%,100% { opacity:.6 } 50% { opacity:1 } }
@keyframes fire { 0%,70% { opacity:0 } 72%,96% { opacity:1 } 100% { opacity:0 } }
.stars rect { animation: tw 3s ease-in-out infinite }
.march { animation: march 56s linear infinite }
.bob { animation: bob .5s steps(1) infinite }
.fa { animation: blink .5s steps(1) infinite }
.fb { animation: blink .5s steps(1) infinite; animation-delay:-.25s }
.fly { animation: fly 30s linear infinite }
.hover { animation: hover 2.4s ease-in-out infinite }
.drift { animation: drift 14s ease-in-out infinite }
.flick { animation: flick 2.6s steps(4) infinite }
.glow { animation: glow 2.2s ease-in-out infinite }
.fire { animation: fire 5s steps(1) infinite }
.beam { animation: glow 1.4s ease-in-out infinite }
.flag { animation: blink 1.2s steps(1) infinite }
.cur { animation: blink 1s steps(1) infinite }
</style>"""
    )
    p.append(
        f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#05030f"/><stop offset=".45" stop-color="#150a2e"/>'
        f'<stop offset=".8" stop-color="#2a0c3a"/><stop offset="1" stop-color="#1a0b33"/></linearGradient>'
        f'<linearGradient id="title" gradientUnits="userSpaceOnUse" x1="250" y1="0" x2="900" y2="0">'
        f'<stop offset="0" stop-color="#5eead4"/><stop offset=".5" stop-color="#c4b5fd"/>'
        f'<stop offset="1" stop-color="#f472b6"/></linearGradient></defs>'
    )
    p.append(sky())

    # ---- title ---------------------------------------------------------------
    title = "HELLO THERE"
    tw_ = text_width(title, 10)
    tx = (W - tw_) // 2 - 20
    for dx, dy in ((-4, 0), (4, 0), (0, -4), (0, 4), (6, 6)):
        t, _ = text_pixels(title, tx + dx, 20 + dy, 10, INK)
        p.append(t)
    t, _ = text_pixels(title, tx, 20, 10, "url(#title)")
    p.append(t)
    p.append(rect(tx + tw_ + 16, 20, 36, 70, "#5eead4", ' class="cur"'))
    sub = "IDO YAHAV . FULL-STACK DEVELOPER"
    sw = text_width(sub, 4)
    t, _ = text_pixels(sub, (W - sw) // 2 + 3, 107, 4, INK)
    p.append(t)
    t, _ = text_pixels(sub, (W - sw) // 2, 104, 4, "#e9d5ff")
    p.append(t)

    # ---- world ---------------------------------------------------------------
    p.append(hills())
    p.append(castle())
    p.append(road())

    # ---- sky creatures ---------------------------------------------------------
    node = {"g": "#5fa04e", "b": "#c5e8b7", "h": "#f1f5f9", "e": INK, "w": "#ffffff", "t": "#3c873a",
            "c": "#f1f5f9", "d": "#a7e08f"}
    redis = {"g": "#dc382d", "b": "#ffc9c4", "h": "#f1f5f9", "e": INK, "w": "#ffffff", "t": "#a41e11",
             "c": "#f1f5f9", "d": "#ff8a7a"}
    p.append(dragon(206, node, "NODE", "#3c873a", "#ffffff", 4))
    p.append(dragon(206, redis, "REDIS", "#a41e11", "#ffffff", 14))
    p.append(
        ufo(224, {"d": "#fbcfe8", "l": "#ffffff", "p": "#e535ab", "y": "#3b0a2a", "m": "#8a1f68"},
            "GRAPHQL", "#e535ab", "#ffffff", 24)
    )

    # ---- the march -------------------------------------------------------------
    def knight_pal(main, shield, horse, mane):
        return {"p": shield, "k": "#cbd5e1", "v": INK, "c": main, "s": shield, "h": horse, "m": mane,
                "t": mane, "e": INK, "d": INK}

    wizard = {"w": "#0e7490", "l": "#61dafb", "f": "#f2c9a0", "e": INK, "b": "#f1f5f9", "r": "#155e75",
              "o": "#61dafb", "y": "#b9a37a", "d": INK}
    robot = {"a": "#a1a1aa", "l": "#a3e635", "g": "#e4e4e7", "d": "#27272a", "e": "#a3e635"}
    eleph = {"b": "#4f86b8", "E": "#336791", "e": INK, "w": "#ffffff", "c": "#f1f5f9", "d": "#1f3f5c"}
    troop = [
        (KNIGHT, KNIGHT_A, KNIGHT_B, knight_pal("#3178c6", "#ffffff", "#e2e8f0", "#94a3b8"), "TS", "#3178c6", "#ffffff", 9),
        (WIZARD, WIZARD_A, WIZARD_B, wizard, "REACT", "#20232a", "#61dafb", 5),
        (KNIGHT, KNIGHT_A, KNIGHT_B, knight_pal("#f7df1e", "#323330", "#a16207", "#422006"), "JS", "#f7df1e", "#1a1a1a", 9),
        (ELEPHANT, ELEPHANT_A, ELEPHANT_B, eleph, "POSTGRES", "#336791", "#ffffff", 8),
        (KNIGHT, KNIGHT_A, KNIGHT_B, knight_pal("#3776ab", "#ffd43b", "#9ca3af", "#4b5563"), "PY", "#3776ab", "#ffd43b", 9),
        (ROBOT, ROBOT_A, ROBOT_B, robot, "EXPRESS", "#e4e4e7", "#18181b", 6),
        (KNIGHT, KNIGHT_A, KNIGHT_B, knight_pal("#5c6bc0", "#a8b9cc", "#7c7ca3", "#2e2e4d"), "C", "#283593", "#ffffff", 9),
    ]
    for i, (body, la, lb, pal, label, bg, fg, pole) in enumerate(troop):
        p.append(marcher(i, len(troop), body, la, lb, pal, label, bg, fg, pole))

    p.append(rect(3, 3, W - 6, H - 6, "none", ' stroke="#4d2596" stroke-width="6"'))
    p.append("</svg>")
    return "\n".join(p)


if __name__ == "__main__":
    out = ROOT / "assets"
    out.mkdir(exist_ok=True)
    (out / "hero.svg").write_text(build_hero(), encoding="utf-8")
    print("wrote", out / "hero.svg")
