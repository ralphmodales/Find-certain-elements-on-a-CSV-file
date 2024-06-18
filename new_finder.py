import csv
import sys
import os

if len(sys.argv) < 4:
    print("Use this format: python <py_file> <name_file> <csv_file> <output_csv_file>")
    sys.exit(1)
    
name_file = sys.argv[1]
csv_file = sys.argv[2]
output_csv_file = sys.argv[3]

def read_names_from_file(name_file):
    try:
        with open(name_file, 'r') as file:
            names = [line.strip() for line in file.readlines() if line.strip()]
        return names
    except FileNotFoundError:
        print(f"Error: File '{name_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{name_file}': {e}")
        sys.exit(1)
        
def search_names_in_csv(names_to_search, csv_file):
    try:
        with open(csv_file, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  
            
            found_rows = []
            for row in csv_reader:
                for field in row:
                    if any(name.lower() in field.lower() for name in names_to_search):
                        found_rows.append(row)
                        break
            
            return found_rows
    
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{csv_file}': {e}")
        sys.exit(1)

def write_to_csv(output_csv_file, rows):
    try:
        file_exists = os.path.isfile(output_csv_file)
        with open(output_csv_file, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            for row in rows:
                processed_row = []
                for cell in row:
                    if cell.strip():  
                        processed_row.append(cell)
                    else:
                        processed_row.append('N/A')
                csv_writer.writerow(processed_row)
        print(f"Results written to '{output_csv_file}'.")
    except Exception as e:
        print(f"Error writing to '{output_csv_file}': {e}")
        sys.exit(1)

names_to_search = read_names_from_file(name_file)
if names_to_search:
    found_rows = search_names_in_csv(names_to_search, csv_file)
    
    if found_rows:
        write_to_csv(output_csv_file, found_rows)
    else:
        print("No matching names found in the CSV file.")
else:
    print(f"No names found in '{name_file}'.")
