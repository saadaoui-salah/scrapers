import pandas as pd
from urllib.parse import urlparse

def get_unique_domains(csv_file, column_name):
    df = pd.read_csv(csv_file, usecols=[column_name])
    
    # Extract domains
    df[column_name] = df[column_name].dropna().apply(lambda url: urlparse(url).netloc)
    
    return df[column_name].nunique()

if __name__ == "__main__":
    csv_file = "./client-data/casino.csv"  # Change this to your CSV filename
    column_name = "website"  # Change this to your column name
    count = get_unique_domains(csv_file, column_name)
    print(f"Number of unique domains: {count}")