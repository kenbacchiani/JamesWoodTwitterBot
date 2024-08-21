import tweepy
from pybaseball import playerid_lookup, statcast_batter
from datetime import datetime

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

mlbam_id = playerid_lookup("WOOD","JAMES").iloc[0]['key_mlbam']

today = datetime.today()
start_of_month = today.replace(day=1).strftime('%Y-%m-%d')
end_of_month = today.strftime('%Y-%m-%d')
at_bats = statcast_batter(start_of_month, end_of_month, player_id=mlbam_id)
outcome_events = [
    "single", "double", "triple", "home_run", "strikeout", 
    "walk", "hit_by_pitch", "grounded_into_double_play", 
    "field_out", "force_out", "sac_fly", "sac_bunt"
]
outcome_count = {event: 0 for event in outcome_events}
total_at_bats = 0
for index, at_bat in at_bats.iterrows():
    event = at_bat['events']
    if event in outcome_events:
        outcome_count[event] += 1
        total_at_bats += 1
if total_at_bats > 0:
    recap = f"James Woods Monthly Recap ({start_of_month} to {end_of_month}):\n"
    recap += f"Total At-Bats: {total_at_bats}\n"
    for event, count in outcome_count.items():
        if count > 0:
            recap += f"{event.replace('_', ' ').capitalize()}: {count}\n"
    client.create_tweet(text=recap)
    print(f"Tweeted: {recap}")
else:
    print(f"No at-bats found for {player_first_name} {player_name} this month.")
