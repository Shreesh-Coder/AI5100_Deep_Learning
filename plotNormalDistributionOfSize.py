import os
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

def collect_image_sizes(root_dir):
    image_sizes = {}
    for class_dir in tqdm(os.listdir(root_dir), desc="Classes Processed"):
        class_path = os.path.join(root_dir, class_dir)
        if os.path.isdir(class_path):
            sizes = []
            for img_file in os.listdir(class_path):
                try:
                    with Image.open(os.path.join(class_path, img_file)) as img:
                        sizes.append(img.size)  # (width, height)
                except Exception as e:
                    continue  # Skip files that cause errors
            image_sizes[class_dir] = sizes
    return image_sizes


def collect_test_image_sizes(test_dir):
    sizes = []
    for img_file in tqdm(os.listdir(test_dir), desc="Processing Test Images"):
        try:
            with Image.open(os.path.join(test_dir, img_file)) as img:
                sizes.append(img.size)  # (width, height)
        except Exception as e:
            continue  # Skip files that cause errors
    return sizes


def plot_size_distribution(image_sizes):
    widths, heights = [], []
    for sizes in image_sizes.values():
        for (w, h) in sizes:
            widths.append(w)
            heights.append(h)

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.hist(widths, bins=50, color='blue', alpha=0.7)
    plt.title('Width Distribution Across All Classes')
    plt.xlabel('Width')
    plt.ylabel('Frequency')

    plt.subplot(1, 2, 2)
    plt.hist(heights, bins=50, color='green', alpha=0.7)
    plt.title('Height Distribution Across All Classes')
    plt.xlabel('Height')

    plt.tight_layout()
    plt.show()


# Example usage:
# Adjust these paths to your local setup
train_dir = "iith-dl-contest-2024\\train\\train"
val_dir = "C:\\Users\\gupta\\Downloads\\Kaggle-Data-Set\\test"

# Example usage:
# Adjust this path to your local setup
test_dir = "iith-dl-contest-2024\\test\\test"

test_image_sizes = collect_test_image_sizes(test_dir)

train_image_sizes = collect_image_sizes(train_dir)
val_image_sizes = collect_image_sizes(val_dir)

plot_size_distribution(train_image_sizes)  # Plot for training data
plot_size_distribution(val_image_sizes)    # Plot for validation data

test_sizes_dict = {"test": test_image_sizes}
plot_size_distribution(test_sizes_dict)  # This function call remains the same
