import csv
import re

def clean_category_data(input_filename, output_filename):
    with open(input_filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        data = [(row['ID'], re.search(r"'(n\d+)'", row['Category']).group(1)) for row in reader]

    with open(output_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Category'])
        writer.writerows(data)

# Specify your input and output file names
input_file = 'predicted_output_vit_L_14_64_openAI_CLIP.csv'
output_file = 'OpenAICLILP Logs\predicted_output_vit_64_oac_l14.csv'

clean_category_data(input_file, output_file)
