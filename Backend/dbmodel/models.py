# models.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    mobile: str = Field(unique=True, index=True, max_length=10)
    email: Optional[str] = Field(default=None, index=True)
    password: str  # plaintext for now, bcrypt later
    created_at: datetime = Field(default_factory=datetime.utcnow)
    language: Optional[str] = Field(default="English", nullable=True)
    financial_health_score: Optional[int] = Field(default=75, nullable=True)
    persona: Optional[str] = Field(default="Standard User", nullable=True)
    income_type: Optional[str] = Field(default="Variable", nullable=True)
    goal: Optional[str] = Field(default="Budget Optimization", nullable=True)


    '''
    Manual Action Required for Existing Databases
  │ Because Alembic is not configured and  SQLModel.metadata.create_all()  does not
  │ automatically issue  ALTER TABLE  statements to add columns to existing tables 
  │ in PostgreSQL/SQLite, if your database volume ( Backend/dbmodel/data/db )      
  │ already contains a  users  table created prior to this change, you will need to
  │ either:
  │
  │ 1.ALTER TABLE users ADD COLUMN language VARCHAR DEFAULT 'English', ADD   
  │ COLUMN financial_health_score INTEGER DEFAULT 75, ADD COLUMN persona VARCHAR   
  │ DEFAULT 'Standard User', ADD COLUMN income_type VARCHAR DEFAULT 'Variable', ADD
  │ COLUMN goal VARCHAR DEFAULT 'Budget Optimization';  directly against PostgreSQL
  │ via Adminer or  psq
    '''