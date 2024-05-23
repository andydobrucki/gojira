import csv

input_csv = 'input.csv'  # replace with your input file name
output_csv = 'categories.csv'  # replace with your desired output file name

with open(input_csv, 'r') as input_file:
    reader = csv.reader(input_file)
    with open(output_csv, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        for row in reader:
            category = row[0].split(',')[0].strip()
            subcategory = '' if len(row) <= 2 else row[0].split(',')[1].strip()
            writer.writerow([category, subcategory])

print(f"Output file saved as {output_csv}")