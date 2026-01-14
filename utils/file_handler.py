def read_sales_file(file_path):
    records = []
    with open(file_path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("TransactionID"):
                continue
            records.append(line)
    return records

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    """

    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = []

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("TransactionID"):
                        continue
                    lines.append(line)
            return lines

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    print("Error: Unable to read file due to encoding issues.")
    return []
