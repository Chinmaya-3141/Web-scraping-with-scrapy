#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 09:27:56 2025

@author: chinmaya
"""

# import ssl

# from transformers import GPTNeoForCausalLM, GPT2Tokenizer

# import os, json

 

# # custom_cert_path = os.path.join(os.path.dirname(__file__), "Zscaler Root CA.crt")

# # ssl_context = ssl.create_default_context(cafile=custom_cert_path)

# # ssl._create_default_https_context = ssl_context.wrap_socket

 

# tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")

# model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")

 

# def generate_key_insights(merged_content):

#     inputs = tokenizer(merged_content, return_tensors="pt", truncation=True, max_length=1800)

#     outputs = model.generate(inputs["input_ids"], max_new_tokens=200)

#     return tokenizer.decode(outputs[0], skip_special_tokens=True)

# with open('/home/chinmaya/Downloads/output_sentiments.json', 'r', encoding = 'utf-8') as f:
#     data = json.load(f)

# merged_content = " ".join(entry['content'] for entry in data)

# insights = generate_key_insights(merged_content)

# print("Key Insights:")

# print(insights)

# from transformers import BigBirdTokenizer, BigBirdForCausalLM
# import os, json

# # Load BigBird tokenizer and model
# tokenizer = BigBirdTokenizer.from_pretrained("google/bigbird-roberta-base")
# model = BigBirdForCausalLM.from_pretrained("google/bigbird-roberta-base")

# def generate_key_insights(merged_content):
#     # Tokenize input
#     inputs = tokenizer(merged_content, return_tensors="pt", truncation=True, max_length=8192)  # Increase max_length as per model's capacity
#     # Generate output with a larger number of new tokens
#     outputs = model.generate(inputs["input_ids"], max_new_tokens=200)

#     return tokenizer.decode(outputs[0], skip_special_tokens=True)

# # Load your content from the file
# with open('/home/chinmaya/Downloads/output_sentiments.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Merge content
# merged_content = " ".join(entry['content'] for entry in data)

# # Generate insights
# insights = generate_key_insights(merged_content)

# # Print the insights
# print("Key Insights:")
# print(insights)

# import torch
# print(torch.__version__)
# print(torch.cuda.is_available())

# from transformers import pipeline
# import torch

# # Check if GPU is available
# device = 0 if torch.cuda.is_available() else -1  # 0 for GPU, -1 for CPU

# # Initialize the Hugging Face model for zero-shot classification, specifying the device
# model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=device)

# # Example review list
# reviews = [
#     "The login is not working, I can't access my account.",
#     "The app is very slow, it's hard to use.",
#     "Customer support was really helpful when I had an issue.",
#     "The app is good but sometimes it crashes during login."
# ]

# # Define the candidate labels (aspects you want to track)
# candidate_labels = ["login", "responsiveness", "customer support", "app crashes", "performance", "ease of use", "features"]

# # Step 4: Analyze each review using the model (now it will run on GPU if available)
# classification_results = []
# for review in reviews:
#     result = model(review, candidate_labels)
#     classification_results.append(result)

# # Process the results as before
# for result in classification_results:
#     print(result)

# import json
# import pandas as pd
# from transformers import pipeline
# import torch

# # Step 1: Load the data from your JSON file into a DataFrame
# # Replace with your actual JSON file path
# json_file_path = '/home/chinmaya/Downloads/output_sentiments.json'
# with open(json_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Assuming the structure of the data is a list of dictionaries, with each dictionary containing a 'content' field
# df = pd.DataFrame(data)

# # Ensure the reviews are in the 'content' column
# reviews = df['content'].tolist()

# # Step 2: Initialize the Hugging Face pipeline for zero-shot classification
# # This is the model for zero-shot classification (dynamic classification of text content)
# device = 0 if torch.cuda.is_available() else -1  # 0 for GPU, -1 for CPU

# # Load the zero-shot model pipeline
# model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=device)

# # Step 3: Process the reviews dynamically
# classification_results = []

# # Here we won't provide any predefined categories; instead, we let the model handle the classification itself.
# # We'll use very general categories to infer possible topics.
# # These are more generic categories, allowing the model to classify reviews into broader themes.
# candidate_labels = ["product experience", "issue", "performance", "usability", "customer service", "features", "bugs"]

# for review in reviews:
#     result = model(review, candidate_labels)
#     classification_results.append(result)

# # Step 4: Analyze the results and dynamically generate insights
# # We won't define positive/negative categories ourselves; we'll let the model decide based on the scores.
# insight_counts = {label: 0 for label in candidate_labels}

# # Track high-confidence reviews (those that the model is confident about)
# for result in classification_results:
#     best_label = result['labels'][0]  # Get the top predicted label
#     best_score = result['scores'][0]  # Get the score for the best label
    
#     if best_score > 0.5:  # Consider predictions with score > 50% confidence
#         insight_counts[best_label] += 1

# # Step 5: Optionally, run sentiment analysis to classify reviews as positive/negative
# # This is useful if you'd like to see the polarity (positive, negative, or neutral)
# sentiment_analyzer = pipeline("sentiment-analysis", device=device)

# sentiment_results = []
# for review in reviews:
#     sentiment = sentiment_analyzer(review)[0]  # Sentiment result is a list with a dict (label and score)
#     sentiment_results.append(sentiment)

# # Step 6: Display insights from reviews
# print("Insights from Reviews:")

# total_reviews = len(reviews)

# # Display the counts for each dynamic label (topic classification)
# for label, count in insight_counts.items():
#     percentage = (count / total_reviews) * 100
#     print(f"Aspect: {label.capitalize()}")
#     print(f"Number of Reviews: {count}")
#     print(f"Percentage of Total Reviews: {percentage:.2f}%")
    
#     # Optional: Show the most confident reviews related to this label
#     if count > 0:
#         print(f"Reviews mentioning {label.capitalize()}:")
#         for idx, result in enumerate(classification_results):
#             if result['labels'][0] == label and result['scores'][0] > 0.5:
#                 print(f"- Review {idx+1}: {reviews[idx]}")
#         print()

# # Step 7: Analyze the sentiment results (positive/negative classification)
# positive_reviews = [rev for rev, sentiment in zip(reviews, sentiment_results) if sentiment['label'] == 'POSITIVE']
# negative_reviews = [rev for rev, sentiment in zip(reviews, sentiment_results) if sentiment['label'] == 'NEGATIVE']

# print(f"Total Positive Reviews: {len(positive_reviews)}")
# print(f"Total Negative Reviews: {len(negative_reviews)}")
# print(f"Positive Reviews Example: {positive_reviews[:2]}")  # Display a couple of examples
# print(f"Negative Reviews Example: {negative_reviews[:2]}")  # Display a couple of examples

# # Optional: Save the insights to a CSV file for further analysis
# insights_df = pd.DataFrame(insight_counts.items(), columns=['Aspect', 'Count'])
# insights_df['Percentage'] = (insights_df['Count'] / total_reviews) * 100
# insights_df.to_csv("/home/chinmaya/Downloads/review_insights.csv", index=False)

# import json
# import pandas as pd
# from transformers import pipeline
# import torch

# # Step 1: Load the data from your JSON file into a DataFrame
# # Replace with your actual JSON file path
# json_file_path = '/home/chinmaya/Downloads/output_sentiments.json'
# with open(json_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Assuming the structure of the data is a list of dictionaries, with each dictionary containing a 'content' field
# df = pd.DataFrame(data)

# # Ensure the reviews are in the 'content' column
# reviews = df['content'].tolist()

# # Step 2: Initialize the Hugging Face pipeline for zero-shot classification
# # This is the model for zero-shot classification (dynamic classification of text content)
# device = 0 if torch.cuda.is_available() else -1  # 0 for GPU, -1 for CPU

# # Load the zero-shot model pipeline
# model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=device)

# # Step 3: Process the reviews dynamically
# classification_results = []

# # Here we won't provide any predefined categories; instead, we let the model handle the classification itself.
# # We'll use very general categories to infer possible topics.
# candidate_labels = ["product experience", "issue", "performance", "usability", "customer service", "features", "bugs"]

# for review in reviews:
#     result = model(review, candidate_labels)
#     classification_results.append(result)

# # Step 4: Analyze the results and dynamically generate insights
# # We won't define positive/negative categories ourselves; we'll let the model decide based on the scores.
# insight_counts = {label: 0 for label in candidate_labels}

# # Track high-confidence reviews (those that the model is confident about)
# for result in classification_results:
#     best_label = result['labels'][0]  # Get the top predicted label
#     best_score = result['scores'][0]  # Get the score for the best label
    
#     if best_score > 0.5:  # Consider predictions with score > 50% confidence
#         insight_counts[best_label] += 1

# # Step 5: Display insights from reviews
# print("Insights from Reviews:")

# total_reviews = len(reviews)

# # Display the counts for each dynamic label (topic classification)
# for label, count in insight_counts.items():
#     percentage = (count / total_reviews) * 100
#     print(f"Aspect: {label.capitalize()}")
#     print(f"Number of Reviews: {count}")
#     print(f"Percentage of Total Reviews: {percentage:.2f}%")
    
#     # Optional: Show the most confident reviews related to this label
#     if count > 0:
#         print(f"Reviews mentioning {label.capitalize()}:")
#         for idx, result in enumerate(classification_results):
#             if result['labels'][0] == label and result['scores'][0] > 0.5:
#                 print(f"- Review {idx+1}: {reviews[idx]}")
#         print()

# # Step 6: Use the existing sentiment data directly
# df['Sentiment'] = df['sentiment']
# df['Positive Score'] = df['positive_score']
# df['Neutral Score'] = df['neutral_score']
# df['Negative Score'] = df['negative_score']

# # Display the sentiment data along with the original reviews
# print("\nSentiment Analysis Results:")
# print(df[['content', 'Sentiment', 'Positive Score', 'Neutral Score', 'Negative Score']].head())

# # Optional: Save the insights to a CSV file for further analysis
# insights_df = pd.DataFrame(insight_counts.items(), columns=['Aspect', 'Count'])
# insights_df['Percentage'] = (insights_df['Count'] / total_reviews) * 100
# insights_df.to_csv("/home/chinmaya/Downloads/review_insights.csv", index=False)

# from transformers import BartForConditionalGeneration, BartTokenizer
# import torch
# import pandas as pd
# import json

# # Load the BART model and tokenizer
# model_name = "facebook/bart-large-cnn"  # Or use "facebook/bart-base" for faster processing
# model = BartForConditionalGeneration.from_pretrained(model_name)
# tokenizer = BartTokenizer.from_pretrained(model_name)

# # Set device to GPU if available
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# # Load the data from your JSON file into a DataFrame
# json_file_path = '/home/chinmaya/Downloads/output_sentiments.json'
# with open(json_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Assuming the structure of the data is a list of dictionaries, with each dictionary containing a 'content' field
# df = pd.DataFrame(data)

# # Ensure the reviews are in the 'content' column
# reviews = df['content'].tolist()

# # Function for batch processing to generate insights using BART
# def generate_batch_insights_bart(reviews, batch_size=16):
#     insights = []
#     for i in range(0, len(reviews), batch_size):
#         batch_reviews = reviews[i:i + batch_size]

#         # Prepare the batch input text with prompt
#         prompts = [f"Please summarize the main insights and key feedback from this review: {review}" for review in batch_reviews]

#         # Tokenize the batch
#         inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=1024)

#         # Move tensors to the same device as the model (GPU or CPU)
#         inputs = {key: value.to(device) for key, value in inputs.items()}

#         # Generate insights using the model
#         summary_ids = model.generate(inputs['input_ids'], max_length=200, num_beams=4, early_stopping=True)

#         # Decode and collect insights
#         batch_insights = [tokenizer.decode(summary_id, skip_special_tokens=True) for summary_id in summary_ids]
#         insights.extend(batch_insights)

#     return insights

# # Generate insights for the reviews in batch
# insights_batch_bart = generate_batch_insights_bart(reviews)

# # Function to summarize the generated insights into 4 main points
# def summarize_insights(insights):
#     # Prepare the insights as a single string
#     combined_insights = " ".join(insights)

#     # Prompt for summarizing the insights into 4 main points
#     prompt = f"Summarize the following insights into 4 main points:\n{combined_insights}"

#     # Tokenize the input
#     inputs = tokenizer.encode("summarize: " + prompt, return_tensors="pt", max_length=1024, truncation=True)

#     # Move inputs to the same device as the model (GPU or CPU)
#     inputs = inputs.to(device)

#     # Generate a summary with 4 main points
#     summary_ids = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True)

#     # Decode the summary and return it
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary

# # Summarize the generated insights into 4 main points
# summary_of_insights = summarize_insights(insights_batch_bart)

# # Print the summary
# print("\nSummary of Insights (4 Main Points):")
# print(summary_of_insights)

# from transformers import BartForConditionalGeneration, BartTokenizer
# import torch
# import pandas as pd
# import json

# # Load the BART model and tokenizer
# model_name = "facebook/bart-large-cnn"  # Or use "facebook/bart-base" for faster processing
# model = BartForConditionalGeneration.from_pretrained(model_name)
# tokenizer = BartTokenizer.from_pretrained(model_name)

# # Set device to GPU if available
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# # Load the data from your JSON file into a DataFrame
# json_file_path = '/home/chinmaya/Downloads/output_sentiments.json'
# with open(json_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Assuming the structure of the data is a list of dictionaries, with each dictionary containing a 'content' field
# df = pd.DataFrame(data)

# # Ensure the reviews are in the 'content' column
# reviews = df['content'].tolist()

# # Function for batch processing to generate insights using BART
# def generate_batch_insights_bart(reviews, batch_size=4):  # Default batch size reduced to avoid memory issues
#     insights = []
#     for i in range(0, len(reviews), batch_size):
#         batch_reviews = reviews[i:i + batch_size]

#         # Prepare the batch input text with prompt
#         prompts = [f"Please summarize the main insights and key feedback from this review: {review}" for review in batch_reviews]

#         # Tokenize the batch
#         inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=1024)

#         # Move tensors to the same device as the model (GPU or CPU)
#         inputs = {key: value.to(device) for key, value in inputs.items()}

#         # Use no_grad to save memory during inference
#         with torch.no_grad():
#             # Generate insights using the model
#             summary_ids = model.generate(inputs['input_ids'], max_length=200, num_beams=4, early_stopping=True)

#         # Decode and collect insights
#         batch_insights = [tokenizer.decode(summary_id, skip_special_tokens=True) for summary_id in summary_ids]
#         insights.extend(batch_insights)

#         # Clear GPU memory cache after each batch to avoid memory overload
#         torch.cuda.empty_cache()

#     return insights

# # Generate insights for the reviews in batch
# insights_batch_bart = generate_batch_insights_bart(reviews)

# # Function to summarize the generated insights into 4 main points
# def summarize_insights(insights):
#     # Prepare the insights as a single string
#     combined_insights = " ".join(insights)

#     # Prompt for summarizing the insights into 4 main points
#     prompt = f"Summarize the following insights into 4 main points:\n{combined_insights}"

#     # Tokenize the input
#     inputs = tokenizer.encode("summarize: " + prompt, return_tensors="pt", max_length=1024, truncation=True)

#     # Move inputs to the same device as the model (GPU or CPU)
#     inputs = inputs.to(device)

#     # Use no_grad to save memory during inference
#     with torch.no_grad():
#         # Generate a summary with 4 main points
#         summary_ids = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True)

#     # Decode the summary and return it
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary

# # Summarize the generated insights into 4 main points
# summary_of_insights = summarize_insights(insights_batch_bart)

# # Print the summary
# print("\nSummary of Insights (4 Main Points):")
# print(summary_of_insights)


# from transformers import BartForConditionalGeneration, BartTokenizer
# import torch
# import pandas as pd
# import json
# from torch.cuda.amp import autocast  # Importing for mixed precision

# torch.cuda.empty_cache()

# # Load the BART model and tokenizer
# model_name = "sshleifer/distilbart-cnn-12-6"  # Or use "facebook/bart-base" for faster processing
# model = BartForConditionalGeneration.from_pretrained(model_name)
# tokenizer = BartTokenizer.from_pretrained(model_name)

# # from transformers import T5ForConditionalGeneration, T5Tokenizer

# # model_name = "t5-base"
# # model = T5ForConditionalGeneration.from_pretrained(model_name)
# # tokenizer = T5Tokenizer.from_pretrained(model_name)

# # from transformers import AlbertForSequenceClassification, AlbertTokenizer

# # # Load the ALBERT model and tokenizer
# # model_name = "albert-base-v2"  # Example model without sentencepiece
# # model = AlbertForSequenceClassification.from_pretrained(model_name)
# # tokenizer = AlbertTokenizer.from_pretrained(model_name)

# # from transformers import AutoTokenizer, AutoModelForSequenceClassification

# # tokenizer = AutoTokenizer.from_pretrained("albert-base-v2")
# # model = AutoModelForSequenceClassification.from_pretrained("albert-base-v2")


# # Set device to GPU if available
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# # Load the data from your JSON file into a DataFrame
# json_file_path = '/home/chinmaya/Downloads/output_sentiments.json'
# with open(json_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Assuming the structure of the data is a list of dictionaries, with each dictionary containing a 'content' field
# df = pd.DataFrame(data)

# # Ensure the reviews are in the 'content' column
# reviews = df['content'].tolist()

# # Function for batch processing to generate insights using BART
# def generate_batch_insights_bart(reviews, batch_size=48):  
#     insights = []
#     for i in range(0, len(reviews), batch_size):
#         batch_reviews = reviews[i:i + batch_size]

#         # Use a more focused prompt
#         prompts = [f"Extract the main feedback or insights from the following review: {review}" for review in batch_reviews]

#         inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=1024)
#         inputs = {key: value.to(device) for key, value in inputs.items()}

#         with torch.no_grad():
#             with autocast():
#                 summary_ids = model.generate(inputs['input_ids'], max_length=100, num_beams=4, early_stopping=True, no_repeat_ngram_size=3)

#         batch_insights = [tokenizer.decode(summary_id, skip_special_tokens=True) for summary_id in summary_ids]
#         insights.extend(batch_insights)

#         torch.cuda.empty_cache()

#     return insights


# # Function to summarize the generated insights into 4 main points
# def summarize_insights(insights):
#     # Prepare the insights as a single string
#     combined_insights = " ".join(insights)

#     # Prompt for summarizing the insights into 4 main points
#     prompt = f"Summarize the following insights into 4 main points:\n{combined_insights}"

#     # Tokenize the input
#     inputs = tokenizer.encode("summarize: " + prompt, return_tensors="pt", max_length=1024, truncation=True)

#     # Move inputs to the same device as the model (GPU or CPU)
#     inputs = inputs.to(device)

#     # Use no_grad to save memory during inference
#     with torch.no_grad():
#         # Generate a summary with 4 main points
#         summary_ids = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True)

#     # Decode the summary and return it
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary

# # Summarize the generated insights into 4 main points
# summary_of_insights = summarize_insights(insights_batch_bart)

# # Print the summary
# print("\nSummary of Insights (4 Main Points):")
# print(summary_of_insights)

# # import torch
# # torch.cuda.empty_cache()

# from transformers import BartForConditionalGeneration, BartTokenizer
# import torch
# import pandas as pd
# import json
# from torch.cuda.amp import autocast  # Importing for mixed precision

# torch.cuda.empty_cache()

# # Load the BART model and tokenizer
# model_name = "sshleifer/distilbart-cnn-12-6"  # Or use "facebook/bart-base" for faster processing
# model = BartForConditionalGeneration.from_pretrained(model_name)
# tokenizer = BartTokenizer.from_pretrained(model_name)

# # Set device to GPU if available
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# # Load the data from your JSON file into a DataFrame
# json_file_path = '/home/chinmaya/Downloads/output_sentiments.json'
# with open(json_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Assuming the structure of the data is a list of dictionaries, with each dictionary containing a 'content' field
# df = pd.DataFrame(data)

# # Ensure the reviews are in the 'content' column
# reviews = df['content'].tolist()

# # Function to generate insights from reviews in batch
# def generate_batch_insights_bart(reviews, batch_size=32):  
#     insights = []
#     for i in range(0, len(reviews), batch_size):
#         batch_reviews = reviews[i:i + batch_size]

#         # Use a more focused prompt to extract insights
#         prompts = [f"Extract the main feedback or insights from the following review: {review}" for review in batch_reviews]

#         # Tokenize the input batch
#         inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=1024)
#         inputs = {key: value.to(device) for key, value in inputs.items()}

#         # Use mixed precision to save memory during inference
#         with torch.no_grad():
#             with autocast():  # Enable mixed-precision during inference
#                 # Generate insights using the model
#                 summary_ids = model.generate(inputs['input_ids'], max_length=100, num_beams=4, early_stopping=True, no_repeat_ngram_size=3)

#         # Decode and collect insights
#         batch_insights = [tokenizer.decode(summary_id, skip_special_tokens=True) for summary_id in summary_ids]
#         insights.extend(batch_insights)

#         # Clear GPU memory cache after each batch to avoid memory overload
#         torch.cuda.empty_cache()

#     return insights

# # Function to summarize the insights into 4 main points
# def summarize_insights(insights):
#     # Combine all insights into one string
#     combined_insights = " ".join(insights)

#     # Create a focused prompt for summarizing the insights into 4 main points
#     prompt = f"Summarize the following insights into 4 concise and clear bullet points: {combined_insights}"

#     # Tokenize the input prompt
#     inputs = tokenizer.encode("summarize: " + prompt, return_tensors="pt", max_length=1024, truncation=True)
#     inputs = inputs.to(device)

#     # Generate the summary with 4 main points
#     with torch.no_grad():
#         summary_ids = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True, no_repeat_ngram_size=3)

#     # Decode the summary and return it
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary

# # Generate insights for the reviews in batch
# insights_batch_bart = generate_batch_insights_bart(reviews)

# # Summarize the generated insights into 4 main points
# summary_of_insights = summarize_insights(insights_batch_bart)

# # Print the summary
# print("\nSummary of Insights (4 Main Points):")
# print(summary_of_insights)

# # Clear GPU memory cache
# torch.cuda.empty_cache()

# from transformers import BartForConditionalGeneration, BartTokenizer
# import torch
# import pandas as pd
# import json
# from torch.cuda.amp import autocast  # Importing for mixed precision

# torch.cuda.empty_cache()

# # Load the BART model and tokenizer
# model_name = "sshleifer/distilbart-cnn-12-6"  # Or use "facebook/bart-base" for faster processing
# model = BartForConditionalGeneration.from_pretrained(model_name)
# tokenizer = BartTokenizer.from_pretrained(model_name)

# # Set device to GPU if available
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# # Load the new data from your JSON file into a DataFrame
# json_file_path = '/home/chinmaya/Programming/news.json'  # Update the path to your new file
# with open(json_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Assuming the structure of the data is a list of dictionaries
# df = pd.DataFrame(data)

# # Only use the 'headline' field as content for generating insights
# headlines = df['headline'].tolist()

# # Function to generate insights from articles in batch
# def generate_batch_insights_bart(contents, batch_size=32):  
#     insights = []
#     for i in range(0, len(contents), batch_size):
#         batch_contents = contents[i:i + batch_size]

#         # Use a more focused prompt to extract insights
#         prompts = [f"Extract the main feedback or insights from the following news article headline: {content}" for content in batch_contents]

#         # Tokenize the input batch
#         inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=1024)
#         inputs = {key: value.to(device) for key, value in inputs.items()}

#         # Use mixed precision to save memory during inference
#         with torch.no_grad():
#             with autocast():  # Enable mixed-precision during inference
#                 # Generate insights using the model
#                 summary_ids = model.generate(inputs['input_ids'], max_length=100, num_beams=4, early_stopping=True, no_repeat_ngram_size=3)

#         # Decode and collect insights
#         batch_insights = [tokenizer.decode(summary_id, skip_special_tokens=True) for summary_id in summary_ids]
#         insights.extend(batch_insights)

#         # Clear GPU memory cache after each batch to avoid memory overload
#         torch.cuda.empty_cache()

#     return insights

# # Function to summarize the insights into 4 main points
# def summarize_insights(insights):
#     # Combine all insights into one string
#     combined_insights = " ".join(insights)

#     # Create a focused prompt for summarizing the insights into 4 main points
#     prompt = f"Summarize the following insights into 4 concise and clear bullet points: {combined_insights}"

#     # Tokenize the input prompt
#     inputs = tokenizer.encode("summarize: " + prompt, return_tensors="pt", max_length=1024, truncation=True)
#     inputs = inputs.to(device)

#     # Generate the summary with 4 main points
#     with torch.no_grad():
#         summary_ids = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True, no_repeat_ngram_size=3)

#     # Decode the summary and return it
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary

# # Generate insights for the content (headlines) in batch
# insights_batch_bart = generate_batch_insights_bart(headlines)

# # Summarize the generated insights into 4 main points
# summary_of_insights = summarize_insights(insights_batch_bart)

# # Print the summary
# print("\nSummary of Insights (4 Main Points):")
# print(summary_of_insights)

# # Clear GPU memory cache
# torch.cuda.empty_cache()

# from transformers import MBartForConditionalGeneration, MBartTokenizer
# import torch
# import pandas as pd
# import json
# from torch.cuda.amp import autocast  # Importing for mixed precision

# torch.cuda.empty_cache()

# # Load the mBART model and tokenizer (supports multiple languages)
# model_name = "facebook/mbart-large-50-many-to-one-mmt"  # mBART model supporting many languages
# model = MBartForConditionalGeneration.from_pretrained(model_name)
# tokenizer = MBartTokenizer.from_pretrained(model_name)

# # Set device to GPU if available
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# # Load the new data from your JSON file into a DataFrame
# json_file_path = '/home/chinmaya/Programming/news.json'  # Update the path to your new file
# with open(json_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Assuming the structure of the data is a list of dictionaries
# df = pd.DataFrame(data)

# # Only use the 'headline' field as content for generating insights
# headlines = df['headline'].tolist()

# # Function to generate insights from articles in batch (using mBART for multilingual support)
# def generate_batch_insights_mbart(contents, batch_size=32):  
#     insights = []
#     for i in range(0, len(contents), batch_size):
#         batch_contents = contents[i:i + batch_size]

#         # Use a more focused prompt to extract insights
#         prompts = [f"Extract the main feedback or insights from the following news article headline: {content}" for content in batch_contents]

#         # Tokenize the input batch
#         inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=1024)
#         inputs = {key: value.to(device) for key, value in inputs.items()}

#         # Use mixed precision to save memory during inference
#         with torch.no_grad():
#             with autocast():  # Enable mixed-precision during inference
#                 # Generate insights using the model
#                 summary_ids = model.generate(inputs['input_ids'], max_length=100, num_beams=4, early_stopping=True, no_repeat_ngram_size=3)

#         # Decode and collect insights
#         batch_insights = [tokenizer.decode(summary_id, skip_special_tokens=True) for summary_id in summary_ids]
#         insights.extend(batch_insights)

#         # Clear GPU memory cache after each batch to avoid memory overload
#         torch.cuda.empty_cache()

#     return insights

# # Function to summarize the insights into 4 main points
# def summarize_insights(insights):
#     # Combine all insights into one string
#     combined_insights = " ".join(insights)

#     # Create a focused prompt for summarizing the insights into 4 main points
#     prompt = f"Summarize the following insights into 4 concise and clear bullet points: {combined_insights}"

#     # Tokenize the input prompt
#     inputs = tokenizer.encode("summarize: " + prompt, return_tensors="pt", max_length=1024, truncation=True)
#     inputs = inputs.to(device)

#     # Generate the summary with 4 main points
#     with torch.no_grad():
#         summary_ids = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True, no_repeat_ngram_size=3)

#     # Decode the summary and return it
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary

# # Generate insights for the content (headlines) in batch
# insights_batch_mbart = generate_batch_insights_mbart(headlines)

# # Summarize the generated insights into 4 main points
# summary_of_insights = summarize_insights(insights_batch_mbart)

# # Print the summary
# print("\nSummary of Insights (4 Main Points):")
# print(summary_of_insights)

# # Clear GPU memory cache
# torch.cuda.empty_cache()

# from transformers import MBartForConditionalGeneration, MBartTokenizer
# import torch
# import pandas as pd
# import json

# torch.cuda.empty_cache()

# # Load the mBART model and tokenizer
# model_name = "facebook/mbart-large-50"  # Multilingual BART model
# model = MBartForConditionalGeneration.from_pretrained(model_name)
# tokenizer = MBartTokenizer.from_pretrained(model_name)

# # Set device to GPU if available
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# # Load the new data from your JSON file into a DataFrame
# json_file_path = '/home/chinmaya/Programming/news.json'  # Update the path to your new file
# with open(json_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Assuming the structure of the data is a list of dictionaries
# df = pd.DataFrame(data)

# # Only use the 'headline' field as content for generating insights
# headlines = df['headline'].tolist()

# # Function to generate insights from articles in batch
# def generate_batch_insights_mbart(contents, batch_size=32):  
#     insights = []
#     for i in range(0, len(contents), batch_size):
#         batch_contents = contents[i:i + batch_size]

#         # Use a more focused prompt to extract insights
#         prompts = [f"Extract the main feedback or insights from the following news article headline: {content}" for content in batch_contents]

#         # Tokenize the input batch
#         inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=1024)
#         inputs = {key: value.to(device) for key, value in inputs.items()}

#         # Generate insights using the model
#         with torch.no_grad():
#             summary_ids = model.generate(inputs['input_ids'], max_length=100, num_beams=4, early_stopping=True, no_repeat_ngram_size=3)

#         # Decode and collect insights
#         batch_insights = [tokenizer.decode(summary_id, skip_special_tokens=True) for summary_id in summary_ids]
#         insights.extend(batch_insights)

#         # Clear GPU memory cache after each batch to avoid memory overload
#         torch.cuda.empty_cache()

#     return insights

# # Function to summarize the insights into 4 main points
# def summarize_insights(insights):
#     # Combine all insights into one string
#     combined_insights = " ".join(insights)

#     # Create a focused prompt for summarizing the insights into 4 main points
#     prompt = f"Summarize the following insights into 4 concise and clear bullet points: {combined_insights}"

#     # Tokenize the input prompt
#     inputs = tokenizer.encode("summarize: " + prompt, return_tensors="pt", max_length=1024, truncation=True)
#     inputs = inputs.to(device)

#     # Generate the summary with 4 main points
#     with torch.no_grad():
#         summary_ids = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True, no_repeat_ngram_size=3)

#     # Decode the summary and return it
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary

# # Generate insights for the content (headlines) in batch
# insights_batch_mbart = generate_batch_insights_mbart(headlines)

# # Summarize the generated insights into 4 main points
# summary_of_insights = summarize_insights(insights_batch_mbart)

# # Print the summary
# print("\nSummary of Insights (4 Main Points):")
# print(summary_of_insights)

# # Clear GPU memory cache
# torch.cuda.empty_cache()

# from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
# import torch
# import pandas as pd
# import json
# from torch.cuda.amp import autocast  # Importing for mixed precision

# # Set up for GPU if available
# torch.cuda.empty_cache()
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Load the smaller multilingual DistilBERT model and tokenizer
# model_name = "distilbert-base-multilingual-cased"
# model = DistilBertForSequenceClassification.from_pretrained(model_name)
# tokenizer = DistilBertTokenizer.from_pretrained(model_name)

# model.to(device)

# # Load the new data from your JSON file into a DataFrame
# json_file_path = '/home/chinmaya/Programming/news.json'  # Update to your correct file path
# with open(json_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Assuming the structure of the data is a list of dictionaries
# df = pd.DataFrame(data)

# # Extract headlines from the data (assuming 'headline' field)
# headlines = df['headline'].tolist()

# # Function to generate insights from a batch of headlines
# def generate_batch_insights_distilbert(contents, batch_size=8):  
#     insights = []
#     for i in range(0, len(contents), batch_size):
#         batch_contents = contents[i:i + batch_size]
        
#         # Combine the headlines into a single string to allow broader context
#         combined_headlines = " ".join(batch_contents)
        
#         # Use a prompt that encourages the model to extract broader insights
#         prompt = f"Extract the main feedback or trends from the following headlines: {combined_headlines}"

#         # Tokenize the input batch
#         inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=1024)
#         inputs = {key: value.to(device) for key, value in inputs.items()}

#         # Generate insights using the model
#         with torch.no_grad():
#             with autocast():  # Enable mixed-precision during inference
#                 outputs = model(**inputs)

#         # Process and add the generated insights
#         batch_insights = [f"Insight from batch: {output}" for output in outputs.logits]
#         insights.extend(batch_insights)

#         # Clear GPU memory cache after each batch to avoid memory overload
#         torch.cuda.empty_cache()

#     return insights

# # Function to summarize the insights into 4 main points
# def summarize_insights(insights):
#     # Combine all insights into one string
#     combined_insights = " ".join(insights)

#     # Create a focused prompt for summarizing the insights into 4 main points
#     prompt = f"Summarize the following insights into 4 concise and clear bullet points: {combined_insights}"

#     # Tokenize the input prompt
#     inputs = tokenizer.encode("summarize: " + prompt, return_tensors="pt", max_length=512, truncation=True)
#     inputs = inputs.to(device)

#     # Generate the summary with 4 main points
#     with torch.no_grad():
#         with autocast():  # Enable mixed-precision during inference
#             summary_ids = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True, no_repeat_ngram_size=3)

#     # Decode the summary and return it
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary

# # Generate insights for the content (headlines) in batch
# insights_batch_distilbert = generate_batch_insights_distilbert(headlines)

# # Summarize the generated insights into 4 main points
# summary_of_insights = summarize_insights(insights_batch_distilbert)

# # Print the summary
# print("\nSummary of Insights (4 Main Points):")
# print(summary_of_insights)

# # Clear GPU memory cache
# torch.cuda.empty_cache()

# from transformers import BartForConditionalGeneration, BartTokenizer
# import torch
# import pandas as pd
# import json

# torch.cuda.empty_cache()

# # Load the BART model and tokenizer
# model_name = "facebook/bart-base"  # BART base model
# model = BartForConditionalGeneration.from_pretrained(model_name)
# tokenizer = BartTokenizer.from_pretrained(model_name)

# # Set device to GPU if available
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# # Load the new data from your JSON file into a DataFrame
# json_file_path = '/home/chinmaya/Programming/news.json'  # Update the path to your new file
# with open(json_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Assuming the structure of the data is a list of dictionaries
# df = pd.DataFrame(data)

# # Only use the 'headline' field as content for generating insights
# headlines = df['headline'].tolist()

# # Function to generate insights from articles in batch
# def generate_batch_insights_bart(contents, batch_size=8):  
#     insights = []
#     for i in range(0, len(contents), batch_size):
#         batch_contents = contents[i:i + batch_size]

#         # Use a more focused prompt to extract insights
#         prompts = [f"Extract the main feedback or insights from the following news article headline: {content}" for content in batch_contents]

#         # Tokenize the input batch
#         inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=1024)
#         inputs = {key: value.to(device) for key, value in inputs.items()}

#         # Generate insights using the model
#         with torch.no_grad():
#             summary_ids = model.generate(inputs['input_ids'], max_length=100, num_beams=4, early_stopping=True, no_repeat_ngram_size=3)

#         # Decode and collect insights
#         batch_insights = [tokenizer.decode(summary_id, skip_special_tokens=True) for summary_id in summary_ids]
#         insights.extend(batch_insights)

#         # Clear GPU memory cache after each batch to avoid memory overload
#         torch.cuda.empty_cache()

#     return insights

# # Function to summarize the insights into 4 main points
# def summarize_insights(insights):
#     # Combine all insights into one string
#     combined_insights = " ".join(insights)

#     # Create a focused prompt for summarizing the insights into 4 main points
#     prompt = f"Summarize the following insights into 4 concise and clear bullet points: {combined_insights}"

#     # Tokenize the input prompt
#     inputs = tokenizer.encode("summarize: " + prompt, return_tensors="pt", max_length=1024, truncation=True)
#     inputs = inputs.to(device)

#     # Generate the summary with 4 main points
#     with torch.no_grad():
#         summary_ids = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True, no_repeat_ngram_size=3)

#     # Decode the summary and return it
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary

# # Generate insights for the content (headlines) in batch
# insights_batch_bart = generate_batch_insights_bart(headlines)

# # Summarize the generated insights into 4 main points
# summary_of_insights = summarize_insights(insights_batch_bart)

# # Print the summary
# print("\nSummary of Insights (4 Main Points):")
# print(summary_of_insights)

# # Clear GPU memory cache
# torch.cuda.empty_cache()

# from transformers import BartForConditionalGeneration, BartTokenizer
# import torch
# import pandas as pd
# import json

# # Set up for GPU if available
# torch.cuda.empty_cache()
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Load the distilled BART model and tokenizer
# model_name = "sshleifer/distilbart-cnn-12-6"  # Distilled BART model for summarization
# model = BartForConditionalGeneration.from_pretrained(model_name)
# tokenizer = BartTokenizer.from_pretrained(model_name)

# model.to(device)

# # Load the new data from your JSON file into a DataFrame
# json_file_path = '/home/chinmaya/Programming/news.json'  # Update to your correct file path
# with open(json_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Assuming the structure of the data is a list of dictionaries
# df = pd.DataFrame(data)

# # Only use the 'headline' field as content for generating insights
# headlines = df['headline'].tolist()

# # Function to generate insights from a batch of headlines
# def generate_batch_insights_bart(contents, batch_size=512):  
#     insights = []
#     for i in range(0, len(contents), batch_size):
#         batch_contents = contents[i:i + batch_size]

#         # Combine the headlines into a single string to allow broader context
#         combined_headlines = " ".join(batch_contents)
        
#         # Use a prompt that encourages the model to extract broader insights
#         prompt = f"Imagine that you are a market analyst. Extract the main trends or insights from the following headlines for Adani Cement or Ambuja Cement: {combined_headlines}"

#         # Tokenize the input batch
#         inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=1024)
#         inputs = {key: value.to(device) for key, value in inputs.items()}

#         # Generate insights using the model
#         with torch.no_grad():
#             summary_ids = model.generate(inputs['input_ids'], max_length=200, num_beams=6, early_stopping=True, no_repeat_ngram_size=4)

#         # Decode and collect insights
#         batch_insights = [tokenizer.decode(summary_id, skip_special_tokens=True) for summary_id in summary_ids]
#         insights.extend(batch_insights)

#         # Clear GPU memory cache after each batch to avoid memory overload
#         torch.cuda.empty_cache()

#     return insights

# # Function to summarize the insights into 4 main points
# def summarize_insights(insights):
#     # Combine all insights into one string
#     combined_insights = " ".join(insights)

#     # Create a focused prompt for summarizing the insights into 4 main points
#     prompt = f"Imagine that you are tasked with providing a market report. Summarize the following insights into 4 concise and clear bullet points: {combined_insights}"

#     # Tokenize the input prompt
#     inputs = tokenizer.encode("summarize: " + prompt, return_tensors="pt", max_length=512, truncation=True)
#     inputs = inputs.to(device)

#     # Generate the summary with 4 main points
#     with torch.no_grad():
#         summary_ids = model.generate(inputs, max_length=200, num_beams=6, early_stopping=True, no_repeat_ngram_size=4)

#     # Decode the summary and return it
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary

# # Generate insights for the content (headlines) in batch
# insights_batch_bart = generate_batch_insights_bart(headlines)

# # Summarize the generated insights into 4 main points
# summary_of_insights = summarize_insights(insights_batch_bart)

# # Print the summary
# print("\nSummary of Insights (4 Main Points):")
# print(summary_of_insights)

# # Clear GPU memory cache
# torch.cuda.empty_cache()


from transformers import BartForConditionalGeneration, BartTokenizer
import torch
import pandas as pd
import json

# Set up for GPU if available
torch.cuda.empty_cache()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the distilled BART model and tokenizer
model_name = "sshleifer/distilbart-cnn-12-6"  # Distilled BART model for summarization
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

model.to(device)

# Load the new data from your JSON file into a DataFrame
json_file_path = '/home/chinmaya/Programming/news.json'  # Update to your correct file path
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Assuming the structure of the data is a list of dictionaries
df = pd.DataFrame(data)

# Only use the 'headline' field as content for generating insights
headlines = df['headline'].tolist()

# Handle None or missing datetime values by replacing with a default value
datetimes = df['article_datetime'].fillna('Unknown Date').tolist()  # Replace None with 'Unknown Date'

# Function to generate insights from a batch of headlines
def generate_batch_insights_bart(contents, datetimes, batch_size=512):  
    insights = []
    for i in range(0, len(contents), batch_size):
        batch_contents = contents[i:i + batch_size]
        batch_datetimes = datetimes[i:i + batch_size]  # Get the corresponding datetimes

        # Combine the headlines and datetimes into a single string to allow broader context
        combined_headlines = " ".join(batch_contents)
        combined_datetimes = " ".join(batch_datetimes)

        # Modify the prompt to include both the headlines and datetimes
        prompt = f"Imagine that you are a market analyst. Extract the main trends or insights from the following headlines and their respective dates for Adani Cement or Ambuja Cement: {combined_headlines} \n\nDates: {combined_datetimes}"

        # Tokenize the input batch
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=1024)
        inputs = {key: value.to(device) for key, value in inputs.items()}

        # Generate insights using the model
        with torch.no_grad():
            summary_ids = model.generate(inputs['input_ids'], max_length=200, num_beams=6, early_stopping=True, no_repeat_ngram_size=4)

        # Decode and collect insights
        batch_insights = [tokenizer.decode(summary_id, skip_special_tokens=True) for summary_id in summary_ids]
        insights.extend(batch_insights)

        # Clear GPU memory cache after each batch to avoid memory overload
        torch.cuda.empty_cache()

    return insights

# Function to summarize the insights into 4 main points
def summarize_insights(insights):
    # Combine all insights into one string
    combined_insights = " ".join(insights)

    # Create a focused prompt for summarizing the insights into 4 main points
    prompt = f"Imagine that you are tasked with providing a market report. Summarize the following insights into 4 concise and clear bullet points: {combined_insights}"

    # Tokenize the input prompt
    inputs = tokenizer.encode("summarize: " + prompt, return_tensors="pt", max_length=512, truncation=True)
    inputs = inputs.to(device)

    # Generate the summary with 4 main points
    with torch.no_grad():
        summary_ids = model.generate(inputs, max_length=200, num_beams=6, early_stopping=True, no_repeat_ngram_size=4)

    # Decode the summary and return it
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Generate insights for the content (headlines) in batch
insights_batch_bart = generate_batch_insights_bart(headlines, datetimes)

# Summarize the generated insights into 4 main points
summary_of_insights = summarize_insights(insights_batch_bart)

# Print the summary
print("\nSummary of Insights (4 Main Points):")
print(summary_of_insights)

# Clear GPU memory cache
torch.cuda.empty_cache()
