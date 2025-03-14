from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.routers.v1 import auth_router, users_router
import os
load_dotenv()
HOST: str = os.getenv("HOST", "localhost")
PORT: int = int(os.getenv("PORT", 8000))

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc chỉ định ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/api/v1")
# app.include_router(users_router, prefix="api/v1")


@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, workers=1)
