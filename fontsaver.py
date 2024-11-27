import pandas as pd
import sys

def convert_csv_to_excel(csv_path, excel_path):
    print("Starting conversion process...")
    
    try:
        # Read CSV with UTF-8 encoding
        df = pd.read_csv(csv_path, encoding='utf-8')
        print(f"Successfully loaded CSV with {len(df)} rows")
        
        # Try xlsxwriter as an alternative engine
        df.to_excel(excel_path, index=False, engine='xlsxwriter')
        print(f"Successfully saved to Excel: {excel_path}")
        
        # Display first few rows as a sample
        print("\nFirst 5 rows of data:")
        print(df.head())
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Installing required package...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "xlsxwriter"])
        
        # Try again after installation
        df.to_excel(excel_path, index=False, engine='xlsxwriter')
        print(f"Successfully saved to Excel: {excel_path}")

# Use your specific file paths
csv_file = '/Users/emmanuelcuyugan/Library/Mobile Documents/com~apple~CloudDocs/Desktop/sqp_dump/positivev2.csv'
excel_file = '/Users/emmanuelcuyugan/Library/Mobile Documents/com~apple~CloudDocs/Desktop/sqp_dump/positivev2.xlsx'

convert_csv_to_excel(csv_file, excel_file)