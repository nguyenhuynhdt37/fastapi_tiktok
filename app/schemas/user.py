import datetime
from pydantic import BaseModel, Field
from app.models.models import Base


class CreateNewUser(BaseModel):
    email: str = Field(min_length=1, description="Email không được để trống")
    password: str = Field(
        min_length=8, max_length=50, description="Mật khẩu phải từ 8 đến 50 ký tự"
    )
    birthday: str = Field(description="Ngày sinh")


class ShowUser(BaseModel):
    id: int | None
    phone_number: str | None
    email: str | None
    avatar: str | None
    create_at: datetime.datetime | None
    update_at: datetime.datetime | None
    role_id: int | None


class AuthOtp(BaseModel):
    email: str = Field(min_length=1, description="Email không được để trống")
    otp: str = Field(min_length=6, max_length=6, description="OTP phải 6 ký tự")
