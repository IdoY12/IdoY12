#!/usr/bin/env python3
"""
Generates the animated fantasy banner used in the profile README:
  assets/hero.svg  - a dreamlike "other world" landscape: rainbow light rays,
                     floating islands with waterfalls, a crystal spire, glowing
                     flora and a "Hello there" greeting.

Everything is self-contained: no external fonts or images (GitHub strips them
from SVGs), and all motion is plain CSS keyframes / SMIL, which GitHub renders
inside <img> tags.

Run: python3 scripts/make-hero.py
"""
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H = 1200, 420
RAINBOW = ["#ff6b6b", "#ffa94d", "#ffe066", "#8ce99a", "#66d9e8", "#748ffc", "#b197fc", "#f783ac"]
rnd = random.Random(11)


def rays(cx, cy):
    """Rainbow light wedges fanning out of the sky crystal, slowly rotating."""
    out = [f'<g transform="translate({cx},{cy})"><g class="pulse"><g>']
    out.append(
        '<animateTransform attributeName="transform" type="rotate" from="0" to="360" '
        'dur="240s" repeatCount="indefinite"/>'
    )
    n = 32
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = 2 * math.pi * (i + 0.62) / n
        r = 1400
        pts = f"0,0 {r*math.cos(a0):.0f},{r*math.sin(a0):.0f} {r*math.cos(a1):.0f},{r*math.sin(a1):.0f}"
        out.append(f'<polygon points="{pts}" fill="{RAINBOW[i % len(RAINBOW)]}" fill-opacity=".30"/>')
    out.append("</g></g></g>")
    return "".join(out)


def stars():
    out = ['<g class="stars">']
    for _ in range(70):
        x, y = rnd.uniform(0, W), rnd.uniform(0, 210)
        r = rnd.choice([0.9, 1.2, 1.6, 2.1])
        out.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" '
            f'style="animation-delay:-{rnd.uniform(0, 4):.2f}s"/>'
        )
    out.append("</g>")
    return "".join(out)


def rainbow_arc(cx, cy, r0):
    out = ['<g fill="none" stroke-width="7" opacity=".55" filter="url(#soft)">']
    for i, c in enumerate(RAINBOW[:7]):
        r = r0 - i * 7
        out.append(f'<path d="M{cx - r},{cy} A{r},{r} 0 0 1 {cx + r},{cy}" stroke="{c}"/>')
    out.append("</g>")
    return "".join(out)


def island(x, y, w, falls, cls):
    """Floating island: mossy top, violet rock underside, waterfalls to the ground."""
    h = w * 0.42
    out = [f'<g class="{cls}">']
    for fx, fw in falls:  # waterfalls (drawn first so the rim overlaps them)
        top = y + 4
        out.append(f'<rect x="{x + fx}" y="{top}" width="{fw}" height="{H - top}" fill="url(#fall)"/>')
        for k in range(3):
            lx = x + fx + fw * (k + 0.5) / 3
            out.append(
                f'<line class="flow" x1="{lx:.0f}" y1="{top}" x2="{lx:.0f}" y2="{H}" stroke="#fff" '
                f'stroke-opacity=".8" stroke-width="2" stroke-dasharray="14 22" '
                f'style="animation-delay:-{k * 0.4:.1f}s"/>'
            )
    out.append(
        f'<path d="M{x},{y} C{x + w * .1},{y + h * .7} {x + w * .32},{y + h} {x + w * .45},{y + h * 1.05} '
        f'C{x + w * .62},{y + h * .95} {x + w * .9},{y + h * .5} {x + w},{y} Z" fill="url(#rock)"/>'
    )
    out.append(f'<ellipse cx="{x + w / 2}" cy="{y}" rx="{w / 2}" ry="{w * .075}" fill="url(#moss)"/>')
    out.append(
        f'<ellipse cx="{x + w / 2}" cy="{y - w * .02}" rx="{w * .4}" ry="{w * .04}" fill="#f4ff9a" fill-opacity=".45"/>'
    )
    return out


def spire(x, y):
    """Crystal spire with a halo ring, glowing tip and a beam of light."""
    return (
        f'<rect x="{x - 5}" y="0" width="10" height="{y - 118}" fill="url(#beam)" class="pulse"/>'
        f'<polygon points="{x - 15},{y} {x},{y - 120} {x + 15},{y}" fill="url(#crystal)"/>'
        f'<polygon points="{x},{y - 120} {x + 15},{y} {x + 3},{y}" fill="#fff" fill-opacity=".35"/>'
        f'<polygon points="{x - 30},{y} {x - 22},{y - 44} {x - 13},{y}" fill="url(#crystal)" opacity=".85"/>'
        f'<polygon points="{x + 12},{y} {x + 23},{y - 34} {x + 31},{y}" fill="url(#crystal)" opacity=".85"/>'
        f'<ellipse cx="{x}" cy="{y - 70}" rx="34" ry="8" fill="none" stroke="#ffe066" stroke-width="4" '
        f'class="pulse" filter="url(#soft)"/>'
        f'<circle cx="{x}" cy="{y - 122}" r="20" fill="url(#glow)" class="pulse"/>'
        f'<circle cx="{x}" cy="{y - 122}" r="4.5" fill="#fff"/>'
    )


def castle(x, y):
    """Faint castle in the clouds."""
    p = [f'<g fill="#fff" opacity=".7" filter="url(#soft)">']
    for dx, w, h in ((0, 16, 34), (20, 22, 52), (46, 14, 40), (64, 20, 28), (-20, 16, 22)):
        p.append(f'<rect x="{x + dx}" y="{y - h}" width="{w}" height="{h}"/>')
        p.append(f'<polygon points="{x + dx - 2},{y - h} {x + dx + w / 2},{y - h - 22} {x + dx + w + 2},{y - h}"/>')
    p.append(f'<ellipse cx="{x + 32}" cy="{y + 2}" rx="80" ry="10"/>')
    p.append("</g>")
    return "".join(p)


def tendril(x, y, s, flip=False):
    """Curling alien leaf, swaying."""
    sx = -s if flip else s
    return (
        f'<g transform="translate({x},{y}) scale({sx},{s})"><g class="sway">'
        '<path d="M0,0 C10,-70 -30,-120 20,-180 C48,-212 92,-196 84,-164 C78,-146 56,-150 60,-166 '
        'C40,-150 22,-112 30,-60 C34,-34 22,-12 14,0 Z" fill="url(#leaf)" stroke="#1f6b3a" stroke-width="2"/>'
        '<path d="M6,-4 C16,-70 -14,-118 28,-172" fill="none" stroke="#eaffb0" stroke-opacity=".7" stroke-width="2"/>'
        "</g></g>"
    )


def bulb(x, y, s):
    """Purple pod flower with glowing seeds."""
    dots = "".join(
        f'<circle cx="{dx}" cy="{dy}" r="4" fill="#ffe066" class="tw" style="animation-delay:-{i * .5:.1f}s"/>'
        for i, (dx, dy) in enumerate(((-14, -30), (0, -40), (14, -30), (-8, -16), (8, -16)))
    )
    return (
        f'<g transform="translate({x},{y}) scale({s})">'
        '<path d="M0,0 C-44,-10 -40,-58 0,-88 C40,-58 44,-10 0,0 Z" fill="url(#pod)" stroke="#4a1d7a" stroke-width="2"/>'
        '<path d="M0,-88 C-6,-104 6,-112 14,-120" fill="none" stroke="#4a1d7a" stroke-width="3"/>'
        f"{dots}</g>"
    )


def jelly(x, y, s, d):
    """Floating luminous seed (drifts up and down)."""
    lines = "".join(
        f'<path d="M{dx},0 q{4 if i % 2 else -4},14 0,{26 + (i % 3) * 6}" fill="none" stroke="#e5b8ff" '
        f'stroke-opacity=".8" stroke-width="1.5"/>'
        for i, dx in enumerate((-12, -6, 0, 6, 12))
    )
    return (
        f'<g transform="translate({x},{y}) scale({s})"><g class="drift" style="animation-delay:-{d}s">'
        '<circle r="26" cy="-6" fill="url(#glowp)"/>'
        '<path d="M-18,0 C-18,-24 18,-24 18,0 Z" fill="#d6a4ff" fill-opacity=".9"/>'
        f"{lines}</g></g>"
    )


def build_hero():
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="Hello there - I\'m Ido Yahav, full-stack developer">'
    ]
    p.append(
        """<style>
@keyframes tw { 0%,100% { opacity:.25 } 50% { opacity:1 } }
@keyframes pulse { 0%,100% { opacity:.7 } 50% { opacity:1 } }
@keyframes bobA { 0%,100% { transform:translateY(0) } 50% { transform:translateY(-8px) } }
@keyframes bobB { 0%,100% { transform:translateY(-6px) } 50% { transform:translateY(4px) } }
@keyframes drift { 0%,100% { transform:translate(0,0) } 50% { transform:translate(10px,-22px) } }
@keyframes flow { to { stroke-dashoffset:-36 } }
@keyframes sway { 0%,100% { transform:rotate(-2.5deg) } 50% { transform:rotate(3deg) } }
@keyframes fly { 0% { transform:translate(0,0); opacity:0 } 15%,80% { opacity:1 } 100% { transform:translate(40px,-120px); opacity:0 } }
@keyframes cloud { from { transform:translateX(-260px) } to { transform:translateX(1460px) } }
.stars circle, .tw { animation: tw 3.2s ease-in-out infinite }
.pulse { animation: pulse 4s ease-in-out infinite }
.ia { animation: bobA 7s ease-in-out infinite }
.ib { animation: bobB 9s ease-in-out infinite }
.drift { animation: drift 8s ease-in-out infinite }
.flow { animation: flow 1.1s linear infinite }
.sway { animation: sway 6s ease-in-out infinite; transform-box: fill-box; transform-origin: 50% 100% }
.fly { animation: fly 9s linear infinite }
.cloud { animation: cloud 90s linear infinite }
.t { font-family: Georgia, 'Times New Roman', serif; text-anchor: middle; paint-order: stroke; stroke-linejoin: round }
</style>"""
    )
    p.append(
        """<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#1a1160"/><stop offset=".38" stop-color="#5a2ea6"/>
<stop offset=".66" stop-color="#d45c9c"/><stop offset=".84" stop-color="#ffb37a"/><stop offset="1" stop-color="#ffe9b0"/>
</linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#fff"/><stop offset=".35" stop-color="#fff7c2" stop-opacity=".85"/><stop offset="1" stop-color="#fff7c2" stop-opacity="0"/></radialGradient>
<radialGradient id="glowp"><stop offset="0" stop-color="#e9c6ff" stop-opacity=".9"/><stop offset="1" stop-color="#b56cff" stop-opacity="0"/></radialGradient>
<radialGradient id="veil"><stop offset="0" stop-color="#140a3c" stop-opacity=".55"/><stop offset="1" stop-color="#140a3c" stop-opacity="0"/></radialGradient>
<linearGradient id="far" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f1fbff"/><stop offset="1" stop-color="#b9e4dc"/></linearGradient>
<linearGradient id="mid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a8ecc0"/><stop offset="1" stop-color="#59c08a"/></linearGradient>
<linearGradient id="near" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9ee5a"/><stop offset="1" stop-color="#2f9a4a"/></linearGradient>
<linearGradient id="moss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6f76a"/><stop offset="1" stop-color="#5fb83c"/></linearGradient>
<linearGradient id="rock" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a3fb0"/><stop offset="1" stop-color="#27124f"/></linearGradient>
<linearGradient id="fall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".6" stop-color="#cfefff" stop-opacity=".7"/><stop offset="1" stop-color="#cfefff" stop-opacity=".15"/></linearGradient>
<linearGradient id="crystal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9be7ff"/><stop offset=".5" stop-color="#3b6ef0"/><stop offset="1" stop-color="#7a3df0"/></linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bff6ff" stop-opacity="0"/><stop offset="1" stop-color="#bff6ff" stop-opacity=".8"/></linearGradient>
<linearGradient id="leaf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d8f56a"/><stop offset="1" stop-color="#2f9e44"/></linearGradient>
<linearGradient id="pod" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e599f7"/><stop offset="1" stop-color="#7b2cbf"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff3a6"/><stop offset="1" stop-color="#f5b942"/></linearGradient>
<linearGradient id="title" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#ffe9f7"/></linearGradient>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="1.6"/></filter>
<filter id="haze" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
<clipPath id="frame"><rect width="1200" height="420" rx="18"/></clipPath>
</defs>"""
    )
    p.append('<g clip-path="url(#frame)">')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    p.append(stars())
    p.append(rays(600, 62))

    # sky crystal (the light source)
    p.append('<circle cx="600" cy="62" r="120" fill="url(#glow)" class="pulse"/>')
    p.append('<polygon points="600,40 618,62 600,84 582,62" fill="url(#gold)" stroke="#fff" stroke-width="2"/>')

    # drifting clouds
    for i, (y, s, d) in enumerate(((70, 1.0, 0), (128, 0.7, 40), (36, 0.55, 70))):
        p.append(
            f'<g class="cloud" style="animation-delay:-{d}s"><g transform="translate(0,{y}) scale({s})" '
            f'fill="#fff" fill-opacity=".5" filter="url(#haze)"><ellipse cx="110" cy="0" rx="110" ry="14"/>'
            f'<ellipse cx="150" cy="-12" rx="60" ry="14"/></g></g>'
        )

    p.append(castle(930, 150))
    p.append(rainbow_arc(300, 372, 232))

    # land: far snowy range, mid hills, near meadow
    p.append(
        '<path d="M0,300 L80,268 L150,284 L250,236 L330,270 L430,246 L520,276 L600,226 L690,268 L780,244 '
        'L880,278 L980,240 L1080,272 L1150,256 L1200,270 L1200,420 L0,420 Z" fill="url(#far)" opacity=".92"/>'
    )
    p.append(
        '<path d="M0,330 C120,296 220,322 340,308 C470,292 560,330 690,312 C820,294 930,326 1040,308 '
        'C1110,298 1160,306 1200,300 L1200,420 L0,420 Z" fill="url(#mid)"/>'
    )
    # winding river
    p.append(
        '<path d="M612,318 C580,338 668,350 632,368 C596,386 700,400 660,420 L560,420 C600,400 520,386 568,366 '
        'C610,350 540,338 596,318 Z" fill="#dff6ff" fill-opacity=".85"/>'
    )
    p.append(
        '<path d="M0,372 C150,344 300,372 450,362 C600,352 760,380 900,364 C1020,352 1120,366 1200,356 '
        'L1200,420 L0,420 Z" fill="url(#near)"/>'
    )
    # tiny rock pillars on the plain
    for x, hh in ((420, 20), (470, 14), (760, 22), (820, 15), (540, 12)):
        p.append(f'<rect x="{x}" y="{336 - hh}" width="7" height="{hh}" rx="3" fill="#6fbf93"/>')
        p.append(f'<ellipse cx="{x + 3.5}" cy="{336 - hh}" rx="8" ry="3.5" fill="#8fdc6a"/>')

    # floating islands
    left = island(40, 206, 230, [(150, 34), (196, 18)], "ia")
    left.append(bulb(110, 204, 0.45))
    left.append("</g>")
    p.append("".join(left))
    right = island(905, 226, 260, [(22, 36), (70, 16)], "ib")
    right.append(spire(1060, 224))
    right.append("</g>")
    p.append("".join(right))
    # floating luminous seeds + fireflies
    for x, y, s, d in ((300, 150, 0.6, 0), (392, 96, 0.42, 3), (850, 96, 0.5, 5), (1150, 130, 0.45, 2)):
        p.append(jelly(x, y, s, d))
    for _ in range(22):
        x, y = rnd.uniform(20, W - 60), rnd.uniform(250, 410)
        p.append(
            f'<circle class="fly" cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([2, 2.5, 3])}" fill="#fff7a8" '
            f'style="animation-delay:-{rnd.uniform(0, 9):.1f}s"/>'
        )

    # foreground flora
    p.append(tendril(24, 430, 1.0))
    p.append(tendril(92, 436, 0.7))
    p.append(tendril(1182, 432, 0.95, flip=True))
    p.append(tendril(1118, 438, 0.6, flip=True))
    p.append(bulb(170, 424, 0.8))
    p.append(bulb(1040, 426, 0.7))
    p.append(bulb(232, 430, 0.5))

    # greeting
    p.append('<ellipse cx="600" cy="196" rx="430" ry="92" fill="url(#veil)"/>')
    p.append(
        '<text class="t" x="600" y="208" font-size="104" font-style="italic" font-weight="700" '
        'fill="url(#title)" stroke="#1d0f52" stroke-width="10">Hello there</text>'
    )
    p.append(
        '<text class="t" x="600" y="258" font-size="30" letter-spacing="2" fill="#fff" '
        'stroke="#1d0f52" stroke-width="6">I\'m Ido Yahav  ✦  full-stack developer</text>'
    )
    p.append("</g>")
    p.append("</svg>")
    return "\n".join(p)


if __name__ == "__main__":
    out = ROOT / "assets"
    out.mkdir(exist_ok=True)
    (out / "hero.svg").write_text(build_hero(), encoding="utf-8")
    print("wrote", out / "hero.svg")
