import os

# Define paths
train_labels_dir = "C:/PESU/CIE/archive/yolo_labels/train"
val_labels_dir = "C:/PESU/CIE/archive/yolo_labels/val"

# Function to check label files
def check_labels(directory):
    missing_files = []
    for label_file in os.listdir(directory):
        if label_file.endswith(".txt"):
            label_path = os.path.join(directory, label_file)
            with open(label_path, "r") as f:
                content = f.read().strip()
                if not content:
                    missing_files.append(label_file)
    
    if missing_files:
        print(f"⚠️ Warning: {len(missing_files)} empty label files found in {directory}")
    else:
        print(f" All labels in {directory} are valid!")

# Run checks
check_labels(train_labels_dir)
check_labels(val_labels_dir)
