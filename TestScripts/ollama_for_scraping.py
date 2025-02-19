#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 07:40:02 2025

@author: chinmaya
"""
import os
import requests
import json
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Define the template for Ollama's instructions
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model="llama3.1")
# model = OllamaLLM(model="deepseek-r1")

def fetch_html(url):
    """Fetches the HTML content of a page."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def extract_body_content(html):
    """Extracts the body content from the given HTML."""
    soup = BeautifulSoup(html, "html.parser")
    body = soup.body
    if body:
        return str(body)
    else:
        return "No body content found"

def clean_body_content(body):
    """Cleans the body content by removing scripts and styles, and formatting the text."""
    soup = BeautifulSoup(body, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    clean_content = soup.get_text(separator="\n")
    return "\n".join(line.strip() for line in clean_content.splitlines() if line.strip())

def chunk_cleaned_content(cleaned_content, chunk_size=6000):
    """Chunks the cleaned content into smaller parts based on the specified chunk size."""
    return [cleaned_content[i: i + chunk_size] for i in range(0, len(cleaned_content), chunk_size)]

def parse_with_ollama(dom_chunks, parse_description):
    """Uses Ollama to extract information from the cleaned content."""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({
            "dom_content": chunk,
            "parse_description": parse_description,
        })
        print(f"Chunks Processed: {i}/{len(dom_chunks)}")
        parsed_results.append(response)

    return parsed_results  # Return as a list for JSON

def generate_filename_from_url(url):
    """Generates a valid filename from the URL."""
    parsed_url = urlparse(url)
    filename = parsed_url.path.strip("/").replace("/", "_")  # Replace slashes with underscores
    if not filename:  # If URL is just the domain
        filename = parsed_url.netloc
    return filename

# Example usage:
# url = "https://www.livemint.com/market/stock-market-news/ambuja-cement-q3-results-net-profit-soars-242-yoy-to-rs-1-758-crore-total-income-up-28-11738136777013.html"  # Replace with the desired URL
# url = 'https://www.thehindu.com/business/i-t-refund-propels-ambuja-cements-q3-pat-to-2620-crore/article69155221.ece'
url ='https://www.dutchcowboys.nl/advertising/de-10-grappigste-reclames-ter-wereld-van-afgelopen-jaar'
html = fetch_html(url)

if html:
    body_content = extract_body_content(html)
    cleaned_content = clean_body_content(body_content)
    dom_chunks = chunk_cleaned_content(cleaned_content)
    # parse_description = "Find the headline, and then find any content which is part of the article basis the headline."
    parse_description = "Find any content which is part of the article and try to put the article back together as completely as possible without adding anything from your side which is not already part of the article."    
    parsed_data = parse_with_ollama(dom_chunks, parse_description)
    
    # Ensure the Output directory exists
    os.makedirs("Outputs", exist_ok=True)
    
    # Generate the filename from the URL
    # filename = generate_filename_from_url(url)
    filename = 'ambuja5'
    
    # Define the full path for the JSON file
    json_file_path = f"Outputs/{filename}.json"
    
    # Write the parsed data to a JSON file in the Output directory
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(parsed_data, json_file, ensure_ascii=False, indent=4)
    
    print(f"Parsed data has been written to '{json_file_path}'.")
else:
    print("Failed to fetch HTML.")




# import requests
# from langchain_ollama import OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate
# from bs4 import BeautifulSoup

# # Define the template for Ollama's instructions
# template = (
#     "You are tasked with extracting specific information from the following text content: {dom_content}. "
#     "Please follow these instructions carefully: \n\n"
#     "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
#     "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
#     "3. **Empty Response:** If no information matches the description, return an empty string ('')."
#     "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
# )

# model = OllamaLLM(model="llama3.1")

# def fetch_html(url):
#     """Fetches the HTML content of a page."""
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.text
#     else:
#         return None

# def extract_body_content(html):
#     """Extracts the body content from the given HTML."""
#     soup = BeautifulSoup(html, "html.parser")
#     body = soup.body
#     if body:
#         return str(body)
#     else:
#         return "No body content found"

# def clean_body_content(body):
#     """Cleans the body content by removing scripts and styles, and formatting the text."""
#     soup = BeautifulSoup(body, "html.parser")
#     for script_or_style in soup(["script", "style"]):
#         script_or_style.extract()
#     clean_content = soup.get_text(separator="\n")
#     return "\n".join(line.strip() for line in clean_content.splitlines() if line.strip())

# def chunk_cleaned_content(cleaned_content, chunk_size=6000):
#     """Chunks the cleaned content into smaller parts based on the specified chunk size."""
#     return [cleaned_content[i: i + chunk_size] for i in range(0, len(cleaned_content), chunk_size)]

# def parse_with_ollama(dom_chunks, parse_description):
#     """Uses Ollama to extract information from the cleaned content."""
#     prompt = ChatPromptTemplate.from_template(template)
#     chain = prompt | model
#     parsed_results = []

#     for i, chunk in enumerate(dom_chunks, start=1):
#         response = chain.invoke({
#             "dom_content": chunk,
#             "parse_description": parse_description,
#         })
#         print(f"Chunks Processed: {i}/{len(dom_chunks)}")
#         parsed_results.append(response)

#     return "\n".join(parsed_results)

# # Example usage:
# url = "https://www.livemint.com/market/stock-market-news/ambuja-cement-q3-results-net-profit-soars-242-yoy-to-rs-1-758-crore-total-income-up-28-11738136777013.html"  # Replace with the desired URL
# html = fetch_html(url)

# if html:
#     body_content = extract_body_content(html)
#     cleaned_content = clean_body_content(body_content)
#     dom_chunks = chunk_cleaned_content(cleaned_content)
#     parse_description = "Extract all the article text"
#     parsed_data = parse_with_ollama(dom_chunks, parse_description)
#     print(parsed_data)
# else:
#     print("Failed to fetch HTML.")



# from langchain_ollama import OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate
# from bs4 import BeautifulSoup

# template = (
#     "You are tasked with extracting specific information from the following text content: {dom_content}. "
#     "Please follow these instructions carefully: \n\n"
#     "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
#     "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
#     "3. **Empty Response:** If no information matches the description, return an empty string ('')."
#     "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
# )

# model = OllamaLLM(model="llama3.1")


# def extract_body_content(html):
#     """
#     Extracts the body content from the given HTML.
#     """
#     soup = BeautifulSoup(html, "html.parser")
#     body = soup.body
#     if body:

#         return str(body)
#     else:
#         return "No body content found"
    


# def clean_body_content(body):
#     """
#     Cleans the body content by removing scripts and styles, and formatting the text.
#     """
#     soup = BeautifulSoup(body, "html.parser")

#     for script_or_style in soup(["script", "style"]):
#         script_or_style.extract()

#     clean_content = soup.get_text(separator="\n")
#     cleaned_content = "\n".join(
#         line.strip() for line in clean_content.splitlines() if line.strip()
#     )

#     return cleaned_content

# def chunk_cleaned_content(cleaned_content, chunk_size=6000):
#     """
#     Chunks the cleaned content into smaller parts based on the specified chunk size.
#     """
#     return [
#         cleaned_content[x : x + chunk_size]
#         for x in range(0, len(cleaned_content), chunk_size)
#     ]

    
    
# def parse_with_ollama(dom_chunks, parse_description):

#     prompt = ChatPromptTemplate.from_template(template)
#     chain = prompt | model

#     parsed_results = []

#     for i, chunk in enumerate(dom_chunks, start=1):
#         response = chain.invoke(
#             {
#                 "dom_content": chunk,
#                 "parse_description": parse_description,
#             }
#         )

#         print(f"Chunks Processed: {i}/{len(dom_chunks)}")

#         parsed_results.append(response)

#     return "\n".join(parsed_results)