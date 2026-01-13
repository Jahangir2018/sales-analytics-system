def read_sales_file(file_path):
    records = []
    with open(file_path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("TransactionID"):
                continue
            records.append(line)
    return records
