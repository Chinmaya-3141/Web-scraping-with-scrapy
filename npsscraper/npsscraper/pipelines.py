# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import sqlite3

# class NpsscraperPipeline:
#     # Begin feeding data to pipeline
#     def open_spider(self, spider):
#         logging.warning('Spider - Pipeling Opened')
        
#     # Closes pipeline once done
#     def close_spider(self, spider):
#         logging.warning('Spider - Pipeling Closed')
        
        
#     def process_item(self, item, spider):
#         return item
    
class MongoDBPipeline:
    
    collection_name = 'reviews'
    
    # Begin feeding data to mongo pipeline
    def open_spider(self, spider):
        
        # Configure Mongo Cluster username, password, read-write privileges, IP access list
        # Get connection string for cluster, insert in self.client.
        # Can fetch from a file with extra code.
        self.client = pymongo.MongoClient("")
        self.db = self.client['Review_Database']
        logging.warning('Spider - Pipeling Opened')
        
    # Closes pipeline once done
    def close_spider(self, spider):
        self.client.close()
        logging.warning('Spider - Pipeling Closed')
        
        
    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item

class SQLite3Pipeline:
    
    # Begin feeding data to pipeline
    def open_spider(self, spider):
        
        logging.warning('Spider - Pipeling Opened')
        self.connection = sqlite3.connect('review.db')
        self.c = self.connection.cursor()   #cursor object helps execute SQL queries
        try:
            self.c.execute('''
                           CREATE TABLE reviews(
                               transaction_id TEXT PRIMARY KEY,
                               app_name TEXT,
                               date_of_review TEXT,
                               reviewer_name TEXT,
                               review_text TEXT,
                               rating_numeric INTEGER,
                               helpful_numeric INTEGER
                               )
    
                ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass
        logging.warning('Spider - Table Created')
        
        
    # Closes pipeline once done
    def close_spider(self, spider):
        self.connection.close()
        logging.warning('Spider - Pipeling Closed')
        
        
    def process_item(self, item, spider):
        self.c.execute('''
                       INSERT INTO reviews (
                           transaction_id, 
                           app_name, 
                           date_of_review, 
                           reviewer_name, 
                           review_text, 
                           rating_numeric, 
                           helpful_numeric
                           ) 
                       Values (?,?,?,?,?,?,?)
            ''',(
                   item.get('transaction_id'),
                   item.get('app_name'),
                   item.get('date_of_review'),
                   item.get('reviewer_name'),
                   item.get('review_text'),
                   item.get('rating_numeric'),
                   item.get('helpful_numeric')
               ))
        self.connection.commit()
        return item