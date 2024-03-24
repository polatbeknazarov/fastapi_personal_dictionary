import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import Base, database
from auth.routes import router as auth_router
from auth.models import User
from dictionary.routes import router as dictionary_router
from dictionary.models import Word


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all, tables=[User.__table__, Word.__table__,])
        await conn.run_sync(Base.metadata.create_all, tables=[User.__table__, Word.__table__,])

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(dictionary_router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
