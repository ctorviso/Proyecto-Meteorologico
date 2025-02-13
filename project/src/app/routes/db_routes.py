from app.db.db_handler import DBHandler
from fastapi import APIRouter, HTTPException

db = DBHandler()
router = APIRouter()
