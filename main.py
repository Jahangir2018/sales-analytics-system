from utils.file_handler import read_sales_file
from utils.data_processor import clean_and_process_data

DATA_PATH = "data/sales_data.txt"

def main():
    raw = read_sales_file(DATA_PATH)
    clean_and_process_data(raw)

if __name__ == "__main__":
    main()

