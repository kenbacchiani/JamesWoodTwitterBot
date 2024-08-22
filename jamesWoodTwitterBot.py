from pybaseball import playerid_lookup, statcast_batter, playerid_reverse_lookup
import pandas as pd
from datetime import datetime, timedelta
import tweepy
import textwrap

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
yesterday = today - timedelta(days=1)
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
    tweet_content = f"James Wood's at-bats on {yesterday.strftime('%B %d, %Y')}:\n"
    for index, row in at_bats.iterrows():
        inning = row['inning']
        pitcherThrows = row['p_throws']
        pitcher_id = row['pitcher']
        pitcherDetails = playerid_reverse_lookup([pitcher_id])
        if not pitcherDetails.empty:
            pitcher_Firstname = playerid_reverse_lookup([pitcher_id]).iloc[0]['name_first']
            pitcher_Firstname = pitcher_Firstname[0].upper() + "."
            pitcher_Lastname = playerid_reverse_lookup([pitcher_id]).iloc[0]['name_last']
            pitcher_Lastname = pitcher_Lastname[0].upper() + pitcher_Lastname[1:]
        else:
            pitcher_Firstname = "Unknown"
            pitcher_Lastname = ""
        result = row['events']
        exit_velocity = row['launch_speed']
        if pd.notna(exit_velocity):
            tweet_content += (f"Inning: {inning} vs {pitcherThrows}HP {pitcher_Firstname} {pitcher_Lastname}, Result: {result}, "
                              f"EV: {exit_velocity} MPH\n")
        else:
            tweet_content += (f"Inning: {inning} vs {pitcherThrows}HP {pitcher_Firstname} {pitcher_Lastname}, Result: {result}\n")
    if len(tweet_content) >= 280:
        print(tweet_content)
        client.create_tweet(text=tweet_content[:280])
    else:
        print(tweet_content)
        client.create_tweet(text=tweet_content)

        
