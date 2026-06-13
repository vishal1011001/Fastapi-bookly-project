from sqlmodel import text, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.config import Config

engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)

async def init_db():
    async with engine.begin() as conn:
        from src.books.models import BookModel
        
        await conn.run_sync(SQLModel.metadata.create_all)        
