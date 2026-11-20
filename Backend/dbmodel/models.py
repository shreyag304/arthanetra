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


class UserFinancialProfile(SQLModel, table=True):
    __tablename__ = "user_financial_profile"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, unique=True)
    occupation: Optional[str] = Field(default=None, nullable=True)
    preferred_language: Optional[str] = Field(default="English", nullable=True)
    financial_goals: Optional[str] = Field(default=None, nullable=True)
    monthly_income: Optional[float] = Field(default=None, nullable=True)
    age: Optional[int] = Field(default=25, nullable=True)
    owns_land: Optional[bool] = Field(default=False, nullable=True)
    is_tax_payer: Optional[bool] = Field(default=False, nullable=True)
    profile_completed: bool = Field(default=False)
    next_question: Optional[str] = Field(default="occupation", nullable=True)
    
    # Active conversational context tracking
    last_route: Optional[str] = Field(default=None, nullable=True)  # "scam_detection", "gov_scheme", "financial_coach", "profiling"
    last_topic: Optional[str] = Field(default=None, nullable=True)
    last_scam_risk: Optional[float] = Field(default=None, nullable=True)
    last_user_query: Optional[str] = Field(default=None, nullable=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ChatMessageHistory(SQLModel, table=True):
    __tablename__ = "chat_message_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    sender: str = Field(index=True)  # "user" | "assistant"
    message: str
    route: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ScamReport(SQLModel, table=True):
    __tablename__ = "scam_reports"

    report_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, index=True, nullable=True)
    risk_score: float = Field(default=0.0)
    verdict: str = Field(default="LOW_RISK")  # "LOW_RISK" | "HIGH_RISK" | "SCAM"
    flagged_text: str = Field(default="")
    reasoning: str = Field(default="")
    detection_source: str = Field(default="fast_filter")  # "fast_filter" | "llm_analysis"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class GovtScheme(SQLModel, table=True):
    __tablename__ = "govt_schemes"

    scheme_id: Optional[int] = Field(default=None, primary_key=True)
    scheme_name: str = Field(index=True)
    description: str
    category: str
    min_age: Optional[int] = Field(default=None, nullable=True)
    max_age: Optional[int] = Field(default=None, nullable=True)
    requires_land: Optional[bool] = Field(default=False, nullable=True)
    max_income: Optional[float] = Field(default=None, nullable=True)
    target_occupations: Optional[str] = Field(default=None, nullable=True)
    benefits: str
    required_documents: str


class UserSchemeMatch(SQLModel, table=True):
    __tablename__ = "user_scheme_matches"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    scheme_id: int = Field(index=True)
    scheme_name: str
    match_reason: str
    step_by_step_guide: Optional[str] = Field(default=None, nullable=True)
    matched_at: datetime = Field(default_factory=datetime.utcnow)


class FinancialHealthScore(SQLModel, table=True):
    __tablename__ = "financial_health_score"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, unique=True)
    score: float = Field(default=75.0)
    savings_rate: float = Field(default=0.25)
    savings_score: float = Field(default=80.0)
    debt_ratio: float = Field(default=0.15)
    debt_score: float = Field(default=85.0)
    scheme_utilization: float = Field(default=0.50)
    scheme_score: float = Field(default=70.0)
    quiz_score: float = Field(default=70.0)
    monthly_income: float = Field(default=25000.0)
    monthly_savings: float = Field(default=5000.0)
    monthly_debt_emi: float = Field(default=3000.0)
    schemes_enrolled_count: int = Field(default=1)
    quiz_completed: bool = Field(default=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)




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