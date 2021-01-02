import json
import os

def load_config():
    global CONFIG
    with open(config_file, 'r') as configfile:
        CONFIG = json.load( configfile )
    return CONFIG

def save_config():
    with open(config_file, 'w') as configfile:
        json.dump(CONFIG, configfile, indent=4,ensure_ascii=False)

config_file = 'my.json'

CONFIG = {}

RUN_PATH = os.getcwd()

load_config()

if not "coins" in CONFIG:
    CONFIG["coins"] = {}
