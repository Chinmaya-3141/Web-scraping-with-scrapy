# review class = "EGFGHd"
'''
Fetch review blocks, extract data


import scrapy
import re
from datetime import datetime

class ReviewscraperSpider(scrapy.Spider):
    name = "reviewscraper"
    allowed_domains = ["play.google.com/"]
    start_urls = ["https://play.google.com/store/apps/details?id=com.adani.cement&hl=en/",
                  "https://play.google.com/store/apps/details?id=com.adani.adanielectricity&hl=en"]

    def parse(self, response):
        appname = response.xpath('//span[@class="AfwdI"]/text()').get()
        reviews = response.xpath('//div[@class="EGFGHd"]')
        for review in reviews:
            reviewer_name = review.xpath('.//div[@class="X5PpBb"]/text()').get()
            aria_label_rating = review.xpath('.//div[@class="iXRFPc" and @aria-label]/@aria-label').get()
            rating_num = re.search(r'Rated (\d+) stars', aria_label_rating).group(1) if re.search(r'Rated (\d+) stars', aria_label_rating) else None
            date_of_review = review.xpath('.//span[@class="bp9Aid"]/text()').get()
            date_of_review_ddmmyy = datetime.strptime(date_of_review, "%B %d, %Y")
            helpful_for = review.xpath('.//div[@class="AJTPZc"]/text()').get()
            helpful_num = re.search(r'(\d+)', aria_label_rating).group(1) if re.search(r'(\d+) people', aria_label_rating) else None
            yield{
                'appname':appname,
                'reviewer_name':reviewer_name,
                # 'rating':aria_label_rating,
                'rating_num':rating_num,
                'date_of_review':date_of_review_ddmmyy,
                'helpful_num':helpful_num,
                }
 '''           
'''
Without getting review block    


        appname = response.xpath('//span[@class="AfwdI"]/text()').getall()
        reviewer_name = response.xpath('//div[@class="X5PpBb"]/text()').getall()
        aria_label_rating = response.xpath('//div[@class="iXRFPc" and @aria-label]/@aria-label').getall()
        rating_num = [re.search(r'\d+', item) for item in aria_label_rating]
        rating_num = [re.search(r'\d+', item).group(0) if re.search(r'\d+', item) else None for item in aria_label_rating]
        date_of_review = response.xpath('//span[@class="bp9Aid"]/text()').getall()
        helpful_for = response.xpath('//div[@class="AJTPZc"]/text()').getall()            
        yield{
            'appname':appname,
            'reviewer_name':reviewer_name,
            'rating':aria_label_rating,
            'rating_num':rating_num,
            'date_of_review':date_of_review,
            'helpful_for':helpful_for,
            }

 
 
 '''
 
 # Fetch review block, pass to function to extract data.

import scrapy
import re, uuid
from datetime import datetime

class ReviewscraperSpider(scrapy.Spider):
    name = "reviewscraper"
    allowed_domains = ["play.google.com"]
    start_urls = [
        "https://play.google.com/store/apps/details?id=com.adani.cement&hl=en/",
        "https://play.google.com/store/apps/details?id=com.adani.adanielectricity&hl=en/",
        "https://play.google.com/store/apps/details?id=com.adani.myagl"
    ]
    
    app_name_xpath = '//span[@class="AfwdI"]'
    review_box_xpath = '//div[@class="EGFGHd"]'
    # dynamic_review_box_xpath = '//div[@class="RHo1pe"]' #dynamically rendered review objects.
    review_text_xpath = './/div[@class="h3YV2d"]'
    reviewer_name_xpath = './/div[@class="X5PpBb"]'
    rating_in_words_xpath = './/div[@class="iXRFPc" and @aria-label]'
    date_of_review_xpath = './/span[@class="bp9Aid"]'
    helpful_in_words_xpath = './/div[@class="AJTPZc"]'

                                              
    def parse(self, response):
        yield from self.extract_review_data(response)

    def extract_review_data(self, response):
        # Extract the app name
        appname = response.xpath(self.app_name_xpath + '/text()').get()

        # Extract data from review block
        reviews = response.xpath(self.review_box_xpath)
        for review in reviews:
            
            # Generating a unique UUID
            transaction_id = str(uuid.uuid4())  
            
            # Extract review body
            review_text = review.xpath(self.review_text_xpath + '/text()').get()

            # Extract reviewer name
            reviewer_name = review.xpath(self.reviewer_name_xpath + '/text()').get(default="Unknown")

            # Extract rating number from label_rating
            rating_in_words = review.xpath(self.rating_in_words_xpath + '/@aria-label').get()
            rating_numeric = re.search(r'(\d+)', rating_in_words).group(1)

            # Parse the review date
            date_of_review = review.xpath(self.date_of_review_xpath + '/text()').get()
            try:
                date_of_review_ddmmyy = datetime.strptime(date_of_review, "%B %d, %Y")
            except ValueError:
                date_of_review_ddmmyy = None

            # Extract the helpful number from label_rating
            try:
                helpful_in_words = review.xpath(self.helpful_in_words_xpath + '/text()').get()
                helpful_numeric = re.search(r'(\d+)', helpful_in_words).group(1)
            except:
                helpful_numeric = 0

            # Yield the extracted data
            yield {
                'transaction_id':transaction_id,
                'app_name': appname,
                'date_of_review': date_of_review_ddmmyy,
                'reviewer_name': reviewer_name,
                'review_text': review_text,
                'rating_numeric': rating_numeric,
                'helpful_numeric': helpful_numeric
            }
