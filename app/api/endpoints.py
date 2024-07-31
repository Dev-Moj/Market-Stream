from fastapi import APIRouter
from app.database.db_operations import fetch_data

router = APIRouter()

@router.get("/data")
async def read_data():
    data = await fetch_data()
    return data
