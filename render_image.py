#!/usr/bin/env python3
"""Render entry.png: a front page summing up Wednesday 18 Nov 2026.

Drawn with Pillow (used only at build time; the shipped main.py is
standard-library only and just copies this PNG).  The layout is a
newspaper front page: a nameplate, a bold date bar, one dominant lead
story (the Gulf escalation), a second lead (the Crimea Bridge), a grid
of four world stories, a strip with two more, and a markets ticker.

Revision 2: rebalanced vertical rhythm so no panel text crosses its
border, a taller bridge scene whose towers, cables and fallen span
read at thumbnail size, and a Gulf scene whose coast, island and base
sit in separate planes so the labels stay clear of the action.

Stories carried (all reported on 18 November 2026):
  * Iran strikes bases in Kuwait and Bahrain after the U.S. strike on
    Iran's Qeshm Island.
  * Ukraine hits the Kerch / Crimea Bridge a second day; part of the
    road span collapses into the strait.
  * Xi Jinping and Putin meet in Shenzhen ahead of the APEC
    three-leader summit with Trump.
  * Mary Peltola wins Alaska's Senate seat; Democrats 56-44.
  * Ebola in DR Congo more than doubles: 11,000+ cases, 5,400 dead.
  * The United States loses its measles-free status after 26 years.
  * Category 5 Cyclone Xavier hits the Northern Cook Islands.
  * A Russian military plane crashes in Siberia; 19 dead.
  * Markets slide: S&P 500 -1.0%, gold $3,775, Brent crude $91.55.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
RIGHT = W - MARGIN

PAPER = (246, 241, 227)
PANEL_BG = (255, 253, 246)
INK = (20, 20, 20)
WHITE = (255, 255, 255)
RED = (179, 32, 42)
BLUE = (29, 78, 137)
SKY = (34, 53, 92)
SEA = (46, 111, 142)
LAND = (16, 20, 28)
SMOKE = (128, 128, 126)
GOLD = (176, 124, 28)
ORANGE = (232, 119, 34)
YELLOW = (250, 197, 66)
TEAL = (14, 116, 144)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_BOLD = os.path.join(FONT_DIR, "dejavu", "DejaVuSerif-Bold.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "liberation", "LiberationSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "liberation", "LiberationSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text(d, xy, s, fnt, fill=INK, anchor="la"):
    d.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def centered(d, y, s, fnt, fill=INK):
    d.text((W // 2, y), s, font=fnt, fill=fill, anchor="ma")


def rule(d, y, width=3, fill=INK):
    d.line([(MARGIN, y), (RIGHT, y)], fill=fill, width=width)


def starburst(d, cx, cy, r, fill=YELLOW, inner=0.45, points=10):
    """A jagged explosion star centred on (cx, cy)."""
    pts = []
    for i in range(points * 2):
        ang = math.pi * i / points
        rad = r if i % 2 == 0 else r * inner
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill)


def parabola(p0, p1, height, n=40):
    """Sample points on a shallow arc from p0 up and down to p1."""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] + (p1[1] - p0[1]) * t - height * 4 * t * (1 - t)
        pts.append((x, y))
    return pts


def gulf_scene(d, x0, y0, x1, y1):
    """Night scene: launches from Iran's coast, bursts over Gulf bases."""
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    sea_y = y0 + (y1 - y0) * 2 // 3
    d.rectangle([x0, sea_y, x1, y1], fill=SEA)
    # Iran's coast: a headland filling the left edge, top to bottom.
    d.polygon([(x0, y0), (x0 + 96, y0), (x0 + 128, sea_y - 6),
               (x0 + 104, y1), (x0, y1)], fill=LAND)
    # Qeshm island: a low, flat silhouette sitting on the sea line.
    d.polygon([(x0 + 268, sea_y + 3), (x0 + 292, sea_y - 11),
               (x0 + 372, sea_y - 11), (x0 + 396, sea_y + 3)], fill=LAND)
    # The far shore and its base, right: ground first, then buildings
    # standing on the sea line so their silhouettes stay readable.
    d.rectangle([x0 + 672, sea_y + 16, x1, y1], fill=LAND)
    for bx, bw, bh in [(700, 46, 30), (756, 36, 44), (802, 58, 26),
                       (872, 34, 38)]:
        d.rectangle([x0 + bx, sea_y - bh, x0 + bx + bw, sea_y + 16],
                    fill=LAND)
    # Missile arcs from the coast to the base.
    launches = [(x0 + 118, y0 + 22), (x0 + 128, y0 + 44), (x0 + 108, y0 + 64)]
    targets = [(x0 + 722, sea_y - 34), (x0 + 772, sea_y - 48),
               (x0 + 830, sea_y - 30)]
    for p0, p1 in zip(launches, targets):
        # Arc height 22 keeps the apex inside the scene: the endpoints
        # sit near the sea line, so a taller arc would strike through
        # the standfirst text above the scene's top edge.
        d.line(parabola(p0, p1, 22), fill=ORANGE, width=4)
        starburst(d, p0[0], p0[1], 10, fill=YELLOW)
    for tx, ty in targets:
        starburst(d, tx, ty, 24, fill=ORANGE)
        starburst(d, tx, ty, 13, fill=YELLOW)
    # Smoke drifting over the base.
    for sx, sy, sr in [(736, sea_y - 66, 15), (788, sea_y - 76, 19),
                       (838, sea_y - 58, 13)]:
        d.ellipse([sx - sr, sy - sr // 2, sx + sr, sy + sr // 2], fill=SMOKE)
    f = font(SANS_BOLD, 21)
    text(d, (x0 + 12, y1 - 29), "IRAN", f, fill=WHITE)
    text(d, (x1 - 12, y1 - 29), "KUWAIT - BAHRAIN", f, fill=WHITE, anchor="ra")


def bridge_scene(d, x0, y0, x1, y1):
    """The Crimea Bridge: towers and cables, one span fallen."""
    d.rectangle([x0, y0, x1, y1], fill=SEA)
    deck_y = y0 + 24
    mid = (x0 + x1) // 2
    gap = 84
    # Two pylons, clear of the labels, with sagging cables to the deck.
    for tx in (mid - 236, mid + 236):
        d.rectangle([tx - 7, y0 + 4, tx + 7, y1], fill=LAND)
        for side in (-1, 1):
            end = (tx + side * 200, deck_y)
            pts = parabola((tx, y0 + 6), end, -7)
            d.line(pts, fill=LAND, width=3)
    # Standing deck either side of the gap.
    d.rectangle([x0, deck_y, mid - gap, deck_y + 10], fill=LAND)
    d.rectangle([mid + gap, deck_y, x1, deck_y + 10], fill=LAND)
    # The fallen road segment, tilted down into the strait.
    d.polygon([(mid - gap + 4, deck_y + 2), (mid + 52, deck_y + 30),
               (mid + 58, deck_y + 41), (mid - gap + 10, deck_y + 13)],
              fill=LAND)
    # Splash where the segment hit the water.
    for sx in (mid - 52, mid - 6, mid + 38):
        d.arc([sx - 19, y1 - 24, sx + 19, y1 + 8], 180, 360, fill=WHITE,
              width=3)
    # Smoke rising from the break.
    for sx, sy, sr in [(mid - 34, deck_y - 13, 12), (mid + 8, deck_y - 20, 16),
                       (mid + 46, deck_y - 11, 10)]:
        d.ellipse([sx - sr, sy - sr // 2, sx + sr, sy + sr // 2], fill=SMOKE)
    f = font(SANS_BOLD, 20)
    text(d, (x0 + 12, y1 - 27), "KERCH STRAIT", f, fill=WHITE)


def panel(d, x, y, w, h, tab, headline, detail_lines):
    d.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=INK, width=2)
    d.rectangle([x, y, x + 10, y + h], fill=tab)
    text(d, (x + 24, y + 9), headline, font(SANS_BOLD, 27))
    df = font(SANS, 23)
    for i, line in enumerate(detail_lines):
        text(d, (x + 24, y + 45 + i * 25), line, df)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Nameplate -----------------------------------------------------
    centered(d, 14, "THE WORLD TODAY", font(SERIF_BOLD, 58))
    rule(d, 84, 2)
    rule(d, 89, 5)

    # --- Date bar --------------------------------------------------------
    d.rectangle([MARGIN, 98, RIGHT, 154], fill=INK)
    centered(d, 109, "WEDNESDAY 18 NOVEMBER 2026", font(SANS_BOLD, 41),
             fill=WHITE)

    # --- Lead story: the Gulf escalation ---------------------------------
    text(d, (MARGIN, 168), "GULF ESCALATION", font(SANS_BOLD, 29), fill=RED)
    text(d, (MARGIN, 198), "IRAN HITS GULF BASES AFTER", font(SANS_BOLD, 55))
    text(d, (MARGIN, 256), "U.S. STRIKE ON QESHM ISLAND", font(SANS_BOLD, 55))
    sf = font(SANS, 25)
    text(d, (MARGIN, 322),
         "Iranian missiles strike the Ali Al Salem base in Kuwait and sites in",
         sf)
    text(d, (MARGIN, 350),
         "Bahrain, answering the U.S. strike on Iran's Qeshm Island.", sf)
    gulf_scene(d, MARGIN, 388, RIGHT, 492)
    rule(d, 502, 3)

    # --- Second lead: the Crimea Bridge ----------------------------------
    text(d, (MARGIN, 514), "WAR IN UKRAINE", font(SANS_BOLD, 27), fill=BLUE)
    text(d, (MARGIN, 544), "UKRAINE HITS CRIMEA BRIDGE AGAIN;",
         font(SANS_BOLD, 42))
    text(d, (MARGIN, 590), "ROAD SPAN COLLAPSES INTO THE STRAIT",
         font(SANS_BOLD, 42))
    bridge_scene(d, MARGIN, 640, RIGHT, 706)
    rule(d, 714, 3)

    # --- Grid of four world stories ---------------------------------------
    pw = (RIGHT - MARGIN - 20) // 2
    panel(d, MARGIN, 724, pw, 96, GOLD, "XI & PUTIN MEET IN SHENZHEN",
          ["Ahead of three-leader APEC", "summit with President Trump"])
    panel(d, MARGIN + pw + 20, 724, pw, 96, BLUE,
          "DEMOCRATS TAKE SENATE 56-44",
          ["Mary Peltola wins Alaska seat", "for a 56-44 majority"])
    panel(d, MARGIN, 828, pw, 96, RED, "EBOLA DOUBLES IN DR CONGO",
          ["11,000+ cases, 5,400 dead;", "children hit hardest"])
    panel(d, MARGIN + pw + 20, 828, pw, 96, TEAL,
          "CATEGORY 5 CYCLONE XAVIER",
          ["Storm slams the Northern", "Cook Islands, Pacific"])

    # --- Strip: two more stories ------------------------------------------
    centered(d, 934, "U.S. LOSES MEASLES-FREE STATUS AFTER 26 YEARS - 5,400+ CASES",
             font(SANS_BOLD, 22))
    centered(d, 958, "RUSSIAN MILITARY PLANE CRASH IN SIBERIA KILLS 19",
             font(SANS_BOLD, 22))

    # --- Markets ticker -----------------------------------------------------
    d.rectangle([0, 984, W, H], fill=INK)
    centered(d, 993, "MARKETS SLIDE:  S&P 500 -1.0%   GOLD $3,775   BRENT $91.55",
             font(SANS_BOLD, 24), fill=WHITE)
    for tx in (MARGIN + 6, RIGHT - 26):
        d.polygon([(tx, 992), (tx + 20, 992), (tx + 10, 1008)], fill=RED)

    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build().save(out, optimize=True)
    print("wrote", out)
