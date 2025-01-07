from pathlib import Path
import json
import sys  # For exit()

# Get user input for the folder
user = input("Give the user folder name (e.g., Stefanos, Nikos-Windows):\t")
dataset = input("Give the dataset name (e.g., glove-25-angular):\t")

# Specify the root folder
print(f"Seeking inside results/{user}/{dataset}...\n")
root_folder = Path(f"results/{user}/{dataset}")

# Check if the folder exists
if not root_folder.exists():
    print(f"Error: The folder 'results/{user}/{dataset}' does not exist.\n")
    sys.exit(1)  # Exit the program with an error code

mean_precisions_list = []  # List to store all mean_precisions

# Iterate through all .json files in the folder and subdirectories
for json_file in root_folder.rglob("*.json"):
    try:
        # Open the JSON file and parse its content
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            
            # Extract the mean_precisions value from the JSON content
            mean_precisions = data.get("results", {}).get("mean_precisions", None)
            
            # Print the result in a readable format if mean_precisions exists
            if mean_precisions is not None:
                print(f"File: {json_file}")
                print(f"Mean Precision: {repr(mean_precisions)}\n")  # Use repr for accuracy
                
                # Add to the list for overall mean calculation
                mean_precisions_list.append(mean_precisions)
            else:
                print(f"File: {json_file}")
                print("Mean Precision: Not Found\n")
    except Exception as e:
        print(f"Error reading {json_file}: {e}\n")

# Calculate and print the overall mean of all mean_precisions
if mean_precisions_list:
    overall_mean_precision = sum(mean_precisions_list) / len(mean_precisions_list)
    print(f"Total Files Processed: {len(mean_precisions_list)}")
    print(f"Overall Mean Precision: {overall_mean_precision:.15f}\n")  # High precision output
else:
    print("No mean_precisions were found in the provided folder.\n")
