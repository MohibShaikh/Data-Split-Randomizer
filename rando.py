import os
import shutil
import random

# Define your paths
base_dir = 'data_last_neu'  # Replace with the actual base path
consolidated_dir = os.path.join(base_dir, 'consolidated')
output_dirs = {
    'train': os.path.join(base_dir, 'train'),
    'valid': os.path.join(base_dir, 'valid'),
    'test': os.path.join(base_dir, 'test')
}

# Ensure consolidated directories exist
os.makedirs(os.path.join(consolidated_dir, 'images'), exist_ok=True)
os.makedirs(os.path.join(consolidated_dir, 'labels'), exist_ok=True)

# Consolidate all images and labels into one directory
for split in ['train', 'valid', 'test']:
    image_dir = os.path.join(base_dir, split, 'images')
    label_dir = os.path.join(base_dir, split, 'labels')
    
    for file_name in os.listdir(image_dir):
        label_file_name = file_name.replace('.jpg', '.txt').replace('.png', '.txt')
        label_file_path = os.path.join(label_dir, label_file_name)
        
        if os.path.exists(label_file_path):
            shutil.move(os.path.join(image_dir, file_name), os.path.join(consolidated_dir, 'images', file_name))
            shutil.move(label_file_path, os.path.join(consolidated_dir, 'labels', label_file_name))
        else:
            print(f"Skipping {file_name} as the corresponding label is missing.")

# Shuffle the consolidated dataset
image_files = os.listdir(os.path.join(consolidated_dir, 'images'))
random.shuffle(image_files)

# Define split ratios
train_ratio = 0.7
valid_ratio = 0.15
test_ratio = 0.15

# Calculate split indices
total_images = len(image_files)
train_idx = int(train_ratio * total_images)
valid_idx = int((train_ratio + valid_ratio) * total_images)

# Split the data
splits = {
    'train': image_files[:train_idx],
    'valid': image_files[train_idx:valid_idx],
    'test': image_files[valid_idx:]
}

# Move files back to their respective folders
for split, files in splits.items():
    image_dest_dir = os.path.join(output_dirs[split], 'images')
    label_dest_dir = os.path.join(output_dirs[split], 'labels')
    os.makedirs(image_dest_dir, exist_ok=True)
    os.makedirs(label_dest_dir, exist_ok=True)
    
    for file_name in files:
        shutil.move(os.path.join(consolidated_dir, 'images', file_name), os.path.join(image_dest_dir, file_name))
        label_file_name = file_name.replace('.jpg', '.txt').replace('.png', '.txt')
        shutil.move(os.path.join(consolidated_dir, 'labels', label_file_name), os.path.join(label_dest_dir, label_file_name))
