import time
from datetime import timedelta

from helpers.logging import setup_logger
from src.db.db_handler import DBHandler

logger = setup_logger("etl_uploading")

def insert_batches(table, df, start_date, end_date):
    logger.info(f"Inserting batches for date range {start_date} to {end_date}...")
    start_time = time.time()

    db = DBHandler()

    current_date = start_date
    while current_date <= end_date:
        start_time_batch = time.time()
        date_str = current_date.strftime("%Y-%m-%d")
        current_date += timedelta(days=1)

        batch = df[df["fecha"] == date_str]

        if db.historical_exists(table, date_str):
            logger.warning(f"Records for date {date_str} already exist. Skipping...")
            continue

        logger.info(f"Batch size: {len(batch)}")

        if len(batch) == 0:
            logger.info(f"No records for date {date_str}")
            continue

        logger.info(f"Inserting records from {date_str}...")
        db.bulk_insert_data(table, batch.to_dict(orient="list"))
        logger.info(f"Inserted records from {date_str}")

        elapsed_time_batch = time.time() - start_time_batch
        print(f"Batch execution time: {elapsed_time_batch:.4f} seconds")

    elapsed_time = time.time() - start_time
    print(f"Total execution time for all batches: {elapsed_time:.4f} seconds")
