import configparser
import json
from pathlib import Path


def get_config():
    c = configparser.ConfigParser()
    c.read(f"{Path.cwd()}/webster/config/config.ini")
    return c


def get_urls(path):
    with open(path, 'r') as urls_file:
        data = json.load(urls_file)
    return data['urls']

