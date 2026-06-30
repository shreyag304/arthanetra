# models.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    mobile: str = Field(unique=True, index=True, max_length=10)
    password: str  # plaintext for now, bcrypt later
    created_at: datetime = Field(default_factory=datetime.utcnow)