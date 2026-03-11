#!/usr/bin/env python3
"""Generate webapp icons from logobrand.png."""

from pathlib import Path
from PIL import Image

SRC = Path("logobrand.png")
OUT = Path("icons")
OUT.mkdir(exist_ok=True)

img = Image.open(SRC)

# PNG icons at various sizes
png_sizes = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "apple-touch-icon.png": 180,
    "icon-128x128.png": 128,
    "icon-192x192.png": 192,
    "icon-256x256.png": 256,
    "icon-512x512.png": 512,
}

for name, size in png_sizes.items():
    resized = img.resize((size, size), Image.LANCZOS)
    resized.save(OUT / name)
    print(f"  {name} ({size}x{size})")

# Multi-resolution favicon.ico
ico_sizes = [16, 32, 48]
ico_images = [img.resize((s, s), Image.LANCZOS) for s in ico_sizes]
ico_images[0].save(OUT / "favicon.ico", format="ICO", sizes=[(s, s) for s in ico_sizes], append_images=ico_images[1:])
print(f"  favicon.ico ({', '.join(f'{s}x{s}' for s in ico_sizes)})")

# OG image: logo centered on white 1200x630 canvas
og = Image.new("RGB", (1200, 630), (255, 255, 255))
logo_size = 500
logo_resized = img.resize((logo_size, logo_size), Image.LANCZOS)
x = (1200 - logo_size) // 2
y = (630 - logo_size) // 2
og.paste(logo_resized, (x, y), logo_resized)  # use alpha as mask
og.save(OUT / "og-image.png")
print(f"  og-image.png (1200x630)")

print("Done!")
