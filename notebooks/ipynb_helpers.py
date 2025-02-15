import aiohttp
import sys
import os
sys.path.append('..')
from src.shared import helpers
from src.api.services import http_request
from typing import Any

def get_env_var(key: str) -> str:
    return helpers.get_env_var(key)

def replace_url_params(url, **kwargs) -> str:
    return helpers.replace_url_params(url, **kwargs)

def make_request(
    method: str,
    url: str,
    **kwargs
) -> tuple[Any, int]:
    return http_request.make_request(
        method=method,
        url=url,
        **kwargs
    )

async def make_request_async(
    method: str,
    url: str,
    session: aiohttp.ClientSession,
    retries: int = 3,
    delay: int = 2,
    **kwargs,
) -> tuple[Any, int]:
    return await http_request.make_request_async(
        method=method,
        url=url,
        session=session,
        retries=retries,
        delay=delay,
        **kwargs
    )

def convert_latitude(lat):
    
    # Extract degrees and minutes
    degrees = int(lat[:-5])  # First 4 digits are degrees
    minutes = int(lat[-5:-3])  # Last 2 digits are minutes
    
    # Convert to decimal degrees
    latitude_decimal = degrees + minutes / 60.0
    if lat[-1] == 'S':  # If South, make negative
        latitude_decimal = -latitude_decimal
    return latitude_decimal

def convert_longitude(lon):
    
    # Extract degrees and minutes
    degrees = int(lon[:-5])  # First 4 digits are degrees
    minutes = int(lon[-5:-3])  # Last 2 digits are minutes
    
    # Convert to decimal degrees
    longitude_decimal = degrees + minutes / 60.0
    if lon[-1] == 'W':  # If West, make it negative
        longitude_decimal = -longitude_decimal
    return longitude_decimal
