from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_current_user, get_db
import pandas as pd
import numpy as np
from models.forecasting import run

router = APIRouter()

@router.post('/upload')
async def upload(
    file: UploadFile = File(...),
    user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not file.filename.endswith(('.csv', '.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="Invalid file type")
    df = pd.read_excel(file.file) if file.filename.endswith(('xls', 'xlsx')) else pd.read_csv(file.file)
    df.replace({np.nan: None, np.inf: None, -np.inf: None}, inplace=True)

    # Process df or send to ML pipeline
    return process_forecasting(df)

def process_forecasting(data):
    result = run(data)

    return result.to_dict("records")