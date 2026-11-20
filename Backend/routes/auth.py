from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from pydantic import BaseModel, Field
from dbmodel.Database import get_db
from dbmodel.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=10)
    password: str


class LoginResponse(BaseModel):
    message: str
    user_id: int
    name: str
    mobile: str
    email: Optional[str] = None


class RegisterRequest(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=10)
    password: str = Field(..., min_length=1)
    name: Optional[str] = "User"
    email: Optional[str] = None


class RegisterResponse(BaseModel):
    message: str
    user_id: int
    name: str
    mobile: str
    email: Optional[str] = None


class CheckRegistrationResponse(BaseModel):
    mobile: str
    is_registered: bool
    available: bool
    message: str


# authentication endpoint
@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.mobile == payload.mobile)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return LoginResponse(
        message="Login successful",
        user_id=user.id,
        name=user.name,
        mobile=user.mobile,
        email=user.email,
    )


# check registration availability / status endpoint
@router.get("/register", response_model=CheckRegistrationResponse)
def check_registration(
    mobile: str = Query(..., min_length=10, max_length=10, description="10-digit mobile number to check"),
    db: Session = Depends(get_db),
):
    user = db.exec(select(User).where(User.mobile == mobile)).first()
    if user:
        return CheckRegistrationResponse(
            mobile=mobile,
            is_registered=True,
            available=False,
            message="Mobile number is already registered",
        )
    return CheckRegistrationResponse(
        mobile=mobile,
        is_registered=False,
        available=True,
        message="Mobile number is available for registration",
    )


# registration endpoint
@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.exec(select(User).where(User.mobile == payload.mobile)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Mobile number already registered")

    try:
        new_user = User(
            name=payload.name or "User",
            mobile=payload.mobile,
            email=payload.email,
            password=payload.password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return RegisterResponse(
            message="Registration successful",
            user_id=new_user.id,
            name=new_user.name,
            mobile=new_user.mobile,
            email=new_user.email,
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to register user")

