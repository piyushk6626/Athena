import pandas as pd
import re

def clean_csv(input_file, output_file):
    # Load CSV
    df = pd.read_csv(input_file)

    # Ensure required columns exist
    required_columns = ['Name', 'Star', 'Number', 'URL']
    df = df.dropna(subset=required_columns)

    # Function to clean the 'Number' column
    def clean_number(value):
        if pd.isna(value):
            return None
        value = str(value).replace(',', '')  # Remove commas

        # Convert 'K)' notation (e.g., 1.1K) to numerical format
        match = re.search(r'([\d.]+)K\)', value)
        if match:
            return int(float(match.group(1)) * 1000)

        try:
            return abs(int(value))  # Convert to int safely
        except ValueError:
            return None  # Handle unexpected formats gracefully

    # Apply cleaning to 'Number' column
    df['Number'] = df['Number'].apply(clean_number)

    # Save the cleaned CSV
    df.to_csv(output_file, index=False)

# Example usage
clean_csv('DP.csv', 'DP.csv')
import pandas as pd 
def process_csv(file_path, output_file):
    # Load CSV
    df = pd.read_csv(file_path)


    # Remove duplicates based on URL OR (Name, Number, Star)
    df = df.drop_duplicates(subset=["URL"]).drop_duplicates(subset=["Name", "Number", "Star"])

    # Save to a new CSV file
    df.to_csv(output_file, index=False)

    print(f"Processed file saved as: {output_file}")
    
process_csv("DP.csv","DP.csv")