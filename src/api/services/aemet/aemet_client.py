import aiohttp
from src.api.services.http_request import make_request_async

class AEMETClient:

    BASE_URL = "https://opendata.aemet.es/opendata/api"

    ENDPOINTS = {
        'maestro': {
            'municipio': '/maestro/municipio/{municipio_id}'
        },

        # TODO: Add necessary endpoints
    }

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._headers = {'api_key': api_key}

    async def make_request(self, endpoint: str, **kwargs):
        url = self.BASE_URL + endpoint.format(**kwargs)

        async with aiohttp.ClientSession() as session:
            response = await make_request_async(url=url, headers=self._headers, session=session, method='get')

            datos = await make_request_async(url=response[0]['datos'], headers=self._headers, session=session, method='get')
            metadatos = await make_request_async(url=response[0]['metadatos'], headers=self._headers, session=session, method='get')

            return {
                'datos': datos,
                'metadatos': metadatos
            }