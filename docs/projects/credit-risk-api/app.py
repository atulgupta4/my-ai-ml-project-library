
import time
import uuid

import mlflow.sklearn
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from audit import initialize_audit_db, log_prediction


# --------------------------------------------------
# Model configuration
# --------------------------------------------------

MODEL_PATH = "models/credit_risk_model"

MODEL_NAME = "credit-risk-logistic-regression"
MODEL_VERSION = "1"
MODEL_RUN_ID = "442519574eba4901bfc49514bb027143"

DECISION_THRESHOLD = 0.30

FEATURE_COLUMNS = [f"X{i}" for i in range(1, 24)]


# --------------------------------------------------
# Load model and initialize audit database
# --------------------------------------------------

model = mlflow.sklearn.load_model(MODEL_PATH)

initialize_audit_db()

app = FastAPI(
    title="Credit Risk Scoring API",
    description="Predicts credit card customer default risk.",
    version="1.0.0"
)


# --------------------------------------------------
# Request schema
# --------------------------------------------------

class CustomerInput(BaseModel):

    X1: float = Field(description="Credit limit")
    X2: int = Field(description="Sex")
    X3: int = Field(description="Education")
    X4: int = Field(description="Marriage")
    X5: int = Field(description="Age")

    X6: int = Field(description="September repayment status")
    X7: int = Field(description="August repayment status")
    X8: int = Field(description="July repayment status")
    X9: int = Field(description="June repayment status")
    X10: int = Field(description="May repayment status")
    X11: int = Field(description="April repayment status")

    X12: float = Field(description="September bill amount")
    X13: float = Field(description="August bill amount")
    X14: float = Field(description="July bill amount")
    X15: float = Field(description="June bill amount")
    X16: float = Field(description="May bill amount")
    X17: float = Field(description="April bill amount")

    X18: float = Field(description="September payment amount")
    X19: float = Field(description="August payment amount")
    X20: float = Field(description="July payment amount")
    X21: float = Field(description="June payment amount")
    X22: float = Field(description="May payment amount")
    X23: float = Field(description="April payment amount")


# --------------------------------------------------
# Health endpoint
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "model_version": MODEL_VERSION
    }


# --------------------------------------------------
# Prediction endpoint
# --------------------------------------------------

@app.post("/predict")
def predict(customer: CustomerInput):

    try:

        request_id = str(uuid.uuid4())

        customer_data = pd.DataFrame(
            [customer.model_dump()],
            columns=FEATURE_COLUMNS
        )

        start_time = time.perf_counter()

        probability = float(
            model.predict_proba(customer_data)[0, 1]
        )

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        decision = (
            "MANUAL_REVIEW"
            if probability >= DECISION_THRESHOLD
            else "LOW_RISK"
        )

        log_prediction(
            request_id=request_id,
            model_name=MODEL_NAME,
            model_version=MODEL_VERSION,
            run_id=MODEL_RUN_ID,
            probability=probability,
            threshold=DECISION_THRESHOLD,
            decision=decision,
            latency_ms=latency_ms
        )

        return {
            "request_id": request_id,
            "model_name": MODEL_NAME,
            "model_version": MODEL_VERSION,
            "default_probability": round(probability, 6),
            "decision_threshold": DECISION_THRESHOLD,
            "decision": decision,
            "latency_ms": round(latency_ms, 3)
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
