# Twitter-Bot
Twitter Bot that sends tweets from Google spread sheet cells on a regular basis.

The bot uses a Google Spreadsheet to get the content, and tweet it. 


## Installation

To install it, clone the repository and create a virtual environment:

```
python -m venv venv
```

Activate the env:

```
venv\scripts\activate
```

Then install all the libraries:

```
pip install -r requirements.txt
```

Done!

## Configuring it

You will need several configuration items:

* Twitter consumer key
* Twitter consumer secret key
* Twitter token code
* Twitter token secret
* JSON oauth file name for Google Drive

Once you have all that information, copy the settings.py.tmpl to settings.py and fill it.

## Google Spreadsheet

Save ass your tweets in your spread sheet beginning with the second cell. Leave the first cell empyt. The bot will hand it.

## Tweeting by hand

If you want to test it, you only have to run the following command:

```
python tweet.py
```

If everything goes well, you will see the tweet posted in your account.

## Tweeting at given times

As this bot is a script, you can use Cron to tweet 5 times a day, once a week, etc. 
I set it up with AWS; but you can use whichever one you're comfortable with.

## Adding new content

If you want to add new content, all you have to do is to open the Google Spreadsheet and
add a new row with each tweet per row.
