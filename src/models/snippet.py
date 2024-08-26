import uuid
from sqlalchemy import String, Column, Integer, TIMESTAMP,ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

class Snippet(Base):
    __tablename__ = "snippet"
    id = Column(UUID, primary_key=True, index=True, default=str(uuid.uuid4()))
    text = Column(String(256), nullable=False)
