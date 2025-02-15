from fastapi import APIRouter
from src.api.services.aemet.aemet_client import AEMETClient
from src.shared import helpers

client = AEMETClient(api_key=helpers.get_env_var("AEMET_API_KEY"))
router = APIRouter()

@router.get("/municipio/{municipio_id}")
async def get_municipio(municipio_id: str):
    return await client.get_municipio(municipio_id)

@router.get("/tiempo-actual/estacion/{idema}")
async def get_tiempo_actual_estacion(idema: str):
    return await client.get_estacion_data(idema)

@router.get("/tiempo-actual/municipio/{municipio}")
async def get_tiempo_actual_municipio(municipio: str):
    return await client.get_predicciones_municipio(municipio)