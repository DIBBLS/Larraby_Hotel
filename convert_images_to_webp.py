#!/usr/bin/env python3
import os
import sys
from PIL import Image

ROOT = os.path.dirname(__file__)
IMG_DIR = os.path.join(ROOT, 'Images')
QUALITY = 80

if not os.path.isdir(IMG_DIR):
    print('Images directory not found at', IMG_DIR)
    sys.exit(1)

converted = 0
skipped = 0
errors = 0
for dirpath, dirs, files in os.walk(IMG_DIR):
    for fname in files:
        lower = fname.lower()
        if lower.endswith(('.jpg', '.jpeg', '.png')):
            src = os.path.join(dirpath, fname)
            dst = os.path.splitext(src)[0] + '.webp'
            if os.path.exists(dst):
                print('Skipping (exists):', os.path.relpath(dst, ROOT))
                skipped += 1
                continue
            try:
                with Image.open(src) as im:
                    # Preserve alpha when present
                    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
                        out = im.convert('RGBA')
                    else:
                        out = im.convert('RGB')
                    out.save(dst, 'WEBP', quality=QUALITY, method=6)
                print('Converted:', os.path.relpath(src, ROOT), '→', os.path.relpath(dst, ROOT))
                converted += 1
            except Exception as e:
                print('Error converting', src, '-', e)
                errors += 1

print('\nSummary:')
print(' Converted:', converted)
print(' Skipped (already exist):', skipped)
print(' Errors:', errors)

if converted == 0:
    print('No new conversions performed. If you want to replace originals, remove existing .webp files or pass different settings.')
else:
    print('WebP files created alongside originals in the Images/ folder.')
