from twikit import Client
import json
import pandas as pd
from dotenv import load_dotenv
import os
import time
import shutil

# Initialize the client
client = Client('en-US')  # Language code used in API request

# Load the .env file from the 'Credentials' folder
load_dotenv(dotenv_path=os.path.join('Credentials', 'twitter.env'))

# Load the environment variables for authentication
AUTH_INFO_1 = os.getenv('AUTH_INFO_1')
AUTH_INFO_2 = os.getenv('AUTH_INFO_2')
PASSWORD = os.getenv('PASSWORD')

# Specify path for cookies file in the 'Credentials' folder
cookies_path = os.path.join('Credentials', 'cookies.json')
old_cookies_path = os.path.join('Credentials', 'old-cookies.json')

# Check if cookies file exists and is non-empty
if os.path.exists(cookies_path) and os.path.getsize(cookies_path) > 0:
    try:
        # Try to load the cookies
        client.load_cookies(path=cookies_path)
        print("Using cookies to authenticate.")
        
        # Check if the cookies are still valid by making a quick API call (e.g., fetching a user profile)
        user = client.get_user_by_screen_name('zelenskyyua')  # You can change this to any valid username
        print(f"Successfully authenticated using cookies for user: {user.screen_name}")

    except Exception as e:
        # If loading cookies fails or an error occurs, perform a login again
        print(f"Error using cookies: {e}")
        print("Logging in again to refresh cookies...")
        
        # Rename old cookies to 'old-cookies.json' before saving new ones
        if os.path.exists(cookies_path):
            shutil.move(cookies_path, old_cookies_path)  # Rename the current cookies to old-cookies.json
            print("Old cookies renamed to old-cookies.json")
        
        client.login(auth_info_1=AUTH_INFO_1, auth_info_2=AUTH_INFO_2, password=PASSWORD)
        client.save_cookies(cookies_path)
        print("New cookies saved after successful login.")
else:
    # If no cookies or the file is empty, login and save cookies
    print("No valid cookies found. Logging in...")
    client.login(auth_info_1=AUTH_INFO_1, auth_info_2=AUTH_INFO_2, password=PASSWORD)
    client.save_cookies(cookies_path)
    print("New cookies saved after successful login.")

# List of screen names whose tweets to fetch
screen_names = ['zelenskyyua', 'AmbujaCementACL', 'elonmusk']  # Add more screen names as needed

# Initialize a list to store the tweets data
tweets_to_store = []

# Loop through each screen name and fetch the tweets
for screen_name in screen_names:
    user = client.get_user_by_screen_name(screen_name)
    tweets = user.get_tweets('Tweets', count=5)  # You can adjust the count as needed

    for tweet in tweets:
        tweets_to_store.append({
            'screen_name': screen_name,
            'created_at': tweet.created_at,
            'favorite_count': tweet.favorite_count,
            'full_text': tweet.full_text,
        })

# Create the 'outputs' folder if it doesn't exist
output_folder = 'outputs'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define the output JSON file path inside the 'outputs' folder
output_file = os.path.join(output_folder, 'twitter_outputs.json')

# Save the output data to a JSON file inside the 'outputs' folder
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(tweets_to_store, f, ensure_ascii=False, indent=4)

# Print success message and file path
print(f"All tweets saved to file: {output_file}")
print(f"Total tweets fetched: {len(tweets_to_store)}")
