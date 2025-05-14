import piexif
from PIL import Image
import random
import os
from concurrent.futures import ThreadPoolExecutor

def deg_to_dms_rational(deg):
    d = int(deg)
    m = int((deg - d) * 60)
    s = int(((deg - d) * 60 - m) * 60 * 100)
    return ((d, 1), (m, 1), (s, 100))

def get_random_coords():
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    return lat, lon

def replace_gps_data(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img.info.get("exif")
        if not exif_data:
            print(f"Skipping (no EXIF): {image_path}")
            return

        exif_dict = piexif.load(exif_data)

        lat, lon = get_random_coords()

        gps_ifd = {
            piexif.GPSIFD.GPSLatitudeRef: b'N' if lat >= 0 else b'S',
            piexif.GPSIFD.GPSLatitude: deg_to_dms_rational(abs(lat)),
            piexif.GPSIFD.GPSLongitudeRef: b'E' if lon >= 0 else b'W',
            piexif.GPSIFD.GPSLongitude: deg_to_dms_rational(abs(lon)),
        }

        exif_dict["GPS"] = gps_ifd
        exif_bytes = piexif.dump(exif_dict)

        img.save(image_path, exif=exif_bytes)
        print(f"Updated GPS data in: {image_path}")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def process_folder(folder):
    image_paths = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg")) and "_thumb" not in file.lower():
                full_path = os.path.join(root, file)
                image_paths.append(full_path)

    # Use ThreadPoolExecutor to process images in parallel
    with ThreadPoolExecutor() as executor:
        executor.map(replace_gps_data, image_paths)

process_folder(os.path.expanduser("full_res/"))
