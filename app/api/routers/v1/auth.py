from app.core.database import get_db
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from app.libs.checkSyntax import check_is_email
from app.repositories.users import check_email_async
from app.schemas.user import CreateNewUser, ShowUser
from app.repositories.users import create_user_async


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get('/check_email', status_code=status.HTTP_200_OK)
async def check_email(email: str = Query(...), db: AsyncSession = Depends(get_db)):
    if not check_is_email(email):
        raise HTTPException(status_code=400, detail="Email không hợp lệ")
    return await check_email_async(email=email, db=db)


@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def create_user(request: CreateNewUser, db: AsyncSession = Depends(get_db)):
    return await create_user_async(request.dict(), db)


# @router.post('/sent_otp', status_code=status.HTTP_200_OK)
