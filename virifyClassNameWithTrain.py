import os

# Paths to your directories
train_dir = 'E:/iith-dl-contest-2024/train/train'
val_dir = 'C:\\Users\\gupta\\Downloads\\Kaggle-Data-Set\\test'

# Get the list of class directories in both train and val folders
train_classes = {d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))}
val_classes = {d for d in os.listdir(val_dir) if os.path.isdir(os.path.join(val_dir, d))}

# Find classes present in both train and val
common_classes = train_classes.intersection(val_classes)

# Find classes present in train but missing in val
missing_in_val = train_classes.difference(val_classes)

# Find classes present in val but missing in train
missing_in_train = val_classes.difference(train_classes)

# Display the results
print("Common Classes (in both train and val):")
for cls in sorted(common_classes):
    print(cls)

print("\nClasses in Train but Missing in Val:")
for cls in sorted(missing_in_val):
    print(cls)

print("\nClasses in Val but Missing in Train:")
for cls in sorted(missing_in_train):
    print(cls)

# Determine if the train and val sets are perfectly aligned
if not missing_in_val and not missing_in_train:
    print("\nTrain and Val folders have perfectly aligned class directories.")
else:
    print("\nDiscrepancies found between class directories in Train and Val folders.")
