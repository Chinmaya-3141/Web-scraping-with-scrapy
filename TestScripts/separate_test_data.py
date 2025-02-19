#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 20:34:48 2025

@author: chinmaya
"""
import json
import random
import pandas as pd

# Input and output file paths
input_file = 'Outputs/ambuja.json'

# Function to select articles and save them in the desired proportion
def select_articles(total_count, hindi_count, marathi_count, english_count, output_file, selected_articles=None):
    # Load the JSON data from the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Initialize lists to hold articles by language
    hindi_articles = []
    marathi_articles = []
    english_articles = []

    # Keep track of used source_links to avoid duplicates
    used_links = set()

    # Total articles selected
    hindi_selected = 0
    marathi_selected = 0
    english_selected = 0

    # List of valid search terms
    valid_search_terms = ['ambuja cements', 'acc limited', 'orient cement']

    # Separate articles by language based on 'country_language'
    for entry in data:
        if 'country_language' in entry:
            language = entry['country_language'].strip().lower()  # Normalize the language field
            
            # Extract headline and search_term (if available)
            headline = entry.get('headline', 'No headline available')  # Default if not found
            search_term = entry.get('search_term', '').strip().lower()  # Default empty if not found
            
            # Ensure search term is one of the valid options
            if search_term not in valid_search_terms:
                continue  # Skip articles with invalid search terms

            source_link = entry.get('source_link', None)

            # Skip if source link is already used (duplicate)
            if source_link in used_links or not source_link:
                continue

            article = {
                'headline': headline,
                'source_link': source_link,
                'search_term': search_term
            }

            # Classify articles into Hindi, Marathi, and English
            if language == 'hindi' and hindi_selected < hindi_count:
                hindi_articles.append(article)
                hindi_selected += 1
                used_links.add(source_link)  # Add the source link to the used links
            elif language == 'marathi' and marathi_selected < marathi_count:
                marathi_articles.append(article)
                marathi_selected += 1
                used_links.add(source_link)  # Add the source link to the used links
            elif language == 'english' and english_selected < english_count:
                english_articles.append(article)
                english_selected += 1
                used_links.add(source_link)  # Add the source link to the used links

    # Ensure we don't have more than needed
    hindi_articles = random.sample(hindi_articles, min(len(hindi_articles), hindi_count))
    marathi_articles = random.sample(marathi_articles, min(len(marathi_articles), marathi_count))
    english_articles = random.sample(english_articles, min(len(english_articles), english_count))

    # Combine all selected articles
    selected_articles = hindi_articles + marathi_articles + english_articles

    # If there's an already selected set, ensure we don't duplicate articles
    if selected_articles is not None:
        selected_articles = selected_articles[:total_count]

    # Prepare data for Excel export
    excel_data = []
    serial_number = 1

    for article in selected_articles:
        name_1 = f"Name {serial_number}A"
        name_2 = f"Name {serial_number}B"
        name_3 = f"Name {serial_number}C"
        
        # Determine the language for the row
        if article in hindi_articles:
            language = 'Hindi'
        elif article in marathi_articles:
            language = 'Marathi'
        else:
            language = 'English'
        
        # Append the data row to the excel_data list
        excel_data.append({
            'Serial Number': serial_number,
            'name 1': name_1,
            'name 2': name_2,
            'name 3': name_3,
            'headline': article['headline'],
            'source_link': article['source_link'],
            'search_term': article['search_term'],
            'Language': language
        })
        serial_number += 1

    # Create a DataFrame and export to Excel
    df = pd.DataFrame(excel_data)

    # Write the DataFrame to an Excel file (use openpyxl as the engine)
    df.to_excel(output_file, index=False, engine='openpyxl')

    print(f"Data has been written to {output_file}")

# First batch: 50 articles with the specified proportions
select_articles(50, 10, 10, 30, 'Outputs/50-samples.xlsx')

# Continue with adding more articles to make a total of 100 articles in the specified proportions
# Ensure the first 50 are included in the next 100-sample file
select_articles(100, 20, 20, 60, 'Outputs/100-samples.xlsx', selected_articles=[])


# import json
# import random
# import pandas as pd

# # Input and output file paths
# input_file = 'Outputs/ambuja.json'

# # Function to select articles and save them in the desired proportion
# def select_articles(total_count, hindi_count, marathi_count, english_count, output_file):
#     # Load the JSON data from the input file
#     with open(input_file, 'r', encoding='utf-8') as file:
#         data = json.load(file)

#     # Initialize lists to hold articles by language
#     hindi_articles = []
#     marathi_articles = []
#     english_articles = []

#     # Keep track of used source_links to avoid duplicates
#     used_links = set()

#     # Total articles selected
#     hindi_selected = 0
#     marathi_selected = 0
#     english_selected = 0

#     # List of valid search terms
#     valid_search_terms = ['ambuja cements', 'acc limited', 'orient cement']

#     # Separate articles by language based on 'country_language'
#     for entry in data:
#         if 'country_language' in entry:
#             language = entry['country_language'].strip().lower()  # Normalize the language field
            
#             # Extract headline and search_term (if available)
#             headline = entry.get('headline', 'No headline available')  # Default if not found
#             search_term = entry.get('search_term', '').strip().lower()  # Default empty if not found
            
#             # Ensure search term is one of the valid options
#             if search_term not in valid_search_terms:
#                 continue  # Skip articles with invalid search terms

#             source_link = entry.get('source_link', None)

#             # Skip if source link is already used (duplicate)
#             if source_link in used_links or not source_link:
#                 continue

#             article = {
#                 'headline': headline,
#                 'source_link': source_link,
#                 'search_term': search_term
#             }

#             # Classify articles into Hindi, Marathi, and English
#             if language == 'hindi' and hindi_selected < hindi_count:
#                 hindi_articles.append(article)
#                 hindi_selected += 1
#                 used_links.add(source_link)  # Add the source link to the used links
#             elif language == 'marathi' and marathi_selected < marathi_count:
#                 marathi_articles.append(article)
#                 marathi_selected += 1
#                 used_links.add(source_link)  # Add the source link to the used links
#             elif language == 'english' and english_selected < english_count:
#                 english_articles.append(article)
#                 english_selected += 1
#                 used_links.add(source_link)  # Add the source link to the used links

#     # Ensure we don't have more than needed
#     hindi_articles = random.sample(hindi_articles, min(len(hindi_articles), hindi_count))
#     marathi_articles = random.sample(marathi_articles, min(len(marathi_articles), marathi_count))
#     english_articles = random.sample(english_articles, min(len(english_articles), english_count))

#     # Combine all selected articles
#     selected_articles = hindi_articles + marathi_articles + english_articles

#     # Prepare data for Excel export
#     excel_data = []
#     serial_number = 1

#     for article in selected_articles:
#         name_1 = f"Name {serial_number}A"
#         name_2 = f"Name {serial_number}B"
#         name_3 = f"Name {serial_number}C"
        
#         # Determine the language for the row
#         if article in hindi_articles:
#             language = 'Hindi'
#         elif article in marathi_articles:
#             language = 'Marathi'
#         else:
#             language = 'English'
        
#         # Append the data row to the excel_data list
#         excel_data.append({
#             'Serial Number': serial_number,
#             'name 1': name_1,
#             'name 2': name_2,
#             'name 3': name_3,
#             'headline': article['headline'],
#             'source_link': article['source_link'],
#             'search_term': article['search_term'],
#             'Language': language
#         })
#         serial_number += 1

#     # Create a DataFrame and export to Excel
#     df = pd.DataFrame(excel_data)

#     # Write the DataFrame to an Excel file
#     df.to_excel(output_file, index=False)

#     print(f"Data has been written to {output_file}")

# # First batch: 50 articles with the specified proportions
# select_articles(50, 10, 10, 30, 'Outputs/50-samples.xlsx')

# # Continue with adding more articles to make a total of 100 articles in the specified proportions
# select_articles(100, 20, 20, 60, 'Outputs/100-samples.xlsx')



# import json
# import random
# import pandas as pd

# # Input and output file paths
# input_file = 'Outputs/ambuja.json'
# output_file = 'Outputs/100-samples.xlsx'

# # Load the JSON data from the input file
# with open(input_file, 'r', encoding='utf-8') as file:
#     data = json.load(file)

# # Initialize lists to hold articles by language
# hindi_articles = []
# marathi_articles = []
# english_articles = []

# # Counters for the language-specific proportions
# hindi_count = 0
# marathi_count = 0
# english_count = 0

# # Total number of articles to pick
# max_hindi = 20
# max_marathi = 20
# max_english = 60

# # List of valid search terms
# valid_search_terms = ['ambuja cements', 'acc limited', 'orient cement']

# # Separate articles by language based on 'country_language'
# for entry in data:
#     if 'country_language' in entry:
#         language = entry['country_language']
        
#         # Extract headline and search_term (if available)
#         headline = entry.get('headline', 'No headline available')  # Default if not found
#         search_term = entry.get('search_term', '').strip().lower()  # Default empty if not found
        
#         # Ensure search term is one of the valid options
#         if search_term not in valid_search_terms:
#             continue  # Skip articles with invalid search terms

#         article = {
#             'headline': headline,
#             'source_link': entry.get('source_link', 'No source link available'),
#             'search_term': search_term
#         }

#         # Classify articles into Hindi, Marathi, and English
#         if language == 'Hindi' and hindi_count < max_hindi:
#             hindi_articles.append(article)
#             hindi_count += 1
#         elif language == 'Marathi' and marathi_count < max_marathi:
#             marathi_articles.append(article)
#             marathi_count += 1
#         elif language == 'English' and english_count < max_english:
#             english_articles.append(article)
#             english_count += 1

# # Make sure we don't have more than needed
# hindi_articles = random.sample(hindi_articles, min(len(hindi_articles), max_hindi))
# marathi_articles = random.sample(marathi_articles, min(len(marathi_articles), max_marathi))
# english_articles = random.sample(english_articles, min(len(english_articles), max_english))

# # Combine all selected articles
# selected_articles = hindi_articles + marathi_articles + english_articles

# # Prepare data for Excel export
# excel_data = []
# serial_number = 1

# for article in selected_articles:
#     name_1 = f"Name {serial_number}A"
#     name_2 = f"Name {serial_number}B"
#     name_3 = f"Name {serial_number}C"
    
#     # Determine the language for the row
#     if article in hindi_articles:
#         language = 'Hindi'
#     elif article in marathi_articles:
#         language = 'Marathi'
#     else:
#         language = 'English'
    
#     # Append the data row to the excel_data list
#     excel_data.append({
#         'Serial Number': serial_number,
#         'name 1': name_1,
#         'name 2': name_2,
#         'name 3': name_3,
#         'headline': article['headline'],
#         'source_link': article['source_link'],
#         'search_term': article['search_term'],
#         'Language': language
#     })
#     serial_number += 1

# # Create a DataFrame and export to Excel
# df = pd.DataFrame(excel_data)

# # Write the DataFrame to an Excel file
# df.to_excel(output_file, index=False)

# print(f"Data has been written to {output_file}")
