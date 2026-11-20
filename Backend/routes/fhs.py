from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Query
from sqlmodel import Session
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import io
from dbmodel.Database import get_db
from services.fhs_engine import recalculate_and_store_fhs, calculate_fhs_from_dataframe, get_or_create_fhs_record

router = APIRouter(
    prefix="/fhs",
    tags=["Financial Health Score"]
)


class FHSUpdateRequest(BaseModel):
    user_id: Optional[int] = 1
    monthly_savings: Optional[float] = None
    monthly_debt_emi: Optional[float] = None
    monthly_income: Optional[float] = None
    quiz_score: Optional[float] = None


@router.get("")
def get_user_fhs(user_id: int = Query(1), db: Session = Depends(get_db)):
    """
    Returns user's current Financial Health Score and component breakdown from financial_health_score table.
    """
    return recalculate_and_store_fhs(session=db, user_id=user_id)


@router.post("/recalculate")
def recalculate_fhs(user_id: int = Query(1), db: Session = Depends(get_db)):
    """
    Recalculates FHS from latest database entries (schemes, income, debt, quiz).
    """
    return recalculate_and_store_fhs(session=db, user_id=user_id)


@router.post("/update")
def update_financial_data(payload: FHSUpdateRequest, db: Session = Depends(get_db)):
    """
    Updates user financial data (savings, EMI, quiz) and triggers pure math FHS recalculation.
    """
    user_id = payload.user_id or 1
    return recalculate_and_store_fhs(
        session=db,
        user_id=user_id,
        savings=payload.monthly_savings,
        debt_emi=payload.monthly_debt_emi,
        income=payload.monthly_income,
        quiz_score=payload.quiz_score
    )


@router.post("/calculate")
async def calculate_score(
    file: UploadFile = File(...),
    current_liquid_balance: float = Form(100000.0, description="Current savings balance entered by user"),
    user_id: int = Form(1),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported for statement analysis.")
        
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        result = calculate_fhs_from_dataframe(df, current_liquid_balance, session=db, user_id=user_id)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
