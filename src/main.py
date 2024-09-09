import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException, Request
from core.config import uvicorn_options
from sqlalchemy import text
from db.db import db_dependency
from api import api_router
import logging
from fastapi.responses import JSONResponse
from core.logger import LOGGING_CONFIG
import logging.config
import logging.handlers
import atexit
from contextlib import asynccontextmanager
from typing import AsyncContextManager

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncContextManager[None]:
    logging.config.dictConfig(LOGGING_CONFIG)
    # получаем обработчик очереди из корневого логгера
    queue_handler = logging.getHandlerByName("queue_handler")
    try:
        # если логгер есть
        if queue_handler is not None:
            # запускаем слушатель очереди
            queue_handler.listener.start()
            # регистрируем функцию, которая будет вызвана при завершении работы программы
            atexit.register(queue_handler.listener.stop)
        yield
    finally:
        # в случае ошибки выключаем слушатель
        if queue_handler is not None:
            queue_handler.listener.stop()

app = FastAPI(lifespan=lifespan, docs_url="/api/openapi")

router = APIRouter()

@app.get('/ping')
async def ping(db: db_dependency):
    try:
        await db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False

app.include_router(router)
app.include_router(api_router)


logger = logging.getLogger("app")

@app.exception_handler(Exception)
async def exception(request: Request, exc: Exception):
    logger.error(f"{request.url} | Error in application: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": exc}
    )


@app.exception_handler(HTTPException)
async def exception(request: Request, exc: HTTPException):
    logger.error(f"{request.url} | Error in application: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )



logging.config.dictConfig(LOGGING_CONFIG)

if __name__ == '__main__':
    # print для отображения настроек в терминале при локальной разработке
    print(uvicorn_options)
    uvicorn.run(
        'main:app',
        **uvicorn_options
    )