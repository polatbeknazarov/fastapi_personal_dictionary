import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import Base, database


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
