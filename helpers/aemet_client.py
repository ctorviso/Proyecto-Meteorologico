import json
import aiohttp
from helpers.http_request import get_async
from helpers.logger import setup_logger


def _format_fecha(fecha: str):
    return f"{fecha}T00:00:00UTC"


class AEMETClient:
    BASE_URL = "https://opendata.aemet.es/opendata/api"

    ENDPOINTS = {
        'maestro': {
            'municipio': '/maestro/municipio/{municipio_id}'
        },
        'observacion-convencional': {
            'tiempo-actual': '/observacion/convencional/datos/estacion/{idema}'
        },
        'predicciones-especificas': {
            'municipio-horaria': '/prediccion/especifica/municipio/horaria/{municipio}'
        },
        'valores-climatologicos': {
            'estacion-diaria': '/valores/climatologicos/diarios/datos/fechaini/{fechaIniStr}/fechafin/{fechaFinStr}/estacion/{idema}',
            'estaciones-diaria': '/valores/climatologicos/diarios/datos/fechaini/{fechaIniStr}/fechafin/{fechaFinStr}/todasestaciones'
        }
    }

    _instance = None
    _api_key = None

    def __new__(cls, api_key: str):
        if cls._instance is None:
            cls._instance = super(AEMETClient, cls).__new__(cls)
            cls._instance._initialize(api_key)
        return cls._instance

    def _initialize(self, api_key: str):
        self.logger = setup_logger("aemet_client")
        self.set_api_key(api_key)

    def set_api_key(self, api_key: str):
        self._api_key = api_key

    def _headers(self):
        return {'api_key': self._api_key}

    async def _make_request(self, session: aiohttp.ClientSession, endpoint: str, **kwargs):
        url = self.BASE_URL + endpoint.format(**kwargs)
        self.logger.info(f"Making request to {url}")

        response = await get_async(url=url, session=session, headers=self._headers())
        if response[0]['estado'] == 404:
            raise ValueError(f"Resource not found: {response[0]['descripcion']}")

        self.logger.info(f"Response: {response}")

        datos = await get_async(url=response[0]['datos'], session=session, headers=self._headers())
        metadatos = await get_async(url=response[0]['metadatos'], session=session, headers=self._headers())

        return {
            'datos': datos,
            'metadatos': metadatos
        }

    async def get_predicciones_municipio(self, session, municipio: str):
        endpoint = self.ENDPOINTS['predicciones-especificas']['municipio-horaria']
        response = await self._make_request(session, endpoint.format(municipio=municipio))

        return json.loads(response['datos'][0])[0]['prediccion']['dia']

    async def get_estacion_data(self, session, idema: str):
        endpoint = self.ENDPOINTS['observacion-convencional']['tiempo-actual']
        response = await self._make_request(session, endpoint.format(idema=idema))

        return json.loads(response['datos'][0])

    async def get_municipio(self, session, municipio_id: str):
        endpoint = self.ENDPOINTS['maestro']['municipio']
        response = await self._make_request(session, endpoint, municipio_id=municipio_id)

        return json.loads(response['datos'][0])

    async def get_historico_estacion(self, session, fechaIniStr: str, fechaFinStr: str, idema: str):
        endpoint = self.ENDPOINTS['valores-climatologicos']['estacion-diaria']
        response = await self._make_request(session, endpoint, fechaIniStr=_format_fecha(fechaIniStr),
                                            fechaFinStr=_format_fecha(fechaFinStr), idema=idema)

        return json.loads(response['datos'][0])

    async def get_historico_todas_estaciones(self, session, fechaIniStr: str, fechaFinStr: str):
        endpoint = self.ENDPOINTS['valores-climatologicos']['estaciones-diaria']
        response = await self._make_request(session, endpoint, fechaIniStr=_format_fecha(fechaIniStr),
                                            fechaFinStr=_format_fecha(fechaFinStr))

        return json.loads(response['datos'][0])
