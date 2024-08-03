from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.database.models import Model


engine = create_async_engine(
    "sqlite+aiosqlite:///sqlite/base.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)