#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 11:10:58 2025

@author: chinmaya
"""

import json
import sqlite3

def json_to_sqlite(json_file, db_file, table_name):
    # Open the JSON file and load the data
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Connect to the SQLite database (this will create the DB if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table with columns based on JSON keys
    if not data:  # Handle empty JSON
        print("The JSON file is empty.")
        return

    columns = ", ".join(data[0].keys())  # Get the keys of the first dictionary in the list
    placeholders = ", ".join(['?'] * len(data[0]))  # Placeholder for SQL insertion
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
    
    try:
        cursor.execute(create_table_query)
        print(f"Table '{table_name}' created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        return

    # Convert all values to UTF-8 encoded strings before inserting
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    for record in data:
        # Convert all values to UTF-8 encoded strings
        values = [str(value).encode('utf-8').decode('utf-8') if isinstance(value, list) else str(value) for value in record.values()]
        
        try:
            cursor.execute(insert_query, values)
        except sqlite3.Error as e:
            print(f"Error inserting record: {e}")
            continue

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print(f"Data successfully inserted into '{table_name}'.")

# Example usage
json_file = '/home/chinmaya/Programming/Web-scraping-with-scrapy/Outputs/ambuja.json'  # Replace with your JSON file
db_file = '/home/chinmaya/Programming/Web-scraping-with-scrapy/Outputs/ambuja.db'  # Replace with your desired database file
table_name = 'complete_data'  # Replace with your desired table name
json_to_sqlite(json_file, db_file, table_name)



# import json
# import sqlite3

# def json_to_sqlite(json_file, db_file, table_name):
#     # Open the JSON file and load the data
#     with open(json_file, 'r') as f:
#         data = json.load(f)

#     # Connect to the SQLite database (this will create the DB if it doesn't exist)
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()

#     # Create table with columns based on JSON keys
#     # Get the keys from the first dictionary
#     if not data:  # Handle empty JSON
#         print("The JSON file is empty.")
#         return

#     columns = ", ".join(data[0].keys())  # Get the keys of the first dictionary in the list
#     placeholders = ", ".join(['?'] * len(data[0]))  # Placeholder for SQL insertion
#     create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
    
#     try:
#         cursor.execute(create_table_query)
#         print(f"Table '{table_name}' created successfully.")
#     except sqlite3.Error as e:
#         print(f"Error creating table: {e}")
#         return

#     # Insert each record from the JSON data
#     insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
#     for record in data:
#         values = tuple(record.values())  # Extract values in order of the keys
#         try:
#             cursor.execute(insert_query, values)
#         except sqlite3.Error as e:
#             print(f"Error inserting record: {e}")
#             continue

#     # Commit the changes and close the connection
#     conn.commit()
#     conn.close()
#     print(f"Data successfully inserted into '{table_name}'.")

# # Example usage
# json_file = '/home/chinmaya/Programming/Web-scraping-with-scrapy/Outputs/ambuja.json'  # Replace with your JSON file
# db_file = 'database.db'  # Replace with your desired database file
# table_name = 'json_data'  # Replace with your desired table name
# json_to_sqlite(json_file, db_file, table_name)



# import sqlite3
# import ijson  # For streaming JSON parsing
# import json  # For serializing lists
# import os  # To check and create directories if needed

# # Function to ensure that the directory for the DB exists
# def create_directory_if_needed(db_path):
#     directory = os.path.dirname(db_path)
#     if not os.path.exists(directory):
#         os.makedirs(directory)

# # Function to create the SQLite table
# def create_table():
#     db_path = '/home/chinmaya/Programming/Web-scraping-with-scrapy/Outputs/ambuja_test.db'  # Replace this with your desired path to the DB

#     # Ensure the directory exists
#     create_directory_if_needed(db_path)
    
#     # Connect to the SQLite database (this will create it if it doesn't exist)
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # Create the table if it doesn't already exist
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS articles (
#             transaction_id TEXT,
#             article_datetime TEXT,
#             search_term TEXT,
#             country_name TEXT,
#             country_language TEXT,
#             news_source TEXT,
#             authors TEXT,
#             headline TEXT,
#             description TEXT,
#             article_body TEXT,
#             source_link TEXT,
#             keywords TEXT,
#             tags TEXT,
#             article_images TEXT,
#             all_images TEXT,
#             article_metadata TEXT,
#             full_html TEXT
#         )
#     ''')

#     # Commit changes and close the connection
#     conn.commit()
#     conn.close()

# # Function to process JSON and insert data into SQLite
# def process_json_to_sqlite(json_file):
#     # Connect to the SQLite database
#     conn = sqlite3.connect('/home/chinmaya/Programming/Web-scraping-with-scrapy/Outputs/ambuja_test.db')
#     cursor = conn.cursor()

#     # Open the JSON file and process it in chunks
#     with open(json_file, 'r') as f:
#         # Initialize the streaming JSON parser
#         objects = ijson.items(f, 'item')  # 'item' is the key where data starts in the JSON
        
#         # Insert data into SQLite in chunks
#         for obj in objects:
#             # Serialize list fields into JSON strings
#             authors = json.dumps(obj.get('authors', []))  # Default to empty list if authors is missing
#             article_images = json.dumps(obj.get('article_images', []))
#             all_images = json.dumps(obj.get('all_images', []))
#             tags = json.dumps(obj.get('tags', []))  # Serialize other lists into JSON strings
#             keywords = json.dumps(obj.get('keywords', []))  # Serialize the keywords list into a JSON string

#             # Combine all fields into a tuple for insertion (excluding 'id' column as it's auto-incremented)
#             values = (
#                 obj.get('transaction_id'),
#                 obj.get('article_datetime'),
#                 obj.get('search_term'),
#                 obj.get('country_name'),
#                 obj.get('country_language'),
#                 obj.get('news_source'),
#                 authors,  # JSON serialized list
#                 obj.get('headline'),
#                 obj.get('description'),
#                 obj.get('article_body'),
#                 obj.get('source_link'),
#                 keywords,  # JSON serialized list for keywords
#                 tags,  # JSON serialized list
#                 article_images,  # JSON serialized list
#                 all_images,  # JSON serialized list
#                 obj.get('article_metadata'),
#                 obj.get('full_html')
#             )

#             # Insert data into SQLite table (Note: we do not include 'id' as it's auto-incremented)
#             cursor.execute('''
#                 INSERT INTO articles (
#                     transaction_id, article_datetime, search_term, country_name, country_language,
#                     news_source, authors, headline, description, article_body, source_link,
#                     keywords, tags, article_images, all_images, article_metadata, full_html
#                 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
#             ''', values)
        
#         # Commit changes and close the connection
#         conn.commit()

#     conn.close()

# # Create the table
# create_table()

# # Process large JSON file and insert data into SQLite
# process_json_to_sqlite('/home/chinmaya/Programming/Web-scraping-with-scrapy/Outputs/ambuja.json')




# import sqlite3
# import ijson  # For streaming JSON parsing
# import os  # To check and create directories if needed

# # Function to ensure that the directory for the DB exists
# def create_directory_if_needed(db_path):
#     directory = os.path.dirname(db_path)
#     if not os.path.exists(directory):
#         os.makedirs(directory)

# # Function to create the SQLite table
# def create_table():
#     db_path = '/home/chinmaya/Programming/Web-scraping-with-scrapy/Outputs/ambuja_test.db'  # Replace this with your desired path to the DB

#     # Ensure the directory exists
#     create_directory_if_needed(db_path)
    
#     # Connect to the SQLite database (this will create it if it doesn't exist)
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # Create the table if it doesn't already exist
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS articles (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             transaction_id TEXT,
#             article_datetime TEXT,
#             search_term TEXT,
#             country_name TEXT,
#             country_language TEXT,
#             news_source TEXT,
#             authors TEXT,
#             headline TEXT,
#             description TEXT,
#             article_body TEXT,
#             source_link TEXT,
#             keywords TEXT,
#             tags TEXT,
#             article_images TEXT,
#             all_images TEXT,
#             article_metadata TEXT,
#             full_html TEXT
#         )
#     ''')

#     # Commit changes and close the connection
#     conn.commit()
#     conn.close()

# # Create the table
# # create_table()

# # def create_table():
# #     conn = sqlite3.connect('/Outputs/ambuja_test.db')
# #     cursor = conn.cursor()
# #     cursor.execute('''CREATE TABLE IF NOT EXISTS my_table (
# #                         id INTEGER PRIMARY KEY,
# #                         name TEXT,
# #                         age INTEGER)''')
# #     conn.commit()
# #     conn.close()

# def process_json_to_sqlite(json_file):
#     # Connect to the SQLite database
#     conn = sqlite3.connect('/home/chinmaya/Programming/Web-scraping-with-scrapy/Outputs/ambuja_test.db')
#     cursor = conn.cursor()

#     # Open the JSON file and process it in chunks
#     with open(json_file, 'r') as f:
#         # Initialize the streaming JSON parser
#         objects = ijson.items(f, 'item')  # 'item' is the key where data starts in the JSON
        
#         # Insert data into SQLite in chunks
#         for obj in objects:
#             # Extract the fields from the JSON object
#             transaction_id = obj.get('transaction_id')
#             article_datetime = obj.get('article_datetime')
#             search_term = obj.get('search_term')
#             country_name = obj.get('country_name')
#             country_language = obj.get('country_language')
#             news_source = obj.get('news_source')
#             authors = obj.get('authors')
#             headline = obj.get('headline')
#             description = obj.get('description')
#             article_body = obj.get('article_body')
#             source_link = obj.get('source_link')
#             keywords = obj.get('keywords')
#             tags = obj.get('tags')
#             article_images = obj.get('article_images')
#             all_images = obj.get('all_images')
#             article_metadata = obj.get('article_metadata')
#             full_html = obj.get('full_html')


#             # Combine all fields into a tuple for insertion (including term counts)
#             values = (
#                 transaction_id, article_datetime, search_term, country_name, country_language,
#                 news_source, authors, headline, description, article_body, source_link,
#                 keywords, tags, article_images, all_images, article_metadata, full_html
#             )

#             # Insert data into SQLite table
#             cursor.execute('''
#                 INSERT INTO articles (
#                     transaction_id, article_datetime, search_term, country_name, country_language,
#                     news_source, authors, headline, description, article_body, source_link,
#                     keywords, tags, article_images, all_images, article_metadata, full_html
#                 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             ''', values)
        
#         # Commit changes and close the connection
#         conn.commit()

#     conn.close()
    
# # Create the table
# create_table()
# # Process large JSON file and insert data into SQLite
# process_json_to_sqlite('/home/chinmaya/Programming/Web-scraping-with-scrapy/Outputs/ambuja.json')




# # Process large JSON file and insert data into SQLite
# process_json_to_sqlite('large_data.json')



# import sqlite3
# import ijson  # For streaming JSON parsing

# # Function to create SQLite tables (if needed)
# def create_table():
#     conn = sqlite3.connect('/Outputs/ambuja_test.db')
#     cursor = conn.cursor()
#     cursor.execute('''CREATE TABLE IF NOT EXISTS my_table (
#                         id INTEGER PRIMARY KEY,
#                         name TEXT,
#                         age INTEGER)''')
#     conn.commit()
#     conn.close()

# # Function to process and insert data from JSON file into SQLite
# def process_json_to_sqlite(json_file):
#     # Connect to the SQLite database
#     conn = sqlite3.connect('my_database.db')
#     cursor = conn.cursor()

#     # Open the JSON file and process it in chunks
#     with open(json_file, 'r') as f:
#         # Initialize the streaming JSON parser
#         objects = ijson.items(f, 'item')  # 'item' is the key where data starts in the JSON
        
#         # Insert data into SQLite in chunks
#         for obj in objects:
#             # Assuming JSON structure like {'name': 'John', 'age': 30}
#             name = obj.get('name')
#             age = obj.get('age')
            
#             # Insert into SQLite table
#             cursor.execute("INSERT INTO my_table (name, age) VALUES (?, ?)", (name, age))
        
#         # Commit changes and close the connection
#         conn.commit()

#     conn.close()

# # Create the table
# create_table()

# # Process large JSON file and insert data into SQLite
# process_json_to_sqlite('large_data.json')
