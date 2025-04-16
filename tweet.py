import json
import gspread
from pytwitter import Api
from config import settings


api = Api(
    access_token=settings.access_token,
    access_secret=settings.access_secret,
    consumer_key=settings.consumer_key,
    consumer_secret=settings.consumer_secret,
)

def load_saved_tweets_from_sheet(saved_tweets_sheet):
    """ Load the saved tweets from a Google Sheet. """
    # Get all values from column A of the saved tweets sheet
    saved_tweets = saved_tweets_sheet.col_values(1)
    return saved_tweets


def save_tweet_to_sheet(saved_tweets_sheet, tweet):
    """ Save a tweet to the saved tweets Google Sheet. """
    # Find the next empty row in the saved tweets sheet
    next_row = find_next_empty_row(saved_tweets_sheet, start_row=1)
    saved_tweets_sheet.update(f"A{next_row}", tweet)


def post_tweet():
    """ Fetches the next tweet from the original tweets Google Sheet, posts it to Twitter,
    and saves it to the saved tweets Google Sheet. """

    # Authenticate with Google Sheets using a service account
    gc = gspread.service_account("credentials.json")

    spreadsheet = gc.open("kweku")

    # Open sheets
    original_tweets_sheet = spreadsheet.sheet1
    saved_tweets_sheet = spreadsheet.worksheet("saved_tweets")

    # Load saved tweets from the saved tweets sheet
    saved_tweets = load_saved_tweets_from_sheet(saved_tweets_sheet)

    if len(saved_tweets) > 9:
        saved_tweets_sheet.delete_rows(1)

    # Iterate over rows in the original tweets sheet starting from A2
    row = 2
    while True:
        next_tweet = original_tweets_sheet.acell(f"A{row}").value

        if next_tweet not in saved_tweets:
            try:
                # Post the tweet
                # api.create_tweet(text=next_tweet)

                # Save the tweet to the saved tweets sheet
                save_tweet_to_sheet(saved_tweets_sheet, next_tweet)

                # Move the current tweet to the next empty row in the original tweets sheet
                next_row = find_next_empty_row(original_tweets_sheet, start_row=2)
                original_tweets_sheet.update(f"A{next_row}", next_tweet)

                # Delete the original row after posting the tweet
                original_tweets_sheet.delete_rows(row)
                break  # Exit the loop after posting the tweet
            except Exception as e:
                print(f"Error posting tweet: {e}")
                return
        row += 1  # Move to the next row if the tweet is already in saved_tweets


    # Find the next empty row in the sheet starting from row 2
    next_row = find_next_empty_row(original_tweets_sheet, start_row=2)

    # Move the current tweet from A2 to the next empty row
    current_cell_value = original_tweets_sheet.acell("A2").value
    original_tweets_sheet.update(f"A{next_row}", current_cell_value)

    # Delete the original row (row 2) after posting the tweet
    original_tweets_sheet.delete_rows(2)


def find_next_empty_row(worksheet, start_row=1):
    """Takes a worksheet object and an optional start row and returns #
    the index of the next empty row in column A."""

    # Get all values in column A
    values = worksheet.col_values(1)

    # Iterate through the rows starting from the specified start_row
    for i in range(start_row - 1, len(values)):
        if not values[i]:  # Check if the cell is empty
            return i + 1  # Return the 1-based index of the empty row

    # If no empty cell is found, return the next row index
    return len(values) + 1

post_tweet()
