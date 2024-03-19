import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
