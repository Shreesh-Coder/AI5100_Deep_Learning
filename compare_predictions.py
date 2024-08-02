import pandas as pd
import sys

def calculate_accuracy_and_loss(pretrained_csv_path, predictions_csv_path):
    # Load the datasets
    pretrained_df = pd.read_csv(pretrained_csv_path)
    predictions_df = pd.read_csv(predictions_csv_path)

    # Merge the dataframes on the 'ID' column to compare labels
    comparison_df = pd.merge(pretrained_df, predictions_df, on='ID', suffixes=('_true', '_pred'))

    # Calculate accuracy: the percentage of correct predictions
    accuracy = (comparison_df['Category_true'] == comparison_df['Category_pred']).mean()

    # Calculate loss: simply the number of incorrect predictions for simplicity
    loss = (comparison_df['Category_true'] != comparison_df['Category_pred']).sum()

    return accuracy, loss

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py pretrained_csv_path predictions_csv_path")
        sys.exit(1)

    pretrained_csv_path = sys.argv[1]
    predictions_csv_path = sys.argv[2]

    # Calculate and print the accuracy and loss
    accuracy, loss = calculate_accuracy_and_loss(pretrained_csv_path, predictions_csv_path)
    print(f"Accuracy: {accuracy*100:.2f}%")
    print(f"Loss: {loss}")
