#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 00:01:00 2025

@author: chinmaya
"""
# Changes:
# Add article-after-date variable to skip articles beyond certain date - process_article_box().
# for failure to download with article, try to download using scrapy without selenium first, before falling back to scrapy with selenium - process_article_box(), follow_article().
# Build sample middleware with SQLAlchemy engine to try working with Postgres. - Pipeline file. Also separate code once JSON is complete.
# Check output for paywalled articles, build in paywall circumvention methods in case present.
# (Optional) Pass dictionary to follow_article() instead of function parameters - process_article_box().
# (Optional) Possibly form all urls and then yield from there - start_requests().
# Check storage options for data, complete html, etc. - Mongo, Postgres.
# Find options to train models to extract article from code. - Ollama, Pytorch.


# import asyncio
# import aiohttp
# from scrapy.utils.defer import deferred_from_coro

import scrapy
from googlenewsdecoder import gnewsdecoder
from newspaper import Article, ArticleException

from scrapy.http import HtmlResponse
from twisted.internet.error import ConnectionLost, TimeoutError

import re, uuid, string, os, json, logging #time
from datetime import datetime
from dotenv import load_dotenv
import requests


brand_path = '../../Config/ambuja.env'
language_path = '../Config/language_region_codes.env'
# language_path = '../Config/language_limited.env'

load_dotenv(dotenv_path=brand_path)
load_dotenv(dotenv_path=language_path)

def load_and_process_env_variable(env_var_name, fallback_path=''):
    # Fetch the raw string from the environment variable
    content = os.getenv(env_var_name, fallback_path)
    # Remove comments (lines starting with # or //)
    content = re.sub(r'^\s*(#|//).*$', '', content, flags=re.MULTILINE)
    # Strip any leading/trailing whitespace
    content = content.strip()  
    try:
        # Convert the cleaned JSON string into a Python dictionary
        parsed_data = json.loads(content)
        return parsed_data
    except json.JSONDecodeError as e:
        print(f"Failed to decode the JSON from the environment variable '{env_var_name}': {e}")
        return {}

class NewsscrapeSpider(scrapy.Spider):
    name = "newsscrape"

    # Load and clean up the values from the .env files for client
    brands_client = os.getenv('BRANDS')
    search_terms_client = [term.strip() for term in os.getenv('SEARCH_TERMS', '').split(',')] if os.getenv('SEARCH_TERMS') else []
    count_part_terms_client = [term.strip() for term in os.getenv('COUNT_PART_TERMS', '').split(',')] if os.getenv('COUNT_PART_TERMS') else []
    count_full_term_only_client = [term.strip() for term in os.getenv('COUNT_FULL_TERM_ONLY', '').split(',')] if os.getenv('COUNT_FULL_TERM_ONLY') else []
    
    # Load and clean up the values from the .env files for competitor
    brands_competitor = os.getenv('BRANDS_COMPETITOR')
    search_terms_competitor = [term.strip() for term in os.getenv('SEARCH_TERMS_COMPETITOR', '').split(',')] if os.getenv('SEARCH_TERMS_COMPETITOR') else []
    count_part_terms_competitor = [term.strip() for term in os.getenv('COUNT_PART_TERMS_COMPETITOR', '').split(',')] if os.getenv('COUNT_PART_TERMS_COMPETITOR') else []
    count_full_term_only_competitor = [term.strip() for term in os.getenv('COUNT_FULL_TERM_ONLY_COMPETITOR', '').split(',')] if os.getenv('COUNT_FULL_TERM_ONLY_COMPETITOR') else []
    
    search_terms = search_terms_client + search_terms_competitor
    count_full_term_only = count_full_term_only_client + count_full_term_only_competitor
    
    supported_language_region_codes = load_and_process_env_variable('LANGUAGE_REGION_CODES')
    unsupported_language_region_codes = load_and_process_env_variable('UNSUPPORTED_CODES')
    all_language_region_codes = {**supported_language_region_codes, **unsupported_language_region_codes}

    

    # Define XPaths for scraping
    article_box_xpath = '//c-wiz[@class="PO9Zff Ccj79 kUVvS"]'
    headline_xpath = './/a[contains(@class,"JtKRv")]'
    datetime_xpath = './/div[contains(@class,"UOVeFe")]/time/@datetime'
    href_path = './/a[@class="JtKRv"]/@href'

    # Function to remove whitespace and punctuation.    
    def clean_text(*texts):
        # Replace None or unexpected blank values with empty strings
        cleaned_texts = [text if text and isinstance(text, str) else '' for text in texts]
        
        # Join the texts, remove punctuations, lowercase, and clean extra spaces
        combined_text = ' '.join(cleaned_texts)
        combined_text = combined_text.translate(str.maketrans('', '', string.punctuation)).lower().strip()          
        combined_text = combined_text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
        combined_text = ' '.join(combined_text.split())  # Remove multiple spaces
        return combined_text
    # Remove only whitespaces
    def clean_spaces(*texts):
        # Replace None or unexpected blank values with empty strings
        cleaned_texts = [text if text and isinstance(text, str) else '' for text in texts]
        
        # Join the texts, remove punctuations, lowercase, and clean extra spaces
        combined_text = ' '.join(cleaned_texts)
        combined_text = combined_text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
        combined_text = ' '.join(combined_text.split())  # Remove multiple spaces
        return combined_text
    
    # Create all requests in tasks, assign session and start executing asynchronously
    def start_requests(self):
        self.logger.debug(f"BRANDS: {self.brands_client}")
        self.logger.debug(f"SEARCH_TERMS: {self.search_terms_client}")
        self.logger.debug(f"COUNT_PART_TERMS: {self.count_part_terms_client}")
        self.logger.debug(f"COUNT_FULL_TERM_ONLY: {self.count_full_term_only_client}")
        self.logger.debug(f"\n\nBRANDS: {self.brands_competitor}")
        self.logger.debug(f"SEARCH_TERMS: {self.search_terms_competitor}")
        self.logger.debug(f"COUNT_PART_TERMS: {self.count_part_terms_competitor}")
        self.logger.debug(f"COUNT_FULL_TERM_ONLY: {self.count_full_term_only_competitor}")
        self.logger.debug(f"LANGUAGE_REGION_CODES (Newspaper3k supported): {os.getenv('LANGUAGE_REGION_CODES')}")
        self.logger.debug(f"LANGUAGE_REGION_CODES (Not Newspaper3k supported): {os.getenv('UNSUPPORTED_CODES')}")
        # self.logger.debug(f"\n\n\n\n\n\n\n\n  LANGUAGE_REGION_CODES: {self.all_language_region_codes}")     

        for term in self.search_terms:
            search_term = term.replace(" ", "+")
            # self.logger.warning(f"\n\n\n\n\n\n\n\nNew search term found: {search_term}\n\n\n\n\n\n\n\n")
            for language, data in self.all_language_region_codes.items():
                search_url = f"https://news.google.com/search?q={search_term}&hl={language}&gl={data['region']}"
                metadata = {
                    'search_term': term,
                    'language': language,
                    'region': data['region'],
                    'country_name': data['country_name'],
                    'country_language': data['language'],
                }
                html_body = requests.get(search_url)
                # self.logger.warning(f"\n\n\n\n\n\n\n\nNew search term requested in new language: {data['language']}\n\n\n\n\n\n\n\n")
                request = scrapy.Request(url=search_url, callback=self.parse, meta=metadata)
                html_content = HtmlResponse(url=search_url, body= html_body.content, encoding='utf-8', request = request)
                html_content.meta.update(metadata)
                yield from self.extract_article_data(html_content)   
            
    def extract_article_data(self, response):
        article_boxes = response.xpath(self.article_box_xpath)
        self.logger.info(f'{len(article_boxes)} articles retrieved')
        for box in article_boxes:
            yield from self.process_article_box(box,response)
        
    def process_article_box(self, box,response):
        # Extract the article link and headline
        headline = box.xpath(self.headline_xpath + '/text()').get().strip() if box.xpath(self.headline_xpath) else 'No Headline'
        
        # Get datetime from the article
        datetime_str = box.xpath(self.datetime_xpath).get()
        dt = None
        if datetime_str:
            try:
                if 'Z' in datetime_str:
                    datetime_str = datetime_str.replace('Z', '+00:00')
                dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
            except ValueError as e:
                logging.error(f"Error parsing datetime: {e}")

        datetime_sql = dt.isoformat() if dt else None
        
        href_value = box.xpath(self.href_path).get()
        link = f"https://news.google.com{href_value.lstrip('.')}" if href_value else ''
        source_link = link
        
        try:
            # Decode the URL using gnewsdecoder
            decoded_url = gnewsdecoder(link, interval=1)
            if decoded_url.get("status"):
                source_link = decoded_url["decoded_url"]
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            
        transaction_id = str(uuid.uuid4()) 
        if response.meta['language'] not in self.unsupported_language_region_codes:
            yield from self.follow_article(response, source_link, headline, datetime_sql, transaction_id)
        else:
            metadata = {
                    'transaction_id':transaction_id,
                    'search_term': response.meta.get('search_term'),
                    'language': response.meta.get('language'),
                    'region': response.meta.get('region'),
                    'country_name': response.meta.get('country_name'),
                    'country_language': response.meta.get('country_language'),
                    'source_link':source_link,
                    'headline':headline,
                    'article_datetime':datetime_sql,
                }
            try:
                yield response.follow(url=source_link, callback=self.parse_article, meta = metadata)
            except (ArticleException, ConnectionLost, TimeoutError) as e:
                try:
                    self.logger.error(f"Failed to download {source_link} using scrapy: {e}. Retrying using Selenium")
                    metadata.update({'selenium':True})
                    yield response.follow(url=source_link, callback=self.parse_article, meta = metadata)
                    self.logger.error(f"\n\n\n\n\n\nSuccessfully downloaded article from {source_link} upon retry.\n\n\n\n\n\n")
                except:
                    self.logger.info(f"Failed to download article: {source_link}.")

    def follow_article(self, response, source_link, headline, datetime_sql, transaction_id):
        # Prepare the article metadata
        # meta = response.meta
        # self.logger.warning(f"\n\n\n\n\n\n\n\nsource link:{source_link}\n\n\n\n\n\n\n\n")
        meta = {
            'transaction_id': transaction_id,
            'search_term': response.meta.get('search_term'),
            'country_name': response.meta.get('country_name'),
            'country_language': response.meta.get('country_language'),
            'headline': headline,
            'article_datetime': datetime_sql,
            'source_link': source_link,
            }
        # self.logger.warning(f"\n\n\n\n\n\n\n\nsource metadata :{meta}\n\n\n\n\n\n\n\n")          
        try:
            article = Article(source_link)
            article.download()
            article.parse()
            # meta = response.meta
            # article_test_data = article.meta_description
            # self.logger.warning(f"\n\n\n\n\n\n\n\article_test_data: {article_test_data}\n\n\n\n\n\n\n\n")            
            
            meta.update({
                'description': article.meta_description,
                'article_body': article.text,
                'authors': article.authors,
                'keywords': article.meta_keywords,
                'tags': article.tags,
                'article_images': article.meta_img,
                'all_images': article.images,
                'article_metadata': article.meta_data,
            })
            # self.logger.warning(f"\n\n\n\n\n\n\n\nupdated metadata: {meta}\n\n\n\n\n\n\n\n")
            yield response.follow(url=source_link, callback=self.parse_article, meta = meta)
                    
        except (ArticleException,ConnectionLost, TimeoutError) as e:
            self.logger.error(f"\n\n\n\n\n\nFailed to download article from {source_link} using Article. Error: {str(e)}")
            try:
                self.logger.info(f"Trying to download {source_link} using Selenium\n\n\n\n")
                meta.update({'selenium':True})
                yield response.follow(url=source_link, callback=self.parse_article, meta = meta)
            except:
                self.logger.error(f"Failed to download article: {source_link}.")

    def parse_article(self, response):
        # Get the full URL of the page
        # self.logger.warning("\n\n\n\n\n\n\n\n Parse Article Called here \n\n\n\n\n\n\n\n")
        self.logger.info(f"visiting url: {response.meta['source_link']}")
        # meta = response.meta
        # self.logger.warning(f"\n\n\n\n\n\n\n\n passed metadata: {response.meta}\n\n\n\n\n\n\n\n")
        
        source_html = response.text

        # Search for description
        if(response.meta.get('description')):
            description = response.meta.get('description')
        else:
            try:
                description = response.xpath("//meta[contains(@property,'description')]/@content").get()
                if not description:
                    raise ValueError("No content found for description")
            except Exception:
                try:
                    description = response.xpath("//meta[contains(@name,'description')]/@content").get()
                    if not description:
                        raise ValueError("No content found for description")
                except Exception:
                    description = "Not Available"

        # Search for author
        if(response.meta.get('authors')):
            authors = response.meta.get('authors')
        else:                 
            try:
                authors = response.xpath("//meta[contains(@property,'site_name')]/@content").get()
                if not authors:  # If no content is found, handle it
                    raise ValueError("No content found for author")
            except Exception:
                try:
                    authors = response.xpath("//meta[contains(@name,'site_name')]/@content").get()
                    if not authors:
                        raise ValueError("No content found for author")
                except Exception:
                    try:
                        pattern = r"https?://(?:[a-zA-Z0-9-]+\.)?([a-zA-Z0-9-]+)(?=\.[a-zA-Z]+(?:\/|$))"
                        match = re.search(pattern, response.meta['source_link'])
                        if match:
                            authors = match.group(1)  # This will print the domain name
                    except Exception:
                        authors = "Not Available"  # Default to "Not Available" if both fail
 
               
        try:
            source = response.xpath("//meta[contains(@property,'site_name')]/@content").get()
            if not source:  # If no content is found, handle it
                raise ValueError("No content found for og:site_name")
        except Exception:
            try:
                source = response.xpath("//meta[contains(@name,'site_name')]/@content").get()
                if not source:
                    raise ValueError("No content found for og:site_name")
            except Exception:
                try:
                    pattern = r"https?://(?:[a-zA-Z0-9-]+\.)?([a-zA-Z0-9-]+)(?=\.[a-zA-Z]+(?:\/|$))"
                    match = re.search(pattern, response.meta['source_link'])
                    if match:
                        source = match.group(1)  # This will print the domain name
                except Exception:
                    source = "Not Available"  # Default to "Not Available" if both fail
                    
        # Search for keywords
        if(response.meta.get('keywords')):
            keywords = response.meta.get('keywords')
        else:                 
            try:
                keywords = response.xpath("//meta[contains(@name,'keywords')]/@content").get()
                if not keywords:  # If no content is found, handle it
                    raise ValueError("No content found for keywords")
            except Exception:
                try:
                    keywords = response.xpath("//meta[contains(@name,'news_keywords')]/@content").get()
                    if not keywords:
                        raise ValueError("No content found for keywords")
                except Exception:
                    try:
                        keywords = response.xpath("//meta[contains(@property,'keywords')]/@content").get()
                        if not keywords:  # If no content is found, handle it
                            raise ValueError("No content found for keywords")
                    except Exception:
                        try:
                            keywords = response.xpath("//meta[contains(@property,'news_keywords')]/@content").get()
                            if not keywords:
                                raise ValueError("No content found for keywords")
                        except Exception:
                            keywords = "Not Available"  # Default to "Not Available" if both fail
        if(response.meta.get('tags')):
            tags = response.meta.get('tags')
        else:
            tags=[]
            
        if(response.meta.get('article_images')):
            images = response.meta.get('article_images')
        else:
            images=[]
                        
        if(response.meta.get('all_images')):
            all_images = response.meta.get('all_images')
        else:
            all_images=[]
            
        if(response.meta.get('article_metadata')):
            article_metadata = response.meta.get('article_metadata')
        else:
            article_metadata=[]
            
        if(response.meta.get('article_body')):
            article_body = response.meta.get('article_body')
        else:
            article_body=[]
        
        
                
        # Join headline and description, clean string by removing punctuation, make lowercase
        clean_search_string = self.clean_text(response.meta.get('headline'),description,article_body)
        
        # Create a dictionary to store product matches with 0 count
        product_match = {term: 0 for term in self.count_part_terms_client + self.count_full_term_only_client + self.count_full_term_only_competitor + self.count_part_terms_competitor}
        
        # First pass: Count full terms
        for term in self.count_part_terms_client + self.count_full_term_only_client + self.count_full_term_only_competitor + self.count_part_terms_competitor:
            clean_term = self.clean_text(term)
            
            # Count the full term occurrences
            full_term_count = len(re.findall(r'\b' + re.escape(clean_term) + r'\b', clean_search_string))
            
            if full_term_count > 0:
                product_match[term] += full_term_count
                
        # Second pass: Count partial terms independently, but not if already counted as full term
        for term in self.count_part_terms_client + self.count_part_terms_competitor:
            clean_term = self.clean_text(term)
        
            # Remove any brand terms from both client and competitor brands if they are a prefix in the partial term
            clean_term_without_brand = clean_term
            for brand in self.brands_client + self.brands_competitor:  # Combine both client and competitor brands
                clean_brand = self.clean_text(brand)
                
                # Check if the partial term starts with any of the brand terms
                if clean_term.startswith(clean_brand):
                    # If yes, remove the brand term from the search string
                    clean_term_without_brand = clean_term.replace(clean_brand, '', 1)  # Only remove the first occurrence
            
            # Count the partial term only if it's not already counted as part of the full term
            if clean_term_without_brand in clean_search_string:
                # Ensure it's not part of the full term already counted
                if not re.search(r'\b' + re.escape(clean_term) + r'\b', clean_search_string):
                    cleaned_term_count = len(re.findall(r'\b' + re.escape(clean_term_without_brand) + r'\b', clean_search_string))
                    product_match[term] += cleaned_term_count
        
        item =  {
                'transaction_id': response.meta.get('transaction_id'),
                'article_datetime': response.meta.get('article_datetime'),
                'search_term': response.meta.get('search_term'),
                'country_name': response.meta.get('country_name'),      
                'country_language': response.meta.get('country_language'),
                'news_source': source,
                'authors':authors,
                'headline': response.meta.get('headline'),
                'description': description,
                'article_body':article_body,
                'source_link': response.meta.get('source_link'),
                'keywords':keywords,
                'tags':tags,
                'article_images':images,
                'all_images':all_images,
                'article_metadata':article_metadata,
                'full_html':source_html,
                #'source': domain,  # Extracted domain (website source)
                **{f"{term.replace(' ', '_').lower()}_count": product_match.get(term, 0) for term in self.count_part_terms_client + self.count_part_terms_competitor + self.count_full_term_only_client + self.count_full_term_only_competitor}          
            }
        
        # self.logger.info(f"\n\n\n\nYielding item: {item}\n\n\n\n")

        yield item