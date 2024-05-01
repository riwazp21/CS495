#Author: Riwaz Poudel
#Input of the code: csv file that has comment processes from comment_scraper.py
#Output of the code: a Csv file inside PecessesedComment directory. The csv file will be named the same as the passed file. The output csv file will have following columns: Title, URL, Author, Upvotes, Comments, Created UTC, Cleaned_Comment, and Expanded_Comment.
#How to run this code: Use the command line argument. The file name/apth should be passed as the first argument. For example: python commentCleaner.py comment_democrats.csv will clean all the comments inside the file and put it in the new directory 

import pandas as pd
import sys
import re
import os
from urllib.parse import urlparse
import contractions

def clean_comment(comment):
    comment = str(comment)
    # Remove [deleted] comments and comments with URLs
    if comment.lower() == '[deleted]' or comment.lower() == '[removed]' or re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', comment):
        return None

    # Lowercase everything
    comment = comment.lower()

    # Remove Äú and Äù
    comment = comment.replace('Äú', '').replace('Äù', '')

    # Remove special characters, symbols, and emojis
    comment = re.sub(r'[^\w\s]', '', comment)

    # Remove punctuation marks
    comment = re.sub(r'[^\w\s]', '', comment)

    # Remove numbers
    comment = re.sub(r'\d+', '', comment)
    if comment == '':
        return None

    # Remove extra spaces
    #comment = ' '.join(comment.split())
    #print("Cleanig comments\n")
    #print(comment)
    #print("\n")

    return comment

def expand_contractions(comment):
    # Add your own expansion rules if needed
    expanded_words = []
    for word in comment.split():
        expanded_words.append(contractions.fix(word))
    expanded_text = ' '.join(expanded_words)
    return expanded_text

def process_csv(input_csv_path, output_csv_path):
    # Read CSV file into a DataFrame

    df = pd.read_csv(input_csv_path)
    #print(input_csv_path)


    # Clean and process each comment
    df['Cleaned_Comment'] = df['Comment'].apply(clean_comment)
    #print(df['Cleaned_Comment'])

    df = df.dropna(subset=['Cleaned_Comment'])
    df['Expanded_Comment'] = df['Cleaned_Comment'].apply(expand_contractions)

    
    # Save the cleaned DataFrame to a new CSV file
    df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_csv_file.csv")
        sys.exit(1)

    input_csv_file = sys.argv[1]
    output_csv_file = f"/Users/riwazp/Desktop/PolicingSentiments/ProcessedComment/{os.path.basename(input_csv_file)}"
    process_csv(input_csv_file, output_csv_file)

