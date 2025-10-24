import logging
import os
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR,exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# logging.basicConfig(
#     filename=LOG_FILE,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

#get daily rotation and explicit handler setup:
import logging.handlers
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when="midnight", backupCount=7, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(handler)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger