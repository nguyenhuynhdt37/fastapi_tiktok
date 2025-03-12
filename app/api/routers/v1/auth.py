from app.core.database import get_db
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.libs.checkSyntax import check_is_email
from app.repositories.users import check_email_async


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get('/check_email', status_code=status.HTTP_200_OK)
async def check_email(email: str = Query(...), db: AsyncSession = Depends(get_db)):
    if not check_is_email(email):
        raise HTTPException(status_code=400, detail="Email không hợp lệ")
    return await check_email_async(email=email, db=db)
