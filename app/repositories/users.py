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

from app.schemas.user import AuthOtp


async def check_email_async(email: str, db: AsyncSession) -> dict:
    email = email.lower()
    exists = (
        await db.execute(select(models.Tbluser).filter(models.Tbluser.email == email))
    ).scalar_one_or_none()

    if exists:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    return {"message": "Email hợp lệ"}


async def create_user_async(request: dict, db: AsyncSession) -> models.Tbluser:
    try:
        if not check_is_email(request["email"]):
            raise HTTPException(status_code=400, detail="Email không hợp lệ")
        userModel = await db.execute(
            select(models.Tbluser).filter(models.Tbluser.email == request["email"])
        )
        if userModel.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email đã tồn tại")
        dt = datetime.strptime(request["birthday"], "%Y-%m-%dT%H:%M:%S.%fZ")
        dt = dt.replace(tzinfo=timezone.utc)
        user_create = models.Tbluser(**request)
        user_create.birthday = dt
        user_create.role_id = 2
        user_create.code = generate_otp()
        user_create.CodeExpiryTime = datetime.now() + timedelta(minutes=5)
        db.add(user_create)
        await db.commit()
        await db.refresh(user_create)
        await send_email(
            to_email=str(user_create.email),
            subject="Xác thực email",
            template_name="email_otp.html",
            otp=user_create.code,
        )
        return user_create
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi database: {str(e)}")


async def refresh_otp_async(email: str, db: AsyncSession):
    try:
        email = email.lower()
        user = (
            await db.execute(
                select(models.Tbluser).filter(models.Tbluser.email == email)
            )
        ).scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=400, detail="Email không tồn tại")
        user.code = generate_otp()
        user.CodeExpiryTime = datetime.now() + timedelta(minutes=5)
        await db.commit()
        await db.refresh(user)
        await send_email(
            to_email=str(user.email),
            subject="Xác thực email",
            template_name="email_otp.html",
            otp=user.code,
        )
        return {"message": "Mã OTP đã được gửi lại"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi database: {str(e)}")


async def authentication_otp_async(request: AuthOtp, db: AsyncSession):
    try:
        if not check_is_email(request.email):
            raise HTTPException(status_code=400, detail="Email không hợp lệ")
        userModel = (
            await db.execute(
                select(models.Tbluser).filter(models.Tbluser.email == request.email)
            )
        ).scalar_one_or_none()
        if not userModel:
            raise HTTPException(status_code=400, detail="Email không tồn tại")
        if userModel.isActive == 1:
            raise HTTPException(status_code=400, detail="Tài khoản đã được xác thực")
        if userModel.code != request.otp:
            raise HTTPException(status_code=400, detail="Mã OTP không hợp lệ")
        if (
            userModel.CodeExpiryTime is None
            or userModel.CodeExpiryTime < datetime.now()
        ):
            raise HTTPException(status_code=400, detail="OTP đã hết hạn")
        userModel.isActive = 1
        await db.commit()
        await db.refresh(userModel)
        return {"message": "Xác thực thành công"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi database: {str(e)}")
