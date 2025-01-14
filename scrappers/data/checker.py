import pandas as pd
import json

def check():
    data = {}
    jsonf = {}
    df = pd.read_csv('./scrappers/data/combined.csv', usecols=['url', 'page', 'category', 'location'])
    for url, page, category in zip(df['url'], df['page'], df['category']):
        key = category
        if curr_page := data.get(key):
            if page > curr_page:
                data[key] = page
                jsonf[key] = url
        else:
            data[key] = page
            jsonf[key] = url
    missing = pd.DataFrame(list(jsonf.items()), columns=['category_location', 'page'])
    missing.to_json('./missing.json', orient='records', indent=4)
    print(data)

def combine():
    # Read both CSV files
    df1 = pd.read_csv('./scrappers/data/page.csv')
    df2 = pd.read_csv('./scrappers/data/combined.csv')

    # Concatenate them vertically
    combined_df = pd.concat([df1, df2], ignore_index=True)

    # Save to a new CSV file
    combined_df.to_csv('combined.csv', index=False)

    print("Files have been successfully concatenated into 'combined.csv'")


combine()

