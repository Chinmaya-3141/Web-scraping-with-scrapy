# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
# from scrapy.middleware import BaseMiddleware  # This is the correct base class
from scrapy.downloadermiddlewares.retry import RetryMiddleware  # We can inherit from this
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium.webdriver.edge.options import Options as EdgeOptions
import time, random
import logging

class NpsnewsscrapeDownloaderMiddleware(RetryMiddleware):
    def __init__(self, *args, **kwargs):
        # Set up Firefox WebDriver (headless)
        firefox_options = FirefoxOptions()
        firefox_options.add_argument('--headless')  # Run Firefox in headless mode
        # Set the custom User-Agent in the WebDriver options
        user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0"  # Replace with your desired User-Agent string
        firefox_options.set_preference("general.useragent.override", user_agent)
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

            # Generate a random wait time between 2 and 4 seconds
            rand_wait = random.uniform(2, 4)
        
            # Wait for the randomly generated time
            time.sleep(rand_wait)

            # Log the time taken for loading
            self.logger.info(f"Page loaded in {rand_wait} seconds: {request.url}")

            # Get the fully rendered HTML page source from Selenium
            content = self.driver.page_source

            # Log the page content size
            self.logger.info(f"Page content size: {len(content)} characters")

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




# from scrapy import signals

# # useful for handling different item types with a single interface
# from itemadapter import is_item, ItemAdapter
# from scrapy.http import HtmlResponse
# # from scrapy.middleware import BaseMiddleware  # This is the correct base class
# from scrapy.downloadermiddlewares.retry import RetryMiddleware  # We can inherit from this
# from selenium import webdriver
# # from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
# # from selenium.webdriver.edge.options import Options as EdgeOptions
# import time
# import logging

# class NpsnewsscrapeDownloaderMiddleware(RetryMiddleware):
#     def __init__(self, *args, **kwargs):
#         # Set up Firefox WebDriver (headless)
#         firefox_options = FirefoxOptions()
#         firefox_options.add_argument('--headless')  # Run Firefox in headless mode
#         self.driver = webdriver.Firefox(options=firefox_options)

#         # Set up logging
#         logging.basicConfig(level=logging.INFO)
#         self.logger = logging.getLogger(__name__)

#         # Ensure the RetryMiddleware is properly initialized
#         super().__init__(*args, **kwargs)

#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         """This method is used to initialize the middleware."""
#         # Call the parent class's from_crawler to make sure retry settings are applied
#         return super(NpsnewsscrapeDownloaderMiddleware, cls).from_crawler(crawler, *args, **kwargs)

#     def process_request(self, request, spider):
#         """Process the request using Selenium WebDriver."""
#         self.logger.info(f"Fetching page: {request.url}")
#         self.driver.get(request.url)

#         # Allow some time for the page to load
#         time.sleep(3)

#         # Log the time taken for loading
#         self.logger.info(f"Page loaded in 3 seconds: {request.url}")

#         # Get the fully rendered HTML page source from Selenium
#         content = self.driver.page_source

#         # Log the page content size
#         self.logger.info(f"Page content size: {len(content)} characters")

#         # Return an HtmlResponse with the content
#         return HtmlResponse(request.url, body=content, encoding='utf-8', request=request)

#     def process_response(self, request, response, spider):
#         """Return the response without changes."""
#         return response

#     def process_exception(self, request, exception, spider):
#         """Handle exceptions in the downloader process."""
#         pass

#     def close(self):
#         """Close the Selenium WebDriver session."""
#         self.logger.info("Closing the Selenium WebDriver session.")
#         self.driver.quit()





# class NpsnewsscrapeSpiderMiddleware:
#     @classmethod
#     def from_crawler(cls, crawler):
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s

#     def process_spider_input(self, response, spider):
#         # This method is called for each response going through the spider middleware.
#         return None

#     def process_spider_output(self, response, result, spider):
#         # This method handles the output from the spider and needs to return requests or items.
#         for item in result:
#             yield item

#     def process_spider_exception(self, response, exception, spider):
#         # This method can be used to handle exceptions raised in the spider processing.
#         pass

#     def process_start_requests(self, start_requests, spider):
#         # This method is for processing start requests for the spider.
#         for r in start_requests:
#             yield r

#     def spider_opened(self, spider):
#         # Logging that the spider has been opened
#         spider.logger.info("Spider opened: %s" % spider.name)






# class SeleniumMiddleware(BaseMiddleware):
#     def __init__(self, driver_type='firefox'):
#         """
#         Initialize Selenium WebDriver based on the selected driver type.
#         Default is 'firefox'. You can set 'chrome' or 'edge' to use those drivers.
#         """
#         self.driver_type = driver_type.lower()

#         if self.driver_type == 'chrome':
#             chrome_options = ChromeOptions()
#             chrome_options.add_argument('--headless')
#             chrome_options.add_argument('--disable-gpu')
#             chrome_options.add_argument('--no-sandbox')
#             self.driver = webdriver.Chrome(options=chrome_options)
#         elif self.driver_type == 'firefox':
#             firefox_options = FirefoxOptions()
#             firefox_options.add_argument('--headless')
#             self.driver = webdriver.Firefox(options=firefox_options)
#         elif self.driver_type == 'edge':
#             edge_options = EdgeOptions()
#             edge_options.add_argument('--headless')
#             self.driver = webdriver.Edge(options=edge_options)
#         else:
#             raise ValueError("Unsupported driver type. Use 'chrome', 'firefox', or 'edge'.")

#         # Set up logging
#         logging.basicConfig(level=logging.INFO)
#         self.logger = logging.getLogger(__name__)

#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         """Initialize the middleware with a driver type from Scrapy settings."""
#         driver_type = crawler.settings.get('SELENIUM_DRIVER', 'firefox')  # Default to Firefox
#         middleware = super(SeleniumMiddleware, cls).from_crawler(crawler, *args, **kwargs)
#         middleware.driver_type = driver_type
#         return middleware

#     def process_request(self, request, spider):
#         """Process the request using the selected Selenium WebDriver."""
#         self.logger.info(f"Fetching page: {request.url}")

#         self.driver.get(request.url)

#         # Sleep for 3 seconds to allow the page to fully load (static wait)
#         time.sleep(3)

#         # Log the time taken for loading
#         self.logger.info(f"Page loaded in 3 seconds: {request.url}")

#         # Get the fully rendered HTML page source from Selenium
#         content = self.driver.page_source
        
#         # Log the page content length (just an example of logging some useful data)
#         self.logger.info(f"Page content size: {len(content)} characters")

#         # Return an HtmlResponse with the content
#         return HtmlResponse(request.url, body=content, encoding='utf-8', request=request)

#     def process_response(self, request, response, spider):
#         """Not used here, simply pass the response."""
#         return response

#     def close(self):
#         """Close the Selenium WebDriver session."""
#         self.logger.info("Closing the Selenium WebDriver session.")
#         self.driver.quit()


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
