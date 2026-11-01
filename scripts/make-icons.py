#!/usr/bin/env python3
"""Regenerate every icon from assets/icon-source.jpg (the dragon-mask picture).
Usage: python3 scripts/make-icons.py   (needs: pip install pillow)"""
import os
from PIL import Image, ImageFilter, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = Image.open(os.path.join(ROOT, "assets", "icon-source.jpg")).convert("RGB")
W, H = SRC.size  # 736 x 977

# Square crop: brow/eyes down to the dragon jaw
TOP = 150
crop = SRC.crop((0, TOP, W, TOP + W))  # 736 x 736

def save(img, rel):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    img.save(p, optimize=True)

def rounded(img, radius_frac=0.22):
    s = img.size[0]
    m = Image.new("L", (s * 4, s * 4), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, s * 4 - 1, s * 4 - 1), radius=int(s * 4 * radius_frac), fill=255)
    m = m.resize((s, s), Image.LANCZOS)
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    out.paste(img.convert("RGBA"), (0, 0), m)
    return out

def circle(img):
    s = img.size[0]
    m = Image.new("L", (s * 4, s * 4), 0)
    ImageDraw.Draw(m).ellipse((0, 0, s * 4 - 1, s * 4 - 1), fill=255)
    m = m.resize((s, s), Image.LANCZOS)
    out = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    out.paste(img.convert("RGBA"), (0, 0), m)
    return out

# ---- master + web/PWA icons ----
master = crop.resize((1024, 1024), Image.LANCZOS)
save(master, "assets/icon.png")
for n in (192, 512):
    save(master.resize((n, n), Image.LANCZOS), f"www/icon-{n}.png")
save(master.resize((180, 180), Image.LANCZOS), "www/apple-touch-icon.png")
save(master.resize((64, 64), Image.LANCZOS), "www/favicon.png")

# maskable (PWA): art inset to the 80% safe zone over a blurred copy of itself
def adaptive_layers(size):
    bg = master.resize((size, size), Image.LANCZOS).filter(ImageFilter.GaussianBlur(size // 18))
    fg_art = master.resize((int(size * 0.74), int(size * 0.74)), Image.LANCZOS)
    fg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    off = (size - fg_art.size[0]) // 2
    fg.paste(fg_art, (off, off))
    return bg.convert("RGBA"), fg

bg512, fg512 = adaptive_layers(512)
mask512 = bg512.copy(); mask512.alpha_composite(fg512)
save(mask512.convert("RGB"), "www/icon-maskable-512.png")

# ---- Android mipmaps (legacy + adaptive layers) ----
dens = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
for d, k in dens.items():
    legacy = int(48 * k)
    base = master.resize((legacy, legacy), Image.LANCZOS)
    save(rounded(base), f"android-icons/res/mipmap-{d}/ic_launcher.png")
    save(circle(base), f"android-icons/res/mipmap-{d}/ic_launcher_round.png")
    layer = int(108 * k)
    bg, fg = adaptive_layers(layer)
    save(bg.convert("RGB"), f"android-icons/res/mipmap-{d}/ic_launcher_background.png")
    save(fg, f"android-icons/res/mipmap-{d}/ic_launcher_foreground.png")

xml = '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@mipmap/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
'''
for name in ("ic_launcher.xml", "ic_launcher_round.xml"):
    p = os.path.join(ROOT, "android-icons/res/mipmap-anydpi-v26", name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(xml)
print("icons done")
