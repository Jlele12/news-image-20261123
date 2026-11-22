#!/usr/bin/env python3
"""Generate a single-image summary of 23 November 2026 world news.

Renders a dark front-page poster of the day's five biggest stories at
1024x1024 (the make.fun news-image gate's size cap).  Requires Pillow.
Usage: python3 generate.py [output.png]
"""
import os
import sys
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (12, 13, 20)
PANEL = (22, 25, 38)
ACCENTS = [(229, 57, 53), (255, 152, 0), (38, 166, 154), (92, 124, 250), (206, 147, 216)]
FG = (235, 238, 245)
MUTED = (150, 158, 175)

STORIES = [
    ("IRAN STRIKES BAHRAIN, US BASES",
     "Iran hits a civilian site in Bahrain and two US bases; unveils twin-missile launcher aimed at Trump."),
    ("COP31 COLLAPSES IN ANTALYA",
     "Fourth draft rejected over fossil fuels; Guterres blasts 'powerful fossil fuel interests'."),
    ("AI MARKETS SHUDDER",
     "Anthropic's record $81.3B IPO: shares -9%; KOSPI at 10-month low; Chinese tech sheds $1.7T."),
    ("UKRAINE WAR HITS THE BALTIC",
     "Drone sets Russian cargo ship Sparta II ablaze; UK calls Putin a 'cold-blooded killer'."),
    ("CHINA-JAPAN WAR OF WORDS",
     "Beijing paints Japan as an aggressor and resurgent threat; spies chase AI chips."),
]


def font(size, bold=False):
    names = ["DejaVuSans-Bold.ttf"] if bold else ["DejaVuSans.ttf"]
    for n in names:
        p = "/usr/share/fonts/truetype/dejavu/" + n
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def draw_wrapped(d, xy, text, f, width, fill, gap=6):
    x, y = xy
    for line in textwrap.wrap(text, width):
        d.text((x, y), line, font=f, fill=fill)
        y += f.size + gap
    return y


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.text((44, 26), "THE WORLD IN ONE FRAME", font=font(50, True), fill=FG)
    d.text((44, 86), "23 NOVEMBER 2026  ·  FRONT PAGE OF PLANET EARTH", font=font(21), fill=MUTED)
    d.line((44, 124, W - 44, 124), fill=(70, 76, 96), width=3)

    y = 148
    bar_w = 16
    block_h = 144
    for i, (head, body) in enumerate(STORIES):
        color = ACCENTS[i % len(ACCENTS)]
        d.rectangle((44, y, W - 44, y + block_h), fill=PANEL)
        d.rectangle((44, y, 44 + bar_w, y + block_h), fill=color)
        d.text((76, y + 18), head, font=font(27, True), fill=color)
        draw_wrapped(d, (76, y + 58), body, font(19), 54, FG)
        d.text((W - 110, y + 18), f"{i+1:02d}", font=font(27, True), fill=(70, 76, 96))
        y += block_h + 16

    d.line((44, y, W - 44, y), fill=(70, 76, 96), width=3)
    y += 14
    d.text((44, y), "ALSO: El Chapo Isidro captured in Mexico · Alcaraz wins ATP Finals ·",
           font=font(17), fill=MUTED)
    d.text((44, y + 24), "Bangladesh political violence spreads · UN 'killer robots' talks agreed for 2028",
           font=font(17), fill=MUTED)

    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img.save(out, "PNG", optimize=True)
    print(f"saved {out} ({W}x{H}, {os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
