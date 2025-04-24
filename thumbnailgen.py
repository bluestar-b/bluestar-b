from pathlib import Path
from PIL import Image

base_dir = Path('full_res')
thumb_suffix = '_thumb'
thumb_size = (256, 256)

def make_thumbnail(img_path: Path):
    if thumb_suffix in img_path.stem:
        return

    thumb_path = img_path.with_name(f"{img_path.stem}{thumb_suffix}{img_path.suffix}")
    if thumb_path.exists():
        return

    try:
        with Image.open(img_path) as img:
            img.convert('RGB')
            img.thumbnail(thumb_size)
            img.save(thumb_path, quality=50)
            print(f"✓ {thumb_path.relative_to(base_dir)}")
    except Exception as e:
        print(f"✗ Failed {img_path}: {e}")

for img_file in base_dir.rglob("*"):
    if img_file.is_file() and img_file.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp"]:
        make_thumbnail(img_file)
