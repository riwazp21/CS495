#Author: Riwaz Poudel
#Input of the code: csv file that has comment processes from commentCleaner.py
#Output of the code: a Csv file inside PecessesedComment directory. The csv file will be named the same as the passed file. The output csv file will have following columns: Title, URL, Author, Upvotes, Comments, Created UTC, Cleaned_Comment, and Expanded_Comment, VADER_Sentiment, and TextBlob_Sentiment.
#How to run this code: Use the command line argument. The file name/path should be passed as the first argument. For example: python sentiment.py comment_democrats.csv will run sentiment analysis on all the comments inside the file and put it in the directory
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import sys
import os

def analyze_sentiment(comment):
    # VADER Sentiment Analysis
    comment = str(comment)
    vader_analyzer = SentimentIntensityAnalyzer()
    vader_score = vader_analyzer.polarity_scores(comment)['compound']

    # TextBlob Sentiment Analysis
    textblob_score = TextBlob(comment).sentiment.polarity

    return vader_score, textblob_score

def conduct_sentiment_analysis(input_csv_path, output_csv_folder):
    # Read CSV file into a DataFrame
    df = pd.read_csv(input_csv_path, encoding='utf-8')

    # Apply sentiment analysis function to each row
    df[['VADER_Sentiment', 'TextBlob_Sentiment']] = df['Expanded_Comment'].apply(analyze_sentiment).apply(pd.Series)

    # Extract the filename (excluding directory and extension) to use as the output filename
    output_filename = os.path.splitext(os.path.basename(input_csv_path))[0]

    # Save the DataFrame with sentiment scores to a new CSV file
    output_csv_path = os.path.join(output_csv_folder, f"{output_filename}.csv")
    df.to_csv(output_csv_path, index=False)

    print(f'Sentiment analysis completed. Results saved to {output_csv_path}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_csv_file.csv")
        sys.exit(1)

    input_csv_file = sys.argv[1]
    output_csv_folder = "/Users/riwazp/Desktop/PolicingSentiments/ProcessedComment"
    os.makedirs(output_csv_folder, exist_ok=True)

    conduct_sentiment_analysis(input_csv_file, output_csv_folder)

