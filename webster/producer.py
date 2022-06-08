import requests
import json
import logging
from common import get_config, get_urls
from kafka import KafkaProducer
from datetime import datetime


def create_producer(conf):
    try:
        logging.info("[Webster] Creating Kafka Producer")
        return KafkaProducer(bootstrap_servers=conf["kafka"]["service_uri_ssl"],
                             security_protocol="SSL",
                             ssl_cafile=conf["kafka"]["ssl_cafile"],
                             ssl_keyfile=conf["kafka"]["ssl_keyfile"],
                             ssl_certfile=conf["kafka"]["ssl_certfile"],
                             )
    except BaseException as e:
        logging.error("[Webster] Consumer could not be created {e=}")
        raise


def get_metrics(key, url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return json.dumps({
            'key': key,
            'url': url,
            'response_time': response.elapsed.total_seconds(),
            'status_code': response.status_code,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }, default=str).encode('utf-8')
    except BaseException as e:
        logging.error("[Webster] Metrics could not be prepared {e=}")
        raise


def producer(conf):
    try:
        urls = get_urls(conf["urlsJson"]["path"])
        p = create_producer(conf)
        logging.info(f"[Webster] Producing {len(urls)} messages")
        for url in urls:
            for key in url:
                logging.info(f"[Webster] Getting metrics for {key}")
                get_metrics(key, url[key])
                message = get_metrics(key, url[key])
                logging.info(f"[Webster] Sending message: {message}")
                p.send(conf["kafka"]["topic"], message)
        p.flush()
    except BaseException as e:
        logging.error("[Webster] Messages could not be sent {e=}")
        raise


if __name__ == '__main__':
    config = get_config()
    logging.basicConfig(filename=config["logging"]["path"], level=logging.INFO)
    producer(config)
