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

@app.middleware("http")
async def log_structured_requests(request: Request, call_next):
    logger.info({
        "event": "request",
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "client": request.client.host
    })
    response = await call_next(request)
    logger.info({
        "event": "response",
        "status_code": response.status_code
    })
    return response

init(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)