import logging
import sqlite3

from constants import FEED_MAPPING


logging.basicConfig(level=logging.INFO)

drop_feed_table_query = "DROP TABLE IF EXISTS FEED;"
create_feed_table_query = """
CREATE TABLE "feed" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(20) NOT NULL,
    "description" VARCHAR(100) NOT NULL,
    "frequency" VARCHAR(10) NOT NULL
)
"""

create_worker_table_query = """
CREATE TABLE "worker" (
    "id" VARCHAR(50) NOT NULL  PRIMARY KEY,
    "status" VARCHAR(20) NOT NULL,
    "created_by" VARCHAR(20),
    "created_at" TIMESTAMP,
    "feed_id" INT NOT NULL REFERENCES "feed" ("id") ON DELETE CASCADE /* The feed under which workers are running  */
)
"""


create_result_table_query ="""
CREATE TABLE "result" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "job_id" VARCHAR(50) NOT NULL,
    "key_name" VARCHAR(50) NOT NULL,
    "value" VARCHAR(50) NOT NULL,
    "worker_id" VARCHAR(50) NOT NULL REFERENCES "worker" ("id") ON DELETE CASCADE /* The results saved by the workers */
)
"""

insert_val = ','.join([f"({val['id']},'{name}','{val['description']}','{val['frequency']}')" for name,val in FEED_MAPPING.items() ])

insert_feeds_query =f"""
INSERT INTO FEED(ID, NAME, DESCRIPTION, FREQUENCY)
VALUES {insert_val} ;
"""


def create_db():
    conn = sqlite3.connect('scrapers.db')

    cur = conn.cursor()

    run_order = [drop_feed_table_query,
                create_feed_table_query,
                create_worker_table_query,
                create_result_table_query,
                insert_feeds_query
                ]
    for create_query in run_order:
        
        
        logging.info(f"Running Create Table queries {create_query}")
        cur.execute(create_query)
    conn.commit()

    logging.info("DB initialized")

if __name__ == "__main__":
    logging.info("Initializing DB")
    create_db()