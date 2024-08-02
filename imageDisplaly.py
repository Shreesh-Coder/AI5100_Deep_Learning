import imgaug.augmenters as iaa
import matplotlib.pyplot as plt
import cv2
import numpy as np

def load_image(image_path):
    """ Load an image from a file path. """
    image = cv2.imread(image_path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def create_individual_augmenters():
    """ Create list of augmentations to apply individually. """
    return [
        iaa.Fliplr(1),  # Flip image horizontally
        iaa.GaussianBlur(sigma=3.0),  # Apply Gaussian blur
        iaa.Affine(rotate=30),  # Rotate image by 30 degrees
        iaa.Affine(shear=15),  # Shear by 15 degrees
        iaa.Multiply(1.2),  # Increase brightness
        iaa.LinearContrast(1.5),  # Increase contrast
        iaa.AddToHueAndSaturation(20),  # Increase hue and saturation
        iaa.Resize({"height": 224, "width": 224}),  # Resize to 224x224
        iaa.CropToFixedSize(width=64, height=64)  # Crop to 64x64
    ]

def apply_augmentations(image, augmenters):
    """ Apply each augmentation to the image and return results. """
    images = [augmenter(image=image) for augmenter in augmenters]
    return images

def plot_images(original_image, augmented_images, titles):
    """ Plot the original and augmented images. """
    plt.figure(figsize=(15, 8))
    plt.subplot(3, 4, 1)
    plt.imshow(original_image)
    plt.title("Original")
    plt.axis('off')

    for i, (img, title) in enumerate(zip(augmented_images, titles), start=2):
        plt.subplot(3, 4, i)
        plt.imshow(img)
        plt.title(title)
        plt.axis('off')

    plt.tight_layout()
    plt.show()

# Path to an example image
image_path = 'iith-dl-contest-2024\\train\\train\\n01443537\\n01443537_71.JPEG'
original_image = load_image(image_path)
augmenters = create_individual_augmenters()
titles = ["Flip LR", "Gaussian Blur", "Rotate 30", "Shear 15", "Brighten", "Increase Contrast", "Hue + Sat", "Resize 224x224", "Crop 64x64"]
augmented_images = apply_augmentations(original_image, augmenters)
plot_images(original_image, augmented_images, titles)
