import os
import shutil

# Paths to your directories
train_dir = 'E:/iith-dl-contest-2024/train/train'
val_dir = 'C:\\Users\\gupta\\Downloads\\Kaggle-Data-Set\\ILSVRC2012_img_train.tar'
destination_dir = 'C:\\Users\\gupta\\Downloads\\Kaggle-Data-Set\\train'

# Create the destination directory if it doesn't already exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Iterate through the folders in the train directory
for folder_name in os.listdir(train_dir):
    train_subfolder_path = os.path.join(train_dir, folder_name)
    
    # Check if this is indeed a folder
    if os.path.isdir(train_subfolder_path):
        # Construct the path to the potential matching folder in the val directory
        val_subfolder_path = os.path.join(val_dir, folder_name)
        
        # Check if the folder exists in the val directory
        if os.path.exists(val_subfolder_path) and os.path.isdir(val_subfolder_path):
            # Construct the destination path for this folder
            destination_subfolder_path = os.path.join(destination_dir, folder_name)
            
            # Copy the folder from val to the destination directory
            # Use shutil.copytree if you're copying the folder and its content for the first time
            # If the folder might already exist at the destination and you want to merge/update it,
            # consider a more complex logic that handles file conflicts
            if not os.path.exists(destination_subfolder_path):
                shutil.copytree(val_subfolder_path, destination_subfolder_path)
                print(f"Copied: {folder_name}")
            else:
                print(f"Folder '{folder_name}' already exists at the destination. Skipped.")

print("Operation completed.")
