import gspread
from pytwitter import Api
from config import settings


def post_tweet(event=None, context=None):
    """
    Fetches the next tweet from a Google Sheet, posts it to Twitter,
    and updates the sheet by moving the tweet to the next empty row.

    Args:
        event (dict, optional): Event data, if triggered by an event. Defaults to None.
        context (dict, optional): Context data, if triggered by an event. Defaults to None.
    """

    # Authenticate with Google Sheets using a service account
    gc = gspread.service_account("credentials.json")

    # Authenticate with the Twitter API using credentials from settings
    api = Api(
        access_token=settings.access_token,
        access_secret=settings.access_secret,
        consumer_key=settings.consumer_key,
        consumer_secret=settings.consumer_secret,
    )

    # Open the Google Sheet named "kweku" and access the first sheet
    wks = gc.open("kweku").sheet1

    # Get the next tweet from cell A2
    next_tweet = wks.acell("A2").value
    print(f"Next tweet: {next_tweet}")

    # Post the tweet to Twitter
    api.create_tweet(text=next_tweet)

    # Find the next empty row in the sheet starting from row 2
    next_row = find_next_empty_row(wks, start_row=2)

    # Move the current tweet from A2 to the next empty row
    current_cell_value = wks.acell("A2").value
    wks.update(f"A{next_row}", current_cell_value)

    # Delete the original row (row 2) after posting the tweet
    wks.delete_rows(2)


def find_next_empty_row(worksheet, start_row=1):
    """Takes a worksheet object and an optional start row and returns #
    the index of the next empty row in column A."""

    # Get all values in column A
    values = worksheet.col_values(1)
    print(len(values))

    # Iterate through the rows starting from the specified start_row
    for i in range(start_row - 1, len(values)):
        if not values[i]:  # Check if the cell is empty
            return i + 1  # Return the 1-based index of the empty row

    # If no empty cell is found, return the next row index
    return len(values) + 1

post_tweet()
