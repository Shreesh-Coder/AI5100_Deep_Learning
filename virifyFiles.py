import os
import filecmp

def print_diff_files(dcmp):
    for name in dcmp.diff_files:
        print("Different file: %s found in %s and %s" % (name, dcmp.left, dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)

def compare_dirs(dir1, dir2):
    """
    Compares files in two directories recursively.
    
    :param dir1: Path to the first directory.
    :param dir2: Path to the second directory.
    """
    dcmp = filecmp.dircmp(dir1, dir2)
    
    if dcmp.left_only or dcmp.right_only or dcmp.diff_files:
        print("Differences found:")
        if dcmp.left_only:
            print(f"Files/folders only in {dir1}: {dcmp.left_only}")
        if dcmp.right_only:
            print(f"Files/folders only in {dir2}: {dcmp.right_only}")
        print_diff_files(dcmp)
    else:
        print("The directories are identical.")
    
    # This does not consider common_funny as they are files that are in both directories but
    # could not be compared.
    for sub_dcmp in dcmp.subdirs.values():
        compare_dirs(sub_dcmp.left, sub_dcmp.right)

# Example usage
dir1 = 'E:/iith-dl-contest-2024/train/train'  # Replace with the path to your first directory
dir2 = 'C:\\Users\\gupta\\Downloads\\Kaggle-Data-Set\\train'  # Replace with the path to your second directory
compare_dirs(dir1, dir2)
