from sqlalchemy.future import select
from starlette import status
from fastapi import HTTPException
from db.db import db_dependency
from models import Snippet
from auth.auth import user_dependency
async def get_snippet_with_id(db: db_dependency, snippet_id):
    result = await db.execute(select(Snippet).filter(Snippet.id == snippet_id))
    return result.scalars().first()

async def create_snippet(text, db: db_dependency, current_user):
    user_id = current_user['user_id']
    db_snippet = Snippet(text=text, user_id=user_id)
    db.add(db_snippet)
    await db.commit()
    await db.refresh(db_snippet)
    return db_snippet

async def change_snippet(text, db:db_dependency, snippet_id, current_user):
    snippet = await get_snippet_with_id(db, snippet_id)
    if snippet:
        if snippet.user_id != current_user['user_id']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        snippet.text = text
        await db.commit()
        await db.refresh(snippet)
    return snippet

async def delete_snippet_with_id(db:db_dependency, snippet_id, current_user):
    snippet = await get_snippet_with_id(db, snippet_id)
    if snippet:
        if snippet.user_id != current_user['user_id']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        await db.delete(snippet)
        await db.commit()
    return snippet