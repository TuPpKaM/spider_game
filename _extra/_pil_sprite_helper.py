import os
from PIL import Image

# Define the base directory
base_dir = 'assets\\units\\spiderling'

# List of subdirectories
sub_dirs = ["Attack_02", "Idle_01", "Idle_02", "Walk_Forward"]

# Function to resize images
def resize_images(directory, scale_factor=0.1):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            file_path = os.path.join(directory, filename)
            with Image.open(file_path) as img:
                # Calculate new dimensions
                new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
                # Resize image
                resized_img = img.resize(new_size, Image.BICUBIC)
                # Save resized image, replacing the original
                resized_img.save(file_path)
                print(f'Resized {file_path} to {new_size}')

# Iterate through each subdirectory and resize images
for sub_dir in sub_dirs:
    full_dir = os.path.join(base_dir, sub_dir)
    resize_images(full_dir)

print("Resizing complete.")
