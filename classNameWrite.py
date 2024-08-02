import os

# Set the path to the directory and the mapping file
directory_path = 'E:/iith-dl-contest-2024/train/train'
mapping_file_path = 'className_mapping_file.txt'
output_file_path = 'classnName_iith_dataset.txt'

# Read directory names from the folder
dir_names = os.listdir(directory_path)

# Load mapping from the file
dir_mapping = {}
with open(mapping_file_path, 'r') as file:
    for line in file:
        parts = line.strip().split()
        if len(parts) >= 3:
            dir_name = parts[0].strip()
            real_name = parts[2].strip()
            dir_mapping[dir_name] = real_name

# Compare directory names and create the output content
output_content = []
for dir_name in dir_names:
    real_name = dir_mapping.get(dir_name, 'Unknown')
    output_content.append(f"{dir_name}: {real_name}\n")

# Write the results to a new file
with open(output_file_path, 'w') as output_file:
    output_file.writelines(output_content)

print(f"Output has been saved to {output_file_path}")