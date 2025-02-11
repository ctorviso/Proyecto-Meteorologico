import aiohttp
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'project/src')))
import helpers
from app.services import http_request
from typing import Any

def get_env_var(key: str) -> str:
    return helpers.get_env_var(key)

def replace_url_params(url, **kwargs) -> str:
    return helpers.replace_url_params(url, **kwargs)

def make_request(
    method: str,
    url: str,
    response_format: str,
    **kwargs
) -> tuple[Any, int]:
    return http_request.make_request(
        method=method,
        url=url,
        response_format=response_format,
        **kwargs
    )

async def make_request_async(
    method: str,
    response_format: str,
    url: str,
    session: aiohttp.ClientSession,
    retries: int = 3,
    delay: int = 2,
    **kwargs,
) -> tuple[Any, int]:
    return await http_request.make_request_async(
        method=method,
        response_format=response_format,
        url=url,
        session=session,
        retries=retries,
        delay=delay,
        **kwargs
    )