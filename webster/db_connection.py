import psycopg2
from common import get_config


def get_db_connection():
    config = get_config()
    return psycopg2.connect(config["database"]["service_uri"])

