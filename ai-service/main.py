from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
import joblib
import os

app = FastAPI(title="CHG-Meridian Residual Value AI Service")

MODEL_PATH = "residual_value_model.pkl"
if not os.path.exists(MODEL_PATH):
    raise RuntimeError("Сначала запустите train_model.py!")

model = joblib.load(MODEL_PATH)

class AssetRequest(BaseModel):
    category: str = Field(..., example="Laptop")
    brand: str = Field(..., example="Dell")
    initial_price_eur: float = Field(..., example=1500.0)
    age_months: int = Field(..., example=36)
    ram_gb: int = Field(..., example=16)
    storage_gb: int = Field(..., example=512)
    grade: str = Field(..., example="Grade A")

@app.post("/predict-residual-value")
def predict_residual_value(request: AssetRequest):
    try:
        input_data = pd.DataFrame([request.model_dump()])
        rf_model = model.named_steps['regressor']
        transformed_input = model.named_steps['preprocessor'].transform(input_data)
        
        preds = [tree.predict(transformed_input)[0] for tree in rf_model.estimators_]
        
        median_val = float(np.median(preds))
        lower_bound = float(np.percentile(preds, 2.5))
        upper_bound = float(np.percentile(preds, 97.5))
        margin_pct = round(((upper_bound - lower_bound) / (2 * median_val)) * 100, 2)
        
        return {
            "predicted_residual_value_eur": round(median_val, 2),
            "confidence_interval_lower_eur": round(lower_bound, 2),
            "confidence_interval_upper_eur": round(upper_bound, 2),
            "margin_error_percentage": margin_pct
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    