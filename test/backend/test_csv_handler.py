import sys
import os
# Ensure the project root is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from io import StringIO
import pandas as pd
from backend.csv_handler import load_csv, validate_csv

def test_load_csv():
    # Create a simple CSV content as a string
    csv_content = "col1,col2\n1,2\n3,4"
    file_obj = StringIO(csv_content)
    
    try:
        df = load_csv(file_obj)
        print("Loaded DataFrame:")
        print(df)
    except Exception as e:
        print("Error in load_csv:", e)

def test_validate_csv():
    csv_content = "col1,col2\n1,2\n3,4"
    file_obj = StringIO(csv_content)
    
    try:
        valid = validate_csv(file_obj)
        print("CSV is valid:", valid)
    except Exception as e:
        print("CSV validation error:", e)

if __name__ == "__main__":
    print("Testing load_csv:")
    test_load_csv()
    print("\nTesting validate_csv:")
    test_validate_csv()
