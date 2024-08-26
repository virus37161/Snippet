import uvicorn
from fastapi import FastAPI, APIRouter
from core.config import uvicorn_options
from sqlalchemy import text
from db.db import db_dependency
from api import api_router
app = FastAPI(docs_url = "/api/openapi")

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
if __name__ == '__main__':
    # print для отображения настроек в терминале при локальной разработке
    print(uvicorn_options)
    uvicorn.run(
        'main:app',
        **uvicorn_options
    )