from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import pandas as pd
import io
from services.fhs_engine import calculate_fhs_from_dataframe

router = APIRouter(
    prefix="/fhs",
    tags=["Financial Health Score"]
)

@router.post("/calculate")
async def calculate_score(
    file: UploadFile = File(...),
    current_liquid_balance: float = Form(100000.0, description="Current savings balance entered by user")
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported for the MVP.")
        
    try:
        # Read the uploaded CSV directly into memory
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Run our scoring engine
        result = calculate_fhs_from_dataframe(df, current_liquid_balance)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
