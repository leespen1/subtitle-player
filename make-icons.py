#!/usr/bin/env python3
"""Generate PWA icons for Subtitle Player.

The icon tells the app's story: a white TV outline labelled "Subtitle Player"
with a smaller rounded "phone" below it showing amber subtitle squiggles, i.e.
the phone you read subtitles on while the film plays on the TV. Rendered at 4x
and downsampled for clean edges. Run this only when the icon design changes; the
PNGs it emits are committed alongside index.html.
"""
import math
from PIL import Image, ImageDraw, ImageFont

BG = (8, 7, 6)            # --bg
PANEL = (18, 16, 13)      # --bg-panel
AMBER = (240, 207, 148)   # --amber
WHITE = (240, 240, 238)
SS = 4  # supersample factor

FONT_PATHS = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def load_font(px):
    for p in FONT_PATHS:
        try:
            return ImageFont.truetype(p, px)
        except OSError:
            continue
    return ImageFont.load_default()


def text_w(font, s):
    b = font.getbbox(s)
    return b[2] - b[0]


def fit_font(lines, max_w, max_h):
    """Largest bold font whose lines fit within the given box."""
    best = load_font(8)
    size = 8
    while size < max_h:
        f = load_font(size)
        asc, desc = f.getmetrics()
        line_h = asc + desc
        total_h = line_h * len(lines)
        widest = max(text_w(f, ln) for ln in lines)
        if widest > max_w or total_h > max_h:
            break
        best, size = f, size + 2
    return best


def squiggle(draw, x0, x1, y, amp, wavelength, width, fill):
    """A sine wave from x0 to x1 at height y, standing in for a line of text."""
    pts = []
    x = x0
    step = max(1, int((x1 - x0) / 80))
    while x <= x1:
        pts.append((x, y + amp * math.sin(2 * math.pi * (x - x0) / wavelength)))
        x += step
    draw.line(pts, fill=fill, width=width, joint="curve")


def draw_icon(size, maskable=False):
    s = size * SS
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Background. Maskable icons must fill the whole canvas (the safe zone is the
    # inner 80%); the plain icon gets a rounded-square badge instead.
    if maskable:
        d.rectangle([0, 0, s, s], fill=BG)
        m = 0.11 * s        # keep the artwork inside the maskable safe zone
    else:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=s * 0.22, fill=BG)
        m = 0.0
    cs = s - 2 * m          # content-box side
    fx = lambda f: m + f * cs
    fy = lambda f: m + f * cs

    stroke = max(2, int(s * 0.02))

    # ---- TV: white rounded-rectangle outline with the app name inside ----
    tv = [fx(0.09), fy(0.06), fx(0.91), fy(0.52)]
    d.rounded_rectangle(tv, radius=s * 0.03, outline=WHITE, width=stroke)

    lines = ["Subtitle", "Player"]
    inner_w = (tv[2] - tv[0]) * 0.82
    inner_h = (tv[3] - tv[1]) * 0.74
    font = fit_font(lines, inner_w, inner_h)
    asc, desc = font.getmetrics()
    line_h = asc + desc
    block_h = line_h * len(lines)
    ty = (tv[1] + tv[3]) / 2 - block_h / 2
    cx = (tv[0] + tv[2]) / 2
    for ln in lines:
        d.text((cx, ty), ln, font=font, fill=WHITE, anchor="ma")
        ty += line_h

    # ---- Phone: smaller rounded rectangle with amber subtitle squiggles ----
    phone = [fx(0.30), fy(0.61), fx(0.70), fy(0.95)]
    d.rounded_rectangle(phone, radius=s * 0.035,
                        fill=PANEL, outline=WHITE, width=max(2, int(s * 0.016)))
    pw = phone[2] - phone[0]
    ph = phone[3] - phone[1]
    pad = pw * 0.16
    left = phone[0] + pad
    right = phone[2] - pad
    sq_w = max(2, int(s * 0.014))
    amp = ph * 0.045
    wl = pw * 0.30
    for i, frac in enumerate((1.0, 0.72, 0.52)):
        y = phone[1] + ph * (0.36 + i * 0.22)
        squiggle(d, left, left + (right - left) * frac, y, amp, wl, sq_w, AMBER)

    return img.resize((size, size), Image.LANCZOS)


def main():
    draw_icon(192).save("icon-192.png")
    draw_icon(512).save("icon-512.png")
    draw_icon(512, maskable=True).save("icon-maskable-512.png")
    draw_icon(180).save("apple-touch-icon.png")
    print("wrote icon-192.png icon-512.png icon-maskable-512.png apple-touch-icon.png")


if __name__ == "__main__":
    main()
