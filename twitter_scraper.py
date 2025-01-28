import asyncio
import os
import json
from twikit import Client
from dotenv import load_dotenv

# Load the .env file from the 'Credentials' folder
load_dotenv(dotenv_path=os.path.join('Credentials', 'twitter.env'))

# Load the environment variables for authentication
USERNAME = os.getenv('AUTH_INFO_1')
EMAIL = os.getenv('AUTH_INFO_2')
PASSWORD = os.getenv('PASSWORD')

# Path to the cookies file
cookies_path = os.path.join('Credentials', 'cookies.json')

# Path to the 'Outputs' folder
output_folder = 'Outputs'

client = Client('en-US')  # Language code used in API request

async def main(search_term):
    # Try to load cookies first
    if os.path.exists(cookies_path):
        client.load_cookies(cookies_path)  # Removed await here
        print("Cookies loaded successfully!")
    else:
        # If no cookies exist, login and save cookies
        await client.login(
            auth_info_1=USERNAME,
            auth_info_2=EMAIL,
            password=PASSWORD
        )
        client.save_cookies(cookies_path)  # Removed await here
        print("Logged in and cookies saved successfully!")

    # Fetch tweets
    tweets = await client.search_tweet(search_term, 'Latest')

    # Prepare the data for saving
    tweet_data = []
    for tweet in tweets:
        tweet_data.append({
            'user': tweet.user.name,
            'text': tweet.text,
            'created_at': tweet.created_at  # Just use the string directly
        })
    
    # Ensure the 'Outputs' folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Dynamic filename based on the search term
    output_file = os.path.join(output_folder, f'twitter_{search_term}.json')

    # Save the tweets data to a JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tweet_data, f, ensure_ascii=False, indent=4)

    print(f"Tweets saved to {output_file}")

# Example usage with the search term 'Adani'
# You can pass the search term dynamically based on your needs
search_term = 'Adani'

# Check if there's an existing event loop
try:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(main(search_term))
    else:
        asyncio.run(main(search_term))
except RuntimeError as e:
    if "There is no current event loop" in str(e):
        asyncio.run(main(search_term))