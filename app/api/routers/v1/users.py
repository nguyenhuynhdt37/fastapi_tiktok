from app.core.database import get_db


from fastapi import APIRouter, status, Depends


router = APIRouter(prefix="/users", tags=["Users"])
