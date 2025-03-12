from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.routers.v1 import auth_router, users_router
import os
load_dotenv()
HOST: str = os.getenv("HOST", "localhost")
PORT: int = int(os.getenv("PORT", 8000))

app = FastAPI(debug=True)
app.include_router(auth_router, prefix="/api/v1")
# app.include_router(users_router, prefix="api/v1")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các domain
    allow_credentials=True,
    # Cho phép tất cả phương thức (GET, POST, PUT, DELETE, ...)
    allow_methods=["*"],
    allow_headers=["*"],  # Cho phép tất cả headers
)


@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, workers=1)
