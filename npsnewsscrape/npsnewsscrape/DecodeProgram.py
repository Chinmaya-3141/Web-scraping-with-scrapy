#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 10:01:58 2025

@author: chinmaya
"""

import sqlite3
import time
from googlenewsdecoder import gnewsdecoder
import logging

# Set up logging
logging.basicConfig(level=logging.WARNING)

# Path to original and new databases
original_db_path = '/home/chinmaya/Programming/npsnewsscrape/news_combined.db'  # Path to your original database
new_db_path = '/home/chinmaya/Programming/npsnewsscrape/news_decoded.db'  # Path to the new database with decoded URLs

# Step 1: Connect to the original database
original_connection = sqlite3.connect(original_db_path)
original_cursor = original_connection.cursor()

# Step 2: Create a new database (this will replicate the original structure)
new_connection = sqlite3.connect(new_db_path)
new_cursor = new_connection.cursor()

# Step 3: Get the structure of the original table
original_cursor.execute('SELECT sql FROM sqlite_master WHERE type="table" AND name="news"')
create_table_sql = original_cursor.fetchone()[0]  # Get the CREATE TABLE statement

# Step 4: Create the same table in the new database, with the new column
# Add the 'decoded_source_url' column to the table
create_table_sql_with_new_column = create_table_sql.replace(
    ')',
    ', decoded_source_url TEXT)'
)
new_cursor.execute(create_table_sql_with_new_column)
new_connection.commit()

# Step 5: Fetch all source URLs from the original database
original_cursor.execute("SELECT transaction_id, link FROM news WHERE link IS NOT NULL")
source_urls = original_cursor.fetchall()  # This will return a list of tuples (transaction_id, link)

# Step 6: Decode each URL and insert the results into the new database
interval_time = 1  # Interval between requests to avoid rate-limiting

for transaction_id, source_url in source_urls:
    try:
        print(f"Processing URL: {source_url}")

        # Decode the URL using gnewsdecoder
        decoded_url_response = gnewsdecoder(source_url, interval=interval_time)
        
        if decoded_url_response.get("status"):
            decoded_url = decoded_url_response["decoded_url"]
            print(f"Decoded URL: {decoded_url}")

            # Step 7: Insert the data into the new database with the decoded URL
            new_cursor.execute('''
                INSERT INTO news (transaction_id, search_term, country_name, country_language, 
                                  news_source, headline, description, article_datetime, 
                                  link, ambuja_kawach_count, ambuja_cool_walls_count, 
                                  ambuja_compocem_count, ambuja_plus_count, decoded_source_url)
                SELECT transaction_id, search_term, country_name, country_language, 
                       news_source, headline, description, article_datetime, 
                       link, ambuja_kawach_count, ambuja_cool_walls_count, 
                       ambuja_compocem_count, ambuja_plus_count, ?
                FROM news WHERE transaction_id = ?
            ''', (decoded_url, transaction_id))

            new_connection.commit()

        else:
            print(f"Error decoding URL: {decoded_url_response['message']}")
    
    except Exception as e:
        print(f"Error occurred while processing {source_url}: {e}")

    # Adding delay between requests
    time.sleep(interval_time)

# Step 8: Close the connections
original_connection.close()
new_connection.close()

print(f"Database with decoded URLs saved as '{new_db_path}'")
