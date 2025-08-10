from settings import POSTGRES_DSN
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(POSTGRES_DSN, echo=False)
async_sessionmaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session() -> AsyncSession:
    async with async_sessionmaker() as session:
        yield session
