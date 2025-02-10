from typing import Any

import requests
import aiohttp
import asyncio
from app.services.http_error import RequestFailedError
from app.services.http_error import error_map, retryable_exceptions, \
    UnsupportedMethodError, ClientError, MaximumRetriesError

request_map = {
    'get': requests.get,
    'post': requests.post,
    'delete': requests.delete,
    'put': requests.put,
}


def get_request_func(method: str, session: aiohttp.ClientSession):
    request_map_async = {
        'get': session.get,
        'post': session.post,
        'delete': session.delete,
        'put': session.put,
    }

    method_lower = method.lower()
    if method_lower not in request_map_async:
        raise UnsupportedMethodError  # ✅ More informative error

    return request_map_async[method_lower]


def make_request(
    method: str,
    url: str,
    **kwargs
) -> tuple[Any, int]:

    method = request_map.get(method.lower())
        
    if not method:
        raise UnsupportedMethodError(method)
    
    try:
        response = method(url, **kwargs)
        response.raise_for_status()
        
        return response, response.status_code

    except requests.exceptions.RequestException as req_err:
        print(f"Request failed: {req_err}")
        return {"error": str(req_err)}, 500

    except Exception as e:
        print('Error occurred:', e)
        return {"error": str(e)}, 500

async def make_request_async(
    method: str,
    response_format: str,
    url: str,
    session: aiohttp.ClientSession,
    retries: int = 3,
    delay: int = 2,
    **kwargs,
) -> tuple[Any, int]:
    
    method_func = get_request_func(method, session)

    if not method:
        raise UnsupportedMethodError(method)

    attempts = 0
    while attempts < retries:
        attempts += 1
        
        try:
            async with method_func(url=url, **kwargs) as response:
                
                if response.status in error_map:
                    exception = error_map[response.status](response.status, response.reason)
                    
                    if exception in retryable_exceptions:
                        await asyncio.sleep(delay)
                        continue
                        
                    raise exception
                    
                if not (200 <= response.status < 300):
                    raise RequestFailedError(response.status, response.reason)

                if response_format == 'json':
                    return await response.json(), response.status
                elif response_format == 'text':
                    return await response.text(), response.status
                else:
                    return await response.read(), response.status
                
        except aiohttp.ClientError as e:
            
            if attempts >= retries:
                if hasattr(e, 'status'):
                    raise ClientError(e.status, str(e))
                raise
            
            await asyncio.sleep(delay)
            continue
                
        except Exception as e:
            
            if attempts >= retries:
                if hasattr(e, 'status'):
                    raise RequestFailedError(e.status, str(e))
                else:
                    raise
            await asyncio.sleep(delay)
            
            continue

    raise MaximumRetriesError # 504

async def request_batch_async(
    url: str,
    method: str,
    data: list[dict],
    retries: int = 3,
    delay: int = 2,
    **kwargs
) -> list[tuple[dict, int]]:

    async with aiohttp.ClientSession() as session:
        tasks = [
            make_request_async(
                method=method,
                url=url,
                session=session,
                retries=retries,
                delay=delay,
                json=item,
                **kwargs
            ) for item in data
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    return responses
