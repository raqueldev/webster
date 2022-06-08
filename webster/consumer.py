import json
import logging
from db_connection import get_db_connection
from common import get_config
from kafka import KafkaConsumer


def create_consumer(conf):
    try:
        logging.info("[Webster] Creating Kafka Consumer")
        return KafkaConsumer(bootstrap_servers=conf["kafka"]["service_uri_ssl"],
                             auto_offset_reset='earliest',
                             security_protocol='SSL',
                             ssl_cafile=conf["kafka"]["ssl_cafile"],
                             ssl_keyfile=conf["kafka"]["ssl_keyfile"],
                             ssl_certfile=conf["kafka"]["ssl_certfile"],
                             client_id='webster',
                             group_id='webster_0',
                             consumer_timeout_ms=10000
                             )
    except BaseException as e:
        logging.error("[Webster] Consumer could not be created {e=}")
        raise


def consumer(conf):
    try:
        c = create_consumer(conf)

        c.subscribe([conf["kafka"]["topic"]])
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        for message in c:
            msg_json = json.loads(message.value.decode('utf-8'))
            logging.info(f"[Webster] Consuming message: {msg_json}")
            logging.info(f"[Webster] Sending metrics to db: {msg_json['key']}, "
                         f"{msg_json['url']}, "
                         f"{msg_json['response_time']}, "
                         f"{msg_json['status_code']}, "
                         f"{msg_json['created_at']}"
                         )
            query = """INSERT INTO webster_metrics (response_time, status_code, url, website, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (website) DO UPDATE SET (response_time, status_code, updated_at)
            = (EXCLUDED.response_time, EXCLUDED.status_code, EXCLUDED.updated_at); """
            cursor.execute(query, (msg_json['response_time'],
                                   msg_json['status_code'],
                                   msg_json['url'],
                                   msg_json['key'],
                                   msg_json['created_at'],
                                   msg_json['updated_at']
                                   ))
            db_connection.commit()

            query_history = """INSERT INTO webster_metrics_history (response_time, status_code, url, website,
            created_at)VALUES(%s, %s, %s, %s, %s); """
            cursor.execute(query_history, (msg_json['response_time'],
                                           msg_json['status_code'],
                                           msg_json['url'],
                                           msg_json['key'],
                                           msg_json['created_at'],
                                           ))
            db_connection.commit()
        c.commit()
        c.close()
        cursor.close()
        db_connection.close()
    except BaseException as e:
        logging.error("[Webster] Messages could not be consumed {e=}")
        print("error")
        raise


if __name__ == '__main__':
    config = get_config()
    logging.basicConfig(filename=config["logging"]["path"], level=logging.INFO)
    logging.basicConfig(filename=config["logging"]["path_errors"], level=logging.ERROR)
    consumer(config)

