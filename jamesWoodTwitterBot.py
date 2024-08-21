from pybaseball import playerid_lookup, statcast_batter
import pandas as pd
from datetime import datetime, timedelta
import tweepy

API_KEY = ""
API_SECRET_KEY = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

today = datetime.today()
date_string = today.strftime('%Y-%m-%d')
james_wood_id = playerid_lookup("WOOD","JAMES").iloc[0]['key_mlbam']
at_bats = statcast_batter(start_dt=date_string, end_dt=date_string, player_id=james_wood_id)
at_bats = at_bats.dropna(subset=['events'])
if at_bats.empty:
    tweet = f"James Wood did not have any at-bats on {today.strftime('%B %d, %Y')}."
    client.create_tweet(text=tweet)
    print(tweet)
else:
    at_bats = at_bats.sort_values(by='inning')
    tweet_content = f"James Wood's at-bats on {today.strftime('%B %d, %Y')}:\n"
    for index, row in at_bats.iterrows():
        inning = row['inning']
        result = row['events']
        exit_velocity = row['launch_speed']
        if pd.notna(exit_velocity):
            tweet_content += (f"Inning: {inning}, Result: {result}, "
                              f"Exit Velocity: {exit_velocity} MPH\n")
        else:
            tweet_content += (f"Inning: {inning}, Result: {result}\n")
    if len(tweet_content) > 280:
        tweet_content = tweet_content[:277] + "..." 
    client.create_tweet(text=tweet_content)