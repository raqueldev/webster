import logging
from common import get_config
from db_connection import get_db_connection


config = get_config()
logging.basicConfig(filename=config["logging"]["path"], level=logging.INFO)

db_conn = get_db_connection()
cursor = db_conn.cursor()
cursor.execute("SELECT current_database()")
result = cursor.fetchone()
logging.info("Successfully connected to: {}".format(result[0]))

# prepare DB
query = """CREATE TABLE IF NOT EXISTS webster_metrics (
                   website VARCHAR(15) NOT NULL PRIMARY KEY,
                   response_time FLOAT(8) NOT NULL,
                   status_code SERIAL NOT NULL,
                   url VARCHAR(255) NOT NULL,
                   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
                   updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_DATE)"""
cursor.execute(query)
db_conn.commit()
logging.info("Table for Metrics successfully created")

query = """CREATE TABLE IF NOT EXISTS webster_metrics_history (
                   metrics_id SERIAL NOT NULL PRIMARY KEY,
                   website VARCHAR(15) NOT NULL ,
                   response_time FLOAT(8) NOT NULL,
                   status_code SERIAL NOT NULL,
                   url VARCHAR(255) NOT NULL,
                   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_DATE)"""
cursor.execute(query)
db_conn.commit()
logging.info("Table History successfully created")
cursor.close()
db_conn.close()
