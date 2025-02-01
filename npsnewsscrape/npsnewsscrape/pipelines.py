# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging, os
from dotenv import load_dotenv
import sqlite3

class SQLite3Pipeline:
    
    def __init__(self):
        # Load environment variables from the .env files
        load_dotenv(dotenv_path='../config/ambuja.env')  # Adjust the path as needed
        
        # Dynamically fetch the count terms from the environment variables
        self.count_part_terms = [term.strip() for term in os.getenv('COUNT_PART_TERMS', '').split(',')] if os.getenv('COUNT_PART_TERMS') else []
        self.count_full_term_only = [term.strip() for term in os.getenv('COUNT_FULL_TERM_ONLY', '').split(',')] if os.getenv('COUNT_FULL_TERM_ONLY') else []
        
        # Merge part terms and full terms
        self.all_count_terms = self.count_part_terms + self.count_full_term_only
        
        # Get the database name from the environment variables (with a default value if not set)
        self.db_name = os.getenv('DB_NAME', 'news.db')  # Default to 'news.db' if DB_NAME is not found
        self.table_name = os.getenv('TABLE_NAME', 'news')  # Default to 'news.db' if DB_NAME is not found

    # Begin feeding data to pipeline
    def open_spider(self, spider):
        logging.warning('Spider - Pipeline Opened')
        
        # Ensure the Outputs directory exists
        os.makedirs('../Outputs', exist_ok=True)  # Create Outputs folder if it doesn't exist
        db_path = os.path.join('../Outputs', self.db_name)
        
        # Connect to SQLite3 database
        self.connection = sqlite3.connect(db_path)
        self.c = self.connection.cursor()
        
        # Check if the table already exists
        self.c.execute(f'''
            SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}';
        ''')
        result = self.c.fetchone()
        
        # If the table doesn't exist, create it
        if not result:
            try:
                count_columns = ', '.join([f"{term.replace(' ', '_').lower()}_count INTEGER" for term in self.all_count_terms])
                self.c.execute(f'''
                    CREATE TABLE {self.table_name} (
                        transaction_id TEXT PRIMARY KEY,
                        article_datetime TEXT NOT NULL,
                        search_term TEXT,
                        country_name TEXT,
                        country_language TEXT,
                        news_source TEXT,
                        headline TEXT,
                        description TEXT,
                        source_link TEXT,
                        {count_columns}  -- Dynamically created columns for count terms
                    )
                ''')
                self.connection.commit()
                logging.warning('Spider - Table {self.table_name} Created')
            except sqlite3.Error as e:
                logging.error(f"Error creating table: {e}")
        else:
            logging.warning('Spider - Table {self.table_name} Already Exists')
        
        
    # Closes pipeline once done
    def close_spider(self, spider):
        self.connection.close()
        logging.warning('Spider - Pipeline Closed')
        
        
    def process_item(self, item, spider):
        # Check if source_link is available
        count_columns = [col for col in item.keys() if '_count' in col]
        count_values = [item.get(col, 0) for col in count_columns]
        
        try:
            source_link = item.get('source_link')
        # If source_link is available, check for duplicacy based on source_link, country_name, and country_language
            if source_link:
                self.c.execute('''
                                   SELECT COUNT(*) FROM news 
                                   WHERE source_link = ? 
                                   AND country_name = ? 
                                   AND country_language = ?
                                ''', 
                                (
                                    source_link,
                                    item.get('country_name'),
                                    item.get('country_language')
                                )
                            )
            else:
                # If source_link is not available, check for duplicacy based on news_source, headline, and article_datetime
                self.c.execute('''
                                   SELECT COUNT(*) FROM news 
                                   WHERE news_source = ? 
                                   AND headline = ? 
                                   AND article_datetime = ?
                                ''', 
                                (
                                    item.get('news_source'),
                                    item.get('headline'),
                                    item.get('article_datetime')
                                )
                            )

        # Fetches first row of query result as tuple, [0] grabs first element of first row tuple
        
        
            duplicate_count = self.c.fetchone()[0]
            if duplicate_count == 0:  # If no duplicate exists, insert
                self.c.execute(f'''
                                    INSERT INTO {self.table_name} (
                                        transaction_id,
                                        article_datetime,                                    
                                        search_term, 
                                        country_name, 
                                        country_language, 
                                        news_source,
                                        headline,
                                        description,
                                        source_link,
                                        {', '.join(count_columns)}  -- Dynamically insert count columns
                                    ) 
                                    VALUES (?,?,?,?,?,?,?,?,?, {'?, ' * len(count_columns)}?)  -- Use placeholders for values
                                ''', 
                                    (
                                        item.get('transaction_id'),
                                        item.get('article_datetime'),                                
                                        item.get('search_term'),
                                        item.get('country_name'),
                                        item.get('country_language'),
                                        item.get('news_source'),
                                        item.get('headline'),
                                        item.get('description'),
                                        item.get('source_link'),
                                        *count_values  # Pass dynamic count values
                                    )
                            )


                self.connection.commit()
            else:
                logging.info(f"Duplicate item found for {item.get('headline')}. Skipping insertion.")
        except sqlite3.Error as e:
            self.logger.error(f"Error processing item: {e}")
            self.connection.rollback()  # Rollback in case of error
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
