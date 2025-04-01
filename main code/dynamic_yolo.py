import torch
import psutil
import cv2
import os
from ultralytics import YOLO

# Define thresholds
CPU_THRESHOLD = 60
MEMORY_THRESHOLD = 70

# Load YOLO models
model_nano = YOLO("yolov8n.pt")  # Fast, lightweight
model_small = YOLO("yolov8s.pt")  # More accurate

# Path to YOLO predictions
input_folder = r"C:\PESU\CIE\archive\runs\detect\predict"
output_folder = r"C:\PESU\CIE\archive\runs\detect\dynamic_output"

os.makedirs(output_folder, exist_ok=True)

# Process each image
for img_name in os.listdir(input_folder):
    img_path = os.path.join(input_folder, img_name)
    image = cv2.imread(img_path)

    if image is None:
        continue

    # Monitor system load
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    # Choose model based on system load
    if cpu_usage > CPU_THRESHOLD or memory_usage > MEMORY_THRESHOLD:
        print(f"Using YOLOv8-Nano for {img_name} (Low Power Mode)")
        results = model_nano(image)
    else:
        print(f"Using YOLOv8-Small for {img_name} (High Accuracy Mode)")
        results = model_small(image)

    # Draw results
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0]
            cls = int(box.cls[0])

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"Class: {cls} | {confidence:.2f}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save output
    output_path = os.path.join(output_folder, img_name)
    cv2.imwrite(output_path, image)

print(f"Processing complete! Check output images in {output_folder}")
