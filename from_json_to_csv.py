import json
import csv
import glob

# Get all JSON files in the folder (adjust path if needed)
json_files = glob.glob("*.json")

all_rows = []

for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)

            # Ensure the file content is a list
            if isinstance(data, list):
                all_rows.extend(data)
            else:
                print(f"Warning: {file} does not contain a list.")
        except json.JSONDecodeError as e:
            print(f"Error reading {file}: {e}")

# Write to CSV
if all_rows:
    fieldnames = all_rows[0].keys()  # Persona, Rating, Review Text

    with open("merged_reviews.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print("CSV created: merged_reviews.csv")
else:
    print("No data found.")
