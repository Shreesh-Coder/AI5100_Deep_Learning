import os
import tarfile

# Paths to your directories
train_dir = 'E:/iith-dl-contest-2024/train/train'
val_tar_path = 'C:\\Users\\gupta\\Downloads\\Kaggle-Data-Set\\ILSVRC2012_img_train.tar'
destination_dir = 'C:\\Users\\gupta\\Downloads\\Kaggle-Data-Set\\train'

# Ensure the destination directory exists
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

with tarfile.open(val_tar_path, "r") as tar:
    # Iterate through directories in the train directory
    for folder_name in os.listdir(train_dir):
        train_subfolder_path = os.path.join(train_dir, folder_name)
        
        # Confirm it's a directory
        if os.path.isdir(train_subfolder_path):
            # Expected TAR file name within the main TAR
            tar_file_name = folder_name + '.tar'
            
            # Check if the TAR file exists in the main TAR
            try:
                member = tar.getmember(tar_file_name)
                print(f"Extracting {tar_file_name}...")

                # Extract the TAR file to a temporary location
                tar.extract(member, path=destination_dir)
                extracted_tar_path = os.path.join(destination_dir, member.name)

                # Create a corresponding directory within destination_dir
                new_dir_path = os.path.join(destination_dir, folder_name)
                if not os.path.exists(new_dir_path):
                    os.makedirs(new_dir_path)

                # Open the extracted TAR and extract its contents into the new directory
                with tarfile.open(extracted_tar_path, "r") as inner_tar:
                    inner_tar.extractall(path=new_dir_path)

                # Remove the extracted TAR file to clean up
                os.remove(extracted_tar_path)
                print(f"Extracted {tar_file_name} to {new_dir_path}.")

            except KeyError:
                print(f"No TAR file named {tar_file_name} found in the archive.")
        else:
            print(f"'{folder_name}' is not a directory or does not exist in the TAR.")

print("Operation completed.")
