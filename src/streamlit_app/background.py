from datetime import datetime, timedelta, timezone
from helpers import api
from helpers.config import script_dir
import os

from helpers.logger import setup_logger

lct_path = os.path.join(script_dir, '../src/streamlit_app/.lct')
logger = setup_logger('background')

def last_check_time() -> datetime:
    if not os.path.exists(lct_path):
        logger.info(f'Last check time file not found.')
        return None

    with open(lct_path, 'r') as f:
        contents = f.read()
        if not contents or contents.isspace():
            logger.info(f'Last check time file empty.')
            return None

        return datetime.fromisoformat(contents)

def update_last_check_time():
    with open(lct_path, 'w') as f:
        logger.info(f'Updating last check time.')
        f.write(datetime.now(timezone.utc).isoformat())
        logger.info(f'Last check time updated to {datetime.now(timezone.utc)}.')

def check_latest():
    logger.info(f'Checking latest data.')
    lct = last_check_time()
    if lct and datetime.now(timezone.utc) - lct < timedelta(minutes=60):
        logger.info(f'Last check was less than 60 minutes ago. Skipping.')
        return

    if not lct:
        logger.info(f'Last check time not found. Fetching latest data.')

    logger.info(f'Last check was more than 60 minutes ago. Fetching latest data.')
    api.fetch_latest()
    logger.info(f'Latest data requested.')
    update_last_check_time()
