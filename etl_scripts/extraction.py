import asyncio
from datetime import datetime, timedelta, date
import aiohttp
from helpers import config
from helpers.aemet_client import AEMETClient
from helpers.config import get_env_var
from helpers.logger import setup_logger


logger = setup_logger("etl_extraction")

async def extract_historical_data(
        start_date: date,
        end_date: date,
        delay: int = 2,
        max_retries: int = 5
):
    cycle_api_key = get_env_var("AEMET_API_KEY_1") is not None
    logger.info(f"Cycle API Key: {cycle_api_key}")
    num_keys = 1

    if cycle_api_key:
        current = 1
        client = AEMETClient(get_env_var(f"AEMET_API_KEY_{current}"))
        while get_env_var(f"AEMET_API_KEY_{num_keys+1}") is not None:
            num_keys += 1
        logger.info(f"Number of API keys: {num_keys}")
    else:
        client = AEMETClient(get_env_var(f"AEMET_API_KEY"))


    current_start_date = start_date
    end_date = min(datetime.now().date(), end_date)
    all_data = []

    async with aiohttp.ClientSession() as session:
        while current_start_date <= end_date:

            current_end_date = current_start_date + timedelta(days=14)
            current_end_date = min(end_date, current_end_date)

            start_date = current_start_date.strftime("%Y-%m-%d")
            current_end_date = current_end_date.strftime("%Y-%m-%d")

            logger.info(f"Fetching data for date range {start_date} to {current_end_date}...")

            for attempt in range(max_retries+1):

                if attempt == max_retries:
                    raise ValueError("Max retries reached. API is blocking requests.")

                logger.info(f"Attempt {attempt + 1}/{max_retries}")

                try:
                    # noinspection PyUnresolvedReferences
                    data = await client.get_historico_todas_estaciones(session, start_date, current_end_date)

                    if data is not None:
                        all_data.extend(data)
                        logger.info(f"Retrieved data for date range {start_date} to {current_end_date}")
                    else:
                        raise ValueError("Data is None")

                    current_start_date += timedelta(days=15)  # Max batches of 15 days
                    await asyncio.sleep(delay)
                    logger.info("-" * 10)
                    break

                except ValueError as e:
                    logger.error(e)
                    return all_data

                except Exception as e:
                    logger.error(e, e.args)
                    logger.info(f"Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(delay)
                    delay *= 2
                    if cycle_api_key:
                        current = (current % num_keys) + 1
                        client.set_api_key(config.get_env_var(f"AEMET_API_KEY_{current}"))
                    continue

    return all_data
