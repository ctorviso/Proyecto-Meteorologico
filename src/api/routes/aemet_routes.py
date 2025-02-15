from fastapi import APIRouter
from src.api.services.aemet.aemet_client import AEMETClient
from src.shared import helpers

client = AEMETClient(api_key=helpers.get_env_var("AEMET_API_KEY"))
router = APIRouter()

@router.get("/municipio/{municipio_id}")
async def get_municipio(municipio_id: str):
    endpoint = client.ENDPOINTS['maestro']['municipio']
    return await client.make_request(endpoint, municipio_id=municipio_id)

@router.get("/tiempo-actual/{idema}")
async def get_tiempo_actual(idema: str):
    endpoint = client.ENDPOINTS['observacion-convencional']['tiempo-actual']
    return await client.make_request(endpoint, idema=idema)