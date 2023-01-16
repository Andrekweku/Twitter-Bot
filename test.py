import gspread
from twitter import *


consumer_key = "eHPKezxc1UKHOcn9s520MiPJB"
consumer_secret = "nVhkh9xEJQVLmpaV8IOPQ4w1Tj9v2xTmiX8ZZvmrmXsHVOpg6x"
token = "1530015028631445505-YLnB5n92Sxb9bjc3AsvVdueZ8ZmpWW"
token_secret = "XbJzvRmgwl5lcDJFhbWwFmEn0rra6fVI1OusyBUatKF4k"

def test(event=None, context=None):

    gc = gspread.service_account('credentials.json')

    t = Twitter(
        auth=OAuth(token, token_secret, consumer_key, consumer_secret))

    # Open a sheet from a spreadsheet in one go
    wks = gc.open("kweku").sheet1

    # # Get next tweet
    next_tweet = wks.acell('A2').value

    # Update your status
    t.statuses.update(
        status=next_tweet)

    # #Delete current cell and move to next cell
    wks.delete_rows(2)

test()
