#!/usr/bin/env python3
"""
Generates the animated pixel-art SVGs used in the profile README:
  assets/hero.svg         - arcade "level" banner with an original sprite
  assets/player-card.svg  - the stats card ("PLAYER CARD")

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
# Palette (arcade neon)
# ---------------------------------------------------------------------------
BG = "#0a0a14"
GRID = "#12122a"
PURPLE = "#a855f7"
PURPLE_DK = "#6d28d9"
CYAN = "#22d3ee"
PINK = "#f472b6"
YELLOW = "#fde047"
GREEN = "#4ade80"
WHITE = "#f1f5f9"
GRAY = "#64748b"
LIGHT = "#cbd5e1"

# ---------------------------------------------------------------------------
# The sprite: "BYTE" - an original pixel creature. One wide visor eye, an antenna
# with a blinking tip, a dome body and a three-pixel thruster tail.
# Legend: b=body p=body shade v=visor w=visor glint a=antenna t=thruster
# ---------------------------------------------------------------------------
BYTE = [
    "......a......",
    "......a......",
    ".....bbb.....",
    "...bbbbbbb...",
    "..bbbbbbbbb..",
    ".bbvvvvvvvbb.",
    ".bbvwvvvvvbb.",
    ".bbvvvvvvvbb.",
    ".bbbbbbbbbbb.",
    ".bbbbbbbbbbb.",
    "..pbbbbbbbp..",
    "...pp.p.pp...",
    "....t.t.t....",
]
BYTE_PAL = {"b": PURPLE, "p": PURPLE_DK, "v": CYAN, "w": WHITE, "a": PURPLE_DK, "t": PINK}

# Collectibles: small 7x7 pixel icons the sprite "picks up"
ICON_CODE = [  # </>
    ".......",
    ".1...1.",
    "1.....1",
    "1..2..1",
    "1.....1",
    ".1...1.",
    ".......",
]
ICON_DB = [  # database cylinder
    ".11111.",
    "1.....1",
    ".11111.",
    "1.....1",
    ".11111.",
    "1.....1",
    ".11111.",
]
ICON_CLOUD = [
    ".......",
    "...11..",
    "..1..1.",
    ".1....1",
    "1......",
    "1111111",
    ".......",
]
ICON_MOBILE = [
    ".11111.",
    ".1...1.",
    ".1...1.",
    ".1...1.",
    ".1...1.",
    ".11.11.",
    ".11111.",
]
ICON_BOLT = [
    "...11..",
    "..11...",
    ".11....",
    "1111111",
    "....11.",
    "...11..",
    "..11...",
]


def build_hero():
    W, H = 1200, 420
    px = 4
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'shape-rendering="crispEdges" role="img" aria-label="Ido Yahav - full-stack developer">'
    )

    # ---- styles / animations -------------------------------------------------
    parts.append(
        """<style>
@keyframes blink { 0%,49% { opacity:1 } 50%,100% { opacity:0 } }
@keyframes tip { 0%,100% { fill:#f472b6 } 50% { fill:#fde047 } }
@keyframes float { 0%,100% { transform:translateY(0) } 50% { transform:translateY(-10px) } }
@keyframes thrust { 0%,100% { opacity:1 } 50% { opacity:.25 } }
@keyframes visor { 0%,40% { transform:translateX(0) } 50%,90% { transform:translateX(12px) } 100% { transform:translateX(0) } }
@keyframes walk { 0% { transform:translateX(0) } 100% { transform:translateX(980px) } }
@keyframes scroll { 0% { transform:translateX(0) } 100% { transform:translateX(-64px) } }
@keyframes twinkle { 0%,100% { opacity:.2 } 50% { opacity:1 } }
@keyframes glow { 0%,100% { opacity:.55 } 50% { opacity:1 } }
@keyframes shine { 0% { transform:translateX(-200px) } 100% { transform:translateX(1400px) } }
.blink { animation: blink 1s steps(1) infinite }
.tip { animation: tip .6s steps(1) infinite }
.byte { animation: walk 12s linear infinite }
.bob { animation: float 1.6s ease-in-out infinite }
.thr { animation: thrust .3s steps(1) infinite }
.vis { animation: visor 3s steps(1) infinite }
.stars rect { animation: twinkle 2.4s ease-in-out infinite }
.glow { animation: glow 2s ease-in-out infinite }
.shine { animation: shine 9s linear infinite }
</style>"""
    )
    # pickups: each vanishes when the sprite reaches it, +100 pops, respawn at loop end
    pickup_x = [180, 340, 500, 660, 820]
    for i, x in enumerate(pickup_x):
        # sprite starts at x=60; reaches pickup when translateX ~= x-60 -> t = (x-60)/980*12s
        t = (x - 60) / 980 * 12
        p = t / 12 * 100
        parts.append(
            f"<style>@keyframes pk{i} {{ 0%,{p:.1f}% {{ opacity:1 }} {p+0.1:.1f}%,100% {{ opacity:0 }} }}"
            f"@keyframes pop{i} {{ 0%,{p:.1f}% {{ opacity:0; transform:translateY(0) }} {p+0.1:.1f}% {{ opacity:1; transform:translateY(0) }} "
            f"{min(p+8,100):.1f}%,100% {{ opacity:0; transform:translateY(-28px) }} }}"
            f".pk{i} {{ animation: pk{i} 12s steps(1) infinite }} .pop{i} {{ animation: pop{i} 12s linear infinite }}</style>"
        )

    # ---- background -----------------------------------------------------------
    parts.append(
        f'<defs><pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse">'
        f'<rect width="20" height="20" fill="{BG}"/><rect width="1" height="20" fill="{GRID}"/>'
        f'<rect width="20" height="1" fill="{GRID}"/></pattern>'
        f'<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">'
        f'<rect width="4" height="2" fill="#000" fill-opacity="0.18"/></pattern>'
        f'<linearGradient id="title" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/>'
        f'<stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>'
        f'<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="tclip"><rect x="0" y="0" width="{W}" height="{H}"/></clipPath></defs>'
    )
    parts.append(f'<rect width="{W}" height="{H}" fill="url(#g)"/>')

    # stars
    stars = []
    import random

    rnd = random.Random(7)
    for _ in range(60):
        sx, sy = rnd.randrange(0, W, 4), rnd.randrange(0, 250, 4)
        d = rnd.uniform(0, 2.4)
        c = rnd.choice([WHITE, CYAN, PURPLE, PINK])
        stars.append(f'<rect x="{sx}" y="{sy}" width="3" height="3" fill="{c}" style="animation-delay:-{d:.2f}s"/>')
    parts.append('<g class="stars">' + "".join(stars) + "</g>")

    # ---- HUD ------------------------------------------------------------------
    parts.append(f'<rect x="0" y="0" width="{W}" height="44" fill="#05050c"/>')
    parts.append(f'<rect x="0" y="44" width="{W}" height="3" fill="{PURPLE_DK}"/>')
    t, _ = text_pixels("1UP", 28, 14, 3, PINK)
    parts.append(t)
    t, _ = text_pixels("IDO YAHAV", 110, 14, 3, WHITE)
    parts.append(t)
    t, _ = text_pixels("LIVES", 520, 14, 3, LIGHT)
    parts.append(t)
    for i in range(3):
        t, _ = text_pixels("♥", 640 + i * 24, 14, 3, PINK)
        parts.append(t)
    t, _ = text_pixels("LEVEL 22", 780, 14, 3, LIGHT)
    parts.append(t)
    t, _ = text_pixels("SCORE", 960, 14, 3, LIGHT)
    parts.append(t)
    # score counter: five values shown in turn
    for i in range(6):
        val = f"{i*100:05d}"
        start = 0 if i == 0 else (pickup_x[i - 1] - 60) / 980 * 100
        end = 100 if i == 5 else (pickup_x[i] - 60) / 980 * 100
        parts.append(
            f"<style>@keyframes sc{i} {{ 0%,{start:.1f}% {{ opacity:{1 if i==0 else 0} }} "
            f"{start+0.1 if i else 0:.1f}%,{end:.1f}% {{ opacity:1 }} {end+0.1:.1f}%,100% {{ opacity:{0} }} }}"
            f".sc{i} {{ animation: sc{i} 12s steps(1) infinite }}</style>"
        )
        t, _ = text_pixels(val, 1070, 14, 3, YELLOW)
        parts.append(f'<g class="sc{i}">{t}</g>')

    # ---- title ----------------------------------------------------------------
    title = "IDO YAHAV"
    tw = text_width(title, 10)
    tx = (W - tw) // 2
    # glow layer (offset copies, low opacity)
    for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3)):
        t, _ = text_pixels(title, tx + dx, 78 + dy, 10, PURPLE, extra=' fill-opacity="0.22"')
        parts.append(f'<g class="glow">{t}</g>')
    t, _ = text_pixels(title, tx, 78, 10, "url(#title)")
    parts.append(t)
    # moving shine across the title
    parts.append(
        f'<g clip-path="url(#tclip)"><rect class="shine" x="0" y="70" width="160" height="90" fill="url(#sh)"/></g>'
    )

    sub = "FULL-STACK DEVELOPER"
    sw = text_width(sub, 4)
    t, _ = text_pixels(sub, (W - sw) // 2, 168, 4, LIGHT)
    parts.append(t)
    tags = "REACT NATIVE . NODE.JS . TYPESCRIPT . POSTGRES"
    tgw = text_width(tags, 3)
    t, _ = text_pixels(tags, (W - tgw) // 2, 206, 3, CYAN)
    parts.append(t)

    ps = "PRESS ★ TO START"
    pw = text_width(ps, 3)
    t, _ = text_pixels(ps, (W - pw) // 2, 246, 3, YELLOW)
    parts.append(f'<g class="blink">{t}</g>')

    # ---- level floor ----------------------------------------------------------
    floor_y = 372
    parts.append(f'<rect x="0" y="{floor_y}" width="{W}" height="{H - floor_y}" fill="#05050c"/>')
    # scrolling brick pattern
    bricks = []
    for bx in range(-64, W + 64, 32):
        bricks.append(f'<rect x="{bx}" y="{floor_y}" width="28" height="12" fill="{PURPLE_DK}"/>')
        bricks.append(f'<rect x="{bx+16}" y="{floor_y+16}" width="28" height="12" fill="#3b1d7a"/>')
    parts.append(
        f'<g clip-path="url(#tclip)"><g style="animation:scroll 1.2s linear infinite">{"".join(bricks)}</g></g>'
    )
    parts.append(f'<rect x="0" y="{floor_y}" width="{W}" height="2" fill="{PINK}"/>')

    # ---- pickups --------------------------------------------------------------
    icons = [ICON_CODE, ICON_DB, ICON_CLOUD, ICON_MOBILE, ICON_BOLT]
    icon_cols = [CYAN, GREEN, LIGHT, PINK, YELLOW]
    for i, (x, ic, col) in enumerate(zip(pickup_x, icons, icon_cols)):
        y = floor_y - 50
        pal = {"1": col, "2": WHITE}
        s = sprite_pixels(ic, x - 14, y - 14, 4, pal)
        parts.append(f'<g class="pk{i} bob" style="animation-delay:0s,-{i*0.3:.1f}s">{s}</g>')
        t, _ = text_pixels("+100", x - 24, y - 40, 3, YELLOW)
        parts.append(f'<g class="pop{i}">{t}</g>')

    # ---- BYTE the sprite -------------------------------------------------------
    sx, sy = 60, floor_y - 64
    body = sprite_pixels([r.replace("v", ".").replace("w", ".").replace("t", ".") for r in BYTE], 0, 0, px, BYTE_PAL)
    visor = sprite_pixels(
        [r.replace("b", ".").replace("p", ".").replace("a", ".").replace("t", ".") for r in BYTE], 0, 0, px, BYTE_PAL
    )
    thr = sprite_pixels(
        [r.replace("b", ".").replace("p", ".").replace("a", ".").replace("v", ".").replace("w", ".") for r in BYTE],
        0, 0, px, BYTE_PAL,
    )
    parts.append(
        f'<g class="byte"><g transform="translate({sx},{sy})"><g class="bob">'
        f'{body}'
        f'<rect class="tip" x="{6*px}" y="0" width="{px}" height="{px}" fill="{PINK}"/>'
        f'<g class="vis">{visor}</g>'
        f'<g class="thr">{thr}</g>'
        f"</g></g></g>"
    )

    # ---- overlays --------------------------------------------------------------
    parts.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="{PURPLE_DK}" stroke-width="6"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def build_card():
    W, H = 1200, 340
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'shape-rendering="crispEdges" role="img" aria-label="Player card">'
    ]
    parts.append(
        """<style>
@keyframes blink { 0%,49% { opacity:1 } 50%,100% { opacity:0 } }
@keyframes bar { 0% { width:0 } 100% { width:var(--w) } }
@keyframes type { 0% { opacity:0 } 100% { opacity:1 } }
.blink { animation: blink 1s steps(1) infinite }
.bar { animation: bar 1.6s steps(12) forwards }
.row { opacity:0; animation: type .01s steps(1) forwards }
</style>"""
    )
    parts.append(
        f'<defs><pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">'
        f'<rect width="4" height="2" fill="#000" fill-opacity="0.18"/></pattern></defs>'
    )
    parts.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    parts.append(f'<rect x="4" y="4" width="{W-8}" height="{H-8}" fill="none" stroke="{PURPLE_DK}" stroke-width="6"/>')
    # header bar
    parts.append(f'<rect x="10" y="10" width="{W-20}" height="34" fill="#16123a"/>')
    t, _ = text_pixels("PLAYER CARD", 30, 18, 3, PINK)
    parts.append(t)
    t, _ = text_pixels("STATUS: ONLINE", 930, 18, 3, GREEN)
    parts.append(t)
    parts.append(f'<rect class="blink" x="1150" y="20" width="12" height="12" fill="{GREEN}"/>')

    rows = [
        ("NAME", "IDO YAHAV", WHITE),
        ("CLASS", "FULL-STACK DEVELOPER", WHITE),
        ("MAIN WEAPON", "TYPESCRIPT", CYAN),
        ("STACK", "REACT NATIVE . NODE . EXPRESS . PRISMA . POSTGRES", CYAN),
        ("SIDE QUESTS", "PYTHON . C . SECURITY RESEARCH . DEEP LEARNING", LIGHT),
        ("BASE", "ISRAEL", LIGHT),
        ("MOTTO", "BUILD . BREAK . LEARN . SHIP", PINK),
    ]
    y = 68
    for i, (k, v, c) in enumerate(rows):
        t, _ = text_pixels(k, 36, y, 3, PURPLE)
        parts.append(f'<g class="row" style="animation-delay:{i*0.25:.2f}s">{t}</g>')
        t, _ = text_pixels(v, 300, y, 3, c)
        parts.append(f'<g class="row" style="animation-delay:{i*0.25+0.1:.2f}s">{t}</g>')
        y += 30

    # skill bars
    skills = [("FRONTEND", 92, CYAN), ("BACKEND", 88, PURPLE), ("MOBILE", 85, PINK), ("DEVOPS", 60, YELLOW)]
    bx, by = 36, y + 8
    for i, (name, pct, col) in enumerate(skills):
        t, _ = text_pixels(name, bx, by, 3, LIGHT)
        parts.append(t)
        w = int(pct * 2.2)
        parts.append(f'<rect x="{bx+160}" y="{by}" width="220" height="20" fill="#16123a"/>')
        parts.append(
            f'<rect class="bar" x="{bx+160}" y="{by}" height="20" width="0" fill="{col}" '
            f'style="--w:{w}px; animation-delay:{1.8+i*0.2:.1f}s"/>'
        )
        t, _ = text_pixels(f"{pct}", bx + 400, by, 3, col)
        parts.append(t)
        # two columns
        if i == 1:
            bx, by = 640, y + 8
        else:
            by += 30

    # prompt line
    t, cx = text_pixels("> _", 36, H - 34, 3, GREEN)
    parts.append(t)
    parts.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    out = ROOT / "assets"
    out.mkdir(exist_ok=True)
    (out / "hero.svg").write_text(build_hero(), encoding="utf-8")
    (out / "player-card.svg").write_text(build_card(), encoding="utf-8")
    print("wrote", out / "hero.svg", out / "player-card.svg")
