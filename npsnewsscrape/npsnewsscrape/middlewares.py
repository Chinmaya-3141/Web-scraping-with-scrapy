# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from itemadapter import is_item, ItemAdapter
import time, random, os, ast
import logging
from scrapy.http import HtmlResponse
from scrapy.downloadermiddlewares.retry import RetryMiddleware  # We can inherit from this
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from dotenv import load_dotenv


# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.edge.options import Options as EdgeOptions
# from undetected_geckodriver import Firefox
# from undetected_geckodriver import Firefox, Options



# https://github.com/ByteXenon/undetected_geckodriver
# https://github.com/nabinkhadka/rotating-free-proxies
# https://pypi.org/project/rotating-free-proxies/

class NpsnewsscrapeDownloaderMiddleware(RetryMiddleware):
    def __init__(self, *args, **kwargs):
        self.user_agent_path = '../Config/user_agents.env'
        load_dotenv(dotenv_path=self.user_agent_path)
        
        # Set up Firefox WebDriver (headless)
        firefox_options = FirefoxOptions()
        firefox_options.add_argument('--headless')  # Run Firefox in headless mode

        # Load .env variables for user agents and screen resolutions
        user_agents_str = os.getenv("USER_AGENTS")
        desktop_resolutions_str = os.getenv("DESKTOP_RESOLUTIONS")
        mobile_resolutions_str = os.getenv("MOBILE_RESOLUTIONS")
        try:
            user_agents = ast.literal_eval(user_agents_str)
            logging.info("Loaded user agents: {user_agents}")    
        except (ValueError, SyntaxError) as e:
            logging.info(f"Error parsing the user_agents list: {e}")
            
        try:
            desktop_resolutions = ast.literal_eval(desktop_resolutions_str)
            logging.info("Loaded desktop resoutions: {desktop_resolutions}")
        except (ValueError, SyntaxError) as e:
            logging.info(f"Error parsing the desktop resolution list: {e}")
        
        try:
            mobile_resolutions = ast.literal_eval(mobile_resolutions_str)
            logging.info("Loaded mobile resolutions: {mobile_resolutions}")
        except (ValueError, SyntaxError) as e:
            logging.info(f"Error parsing the mobile resolution list: {e}")
        
        # Randomly select a user agent and its associated mobile/desktop flag
        user_agent, is_mobile = random.choice(user_agents)
        
        # Apply the selected user-agent to Firefox options
        firefox_options.set_preference("general.useragent.override", user_agent)
        logging.info(f"Used user-agent: {user_agent}")

        # Choose the appropriate resolution based on the user-agent type (mobile or desktop)
        if is_mobile:
            selected_resolution = random.choice(mobile_resolutions)
            # Enable touch events for mobile-like resolutions
            firefox_options.set_preference("dom.w3c_touch_events.enabled", 1)
            logging.info(f"touchscreen: {is_mobile}")
        else:
            selected_resolution = random.choice(desktop_resolutions)
            # Disable touch events for desktop-like resolutions
            firefox_options.set_preference("dom.w3c_touch_events.enabled", 0)
            logging.info(f"touchscreen: {is_mobile}")
        
        # Set the selected window size
        window_width, window_height = selected_resolution
        firefox_options.add_argument(f"--window-size={window_width},{window_height}")
        logging.info(f"Used resolution: {selected_resolution}")

        self.driver = webdriver.Firefox(options=firefox_options)

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Ensure the RetryMiddleware is properly initialized
        super().__init__(*args, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """This method is used to initialize the middleware."""
        # Call the parent class's from_crawler to make sure retry settings are applied
        return super(NpsnewsscrapeDownloaderMiddleware, cls).from_crawler(crawler, *args, **kwargs)

    def process_request(self, request, spider):
        """Process the request using Selenium WebDriver only if `selenium=True` in the request's meta."""
        # Check if the request requires JavaScript rendering
        if request.meta.get('selenium', False):
            self.logger.info(f"Fetching dynamic page (Selenium): {request.url}")
            self.driver.get(request.url)

            # Generate a random wait time between 5 and 10 seconds
            rand_wait = random.uniform(3,10)
        
            # Wait for the randomly generated time
            time.sleep(rand_wait)

            # Log the time taken for loading
            self.logger.info(f"Page loaded in {rand_wait} seconds: {request.url}")

           #Retrieve rendered HTML
            content = self.driver.page_source
            
            # Random scrolling, 33.5% of the time.
            sample=random.sample(range(1,12),4)
            if(4 in sample):
                scroll_height = random.randint(100, 300)
                self.driver.execute_script(f"window.scrollTo(0, {scroll_height});")
                logging.info("Scrolled")
                # Wait for the randomly generated time
                time.sleep(1)  

            # Log the page content size
            self.logger.info(f"Page content size: {len(content)} characters")
            
            # Generate a random wait time between 2 and 4 seconds 31.5% of the time
            sample=random.sample(range(1,20),7)
            if(4 in sample):
                rand_wait_2 = random.uniform(1,3)
                logging.info("Extra wait")
                # Wait for the randomly generated time
                time.sleep(rand_wait_2)         
            
            # Return an HtmlResponse with the content
            return HtmlResponse(request.url, body=content, encoding='utf-8', request=request)

        # Let Scrapy handle the request if no JavaScript rendering is needed
        return None

    def process_response(self, request, response, spider):
        """Return the response without changes."""
        return response

    def process_exception(self, request, exception, spider):
        """Handle exceptions in the downloader process."""
        pass

    def close(self):
        """Close the Selenium WebDriver session."""
        self.logger.info("Closing the Selenium WebDriver session.")
        self.driver.quit()

class NpsnewsscrapeSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # This method is called for each response going through the spider middleware.
        return None

    def process_spider_output(self, response, result, spider):
        # This method handles the output from the spider and needs to return requests or items.
        for item in result:
            yield item

    def process_spider_exception(self, response, exception, spider):
        # This method can be used to handle exceptions raised in the spider processing.
        pass

    def process_start_requests(self, start_requests, spider):
        # This method is for processing start requests for the spider.
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        # Logging that the spider has been opened
        spider.logger.info("Spider opened: %s" % spider.name)


        # Set the custom User-Agent in the WebDriver options
        # Rotating User-Agent List
        # user_agents = [
        #         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        #         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        #         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        #         "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0",
        #         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
        #     ]
        # List of user agents paired with mobile/desktop info
        
        # user_agents = [
        #         ("Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0", False),  # Desktop
        #         ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", False),  # Desktop
        #         ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36", False),  # Desktop
        #         ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36", False),  # Desktop
        #         ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0", False),  # Desktop
        #         ("Mozilla/5.0 (Linux; Android 10; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36", True),  # Mobile
        #         ("Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36", True),  # Mobile
        #         ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", False),  # Desktop
        #         ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0", False),  # Desktop
        #         ("Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0", False),  # Desktop
        #         ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", False),  # Desktop
        #     ]
        
        # # Define common resolutions for desktop and mobile
        # desktop_resolutions = [
        #     (1366, 768),  # Common laptop size
        #     (1920, 1080), # Full HD
        #     (1280, 800),  # Common laptop size
        #     (1440, 900)   # Another common laptop size
        # ]
        
        # mobile_resolutions = [
        #     (375, 667),  # iPhone 6 dimensions (375x667)
        #     (360, 640),  # Typical Android screen size
        #     (375, 812),  # iPhone X dimensions (375x812)
        #     (414, 896)   # iPhone 11 dimensions (414x896)
        # ]

        # user_agent = random.choice(user_agents)  # Randomly select a User-Agent from the list
        # firefox_options.set_preference("general.useragent.override", user_agent)


















# class NpsnewsscrapeSpiderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.

#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.

#         # Should return None or raise an exception.
#         return None

#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.

#         # Must return an iterable of Request, or item objects.
#         for i in result:
#             yield i

#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.

#         # Should return either None or an iterable of Request or item objects.
#         pass

#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.

#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r

#     def spider_opened(self, spider):
#         spider.logger.info("Spider opened: %s" % spider.name)


# class NpsnewsscrapeDownloaderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.

#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.

#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None

#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.

#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response

#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.

#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass

#     def spider_opened(self, spider):
#         spider.logger.info("Spider opened: %s" % spider.name)
