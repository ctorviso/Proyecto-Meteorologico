import aiohttp
from app.services.http_request import make_request_async

class AEMETClient:

    BASE_URL = "https://opendata.aemet.es/opendata/api/"

    ENDPOINTS = {
        'maestro': {
            'municipios': 'maestro/municipios',
            'municipio': 'maestro/municipio/{municipio_id}'
        }
    }

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._headers = {'api_key': api_key}

    async def get_municipios(self):
        url = self.BASE_URL + self.ENDPOINTS['maestro']['municipios']

        async with aiohttp.ClientSession() as session:
            response = await make_request_async(url=url, response_format='json', headers=self._headers, session=session, method='get')

            datos = await make_request_async(url=response[0]['datos'], response_format='text', headers=self._headers, session=session, method='get')
            metadatos = await make_request_async(url=response[0]['metadatos'], response_format='text', headers=self._headers, session=session, method='get')

            return {
                'datos': datos,
                'metadatos': metadatos
            }