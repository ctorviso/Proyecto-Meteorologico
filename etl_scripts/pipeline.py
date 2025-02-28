import time
import os
from datetime import datetime, timedelta, date
import pandas as pd
from helpers.config import script_dir
from helpers.logging import setup_logger
from etl_scripts.cleaning import clean_historical, provincia_avg_diario
from etl_scripts.uploading import insert_batches
from etl_scripts.extraction import extract_historical_data
from src.db.db_handler import DBHandler
import asyncio

logger = setup_logger("etl_pipeline")

def filter_date_range(start_date, end_date):
    db = DBHandler()

    db_earliest_date = db.get_earliest_historical_date()
    db_latest_date = db.get_latest_historical_date()

    if end_date < db_earliest_date or start_date > db_latest_date:
        logger.info("Requested date range is outside existing data. Processing full range.")
        return start_date, end_date

    new_start_date = start_date
    new_end_date = end_date

    # Adjust start_date to latest + 1
    if db_earliest_date <= start_date <= db_latest_date:
        new_start_date = db_latest_date + timedelta(days=1)
        logger.info(f"Start date adjusted to {new_start_date} (after latest DB date)")

    # Adjust end_date to earliest -1
    if db_earliest_date <= end_date <= db_latest_date:
        new_end_date = db_earliest_date - timedelta(days=1)
        logger.info(f"End date adjusted to {new_end_date} (before earliest DB date)")

    if new_start_date > new_end_date:
        logger.info("No new data to process after filtering existing date range")
        return None, None

    logger.info(f"Processing filtered date range: {new_start_date} to {new_end_date}")
    return new_start_date, new_end_date

async def run_etl(start_date: date, end_date: date):

    os.makedirs(os.path.join(script_dir, '../data/historical/historico'), exist_ok=True)
    os.makedirs(os.path.join(script_dir, '../data/historical/historico_avg'), exist_ok=True)

    if start_date.year != end_date.year:
        logger.error("Start and end date must be in the same year. To process multiple years, run ETL for each year separately.")
        return

    logger.info(f"Running ETL for date range {start_date} to {end_date}...")

    #start_date, end_date = filter_date_range(start_date, end_date)
    if start_date is None:
        return

    data = await extract_historical_data(start_date, end_date)
    if len(data) == 0:
        logger.warning("No data was extracted.")
        return

    df = pd.DataFrame(data)

    df = clean_historical(df)
    avg_df = provincia_avg_diario(df)

    start_date = datetime.strptime(df['fecha'].min(), "%Y-%m-%d")
    end_date = datetime.strptime(df['fecha'].max(), "%Y-%m-%d")

    start_time = time.time()
    logger.info(f"Uploading historical data for date range {start_date} to {end_date}...")

    logger.info("Uploading historico...")
    insert_batches('historico', df)

    logger.info("Uploading historico_avg...")
    insert_batches('historico_avg', avg_df)

    elapsed_time = time.time() - start_time
    logger.info(f"Total execution time for all tables: {elapsed_time:.2f} seconds")

    year = start_date.year

    historical_path = os.path.join(script_dir, f'../data/historical/historico/{year}.csv')
    avg_path = os.path.join(script_dir, f'../data/historical/historico_avg/{year}.csv')

    if not os.path.exists(historical_path): # no data for this year yet
        df.to_csv(historical_path, index=False)
        avg_df.to_csv(avg_path, index=False)
        return

    # append to existing data
    df.to_csv(historical_path, mode='a', header=False, index=False)
    avg_df.to_csv(avg_path, mode='a', header=False, index=False)

    logger.info("ETL process completed.")

async def run_etl_latest():
    logger.info("Running ETL Latest...")

    db = DBHandler()
    current_latest = db.get_latest_historical_date()
    logger.info(f"Current latest: {current_latest}")
    start_date = current_latest + timedelta(days=1)
    end_date = datetime.now().date()

    await run_etl(start_date, end_date)

start = date(year=2018, month=1, day=1)
end = date(year=2018, month=12, day=31) # inclusive
asyncio.run(run_etl(start, end))

#asyncio.run(run_etl_latest())