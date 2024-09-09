from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.exceptions import HTTPException
from services.snippet import *
from schemas.snippet import SnippetSchema
from db.db import db_dependency
from .user import has_role
from auth.auth import user_dependency
snippet_router = APIRouter()

@snippet_router.get("/{snippet_id}")
async def get_snippet(snippet_id, db:db_dependency):
    snippet = await get_snippet_with_id(db, snippet_id)
    return snippet

@snippet_router.post("/post", dependencies=[Depends(has_role(["user"]))])
async def post_snippet(snippet: SnippetSchema, db:db_dependency, current_user:user_dependency):
    result = await create_snippet(snippet.text, db, current_user)
    return result

@snippet_router.put("/{snippet_id}/update", dependencies=[Depends(has_role(["user"]))])
async def update_snippet(snippet: SnippetSchema, db: db_dependency, snippet_id, current_user:user_dependency):
    result = await change_snippet(snippet.text, db, snippet_id, current_user)
    return result

@snippet_router.delete("/{snippet_id}/delete", dependencies=[Depends(has_role(["user"]))])
async def delete_snippet(db: db_dependency, snippet_id, current_user:user_dependency):
    result = await delete_snippet_with_id(db, snippet_id, current_user)
    return result