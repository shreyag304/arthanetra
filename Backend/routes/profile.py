
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Query, Header
from sqlmodel import Session, select
from pydantic import BaseModel, Field
from dbmodel.Database import get_db
from dbmodel.models import User

router = APIRouter(prefix="/profile", tags=["profile"])


class ProfileResponse(BaseModel):
    user_id: int
    id: int
    name: str
    mobile: str
    email: Optional[str] = None
    created_at: Optional[datetime] = None
    language: Optional[str] = "English"
    financial_health_score: Optional[int] = 75
    persona: Optional[str] = "Standard User"
    income_type: Optional[str] = "Variable"
    goal: Optional[str] = "Budget Optimization"


class ProfileUpdateRequest(BaseModel):
    user_id: Optional[int] = None
    id: Optional[int] = None
    name: Optional[str] = None
    mobile: Optional[str] = Field(None, max_length=10)
    password: Optional[str] = None
    email: Optional[str] = None
    language: Optional[str] = None
    financial_health_score: Optional[int] = None
    persona: Optional[str] = None
    income_type: Optional[str] = None
    goal: Optional[str] = None


def _user_to_profile_response(user: User) -> ProfileResponse:
    return ProfileResponse(
        user_id=user.id or 0,
        id=user.id or 0,
        name=user.name,
        mobile=user.mobile,
        email=user.email,
        created_at=user.created_at,
        language=user.language if user.language is not None else "English",
        financial_health_score=user.financial_health_score if user.financial_health_score is not None else 75,
        persona=user.persona if user.persona is not None else "Standard User",
        income_type=user.income_type if user.income_type is not None else "Variable",
        goal=user.goal if user.goal is not None else "Budget Optimization",
    )


@router.get("", response_model=ProfileResponse)
@router.get("/", response_model=ProfileResponse, include_in_schema=False)
def get_profile(
    user_id: Optional[int] = Query(None, description="Optional user ID to query"),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    target_id = user_id
    if target_id is None and authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            try:
                target_id = int(parts[1])
            except ValueError:
                pass

    if target_id is not None:
        user = db.exec(select(User).where(User.id == target_id)).first()
    else:
        user = db.exec(select(User)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return _user_to_profile_response(user)


@router.get("/{user_id}", response_model=ProfileResponse)
def get_profile_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_to_profile_response(user)


@router.put("", response_model=ProfileResponse)
@router.put("/", response_model=ProfileResponse, include_in_schema=False)
def update_profile(
    payload: ProfileUpdateRequest,
    user_id: Optional[int] = Query(None, description="Optional user ID to update"),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    target_id = user_id or payload.user_id or payload.id
    if target_id is None and authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            try:
                target_id = int(parts[1])
            except ValueError:
                pass

    if target_id is not None:
        user = db.exec(select(User).where(User.id == target_id)).first()
    else:
        user = db.exec(select(User)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.name is not None:
        user.name = payload.name
    if payload.email is not None:
        user.email = payload.email
    if payload.password is not None:
        user.password = payload.password
    if payload.mobile is not None and payload.mobile != user.mobile:
        existing_user = db.exec(select(User).where(User.mobile == payload.mobile)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Mobile number already registered")
        user.mobile = payload.mobile
    if payload.language is not None:
        user.language = payload.language
    if payload.financial_health_score is not None:
        user.financial_health_score = payload.financial_health_score
    if payload.persona is not None:
        user.persona = payload.persona
    if payload.income_type is not None:
        user.income_type = payload.income_type
    if payload.goal is not None:
        user.goal = payload.goal

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return _user_to_profile_response(user)
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update user profile")


@router.put("/{user_id}", response_model=ProfileResponse)
def update_profile_by_id(
    user_id: int, payload: ProfileUpdateRequest, db: Session = Depends(get_db)
):
    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.name is not None:
        user.name = payload.name
    if payload.email is not None:
        user.email = payload.email
    if payload.password is not None:
        user.password = payload.password
    if payload.mobile is not None and payload.mobile != user.mobile:
        existing_user = db.exec(select(User).where(User.mobile == payload.mobile)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Mobile number already registered")
        user.mobile = payload.mobile
    if payload.language is not None:
        user.language = payload.language
    if payload.financial_health_score is not None:
        user.financial_health_score = payload.financial_health_score
    if payload.persona is not None:
        user.persona = payload.persona
    if payload.income_type is not None:
        user.income_type = payload.income_type
    if payload.goal is not None:
        user.goal = payload.goal

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return _user_to_profile_response(user)
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update user profile")
