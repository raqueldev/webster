from producer import producer
from consumer import consumer
from common import get_config
from tabulate import tabulate
from db_connection import get_db_connection
import logging


def get_webster_metrics():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    query = """
        SELECT website, url, response_time, status_code, created_at, updated_at
        FROM webster_metrics
        ORDER BY updated_at DESC
    """
    cursor.execute(query)
    results = cursor.fetchall()
    db_conn.commit()
    cursor.close()
    db_conn.close()
    return results


if __name__ == '__main__':
    print("********************************************")
    print("Welcome to Webster - Website Test Response")
    print("Give me a moment to setup the database and your log files....")
    config = get_config()
    logging.basicConfig(filename=config["logging"]["path"], level=logging.INFO)
    print("Starting to produce messages...")
    for x in range(2):
        producer(config)

    print("Starting to consume messages...")

    consumer(config)
    print(f"Webster has finished")

    data = get_webster_metrics()
    print(tabulate(data, headers=['Website', 'url', 'response_time', 'status_code', 'created_at', 'updated_at']))
