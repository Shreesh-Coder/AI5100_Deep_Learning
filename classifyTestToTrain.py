import os
import shutil
import csv

# Path to the CSV file
csv_file = 'OpenAICLILP Logs\\predicted_output_vit_64_oac_l14.csv'

# Path to the directory containing the images
images_directory = 'iith-dl-contest-2024 copy\\test\\test'

# Path to the base directory where directories already exist
base_directory = 'iith-dl-contest-2024 copy\\train\\train'

# Move files to the existing directories
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row if there is one
    for row in reader:
        image_name = row[0]
        directory_name = row[1]
        source_path = os.path.join(images_directory, image_name)
        target_directory = os.path.join(base_directory, directory_name)
        target_path = os.path.join(target_directory, image_name)
        
        # Move the file
        if os.path.exists(source_path) and os.path.exists(target_directory):
            shutil.move(source_path, target_path)
        else:
            if not os.path.exists(source_path):
                print(f"Image not found: {image_name}")
            if not os.path.exists(target_directory):
                print(f"Directory not found: {target_directory}")

print("Images have been moved to the specified directories.")
