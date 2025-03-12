from app.core.database import get_db
from app.schemas.user import CreateNewUser
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(request: CreateNewUser, db: AsyncSession = Depends(get_db)):
    pass
