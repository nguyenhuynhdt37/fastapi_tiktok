from pydantic import BaseModel, Field


class CreateNewUser(BaseModel):
    name: str = Field(min_length=8, max_length=50,
                      description="Tên phải từ 8 đến 50 ký tự")
    email: str = Field(min_length=1,
                       description="Email không được để trống")
    password: str = Field(min_length=8, max_length=50,
                          description="Mật khẩu phải từ 8 đến 50 ký tự")
