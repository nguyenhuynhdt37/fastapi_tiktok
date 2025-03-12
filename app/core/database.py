from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
MYSQL_DB_CONNECT = os.getenv(
    "MYSQL_DB_CONNECT", "mysql+asyncmy://admin:passs@localhost:3306/tiktok")
print(MYSQL_DB_CONNECT)

engine = create_async_engine(MYSQL_DB_CONNECT, echo=True)
print(engine)

async_session = async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        yield session
