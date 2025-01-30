# Scrapy settings for npsnewsscrape project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html

#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "npsnewsscrape"

SPIDER_MODULES = ["npsnewsscrape.spiders"]
NEWSPIDER_MODULE = "npsnewsscrape.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "npsnewsscrape (+http://www.yourdomain.com)"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3

# Adds randomness to the delay
# RANDOMIZE_DOWNLOAD_DELAY = True 

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16


# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "npsnewsscrape.middlewares.NpsnewsscrapeSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#     # 'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,  # Ensure retry middleware is added here
#     # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # Disable default user-agent middleware
#     # "npsnewsscrape.middlewares.NpsnewsscrapeDownloaderMiddleware": 543,  # Custom middleware, keep or remove if not needed
#     'npsnewsscrape.middlewares.SeleniumMiddleware':543,
# }
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,  # Retry middleware
    'npsnewsscrape.middlewares.NpsnewsscrapeDownloaderMiddleware': 543,  # Selenium middleware
}
SELENIUM_DRIVER = 'firefox'

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   #"npsnewsscrape.pipelines.NpsnewsscrapePipeline": 300,
   "npsnewsscrape.pipelines.SQLite3Pipeline": 200,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# Set the feed format to JSON
FEED_FORMAT = 'json'

# Set the feed URI to specify the output file (it can be a path to your desired location)

FEED_URI = '../Outputs/news.json'

RETRY_ENABLED = True
RETRY_TIMES = 3  # Number of retries
RETRY_HTTP_CODES = [408, 429, 500, 502, 503, 504]#,443]  # Retry on 429 errors
# RETRY_PRIORITY_ADJUST = 1  # Adjust the retry priority (can be positive or negative)
RETRY_DELAY = 15  # Delay between retries, in seconds (adjust this)

# SPLASH_URL = 'http://localhost:8050'

# DOWNLOADER_MIDDLEWARES = {
#     'scrapy_splash.SplashCookiesMiddleware': 723,
#     'scrapy_splash.SplashMiddleware': 725,
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
# }

# SPIDER_MIDDLEWARES = {
#     'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
# }

# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
