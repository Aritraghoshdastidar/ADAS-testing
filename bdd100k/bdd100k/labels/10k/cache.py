import os
import json
from glob import glob

# Paths
val_images_path = r"C:\PESU\CIE\archive\bdd100k\bdd100k\images\10k\val"
val_labels_path = r"C:\PESU\CIE\archive\bdd100k\bdd100k\labels\10k\val"
cache_file_path = os.path.join(val_labels_path, "val.cache")

# Scan for images and labels
image_files = sorted(glob(os.path.join(val_images_path, "*.jpg")))
label_files = sorted(glob(os.path.join(val_labels_path, "*.txt")))

# Create cache data
cache_data = {
    "version": 1.0,
    "images": [os.path.basename(img) for img in image_files],
    "labels": {os.path.basename(lbl).replace(".txt", ".jpg"): lbl for lbl in label_files},
    "num_images": len(image_files),
    "num_labels": len(label_files),
}

# Save cache file
with open(cache_file_path, "w") as f:
    json.dump(cache_data, f, indent=4)

print(f"Successfully created cache: {cache_file_path}")
