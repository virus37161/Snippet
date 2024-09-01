from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.exceptions import HTTPException
from services.snippet import *
from schemas.snippet import SnippetSchema
from db.db import db_dependency

snippet_router = APIRouter()

@snippet_router.get("/{snippet_id}")
async def get_snippet(snippet_id, db:db_dependency):
    snippet = await get_snippet_with_id(db, snippet_id)
    return snippet

@snippet_router.post("/post")
async def post_snippet(snippet: SnippetSchema, db:db_dependency):
    result = await create_snippet(snippet.text, db)
    return result

@snippet_router.put("/{snippet_id}/update")
async def update_snippet(snippet: SnippetSchema, db: db_dependency, snippet_id):
    result = await change_snippet(snippet.text, db, snippet_id)
    return result

@snippet_router.delete("/{snippet_id}/delete")
async def delete_snippet(db: db_dependency, snippet_id):
    result = await delete_snippet_with_id(db, snippet_id)
    return result