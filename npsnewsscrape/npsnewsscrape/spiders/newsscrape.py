import scrapy
import re, uuid, string
from datetime import datetime
from googlenewsdecoder import gnewsdecoder
# from twisted.internet.threads import deferToThread

# from scrapy_splash import SplashRequest

class NewsscrapeSpider(scrapy.Spider):
    name = "newsscrape"
    # allowed_domains = ["news.google.com"]
    
    # Class variables for brand/product lines
    brands = ['Ambuja Cements', 'ACC Limited', 'Orient Cement']
    # brands = ['Ambuja Cements']
    count_if_without_ambuja = ['Ambuja Kawach', 'Ambuja Cool Walls', 'Ambuja Compocem']
    # count_if_without_ambuja = ['Ambuja Kawach']
    count_if_full_term_only = ['Ambuja Plus']
    # count_if_full_term_only = []


    # Use dictionary for language-region mapping with country names and languages in words
    language_region_codes = {
        'en-IN': {'region': 'IN', 'country_name': 'India', 'language': 'English'},
        'es': {'region': 'ES', 'country_name': 'Spain', 'language': 'Spanish'},
        'hi': {'region': 'IN', 'country_name': 'India', 'language': 'Hindi'},
        'fr': {'region': 'FR', 'country_name': 'France', 'language': 'French'},
        'de': {'region': 'DE', 'country_name': 'Germany', 'language': 'German'},
        'it': {'region': 'IT', 'country_name': 'Italy', 'language': 'Italian'},
        'pt': {'region': 'BR', 'country_name': 'Brazil', 'language': 'Portuguese'},
        'ja': {'region': 'JP', 'country_name': 'Japan', 'language': 'Japanese'},
        'ko': {'region': 'KR', 'country_name': 'South Korea', 'language': 'Korean'},
        'zh-CN': {'region': 'CN', 'country_name': 'China', 'language': 'Simplified Chinese'},
        'zh-TW': {'region': 'TW', 'country_name': 'Taiwan', 'language': 'Traditional Chinese'},
        'ar': {'region': 'SA', 'country_name': 'Saudi Arabia', 'language': 'Arabic'},
        'ru': {'region': 'RU', 'country_name': 'Russia', 'language': 'Russian'},
        'pl': {'region': 'PL', 'country_name': 'Poland', 'language': 'Polish'},
        'tr': {'region': 'TR', 'country_name': 'Turkey', 'language': 'Turkish'},
        'nl': {'region': 'NL', 'country_name': 'Netherlands', 'language': 'Dutch'},
        'sv': {'region': 'SE', 'country_name': 'Sweden', 'language': 'Swedish'},
        'da': {'region': 'DK', 'country_name': 'Denmark', 'language': 'Danish'},
        'no': {'region': 'NO', 'country_name': 'Norway', 'language': 'Norwegian'},
        'fi': {'region': 'FI', 'country_name': 'Finland', 'language': 'Finnish'},
        'el': {'region': 'GR', 'country_name': 'Greece', 'language': 'Greek'},
        'cs': {'region': 'CZ', 'country_name': 'Czech Republic', 'language': 'Czech'},
        'ro': {'region': 'RO', 'country_name': 'Romania', 'language': 'Romanian'},
        'bg': {'region': 'BG', 'country_name': 'Bulgaria', 'language': 'Bulgarian'},
        'hu': {'region': 'HU', 'country_name': 'Hungary', 'language': 'Hungarian'},
        'th': {'region': 'TH', 'country_name': 'Thailand', 'language': 'Thai'},
        'vi': {'region': 'VN', 'country_name': 'Vietnam', 'language': 'Vietnamese'},
        'id': {'region': 'ID', 'country_name': 'Indonesia', 'language': 'Indonesian'},
        'ms': {'region': 'MY', 'country_name': 'Malaysia', 'language': 'Malay'},
        'tl': {'region': 'PH', 'country_name': 'Philippines', 'language': 'Filipino'}
    }


    # Define XPaths for scraping
    article_box_xpath = '//c-wiz[contains(@class,"PO9Zff")]'
    headline_xpath = './/a[contains(@class,"JtKRv")]'
    datetime_xpath = './/div[contains(@class,"UOVeFe")]/time/@datetime'
    href_path = './/a[@class="JtKRv"]/@href'

    def start_requests(self):
        for term in self.brands + self.count_if_without_ambuja + self.count_if_full_term_only:
            search_term = term.replace(" ", "+")  # Format the term for URL
            
            # Loop through the language-region mapping to create search URLs
            for language, data in self.language_region_codes.items():
                search_url = f"https://news.google.com/search?q={search_term}&hl={language}&gl={data['region']}"
                
                # Use the 'selenium' flag only for the pages that require JavaScript rendering
                yield scrapy.Request(
                    url=search_url,
                    callback=self.extract_article_data,
                    meta={
                        'search_term': term,
                        'language': language,
                        'region': data['region'],
                        'country_name': data['country_name'],
                        'country_language': data['language'],
                        'selenium': True,  # Set this to True for JavaScript-rendered pages
                    }
                )

        
    def extract_article_data(self, response):
        article_boxes = response.xpath(self.article_box_xpath)

        # Loop over each article box on the page
        for box in article_boxes:
            # Generating a unique UUID for the article
            transaction_id = str(uuid.uuid4())
            
            # Get headline
            headline = box.xpath(self.headline_xpath + '/text()').get().strip() if box.xpath(self.headline_xpath) else 'No Headline'
            
            # Get datetime from the article
            datetime_str = box.xpath(self.datetime_xpath).get()
            if datetime_str:
                try:
                    dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    dt = None
            else:
                dt = None
            
            # Format datetime
            if dt:
                datetime_sql = dt.strftime("%Y-%m-%d %H:%M:%S")  # Standard SQL format
            else:
                datetime_sql = None
                                  
 
            # Get article URL
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
                else:
                    print("Error:", decoded_url["message"])
            except Exception as e:
                print(f"Error occurred: {e}")
                
            yield response.follow(
                                    source_link,
                                    callback=self.parse_article,
                                    meta={
                                        'transaction_id': transaction_id,
                                        'search_term': response.meta['search_term'],
                                        'country_name': response.meta['country_name'],
                                        'country_language': response.meta['country_language'],
                                        'headline': headline,
                                        'article_datetime': datetime_sql,
                                        'source_link': source_link,
                                        }
                                    )

    def parse_article(self, response):
        # Get the full URL of the page
        full_url = response.url
        self.logger.info(f"visiting url: {full_url}")

        # Remove punctuation (e.g., .,!,? etc.), convert to lowercase
        try:
            description = response.xpath("//meta[@property='og:description']/@content").get()
            if not description:
                raise ValueError("No content found for og:description")
        except Exception:
            try:
                description = response.xpath("//meta[@name='og:description']/@content").get()
                if not description:
                    raise ValueError("No content found for og:description")
            except Exception:
                description = "Not Available"
        
        def clean_join_text(text1, text2):
            # Combine the two input strings with a space
            combined_text = f"{text1} {text2}"
            
            # Clean the combined text: remove punctuation, convert to lowercase, and strip spaces
            return combined_text.translate(str.maketrans('', '', string.punctuation)).lower().strip()
        def clean_text(text):
            return text.translate(str.maketrans('', '', string.punctuation)).lower().strip()

        # Join headline and description, clean string by removing punctuation, make lowercase
        clean_search_string = clean_join_text(response.meta['headline'],description)
        
        # Create a dictionary to store product matches with 0 count
        product_match = {term: 0 for term in self.count_if_without_ambuja + self.count_if_full_term_only}
        
        # First pass: Count full terms
        for term in self.count_if_without_ambuja + self.count_if_full_term_only:
            clean_term = clean_text(term)
            
            # Count the full term occurrences
            full_term_count = len(re.findall(r'\b' + re.escape(clean_term) + r'\b', clean_search_string))
            
            if full_term_count > 0:
                product_match[term] += full_term_count
        # Second pass: Count partial terms independently, but not if already counted as full term
        for term in self.count_if_without_ambuja:
            clean_term = clean_text(term)
            
            # Clean the term without "Ambuja"
            clean_term_without_ambuja = clean_term.replace('ambuja ', '')
            
            # Count the partial term only if it's not already counted as part of the full term
            if clean_term_without_ambuja in clean_search_string:
                # Ensure it's not part of the full term already counted
                if not re.search(r'\b' + re.escape(clean_term) + r'\b', clean_search_string):
                    cleaned_term_count = len(re.findall(r'\b' + re.escape(clean_term_without_ambuja) + r'\b', clean_search_string))
                    product_match[term] += cleaned_term_count

        # Attempt to get source name                  
        try:
            source = response.xpath("//meta[@property='og:site_name']/@content").get()
            if not source:  # If no content is found, handle it
                raise ValueError("No content found for og:site_name")
        except Exception:
            try:
                source = response.xpath("//meta[@name='og:site_name']/@content").get()
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
        
        item =  {
                'transaction_id': response.meta['transaction_id'],
                'article_datetime': response.meta['article_datetime'],
                'search_term': response.meta['search_term'],        
                'country_name': response.meta['country_name'],      
                'country_language': response.meta['country_language'],
                'news_source': source,
                'headline': response.meta['headline'],
                'description': description,
                'source_link': response.meta['source_link'],
                #'source': domain,  # Extracted domain (website source)
                **{f"{term.replace(' ', '_').lower()}_count": product_match.get(term, 0) for term in self.count_if_without_ambuja + self.count_if_full_term_only}          
            }
        
        self.logger.info(f"Yielding item: {item}")
        
        yield item


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