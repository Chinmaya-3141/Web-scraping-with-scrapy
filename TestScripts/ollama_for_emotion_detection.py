#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 19:03:21 2025

@author: chinmaya
"""

import os
import requests
import json, time
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import defaultdict
import logging

# Define the template for Ollama's instructions
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Set up Ollama model
model = OllamaLLM(model="llama3.1")

# Function to fetch HTML from URL
def fetch_html(url):
    """Fetches the HTML content of a page."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to extract the body content from HTML
def extract_body_content(html):
    """Extracts the body content from the given HTML."""
    soup = BeautifulSoup(html, "html.parser")
    body = soup.body
    if body:
        return str(body)
    else:
        return "No body content found"

# Function to clean the extracted body content
def clean_body_content(body):
    """Cleans the body content by removing scripts and styles, and formatting the text."""
    soup = BeautifulSoup(body, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    clean_content = soup.get_text(separator="\n")
    return "\n".join(line.strip() for line in clean_content.splitlines() if line.strip())

# Function to chunk cleaned content into smaller parts
def chunk_cleaned_content(cleaned_content, chunk_size=6000):
    """Chunks the cleaned content into smaller parts based on the specified chunk size."""
    return [cleaned_content[i: i + chunk_size] for i in range(0, len(cleaned_content), chunk_size)]

# Function to join chunks into a single article text
def join_chunks(dom_chunks):
    """Joins all the cleaned content chunks into one single article text."""
    return ' '.join(dom_chunks)

def classify_emotions(article_text):
    """Classify emotions in the article and return scores using the model."""
    emotions = ['Anxiety', 'Frustration', 'Sadness', 'Joy', 'Surprise', 'Hope', 'Trust', 'Uncertainty/Ambiguity']
    
    dom_chunks = chunk_cleaned_content(article_text, chunk_size=6000)  # Break the article into chunks
    chunk_sizes = [len(chunk) for chunk in dom_chunks]  # Store the size of each chunk
    total_size = sum(chunk_sizes)  # Calculate total size of the article

    categorized_emotions = {
        "major": [],
        "neutral": [],
        "rejected": []
    }

    for emotion in emotions:
        total_score = 0
        explanations = []
        
        for idx, chunk in enumerate(dom_chunks):
            prompt = ChatPromptTemplate.from_template(f"""
                Analyze the article below and **only** return the following:
                1. A score between 0 and 1 indicating how strongly the emotion '{emotion}' is present.
                2. A brief explanation (max 15 words) of why this emotion is present.
                
                Respond **only** with the two parts: 
                'Score: [score] - Explanation: [brief explanation]'
                
                DO NOT include any extra information, article summaries, or general context.
                Just focus on this emotion.

                {chunk}
            """)
            
            chain = prompt | model
            response = chain.invoke({"dom_content": chunk})
            
            if response:
                try:
                    if 'Score:' in response and 'Explanation:' in response:
                        emotion_part, explanation_part = response.split(" - Explanation: ", 1)
                        score_part = emotion_part.split(':')[1].strip()
                        score = round(float(score_part), 3)
                        explanation = explanation_part.strip()
                        
                        # Weight the score based on the chunk's size
                        chunk_weight = chunk_sizes[idx] / total_size
                        weighted_score = score * chunk_weight
                        total_score += weighted_score
                        explanations.append(explanation)
                    else:
                        explanations.append(f"Invalid response for emotion '{emotion.lower()}'.")
                except ValueError:
                    explanations.append(f"Error in processing the response for emotion '{emotion.lower()}'.")
            else:
                explanations.append(f"No response for emotion '{emotion.lower()}' in chunk.")
        
        # Categorize the emotion based on the total weighted score
        if total_score > 0.7:
            categorized_emotions["major"].append({
                "emotion": emotion,
                "score": round(total_score, 3),
                "explanation": " | ".join(explanations)
            })
        elif total_score >= 0.5:
            categorized_emotions["neutral"].append({
                "emotion": emotion,
                "score": round(total_score, 3),
                "explanation": " | ".join(explanations)
            })
        else:
            categorized_emotions["rejected"].append({
                "emotion": emotion,
                "score": round(total_score, 3),
                "explanation": " | ".join(explanations)
            })
    
    return categorized_emotions


# Function to get the emotion with the highest score
def get_highest_score_label(categorized_emotions):
    """Returns the emotion with the highest score and its score."""
    # Flatten the categorized_emotions dict to get all emotions and their scores
    all_emotions = []
    for category in categorized_emotions.values():
        for item in category:
            all_emotions.append((item["emotion"], item["score"]))

    # Get the highest emotion
    if all_emotions:
        highest_emotion, highest_score = max(all_emotions, key=lambda x: x[1])
        return highest_emotion, highest_score
    else:
        return None, 0


def save_output_to_json(results, filename="../Outputs/articles_output.json"):
    """Save the output into a single JSON file with results for multiple URLs."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Ensure the parent directory exists
    
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)
        
    print(f"All outputs have been written to {filename}")



def process_multiple_urls(urls):
    """Processes a list of URLs and returns the results."""
    all_results = []
    
    # Loop over each URL
    for url in urls:
        start_time = time.time()  # Start timing for this article
        print(f"Processing {url}...")
        print("requested html")
        html = fetch_html(url)
        print("fetched html")
        if html:
            print("Html true")
            # Extract and clean the body content
            body_content = extract_body_content(html)
            cleaned_content = clean_body_content(body_content)
            print("content cleaned")
            
            # Classify emotions in the article text
            categorized_emotions = classify_emotions(cleaned_content)
            print("classified emotion")
            
            # Get the emotion with the highest score
            highest_emotion, highest_score = get_highest_score_label(categorized_emotions)
            
            # Calculate processing time
            end_time = time.time()
            processing_time = round(end_time - start_time, 2)
            
            # Save the results for this URL
            article_result = {
                "url": url,
                "article_text": cleaned_content,  # Return the entire article text
                "categorized_emotions": categorized_emotions,
                "highest_emotion": highest_emotion,
                "highest_score": highest_score,
                "processing_time_seconds": processing_time  # Time taken to process this article
            }
            
            all_results.append(article_result)
        else:
            all_results.append({
                "url": url,
                "error": "Failed to fetch HTML",
                "processing_time_seconds": None
            })
    
    return all_results

# List of URLs you want to process
urls = [
    "https://hindi.economictimes.com/wealth/bachat/before-budget-2025-cement-stock-idea-brokerages-incred-given-add-rating-on-ambuja-cements-share-check-ambuja-cements-share-target-price/articleshow/117797821.cms",
    "https://hindi.economictimes.com/markets/share-bazaar/ambuja-cements-share-price-motilal-oswal-bulish-valuation-attractive-target-price/articleshow/115890927.cms",
    "https://hindi.moneycontrol.com/news/markets/adani-group-news-ambuja-cements-to-acquire-over-46-percent-stake-in-orient-cement-from-promoters-public-at-rupee-8100-crore-valuation-1931832.html",
    "https://www.navarashtra.com/business/adanis-ambuja-cement-will-be-bought-orient-cement-prominent-cement-company-in-the-country-670783.html",
    "https://marathi.economictimes.com/business-news/ambuja-cements-signs-agreement-to-buy-orient-cement-limited-for-rs-8100-crore/articleshow/114450514.cms",
    "https://marathi.latestly.com/india/adani-group-acquired-penna-cement-company-for-rs-10422-crore-555927.html",
    "https://marathi.economictimes.com/business-news/adani-groups-ambuja-cement-announced-acquisition-of-penna-cement-industries-limited-for-rs-10422-crore/articleshow/110973998.cms",
    "https://www.marketsmojo.com/news/stocks-in-action/ambuja-cements-gains-3-18-on-february-4-2025-despite-recent-decline-2-748842",
    "https://www.constructionweekonline.in/business/jupiter-wagons-secures-major-order-from-ambuja-cements-and-acc",
    "https://www.businesstoday.in/markets/stocks/story/sanghi-industries-merger-prefer-ambuja-cements-to-acc-65-upside-possible-on-adani-stock-says-investec-457709-2024-12-18",
    "https://legal.economictimes.indiatimes.com/news/corporate-business/ambuja-cements-adani-merger-receives-no-objection-letter-from-stock-exchanges/116885509",
    "https://www.businesstoday.in/markets/company-stock/story/ambuja-cements-q3-earnings-net-profit-rises-242-revenue-at-rs-8415-crore-462441-2025-01-29",
    "https://www.sarkaritel.com/ambuja-cements-net-profit-more-than-doubles-in-q3/",
    "https://www.thehindu.com/business/ambuja-cements-to-merge-sanghi-industries-penna-cement-with-itself/article68996624.ece",
    "https://www.businesstoday.in/markets/stocks/story/ultratech-jk-cements-ambuja-cements-axis-shares-top-3-stock-picks-from-cement-space-with-29-upside-464054-2025-02-10"
]

# Call the function to process the URLs and get the results
results = process_multiple_urls(urls)

# Optionally, print the results or save them to a JSON file
print(results)  # Prints all results to the console
save_output_to_json(results)  # Saves the results to a JSON file
