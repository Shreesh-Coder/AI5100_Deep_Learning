import imgaug.augmenters as iaa
import numpy as np
import cv2
import os

def create_augmenters():
    """ Create a sequential list of image augmentations. """
    return iaa.Sequential([
        iaa.Fliplr(0.5),  # horizontally flip 50% of the images
        iaa.Crop(percent=(0, 0.1)),  # random crops
        iaa.Sometimes(0.5,
                      iaa.GaussianBlur(sigma=(0, 0.5))
                      ),
        iaa.ContrastNormalization((0.75, 1.5)),
        iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
        iaa.Multiply((0.8, 1.2), per_channel=0.2),
        iaa.Affine(
            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
            translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
            rotate=(-25, 25),
            shear=(-8, 8)
        )
    ])

def augment_images_in_directory(input_dir, output_dir, num_augmented_images=5):
    """ Augment all images in the specified directory and save to the output directory. """
    aug = create_augmenters()  # Create augmenter pipeline
    for class_name in os.listdir(input_dir):
        class_dir = os.path.join(input_dir, class_name)
        output_class_dir = os.path.join(output_dir, class_name)
        os.makedirs(output_class_dir, exist_ok=True)

        for filename in os.listdir(class_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(class_dir, filename)
                image = cv2.imread(image_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # imgaug works with RGB images

                # Save original image in the output directory
                original_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert back to BGR for saving
                cv2.imwrite(os.path.join(output_class_dir, f"original_{filename}"), original_image)

                # Generate augmented images
                for i in range(num_augmented_images):
                    aug_image = aug(image=image)
                    aug_image = cv2.cvtColor(aug_image, cv2.COLOR_RGB2BGR)  # Convert back to BGR for saving
                    cv2.imwrite(os.path.join(output_class_dir, f"{i}_{filename}"), aug_image)

# Paths to your input and output directories
input_dir = 'iith-dl-contest-2024\\train\\train'
output_dir = 'iith-dl-contest-2024\\train_aug_org\\train'

# Augment images
augment_images_in_directory(input_dir, output_dir)
