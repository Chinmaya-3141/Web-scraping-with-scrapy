# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import sqlite3
import os

class SQLite3Pipeline:
    
    # Begin feeding data to pipeline
    def open_spider(self, spider):
<<<<<<< HEAD
        logging.warning('Spider - Pipeline Opened')
        
        # Ensure the Outputs directory exists
        os.makedirs('../Outputs', exist_ok=True)  # Create Outputs folder if it doesn't exist
        
        # Connect to SQLite3 database
        self.connection = sqlite3.connect('../Outputs/news.db')
        self.c = self.connection.cursor()
        
        # Check if the table already exists
        self.c.execute('''
            SELECT name FROM sqlite_master WHERE type='table' AND name='news';
        ''')
        result = self.c.fetchone()
        
        # If the table doesn't exist, create it
        if not result:
            try:
                self.c.execute('''
                    CREATE TABLE news (
                        transaction_id TEXT PRIMARY KEY,
                        search_term TEXT,
                        country_name TEXT,
                        country_language TEXT,
                        news_source TEXT,
                        headline TEXT,
                        description TEXT,
                        article_datetime TEXT,
                        source_link TEXT,
                        ambuja_kawach_count INTEGER,
                        ambuja_cool_walls_count INTEGER,
                        ambuja_compocem_count INTEGER,
                        ambuja_plus_count INTEGER
                    )
                ''')
                self.connection.commit()
                logging.warning('Spider - Table Created')
            except sqlite3.Error as e:
                logging.error(f"Error creating table: {e}")
        else:
            logging.warning('Spider - Table Already Exists')
=======
        logging.warning('Spider - Pipeling Opened')
        self.connection = sqlite3.connect('../Outputs/news.db')
        self.c = self.connection.cursor()   #cursor object helps execute SQL queries
        try:
            self.c.execute('''
                                CREATE TABLE news(
                                    transaction_id TEXT PRIMARY KEY,
                                    search_term TEXT,
                                    country_name TEXT,
                                    country_language TEXT,
                                    news_source TEXT,
                                    headline TEXT,
                                    description TEXT,
                                    article_datetime TEXT,
                                    source_link TEXT,
                                    ambuja_kawach_count INTEGER,
                                    ambuja_cool_walls_count INTEGER,
                                    ambuja_compocem_count INTEGER,
                                    ambuja_plus_count INTEGER
                                )
                            ''')

            self.connection.commit()
        except sqlite3.OperationalError:
            pass
        logging.warning('Spider - Table Created')
>>>>>>> newsedit
        
        
    # Closes pipeline once done
    def close_spider(self, spider):
        self.connection.close()
        logging.warning('Spider - Pipeline Closed')
        
        
    def process_item(self, item, spider):
        # Check for duplicacy based on 'headline' and 'article_datetime'
        self.c.execute('''
            SELECT COUNT(*) FROM news
            WHERE headline = ? AND article_datetime = ?
        ''', (
            item.get('headline'),
            item.get('article_datetime')
        ))
        
        duplicate_count = self.c.fetchone()[0]
        
        # If no duplicate exists, insert the new item
        if duplicate_count == 0:
            try:
                self.c.execute('''
                    INSERT INTO news (
                        transaction_id,
                        search_term,
                        country_name,
                        country_language,
                        news_source,
                        headline,
                        description,
                        article_datetime,
                        source_link,
                        ambuja_kawach_count,
                        ambuja_cool_walls_count,
                        ambuja_compocem_count,
                        ambuja_plus_count
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item.get('transaction_id'),
                    item.get('search_term'),
                    item.get('country_name'),
                    item.get('country_language'),
                    item.get('news_source'),
                    item.get('headline'),
                    item.get('description'),
                    item.get('article_datetime'),
                    item.get('source_link'),
                    item.get('ambuja_kawach_count', 0),  # Default to 0 if not available
                    item.get('ambuja_cool_walls_count', 0),
                    item.get('ambuja_compocem_count', 0),
                    item.get('ambuja_plus_count', 0)
                ))
                self.connection.commit()
                logging.warning(f"Inserted new article: {item.get('headline')}")
            except sqlite3.Error as e:
                logging.error(f"Error inserting item: {e}")
        
        return item


# from itemadapter import ItemAdapter
# import logging
# import sqlite3

# class SQLite3Pipeline:
    
#     # Begin feeding data to pipeline
#     def open_spider(self, spider):
#         logging.warning('Spider - Pipeline Opened')
#         self.connection = sqlite3.connect('news.db')
#         self.c = self.connection.cursor()  # cursor object helps execute SQL queries
        
#         # Create the news table if it doesn't already exist
#         try:
#             self.c.execute('''
#                 CREATE TABLE IF NOT EXISTS news(
#                     transaction_id TEXT PRIMARY KEY,
#                     search_term TEXT,
#                     country_name TEXT,
#                     country_language TEXT,
#                     news_source TEXT,
#                     headline TEXT,
#                     description TEXT,
#                     article_datetime TEXT,
#                     source_link TEXT,
#                     article_text TEXT,
#                     sitename TEXT,
#                     ambuja_kawach_count INTEGER,
#                     ambuja_cool_walls_count INTEGER,
#                     ambuja_compocem_count INTEGER,
#                     ambuja_plus_count INTEGER
#                 )
#             ''')
#             self.connection.commit()
#         except sqlite3.OperationalError as e:
#             logging.error(f"Error creating table: {e}")
        
#         logging.warning('Spider - Table Created or Already Exists')

#     # Closes pipeline once done
#     def close_spider(self, spider):
#         self.connection.close()
#         logging.warning('Spider - Pipeline Closed')

#     def process_item(self, item, spider):
#         # Check for duplicacy (if same headline and article_datetime exists)
#         self.c.execute('''
#             SELECT COUNT(*) FROM news 
#             WHERE headline = ? AND article_datetime = ?
#         ''', (
#             item.get('headline'),
#             item.get('article_datetime')
#         ))
        
#         # Fetches first row of query result as tuple, [0] grabs first element of the tuple.
#         duplicate_count = self.c.fetchone()[0]
        
#         if duplicate_count == 0:  # If no duplicate exists, insert data
#             self.c.execute('''
#                 INSERT INTO news (
#                     transaction_id, 
#                     search_term, 
#                     country_name, 
#                     country_language, 
#                     news_source, 
#                     headline, 
#                     description, 
#                     article_datetime, 
#                     source_link,
#                     article_text, 
#                     sitename,
#                     ambuja_kawach_count, 
#                     ambuja_cool_walls_count, 
#                     ambuja_compocem_count, 
#                     ambuja_plus_count
#                 ) 
#                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
#             ''', (
#                 item.get('transaction_id'),
#                 item.get('search_term'),
#                 item.get('country_name'),
#                 item.get('country_language'),
#                 item.get('news_source'),
#                 item.get('headline'),
#                 item.get('description'),
#                 item.get('article_datetime'),
#                 item.get('source_link'),
#                 item.get('article_text'),
#                 item.get('sitename'),
#                 item.get('ambuja_kawach_count', 0),  # Default to 0 if no count is provided
#                 item.get('ambuja_cool_walls_count', 0),
#                 item.get('ambuja_compocem_count', 0),
#                 item.get('ambuja_plus_count', 0)
#             ))

#             self.connection.commit()
#             logging.info(f"Inserted article {item.get('transaction_id')} into the database.")
#         else:
#             logging.info(f"Duplicate article {item.get('headline')} found, skipping insertion.")
        
#         return item
