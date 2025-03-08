from datetime import datetime, timedelta, timezone
from helpers import api
from helpers.config import script_dir
import os

lct_path = os.path.join(script_dir, '../src/streamlit_app/.lct')

def last_check_time() -> datetime:
    if not os.path.exists(os.path.join(script_dir, lct_path)):
        update_last_check_time()
        return datetime.now(timezone.utc)

    with open(lct_path, 'r') as f:
        if not f.read() or f.read() == '':
            update_last_check_time()
            return datetime.now(timezone.utc)

        return datetime.fromisoformat(f.read())

def update_last_check_time():
    with open(lct_path, 'w') as f:
        f.write(datetime.now(timezone.utc).isoformat())

def check_latest():
    if datetime.now(timezone.utc) - last_check_time() < timedelta(minutes=60):
        return

    res = api.get_latest_fetch()
    if res:
        fetched_time = datetime.fromisoformat(res['fetched'])
        if datetime.now(timezone.utc) - fetched_time > timedelta(hours=1):
            api.fetch_latest()

    update_last_check_time()
