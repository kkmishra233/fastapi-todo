import time
from typing import Any, Callable, TypeVar
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from core.config import settings
from initialize import init
from fastapi.middleware.cors import CORSMiddleware
from utility.logger import logger

app = FastAPI(
    title=settings.PROJECT_TITLE, 
    version=settings.PROJECT_VERSION
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)