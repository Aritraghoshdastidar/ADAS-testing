import os
import json
from tqdm import tqdm

# Paths
BDD100K_LABELS_TRAIN = r"C:\PESU\CIE\archive\bdd100k_labels_release\bdd100k\labels\bdd100k_labels_images_train.json"
BDD100K_LABELS_VAL = r"C:\PESU\CIE\archive\bdd100k_labels_release\bdd100k\labels\bdd100k_labels_images_val.json"
BDD100K_IMAGES_TRAIN = r"C:\PESU\CIE\archive\bdd100k\bdd100k\images\100k\train"
BDD100K_IMAGES_VAL = r"C:\PESU\CIE\archive\bdd100k\bdd100k\images\100k\val"
YOLO_LABELS_TRAIN_DIR = r"C:\PESU\CIE\archive\yolo_labels\train"
YOLO_LABELS_VAL_DIR = r"C:\PESU\CIE\archive\yolo_labels\val"

# Class mapping
CLASS_MAP = {
    "car": 0,
    "drivable area": 1,
    "lane": 2,
    "traffic sign": 3,
    "traffic light": 4,
    "person": 5,
    "truck": 6,
    "bus": 7,
    "bike": 8,
    "rider": 9,
    "motor": 10,
    "train": 11,
}

# Function to convert BDD100K bbox format to YOLO format
def convert_bbox(size, box):
    dw, dh = 1.0 / size[0], 1.0 / size[1]
    x1, y1, x2, y2 = box
    x_center = ((x1 + x2) / 2.0) * dw
    y_center = ((y1 + y2) / 2.0) * dh
    w = (x2 - x1) * dw
    h = (y2 - y1) * dh
    return x_center, y_center, w, h

# Function to convert labels to YOLO format
def convert_labels(json_path, images_path, output_dir, split):
    os.makedirs(output_dir, exist_ok=True)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for item in tqdm(data, desc=f"Converting {split} Labels"):
        image_name = item["name"]
        image_path = os.path.join(images_path, image_name)
        
        if not os.path.exists(image_path):
            continue  # Skip missing images

        label_file = os.path.join(output_dir, image_name.replace(".jpg", ".txt"))
        with open(label_file, "w", encoding="utf-8") as f:
            for label in item.get("labels", []):  # Use .get() to avoid KeyError
                category = label["category"]
                if category not in CLASS_MAP:
                    continue
                
                class_id = CLASS_MAP[category]
                if "box2d" not in label:
                    continue  # Skip if no bounding box
                
                bbox = label["box2d"]
                x_center, y_center, w, h = convert_bbox((1280, 720), [bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]])
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")
    
    print(f"{split} labels saved in {output_dir}")

# Convert train and val labels
convert_labels(BDD100K_LABELS_TRAIN, BDD100K_IMAGES_TRAIN, YOLO_LABELS_TRAIN_DIR, "Train")
convert_labels(BDD100K_LABELS_VAL, BDD100K_IMAGES_VAL, YOLO_LABELS_VAL_DIR, "Validation")

print("Conversion complete!")