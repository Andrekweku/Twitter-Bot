import gspread
from twitter import *
from config import settings


consumer_key = settings.consumer_key
consumer_secret = settings.consumer_secret
token = settings.token
token_secret = settings.token_secret

def post_tweet(event=None, context=None):

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


post_tweet()