from src.api.services.aemet.aemet_client import AEMETClient
from fastapi import APIRouter
from src.shared import helpers

client = AEMETClient(api_key=helpers.get_env_var("AEMET_API_KEY"))
router = APIRouter()

@router.get(client.ENDPOINTS['maestro']['municipio'])
async def get_municipio(municipio_id: str):
    return await client.make_request(endpoint=client.ENDPOINTS['maestro']['municipio'], municipio_id=municipio_id)
