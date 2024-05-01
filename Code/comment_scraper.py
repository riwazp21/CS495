#Author: Riwaz Poudel
#Input of the code: csv file that has the URL data built from post_scraper.py
#Output of the code: a Csv file with scraped comments inside the CommentData directory. If the inpu is thatsinsane then the output file will be stored as comment_thatsinsane.csv. The comment file will have the following columns: Title, Comment, Author, Created UTC.
#How to run this code: Use the command line argument. The filename name should be passed as the first argument. For example: python comment_scraper.py thatsinsane.csv will scrape all the comments on the posts inside that certain file 

import praw
import csv
import pandas as pd
import os
from datetime import datetime
import time  # Import the time module

# Reddit API credentials
client_id = '' #Redacted because of security reasons to put on GitHub. A unique user needs to use their own client id
client_secret = '' #Redacted because of security reasons to put on GitHub. A unique user needs to use their own client id
user_agent = '' #Redacted because of security reasons to put on GitHub. A unique user needs to use their own client id

# Authenticate with Reddit
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

def scrape_comments_and_save(csv_file_path):
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Create a folder for storing comment data
    comment_data_folder = "CommentData"
    os.makedirs(comment_data_folder, exist_ok=True)

    # Create an empty DataFrame to store all comments
    all_comments_df = pd.DataFrame(columns=['Title', 'Comment', 'Author', 'Created UTC'])

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        try:
            # Fetch submission using Reddit URL
            submission = reddit.submission(url=row['URL'])
            
            # Introduce rate limiting handling
            while True:
                try:
                    submission.comments.replace_more(limit=None)
                    break  # Exit the loop if successful
                except praw.exceptions.RedditAPIException as e:
                    if 'ratelimit' in str(e).lower():
                        print(f'Rate limit reached. Pausing for 5 seconds...')
                        time.sleep(60)  # Pause for 5 seconds before retrying
                    else:
                        raise  # Re-raise the exception if it's not a rate limit issue
            
            # Collect comments and replies
            comments_data = []
            comment_queue = submission.comments[:] 

            while comment_queue:
                comment = comment_queue.pop(0)
                comments_data.append({
                    'Title': row['Title'],
                    'Comment': comment.body,
                    'Author': comment.author.name if comment.author else 'Unknown',
                    'Created UTC': datetime.utcfromtimestamp(comment.created_utc).strftime('%m/%d/%Y %H:%M:%S')
                })
                comment_queue.extend(comment.replies)

            # Append comments to the main DataFrame
            all_comments_df = pd.concat([all_comments_df, pd.DataFrame(comments_data)], ignore_index=True)

            print(f'Comments and replies scraped from {row["URL"]}')

        except Exception as e:
            print(f'Error processing {row["URL"]}: {e}')

    # Save all comments to a single CSV file
    output_file_name = f"Comment_{os.path.splitext(os.path.basename(csv_file_path))[0]}.csv"
    output_file_path = os.path.join(comment_data_folder, output_file_name)
    all_comments_df.to_csv(output_file_path, index=False)

    print(f'All comments and replies saved to {output_file_path}')

# Example usage:
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py input_csv_file.csv")
        sys.exit(1)

    input_csv_file = sys.argv[1]
    scrape_comments_and_save(input_csv_file)



