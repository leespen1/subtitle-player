#!/usr/bin/env python3
"""Generate PWA icons for Subtitle Player.

Draws a closed-caption motif (a rounded "screen" with two amber subtitle bars)
in the app's amber-on-dark palette. Rendered at 4x and downsampled for clean
edges. Run this only when the icon design changes; the PNGs it emits are
committed alongside index.html.
"""
from PIL import Image, ImageDraw

BG = (8, 7, 6)          # --bg
PANEL = (18, 16, 13)    # --bg-panel
AMBER = (240, 207, 148) # --amber
AMBER_DIM = (107, 90, 58)
SS = 4  # supersample factor


def rounded(draw, box, radius, **kw):
    draw.rounded_rectangle(box, radius=radius, **kw)


def draw_icon(size, maskable=False):
    s = size * SS
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Background. Maskable icons must fill the whole canvas (safe zone is the
    # inner 80%); the plain icon gets a rounded-square badge instead.
    if maskable:
        d.rectangle([0, 0, s, s], fill=BG)
        inset = s * 0.16      # keep motif inside the maskable safe zone
    else:
        rounded(d, [0, 0, s - 1, s - 1], radius=s * 0.22, fill=BG)
        inset = s * 0.13

    # The "screen": a rounded rectangle outlined in amber.
    screen = [inset, inset * 1.15, s - inset, s - inset * 1.15]
    rounded(d, screen, radius=s * 0.10, fill=PANEL,
            outline=AMBER_DIM, width=max(1, int(s * 0.012)))

    # Two subtitle bars near the bottom of the screen: a bright full-width line
    # and a shorter dim line beneath it.
    sw = screen[2] - screen[0]
    bar_h = s * 0.075
    left = screen[0] + sw * 0.12
    right = screen[2] - sw * 0.12
    y1 = screen[3] - (screen[3] - screen[1]) * 0.34
    rounded(d, [left, y1, right, y1 + bar_h], radius=bar_h / 2, fill=AMBER)
    y2 = y1 + bar_h * 1.7
    rounded(d, [left, y2, left + (right - left) * 0.6, y2 + bar_h],
            radius=bar_h / 2, fill=AMBER_DIM)

    return img.resize((size, size), Image.LANCZOS)


def main():
    draw_icon(192).save("icon-192.png")
    draw_icon(512).save("icon-512.png")
    draw_icon(512, maskable=True).save("icon-maskable-512.png")
    draw_icon(180).save("apple-touch-icon.png")
    print("wrote icon-192.png icon-512.png icon-maskable-512.png apple-touch-icon.png")


if __name__ == "__main__":
    main()
