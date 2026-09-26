"""
made by claude im too lazy for shii like this
Compress PNG images for low-bandwidth use.

- Keeps .png format and original filenames.
- Resizes images that exceed a max dimension (phone photos are often
  4000px+ wide, which is way more than any web page needs).
- Optionally quantizes colors (palette mode) for a big size reduction,
  since that's where most PNG savings come from.
- Uses PIL's built-in PNG optimizer on top of that.

Usage:
    pip install pillow
    python compress_pngs.py INPUT_DIR OUTPUT_DIR [--max-dim 1600] [--colors 256] [--no-quantize]

Examples:
    python compress_pngs.py ./photos ./photos_compressed
    python compress_pngs.py ./photos ./photos_compressed --max-dim 1200 --colors 128
    python compress_pngs.py ./photos ./photos_compressed --no-quantize   # keep full color, just resize+optimize
"""

import argparse
import sys
from pathlib import Path

from PIL import Image


def compress_png(src_path: Path, dst_path: Path, max_dim: int, colors: int, quantize: bool):
    with Image.open(src_path) as img:
        # Preserve transparency info if present
        has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)

        # Resize if larger than max_dim on the longest side
        w, h = img.size
        if max(w, h) > max_dim:
            scale = max_dim / max(w, h)
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.LANCZOS)

        # Normalize mode before quantizing/saving
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if has_alpha else "RGB")

        if quantize:
            # Palette-based quantization drastically shrinks PNGs.
            # Use adaptive palette; keep alpha via dither-free quantize on RGBA-safe method.
            if has_alpha:
                # Split alpha, quantize color channels, then re-attach alpha
                alpha = img.getchannel("A")
                rgb = img.convert("RGB").quantize(colors=colors, method=Image.MEDIANCUT)
                rgb = rgb.convert("RGBA")
                rgb.putalpha(alpha)
                img = rgb
            else:
                img = img.quantize(colors=colors, method=Image.MEDIANCUT)

        dst_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(dst_path, format="PNG", optimize=True)


def main():
    parser = argparse.ArgumentParser(description="Compress PNG images for low-bandwidth web use.")
    parser.add_argument("input_dir", type=Path, help="Folder containing source .png images")
    parser.add_argument("output_dir", type=Path, help="Folder to write compressed .png images")
    parser.add_argument("--max-dim", type=int, default=1600,
                         help="Max width/height in pixels (default: 1600)")
    parser.add_argument("--colors", type=int, default=256,
                         help="Max palette colors when quantizing (default: 256, min useful ~64)")
    parser.add_argument("--no-quantize", action="store_true",
                         help="Skip color quantization, only resize + optimize")
    args = parser.parse_args()

    if not args.input_dir.is_dir():
        print(f"Input directory not found: {args.input_dir}", file=sys.stderr)
        sys.exit(1)

    png_files = sorted(args.input_dir.glob("*.png")) + sorted(args.input_dir.glob("*.PNG"))
    if not png_files:
        print(f"No .png files found in {args.input_dir}")
        sys.exit(0)

    total_before = 0
    total_after = 0

    for src in png_files:
        dst = args.output_dir / src.name
        before = src.stat().st_size
        try:
            compress_png(src, dst, args.max_dim, args.colors, quantize=not args.no_quantize)
        except Exception as e:
            print(f"  FAILED: {src.name} -> {e}")
            continue
        after = dst.stat().st_size
        total_before += before
        total_after += after
        pct = 100 * (1 - after / before) if before else 0
        print(f"{src.name}: {before/1e6:.1f} MB -> {after/1e6:.2f} MB  ({pct:.0f}% smaller)")

    if total_before:
        pct = 100 * (1 - total_after / total_before)
        print(f"\nTotal: {total_before/1e6:.1f} MB -> {total_after/1e6:.2f} MB ({pct:.0f}% smaller)")


if __name__ == "__main__":
    main()