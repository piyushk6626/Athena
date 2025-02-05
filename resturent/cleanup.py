import pandas as pd
import re

def clean_csv(input_file, output_file):
    # Load CSV
    df = pd.read_csv(input_file)

    # Ensure required columns exist
    required_columns = ['Name', 'Star', 'Number', 'AREA']
    df = df.dropna(subset=required_columns)

    # Function to clean the 'Number' column
    def clean_number(value):
        if pd.isna(value):
            return None
        value = str(value)

        # Convert 'K)' notation (e.g., 1.1K) to numerical format
        match = re.search(r'([\d.]+)K\)', value)
        if match:
            return int(float(match.group(1)) * 1000)

        # Remove negative sign if present
        return abs(int(value))

    # Apply cleaning to 'Number' column
    df['Number'] = df['Number'].apply(clean_number)

    # Save the cleaned CSV
    df.to_csv(output_file, index=False)

# Example usage
clean_csv('Piyushkulkarni_input.csv', 'Piyushkulkarni_output.csv')
