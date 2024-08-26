from pydantic import BaseModel, EmailStr
from typing import Optional

class SnippetSchema(BaseModel):
    text: str