#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 14:13:45 2025

@author: chinmaya
"""
import sqlite3
import random
import json
import os
from googlenewsdecoder import gnewsdecoder

def get_urls_from_db(db_path):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Fetch the link column from the news table
        cursor.execute("SELECT link FROM news")
        
        # Retrieve all the URLs and store them in a list
        urls = [row[0] for row in cursor.fetchall()]
        
        # Close the connection to the database
        conn.close()
        
        if not urls:
            print("No URLs found in the database.")
        return urls
    except sqlite3.Error as e:
        print(f"Error occurred while connecting to the database: {e}")
        return []

def process_urls(db_path, output_json_path):
    # Get URLs from the SQLite database
    source_urls = get_urls_from_db(db_path)
    
    if not source_urls:
        print("No URLs to process. Exiting.")
        return

    # Ensure the directory exists
    output_dir = os.path.dirname(output_json_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the JSON file for writing
    with open(output_json_path, 'w') as json_file:
        # Initialize the JSON file as an empty array
        json_file.write('[')
        
        first = True  # Flag to handle comma separation
        
        # Process each URL using a generator
        for result in generate_decoded_urls(source_urls):
            if not first:
                json_file.write(',\n')  # Add a comma for separation if it's not the first element
            json.dump(result, json_file, indent=4)
            first = False  # Mark that we have processed at least one URL

        # Close the JSON array at the end of the file
        json_file.write('\n]')

def generate_decoded_urls(urls):
    for url in urls:
        try:
            # Generate a random interval time between 1 and 3 seconds for each URL
            interval_time = random.uniform(1, 3)
            print(f"Using an interval time of: {interval_time:.2f} seconds for URL {url}")
            
            # Decode the URL using gnewsdecoder with the generated interval time
            decoded_url = gnewsdecoder(url,interval=interval_time)
            if decoded_url.get("status"):
                yield {"url": url, "decoded_url": decoded_url["decoded_url"]}
                print(f'\n {decoded_url["decoded_url"]}')
            else:
                yield {"url": url, "error": decoded_url["message"]}
                print(f'\n {decoded_url["message"]}')
        except Exception as e:
            yield {"url": url, "error": str(e)}

def main():
    # Hardcoded path to the SQLite database
    db_path = '/home/chinmaya/Programming/Web-scraping-with-scrapy/npsnewsscrape/news_combined.db'  # Change this to your database file path
    
    # Specify the path for the output JSON file
    output_json_path = 'Outputs/links_2.json'
    
    # Process URLs and immediately write to JSON using generator
    process_urls(db_path, output_json_path)
    print("Finished running")

if __name__ == "__main__":
    main()
