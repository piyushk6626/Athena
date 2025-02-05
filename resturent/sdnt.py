import pandas as pd 
def process_csv(file_path, output_file):
    # Load CSV
    df = pd.read_csv(file_path)


    # Remove duplicates based on URL OR (Name, Number, Star)
    df = df.drop_duplicates(subset=["URL"]).drop_duplicates(subset=["Name", "Number", "Star"])

    # Save to a new CSV file
    df.to_csv(output_file, index=False)

    print(f"Processed file saved as: {output_file}")
    
process_csv("svnsdnt.csv","svnsdnt.csv")