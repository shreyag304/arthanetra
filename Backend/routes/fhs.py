from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
import pandas as pd
import io
from services.fhs_engine import calculate_fhs_from_dataframe
from dbmodel.Database import get_db
from dbmodel.models import User
from sqlmodel import Session

router = APIRouter(
    prefix="/financial-health",
    tags=["Financial Health Score"]
)

@router.post("/upload")
async def calculate_score(
    file: UploadFile = File(...),
    current_liquid_balance: float = Form(100000.0, description="Current savings balance entered by user"),
    user_id: int = Form(None),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported for the MVP.")
        
    try:
        # Read the uploaded CSV directly into memory
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Run our scoring engine
        result = calculate_fhs_from_dataframe(df, current_liquid_balance)
        
        # Save to DB if user_id is provided
        if user_id is not None:
            user = db.get(User, user_id)
            if user:
                user.fhs_score = result.get("final_fhs")
                db.add(user)
                db.commit()
                
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
