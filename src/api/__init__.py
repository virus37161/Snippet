from fastapi import APIRouter

from api.v1.snippet import snippet_router
from api.v1.user import user_router
from api.v1.auth import auth_router

api_router = APIRouter()

api_router.include_router(snippet_router)
api_router.include_router(user_router)
api_router.include_router(auth_router)