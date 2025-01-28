from google_play_scraper import search, reviews_all, Sort
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load the .env file from the 'config' folder with the name 'google_play_config.env'
load_dotenv(dotenv_path=os.path.join('Config', 'google_play_config.env'))

# Custom function to handle datetime objects
def datetime_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()  # Convert datetime object to ISO 8601 string

# Function to search for app ID based on app name
def get_app_id(app_name):
    print(f"Searching for app: {app_name}")
    try:
        result = search(app_name, country='in', n_hits=30)  # Search for the app with the given name
        print(result)
        for re in result:
            print(re['title'])
        if len(result) > 0:
            app_id = result[0]['appId']
            print(f"App found: {app_name}")
            print(f"App ID: {app_id}")
            return app_id
        else:
            print(f"No app found with the name '{app_name}'")
            return None
    except Exception as e:
        print(f"Error searching for app '{app_name}': {e}")
        return None

# Function to scrape reviews based on app ID
def scrape_reviews(app_id, app_name, stakeholder, all_reviews):
    print(f"Starting to scrape reviews for app: {app_id}")
    try:
        review_data = reviews_all(
            app_id,
            sleep_milliseconds=200,
            lang='en',
            country='in',
            sort=Sort.NEWEST,
        )
        # Add the app name and stakeholder to each review in the review data
        for review in review_data:
            review['app_name'] = app_name
            review['stakeholder'] = stakeholder
            all_reviews.append(review)  # Append the modified review to the all_reviews list
        print(f"Scraping completed. Total reviews fetched: {len(review_data)}")
    except Exception as e:
        print(f"Failed to complete the scraping process for app '{app_id}': {e}")

# Main function to handle the search and scraping for multiple apps
def main():
    # Load the app names and stakeholders from the .env file
    app_data_str = os.getenv('APP_NAMES_AND_STAKEHOLDERS')
    
    # Parse the string into a list of dictionaries
    app_names = []
    for item in app_data_str.split(','):
        app_name, stakeholder = item.split('|')
        app_names.append({'name': app_name, 'stakeholder': stakeholder})

    # Create the outputs folder if it doesn't exist
    output_folder = os.path.join(os.getcwd(), 'Outputs')  # Using current working directory
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define the output file path in the 'outputs' folder
    output_file = os.path.join(output_folder, 'reviews.json')
    all_reviews = []  # Initialize an empty list to hold all reviews

    # Iterate over the apps and scrape reviews
    for app in app_names:
        app_name = app['name']
        stakeholder = app['stakeholder']
        app_id = get_app_id(app_name)
        if app_id:
            scrape_reviews(app_id, app_name, stakeholder, all_reviews)

    # Save all reviews to a JSON file inside the 'outputs' folder
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_reviews, f, ensure_ascii=False, indent=2, default=datetime_converter)

    print(f"All reviews saved to file: {output_file}")
    print(len(all_reviews))

if __name__ == "__main__":
    main()



# from google_play_scraper import search, reviews_all, Sort
# import json
# from datetime import datetime

# # Custom function to handle datetime objects
# def datetime_converter(o):
#     if isinstance(o, datetime):
#         return o.isoformat()  # Convert datetime object to ISO 8601 string

# # Function to search for app ID based on app name
# def get_app_id(app_name):
#     print(f"Searching for app: {app_name}")
#     try:
#         result = search(app_name,country='in',n_hits=30)  # Search for the app with the given name
#         print(result)

#         for re in result:

#             print(re['title'])

#         if len(result) > 0:

#             app_id = result[0]['appId']

#             print(f"App found: {app_name}")

#             print(f"App ID: {app_id}")

#             return app_id

#         else:

#             print(f"No app found with the name '{app_name}'")

#             return None

#     except Exception as e:

#         print(f"Error searching for app '{app_name}': {e}")

#         return None

 

# # Function to scrape reviews based on app ID

# def scrape_reviews(app_id, app_name, stakeholder, all_reviews):

#     print(f"Starting to scrape reviews for app: {app_id}")

 

#     try:

#         review_data = reviews_all(

#             app_id,

#             sleep_milliseconds=200,

#             lang='en',

#             country='in',

#             sort=Sort.NEWEST,

#         )

 

#         # Add the app name and stakeholder to each review in the review data

#         for review in review_data:

#             review['app_name'] = app_name

#             review['stakeholder'] = stakeholder

#             all_reviews.append(review)  # Append the modified review to the all_reviews list

 

#         print(f"Scraping completed. Total reviews fetched: {len(review_data)}")

#     except Exception as e:

#         print(f"Failed to complete the scraping process for app '{app_id}': {e}")

 

# # Main function to handle the search and scraping for multiple apps

# def main():

#     app_names = [

#                     {'name': 'ACC Cement Connect', 'stakeholder': 'Dealers'},  # Main app for ACC Cement

#                     {'name': 'Ambuja Cement Connect', 'stakeholder': 'Dealers'},  # Main app for Ambuja Cement

#                     {'name': 'Rewards Connect - Adani', 'stakeholder': 'Dealers'},  # Rewards hub, loyalty program, Adani Cement

#                     {'name': 'ACL AASMAN', 'stakeholder': 'Dealers'},  # Ambuja rewards app

#                     {'name': 'WeCare - Adani Cement', 'stakeholder': 'Employees'},  # Employee engagement app

#                     {'name': 'Lakshya-E-Aasmaan', 'stakeholder': 'Employees'},  # App for ACC & Ambuja members

#                     {'name': 'Field Force Assessment - Adani', 'stakeholder': 'Employees'},  # Attendance of field force

#                     {'name': 'WBI-ACL', 'stakeholder': 'Employees'},  # Walk-by inspection for Ambuja Cement

#                     {'name': 'WBI-ACC', 'stakeholder': 'Employees'},  # Walk-by inspection for ACC Cement

#                     {'name': 'Adani Foundations', 'stakeholder': 'Employees'},  # Learning material for Adani Foundation initiatives

#                 ]  # Add app names and stakeholders to search for

   

#     output_file = 'reviews.json'

#     all_reviews = []  # Initialize an empty list to hold all reviews

 

#     for app in app_names:

#         app_name = app['name']

#         stakeholder = app['stakeholder']

#         app_id = get_app_id(app_name)

#         if app_id:

#             scrape_reviews(app_id, app_name, stakeholder, all_reviews)

 

#     # Save all reviews to a JSON file

#     with open(output_file, 'w', encoding='utf-8') as f:

#         json.dump(all_reviews, f, ensure_ascii=False, indent=2, default=datetime_converter)

 

#     print(f"All reviews saved to file: {output_file}")

#     print(len(all_reviews))

 

# if __name__ == "__main__":

#     main()

 

#Code without stakeholders tag

 

# from google_play_scraper import search, reviews_all, Sort

# import json

# from datetime import datetime

 

# # Custom function to handle datetime objects

# def datetime_converter(o):

#     if isinstance(o, datetime):

#         return o.isoformat()  # Convert datetime object to ISO 8601 string

 

# # Function to search for app ID based on app name

# def get_app_id(app_name):

#     print(f"Searching for app: {app_name}")

#     try:

#         result = search(app_name, country='in', n_hits=30)  # Search for the app with the given name

#         if len(result) > 0:

#             app_id = result[0]['appId']

#             print(f"App found: {app_name}")

#             print(f"App ID: {app_id}")

#             return app_id

#         else:

#             print(f"No app found with the name '{app_name}'")

#             return None

#     except Exception as e:

#         print(f"Error searching for app '{app_name}': {e}")

#         return None

 

# # Function to scrape reviews based on app ID

# def scrape_reviews(app_id, app_name, all_reviews):

#     print(f"Starting to scrape reviews for app: {app_id}")

 

#     try:

#         review_data = reviews_all(

#             app_id,

#             sleep_milliseconds=0,

#             lang='en',

#             country='in',

#             sort=Sort.NEWEST,

#         )

 

#         # Add the app name to each review in the review data

#         for review in review_data:

#             review['app_name'] = app_name

#             all_reviews.append(review)  # Append the modified review to the all_reviews list

 

#         print(f"Scraping completed. Total reviews fetched: {len(review_data)}")

#     except Exception as e:

#         print(f"Failed to complete the scraping process for app '{app_id}': {e}")

 

# # Main function to handle the search and scraping for multiple apps

# def main():

#     app_names = [

#         'ACC Cement Connect',  # Main app for ACC Cement

#         'Ambuja Cement Connect',  # Main app for Ambuja Cement

#         'Rewards Connect - Adani',  # Rewards hub, loyalty program, Adani Cement

#         'ACL AASMAN',  # Ambuja rewards app

#         'WeCare - Adani Cement',  # Employee engagement app

#         'Lakshya-E-Aasmaan',  # App for ACC & Ambuja members

#         'Field Force Assessment - Adani',  # Attendance of field force

#         'WBI-ACL',  # Walk-by inspection for Ambuja Cement

#         'WBI-ACC',  # Walk-by inspection for ACC Cement

#         'Adani Foundations',  # Learning material for Adani Foundation initiatives

#     ]  # Add app names to search for

 

#     output_file = 'reviews.json'

#     all_reviews = []  # Initialize an empty list to hold all reviews

 

#     for app_name in app_names:

#         app_id = get_app_id(app_name)

#         if app_id:

#             scrape_reviews(app_id, app_name, all_reviews)

 

#     # Save all reviews to a JSON file

#     with open(output_file, 'w', encoding='utf-8') as f:

#         json.dump(all_reviews, f, ensure_ascii=False, indent=2, default=datetime_converter)

 

#     print(f"All reviews saved to file: {output_file}")

 

# if __name__ == "__main__":

#     main()
