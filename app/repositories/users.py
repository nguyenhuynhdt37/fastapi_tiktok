import datetime
from pathlib import Path
from fastapi import HTTPException
import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import models
from sqlalchemy.exc import SQLAlchemyError
from app.libs.helpers import generate_otp
from app.libs.checkSyntax import check_is_email
from app.repositories.sendEmail import send_email
from datetime import datetime, timedelta, timezone


async def check_email_async(email: str, db: AsyncSession) -> dict:
    email = email.lower()
    exists = (await db.execute(select(models.Tbluser).filter(models.Tbluser.email == email))).scalar_one_or_none()

    if exists:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    return {"message": "Email hợp lệ"}


async def create_user_async(request: dict, db: AsyncSession) -> models.Tbluser:
    try:
        if not check_is_email(request['email']):
            raise HTTPException(status_code=400, detail="Email không hợp lệ")
        userModel = await db.execute(select(models.Tbluser).filter(models.Tbluser.email == request['email']))
        if userModel.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email đã tồn tại")
        dt = datetime.strptime(request['birthday'],
                               "%Y-%m-%dT%H:%M:%S.%fZ")
        dt = dt.replace(tzinfo=timezone.utc)
        user_create = models.Tbluser(**request)
        user_create.birthday = dt
        user_create.code = generate_otp()
        user_create.CodeExpiryTime = datetime.now() + timedelta(minutes=5)
        db.add(user_create)
        await db.commit()
        await db.refresh(user_create)
        await send_email(to_email=str(user_create.email), subject="Xác thực email", template_name="email_otp.html", otp=user_create.code)
        return user_create
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi database: {str(e)}")
