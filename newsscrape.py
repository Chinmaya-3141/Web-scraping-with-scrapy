# Changes
# Fetch with requests.get(), or scrapy-playwright https://github.com/scrapy-plugins/scrapy-playwright
# Remove selenium middleware and test
# parse with newspaper3k package
# build in exception for regional languages.
# check if gnewsdecode can work without 1 second wait
# news_keywords, article.metadata, tags


# from twisted.internet.threads import deferToThread
# from scrapy_splash import SplashRequest
import scrapy
from scrapy.http import HtmlResponse, Request
import requests
import re, uuid, string, os, json, logging, time
from datetime import datetime
from googlenewsdecoder import gnewsdecoder
from dotenv import load_dotenv
from newspaper import Article

brand_path = '../../Config/ambuja.env'
# language_path = '../Config/language_region_codes.env'
language_path = '../Config/language_limited.env'

load_dotenv(dotenv_path=brand_path)
load_dotenv(dotenv_path=language_path)


class NewsscrapeSpider(scrapy.Spider):
    name = "newsscrape"
    # allowed_domains = ["news.google.com"]    

    # Load and clean up the values from the .env file, ensuring empty lists for missing or empty values
    brands = os.getenv('BRANDS')
    search_terms = [term.strip() for term in os.getenv('SEARCH_TERMS', '').split(',')] if os.getenv('SEARCH_TERMS') else []
    count_part_terms = [term.strip() for term in os.getenv('COUNT_PART_TERMS', '').split(',')] if os.getenv('COUNT_PART_TERMS') else []
    count_full_term_only = [term.strip() for term in os.getenv('COUNT_FULL_TERM_ONLY', '').split(',')] if os.getenv('COUNT_FULL_TERM_ONLY') else []

    # Load the language-region-pairs
    language_region_codes_str = os.getenv('LANGUAGE_REGION_CODES', '{}')  # Default to an empty dictionary if not set
    
    try:
        # Convert the JSON string to a dictionary
        language_region_codes = json.loads(language_region_codes_str)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode LANGUAGE_REGION_CODES JSON: {e}")
        language_region_codes = {}  # Fallback to an empty dictionary

    # Define XPaths for scraping
    article_box_xpath = '//c-wiz[@class="PO9Zff Ccj79 kUVvS"]'
    headline_xpath = './/a[contains(@class,"JtKRv")]'
    datetime_xpath = './/div[contains(@class,"UOVeFe")]/time/@datetime'
    href_path = './/a[@class="JtKRv"]/@href'        

    # def start_requests(self):
    #     self.logger.debug(f"BRANDS: {os.getenv('BRANDS')}")
    #     self.logger.debug(f"SEARCH_TERMS: {os.getenv('SEARCH_TERMS')}")
    #     self.logger.debug(f"COUNT_PART_TERMS: {os.getenv('COUNT_PART_TERMS')}")
    #     self.logger.debug(f"COUNT_FULL_TERM_ONLY: {os.getenv('COUNT_FULL_TERM_ONLY')}")
    #     self.logger.debug(f"LANGUAGE_REGION_CODES: {os.getenv('LANGUAGE_REGION_CODES')}")

    #     for term in self.search_terms:
    #         search_term = term.replace(" ", "+")  # Format the term for URL
            
    #         # Loop through the language-region mapping to create search URLs
    #         for language, data in self.language_region_codes.items():
    #             search_url = f"https://news.google.com/search?q={search_term}&hl={language}&gl={data['region']}"
                
    #             # Use the 'selenium' flag only for the pages that require JavaScript rendering
    #             yield scrapy.Request(
    #                 url=search_url,
    #                 callback=self.extract_article_data,
    #                 meta={
    #                     'search_term': term,
    #                     'language': language,
    #                     'region': data['region'],
    #                     'country_name': data['country_name'],
    #                     'country_language': data['language'],
    #                     'selenium': True,  # Set this to True for JavaScript-rendered pages
    #                 }
    #             )


    def start_requests(self):
        self.logger.debug(f"BRANDS: {os.getenv('BRANDS')}")
        self.logger.debug(f"SEARCH_TERMS: {os.getenv('SEARCH_TERMS')}")
        self.logger.debug(f"COUNT_PART_TERMS: {os.getenv('COUNT_PART_TERMS')}")
        self.logger.debug(f"COUNT_FULL_TERM_ONLY: {os.getenv('COUNT_FULL_TERM_ONLY')}")
        self.logger.debug(f"LANGUAGE_REGION_CODES: {os.getenv('LANGUAGE_REGION_CODES')}")
        for term in self.search_terms:
            search_term = term.replace(" ", "+")  # Format the term for URL
            
            # Loop through the language-region mapping to create search URLs
            for language, data in self.language_region_codes.items():
                search_url = f"https://news.google.com/search?q={search_term}&hl={language}&gl={data['region']}"
                page_html = requests.get(search_url)
                
                # Prepare metadata to be passed to parse
                metadata = {
                    'search_term': term,
                    'language': language,   
                    'region': data['region'],
                    'country_name': data['country_name'],
                    'country_language': data['language'],
                }
                time.sleep(1)
                response = HtmlResponse(url=search_url, 
                                        body=page_html.text, 
                                        encoding='utf-8',
                                        request=Request(url=search_url))
                
                response.meta.update(metadata)
                self.logger.info(f"metadata = {response.meta}")
        
                # Call the parse method on the response with the fully rendered HTML
                yield from self.extract_article_data(response)   
    
    def extract_article_data(self, response):
        article_boxes = response.xpath(self.article_box_xpath)
        self.logger.info(f'articles: {len(article_boxes)}')
        art = []
        head=[]
        for box in article_boxes:
            headline = box.xpath(self.headline_xpath + '/text()').get().strip() if box.xpath(self.headline_xpath) else 'No Headline'
            head.append(headline)
            href_value = box.xpath(self.href_path).get()
            if href_value:
                href_value = href_value.lstrip('.')
            else:
                href_value = ''
                
            link = "https://news.google.com" + href_value.replace('\n','').replace('\r','').replace('\t','').replace(' ','')
            source_link = link
            try:
                decoded_url = gnewsdecoder(link, interval=1)
        
                if decoded_url.get("status"):
                    source_link=decoded_url["decoded_url"]
                    art.append(source_link)
                else:
                    logging.error(f"Error:{decoded_url['message']}")
                    art.append(f"{decoded_url['message']}")
            except Exception as e:
                logging.error(f"Error occurred: {e}")
                art.append('Error')
        self.logger.info("\n\n\n\n\n\n Yielding \n\n\n\n\n\n")
        yield{
            'articles':len(article_boxes),
            'headlines':len(head),
            'headlines_list':head,
            'source_url':len(art),
            'url_list':art,
            'term':response.meta['search_term'],
            'language':response.meta['country_language'],
            'country':response.meta['country_name'],

            }

















                
#     def extract_article_data(self, response):
#         article_boxes = response.xpath(self.article_box_xpath)
#         self.logger.info(f'\n\n\n\n\n\n {len(article_boxes)} articles retrieved \n\n\n\n\n\n')

#         # Loop over each article box on the page
#         for box in article_boxes:
#             # Generating a unique UUID for the article
#             transaction_id = str(uuid.uuid4())
#             # Get article URL
#             href_value = box.xpath(self.href_path).get()
#             if href_value:
#                 href_value = href_value.lstrip('.')
#             else:
#                 href_value = ''
                
#             link = "https://news.google.com" + href_value.replace('\n','').replace('\r','').replace('\t','').replace(' ','')
#             source_link = link
#             try:
#                 decoded_url = gnewsdecoder(link, interval=3)
        
#                 if decoded_url.get("status"):
#                     source_link=decoded_url["decoded_url"]
#                 else:
#                     logging.error(f"Error:{decoded_url['message']}")
#             except Exception as e:
#                 logging.error(f"Error occurred: {e}")
                
#             # Get headline
#             headline = box.xpath(self.headline_xpath + '/text()').get().strip() if box.xpath(self.headline_xpath) else 'No Headline'
            
#             # Get datetime from the article
#             datetime_str = box.xpath(self.datetime_xpath).get()
#             if datetime_str:
#                 try:
#                     # If the string has 'Z' indicating UTC time, replace it with '+00:00'
#                     if 'Z' in datetime_str:
#                         datetime_str = datetime_str.replace('Z', '+00:00')  
            
#                     # Attempt to parse the datetime with timezone information
#                     dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")  # Use %z to parse the timezone
#                 except ValueError as e:
#                     # Optional: Log the error or handle it as needed
#                     print(f"Error parsing datetime: {e}")
#                     dt = None
#             else:
#                 dt = None
            
#             # Format datetime to the desired ISO 8601 format with timezone
#             if dt:
#                 # Format datetime to include the timezone with colon in the format: YYYY-MM-DDTHH:MM:SS+00:00
#                 datetime_sql = dt.isoformat()  # isoformat handles both formatting and timezone
#             else:
#                 datetime_sql = None
                
#             if response.meta['language'] not in([
#     "ja-JP", "ms-MY", "ca-ES", "cs-CZ", "et-EE", "lv-LV", "lt-LT", "ro-RO", 
#     "sk-SK", "sl-SI", "bg-BG", "sr-RS", "mr-IN", "hi-IN", "bn-BD", "bn-IN", 
#     "pa-IN", "gu-IN", "ta-IN", "te-IN", "ml-IN", "th-TH"
# ]):  
#                 article = Article(source_link)
#                 article.download()
#                 article.parse()
#                 yield response.follow(
#                                         source_link,
#                                         callback=self.parse_article,
#                                         meta={
#                                             'transaction_id': transaction_id,
#                                             'search_term': response.meta['search_term'],
#                                             'country_name': response.meta['country_name'],
#                                             'country_language': response.meta['country_language'],
#                                             'headline': headline,
#                                             'description':article.meta_description,
#                                             'article_body':article.text,
#                                             'authors':article.authors,
#                                             'article_datetime': datetime_sql,
#                                             'source_link': source_link,
#                                             'keywords':article.meta_keywords,
#                                             'tags':article.tags,
#                                             'article_images':article.meta_img,
#                                             'all_images':article.images,
#                                             'article_metadata':article.meta_data,
#                                             }
#                                         )
#             else:
#                 yield response.follow(
#                                         source_link,
#                                         callback=self.parse_article,
#                                         meta={
#                                             'transaction_id': transaction_id,
#                                             'search_term': response.meta['search_term'],
#                                             'country_name': response.meta['country_name'],
#                                             'country_language': response.meta['country_language'],
#                                             'headline': headline,
#                                             'article_datetime': datetime_sql,
#                                             'source_link': source_link,
#                                             }
#                                         )

#     def parse_article(self, response):
#         # Get the full URL of the page
#         self.logger.info(f"visiting url: {response.meta['source_link']}")
        
#         # Remove punctuation (e.g., .,!,? etc.), convert to lowercase, join.
#         def clean_text(*texts):
#             combined_text = ' '.join(texts)
#             # Remove punctuations, '\n' like characters.
#             combined_text = combined_text.translate(str.maketrans('', '', string.punctuation)).lower().strip()          
#             combined_text = combined_text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
#             # Split and rejoin all words to remove multiple spaces
#             combined_text = ' '.join(combined_text.split())
#             return combined_text
        


#         # Search for description
#         if(response.meta.get('description')):
#             self.logger.info("\n\n\n\n\n\n\n executed \n\n\n\n\n\n\n\n")
#             description = response.meta['description']
#         else:
#             try:
#                 description = response.xpath("//meta[@property='og:description']/@content").get()
#                 if not description:
#                     raise ValueError("No content found for og:description")
#             except Exception:
#                 try:
#                     description = response.xpath("//meta[@name='og:description']/@content").get()
#                     if not description:
#                         raise ValueError("No content found for og:description")
#                 except Exception:
#                     description = "Not Available"

#         # Search for author
#         if(response.meta['authors']):
#             authors = response.meta['authors']
#         else:                 
#             try:
#                 authors = response.xpath("//meta[@property='og:site_name']/@content").get()
#                 if not authors:  # If no content is found, handle it
#                     raise ValueError("No content found for author")
#             except Exception:
#                 try:
#                     authors = response.xpath("//meta[@name='og:site_name']/@content").get()
#                     if not authors:
#                         raise ValueError("No content found for author")
#                 except Exception:
#                     try:
#                         pattern = r"https?://(?:[a-zA-Z0-9-]+\.)?([a-zA-Z0-9-]+)(?=\.[a-zA-Z]+(?:\/|$))"
#                         match = re.search(pattern, response.meta['source_link'])
#                         if match:
#                             authors = match.group(1)  # This will print the domain name
#                     except Exception:
#                         authors = "Not Available"  # Default to "Not Available" if both fail
 
               
#         try:
#             source = response.xpath("//meta[@property='og:site_name']/@content").get()
#             if not source:  # If no content is found, handle it
#                 raise ValueError("No content found for og:site_name")
#         except Exception:
#             try:
#                 source = response.xpath("//meta[@name='og:site_name']/@content").get()
#                 if not source:
#                     raise ValueError("No content found for og:site_name")
#             except Exception:
#                 try:
#                     pattern = r"https?://(?:[a-zA-Z0-9-]+\.)?([a-zA-Z0-9-]+)(?=\.[a-zA-Z]+(?:\/|$))"
#                     match = re.search(pattern, response.meta['source_link'])
#                     if match:
#                         source = match.group(1)  # This will print the domain name
#                 except Exception:
#                     source = "Not Available"  # Default to "Not Available" if both fail
                    
#         # Search for keywords
#         if(response.meta['keywords']):
#             keywords = response.meta['keywords']
#         else:                 
#             try:
#                 keywords = response.xpath("//meta[@name='keywords']/@content").get()
#                 if not keywords:  # If no content is found, handle it
#                     raise ValueError("No content found for keywords")
#             except Exception:
#                 try:
#                     keywords = response.xpath("//meta[@name='news_keywords']/@content").get()
#                     if not keywords:
#                         raise ValueError("No content found for author")
#                 except Exception:
#                     try:
#                         keywords = response.xpath("//meta[@property='keywords']/@content").get()
#                         if not keywords:  # If no content is found, handle it
#                             raise ValueError("No content found for keywords")
#                     except Exception:
#                         try:
#                             keywords = response.xpath("//meta[@property='news_keywords']/@content").get()
#                             if not keywords:
#                                 raise ValueError("No content found for keywords")
#                         except Exception:
#                             keywords = "Not Available"  # Default to "Not Available" if both fail
#         if(response.meta['tags']):
#             tags = response.meta['tags']
#         else:
#             tags=[]
            
#         if(response.meta['article_images']):
#             images = response.meta['article_images']
#         else:
#             images=[]
                        
#         if(response.meta['all_images']):
#             all_images = response.meta['all_images']
#         else:
#             all_images=[]
            
#         if(response.meta['article_metadata']):
#             article_metadata = response.meta['article_metadata']
#         else:
#             article_metadata=[]
            
#         if(response.meta['article_body']):
#             article_body = response.meta['article_body']
#         else:
#             article_body=[]
                
#         # Join headline and description, clean string by removing punctuation, make lowercase
#         clean_search_string = clean_text(response.meta['headline'],description)
        
#         # Create a dictionary to store product matches with 0 count
#         product_match = {term: 0 for term in self.count_part_terms + self.count_full_term_only}
        
#         # First pass: Count full terms
#         for term in self.count_part_terms + self.count_full_term_only:
#             clean_term = clean_text(term)
            
#             # Count the full term occurrences
#             full_term_count = len(re.findall(r'\b' + re.escape(clean_term) + r'\b', clean_search_string))
            
#             if full_term_count > 0:
#                 product_match[term] += full_term_count
#         # Second pass: Count partial terms independently, but not if already counted as full term
#         for term in self.count_part_terms:
#             clean_term = clean_text(term)

#             # Clean the term without the brand name dynamically using brand
#             clean_term_without_brand = clean_term.replace(clean_text(self.brands), '')
            
#             # Count the partial term only if it's not already counted as part of the full term
#             if clean_term_without_brand in clean_search_string:
#                 # Ensure it's not part of the full term already counted
#                 if not re.search(r'\b' + re.escape(clean_term) + r'\b', clean_search_string):
#                     cleaned_term_count = len(re.findall(r'\b' + re.escape(clean_term_without_brand) + r'\b', clean_search_string))
#                     product_match[term] += cleaned_term_count


        
#         item =  {
#                 'transaction_id': response.meta['transaction_id'],
#                 'article_datetime': response.meta['article_datetime'],
#                 'search_term': response.meta['search_term'],
#                 'country_name': response.meta['country_name'],      
#                 'country_language': response.meta['country_language'],
#                 'news_source': source,
#                 'authors':authors,
#                 'headline': response.meta['headline'],
#                 'description': description,
#                 # 'article_body':article_body,
#                 'source_link': response.meta['source_link'],
#                 'keywords':keywords,
#                 'tags':tags,
#                 'article_images':images,
#                 'all_images':all_images,
#                 # 'article_metadata':article_metadata,
#                 #'source': domain,  # Extracted domain (website source)
#                 **{f"{term.replace(' ', '_').lower()}_count": product_match.get(term, 0) for term in self.count_part_terms + self.count_full_term_only}          
#             }
        
#         self.logger.info(f"Yielding item: {item}")
        
#         yield item














# Use package newspaper3k

    # def parse_article(self, response):
    #     # Get the full URL of the article
    #     full_url = response.url
    #     time.sleep(random.uniform(1, 2))
    #     # Create an Article object using the full URL
    #     article = Article(full_url)
        
    #     # Download and parse the article
    #     article.download()
    #     article.parse()
    
    #     # Extract article details
    #     article_text = article.text  # The main article body
    #     article_description = article.meta_description  # The meta description
    #     article_sitename = article.source_url  # The source URL (website hosting the article)
    #     article_url = article.source_url  # The full article URL
        
    #     # Attempt to get source name from the meta data (if available)
    #     try:
    #         source = response.xpath("//meta[@property='og:site_name']/@content").get()
    #         if not source:  # If no content is found, handle it
    #             source = "Not Available"
    #     except Exception:
    #         source = "Not Available"
    
    #     # Prepare the final dictionary to return (this is the final yield)
    #     yield {
    #         'transaction_id': response.meta['transaction_id'],  
    #         'search_term': response.meta['search_term'],        
    #         'country_name': response.meta['country_name'],      
    #         'country_language': response.meta['country_language'],
    #         'news_source': source,
    #         'headline': response.meta['headline'],
    #         'description': article_description,  # Article's meta description
    #         'article_datetime': response.meta['article_datetime'],
    #         'source_link': article_url,  # The URL of the article
    #         # 'full_html': article.html,  # Full HTML content of the article
    #         'article_text': article_text,  # Main article content
    #         'sitename': article_sitename,  # Source website
    #         **{f"{term.replace(' ', '_').lower()}_count": response.meta['product_match'].get(term, 0) for term in self.count_if_without_ambuja + self.count_if_full_term_only}          
    #     }
        
        
        
        
# # Lua script for scrolling the page

# scroll_script = """
# function main(splash)
#     splash.private_mode_enabled = false
#     splash:set_viewport_full()  -- Set the viewport to full size

#     -- Go to the target URL
#     splash:go(splash.args.url)
#     splash:wait(2)  -- Wait a bit longer for the initial page to load

#     local max_scrolls = 10  -- Maximum number of scrolls
#     local current_scrolls = 0
#     local last_article_count = 0
#     local new_article_count = 0

#     -- Loop through scrolling and loading content
#     while current_scrolls < max_scrolls do
#         -- Scroll down by 300 pixels
#         splash:runjs('window.scrollBy(0, 300);')
#         splash:wait(3)  -- Wait for new content to load (3 seconds)

#         -- Check how many articles are loaded after the scroll using the new CSS selector
#         new_article_count = splash:runjs('return document.querySelectorAll("c-wiz.PO9Zff").length')

#         -- Debugging: Check the number of articles loaded
#         print("Articles loaded after scroll: " .. tostring(new_article_count))

#         -- If no new articles are loaded, break the loop
#         if new_article_count == last_article_count then
#             print("No new content loaded. Stopping scroll.")
#             break
#         end

#         -- Update variables for the next iteration
#         last_article_count = new_article_count
#         current_scrolls = current_scrolls + 1
#     end

#     -- Ensure the page has loaded and capture the HTML content
#     local page_html = splash:html()

#     -- Return the HTML content of the page for Scrapy to continue scraping
#     return {
#         html = page_html,
#         url = splash.args.url,  -- Return the URL to continue scraping
#         status_code = 200,      -- Return the status code
#     }
# end
# """

