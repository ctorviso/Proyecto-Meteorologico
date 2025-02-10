from app.services.aemet.aemet_client import AEMETClient
import os
from dotenv import load_dotenv
from fastapi import APIRouter

load_dotenv()

client = AEMETClient(api_key=os.getenv('AEMET_API_KEY'))
router = APIRouter()

@router.get("/municipios")
async def get_municipios():
    return await client.get_municipios()


