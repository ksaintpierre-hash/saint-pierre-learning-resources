"""Bake a tiled, semi-transparent ownership watermark directly into every
preview image's pixels, so a saved/cropped copy still carries it (the
on-page CSS overlay alone can be bypassed with "Save Image As").
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / 'scripts/fonts/DejaVuSans-Bold.ttf'
TEXT = 'SAINT PIERRE LEARNING RESOURCES · PREVIEW ONLY'


def watermark(path: Path):
    base = Image.open(path).convert('RGBA')
    w, h = base.size
    tile_font_size = max(18, w // 34)
    font = ImageFont.truetype(str(FONT), tile_font_size)

    layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    bbox = draw.textbbox((0, 0), TEXT, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    stamp_w, stamp_h = text_w + tile_font_size * 3, text_h + int(tile_font_size * 2.5)
    stamp = Image.new('RGBA', (stamp_w, stamp_h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(stamp)
    sdraw.text((stamp_w / 2, stamp_h / 2), TEXT, font=font, fill=(176, 73, 46, 46), anchor='mm')
    stamp = stamp.rotate(-28, expand=True, resample=Image.BICUBIC)

    sw, sh = stamp.size
    for y in range(-sh, h + sh, sh):
        for x in range(-sw, w + sw, sw):
            layer.alpha_composite(stamp, (x, y))

    out = Image.alpha_composite(base, layer).convert('RGB')
    out.save(path, 'PNG', optimize=True)


if __name__ == '__main__':
    targets = sys.argv[1:]
    if not targets:
        targets = [str(p) for p in (ROOT / 'public/product-previews').glob('*.png')]
    for t in targets:
        watermark(Path(t))
        print(t, flush=True)
