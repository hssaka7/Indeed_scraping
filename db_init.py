import logging
import sqlite3

logging.basicConfig(level=logging.INFO)


drop_feed_table_query = "DROP TABLE IF EXISTS FEED;"
create_feed_table_query = """
CREATE TABLE FEED(
ID INT PRIMARY KEY NOT NULL,
NAME VARCHAR UNIQUE NOT NULL,
DESCRIPTION VARCHAR,
SCHEDULE VARCHAR
);
"""

create_feed_run_history_table_query = """
CREATE TABLE IF NOT EXISTS FEED_RUN_HISTORY(
ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
FEED_ID INT NOT NULL,
STATUS VARCHAR, 
WORKER_ID VARCHAR, 
CREATED_AT DATETIME,
CREATED_BY DATETIME
);
"""

create_result_table_query ="""
CREATE TABLE  IF NOT EXISTS RESULT(
JOB_ID INT NOT NULL,
RUN_ID INT NOT NULL,
KEY_NAME VARCHAR NOT NULL,
VALUE VARCHAR NOR NULL
);
"""


insert_feeds_query = """
INSERT INTO FEED(ID, NAME, DESCRIPTION, SCHEDULE)
VALUES 
(1,'indeed', 'extracts the data from indeed job portal','D'),
(2,'linkedin', 'extracts the data from linkedIn job portal', 'D'),
(3, 'amazon', 'extracts the ddata from amazon.com', 'D');
"""

conn = sqlite3.connect('scrapers.db')

run_order = [drop_feed_table_query,
             create_feed_table_query,
            create_feed_run_history_table_query,
            insert_feeds_query
            ]
for create_query in run_order:
    
    
    logging.info(f"Running Create Table queries {create_query}")
    conn.execute(create_query)
conn.commit()

logging.info("DB initialized")