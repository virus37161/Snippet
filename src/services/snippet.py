from sqlalchemy.future import select

from db.db import db_dependency
from models import Snippet

async def get_snippet(db: db_dependency, snippet_id):
    result = await db.execute(select(Snippet).filter(Snippet.id == snippet_id))
    return result.scalars().first()

async def create_snippet(text, db: db_dependency):
    db_snippet = Snippet(text=text)
    db.add(db_snippet)
    await db.commit()
    await db.refresh(db_snippet)
    return db_snippet