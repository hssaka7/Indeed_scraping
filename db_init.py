import logging
import sqlite3

logging.basicConfig(level=logging.INFO)

FEED_MAPPING = {
    'indeed': {
        "id": 1,
        "description":"extracts the data from indeed job portal",
        "frequency": "D",
    },
    'linkedin': {
        "id": 2,
        "description":"extracts the data from linkedin job portal",
        "frequency": "D",
    },
    'amazon': {
        "id": 3,
        "description":"extracts the data from linkedin job portal",
        "frequency": "D",
    }
}


drop_feed_table_query = "DROP TABLE IF EXISTS FEED;"
create_feed_table_query = """
CREATE TABLE FEED(
ID INT PRIMARY KEY NOT NULL,
NAME VARCHAR UNIQUE NOT NULL,
DESCRIPTION VARCHAR,
FREQUENCY VARCHAR
);
"""

create_worker_table_query = """
CREATE TABLE IF NOT EXISTS WORKER(
ID STRING PRIMARY KEY  NOT NULL,
FEED_ID INT NOT NULL,
STATUS VARCHAR, 
CREATED_AT DATETIME,
CREATED_BY DATETIME
);
"""

create_result_table_query ="""
CREATE TABLE  IF NOT EXISTS RESULT(
JOB_ID VARCHAR NOT NULL,
WORKER_ID STRING NOT NULL,
KEY_NAME VARCHAR NOT NULL,
VALUE VARCHAR NOR NULL
);
"""
insert_val = ','.join([f"({val['id']},'{name}','{val['description']}','{val['frequency']}')" for name,val in FEED_MAPPING.items() ])

insert_feeds_query =f"""
INSERT INTO FEED(ID, NAME, DESCRIPTION, FREQUENCY)
VALUES {insert_val} ;
"""


def create_db():
    conn = sqlite3.connect('scrapers.db')

    run_order = [drop_feed_table_query,
                create_feed_table_query,
                create_worker_table_query,
                insert_feeds_query
                ]
    for create_query in run_order:
        
        
        logging.info(f"Running Create Table queries {create_query}")
        conn.execute(create_query)
    conn.commit()

    logging.info("DB initialized")

# create_db()