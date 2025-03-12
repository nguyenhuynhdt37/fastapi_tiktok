from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import TblUser


async def check_email_async(email: str, db: AsyncSession) -> dict:
    email = email.lower()
    exists = (await db.execute(select(TblUser).filter(TblUser.email == email))).scalar_one_or_none()

    if exists:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    return {"message": "Email hợp lệ"}
