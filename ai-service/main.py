from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Asset Evaluation ML Service")


class AssetEvaluationRequest(BaseModel):
    category: str
    brand: str
    initial_price_eur: float
    age_months: int
    ram_gb: int
    storage_gb: int
    grade: str
    market_avg_price_eur: Optional[float] = None


class AssetEvaluationResponse(BaseModel):
    predicted_residual_value_eur: float
    confidence_interval_lower_eur: float
    confidence_interval_upper_eur: float
    margin_error_percentage: float


@app.post("/predict-residual-value", response_model=AssetEvaluationResponse)
def predict_residual_value(request: AssetEvaluationRequest):
    try:
        # Гибридный расчёт: базой служит рыночная цена (если передана)
        base_price = (
            request.market_avg_price_eur
            if request.market_avg_price_eur
            else request.initial_price_eur * 0.5
        )

        # Поправка на грейд состояния
        grade_modifier = {
            "Grade A": 1.1,
            "Grade B": 1.0,
            "Grade C": 0.85,
        }.get(request.grade, 1.0)

        predicted_value = round(base_price * grade_modifier, 2)
        lower_bound = round(predicted_value * 0.92, 2)
        upper_bound = round(predicted_value * 1.08, 2)
        margin_error = round(
            ((upper_bound - predicted_value) / predicted_value) * 100, 2
        )

        return AssetEvaluationResponse(
            predicted_residual_value_eur=predicted_value,
            confidence_interval_lower_eur=lower_bound,
            confidence_interval_upper_eur=upper_bound,
            margin_error_percentage=margin_error,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    