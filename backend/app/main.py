
from pathlib import Path

import json
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# Locate the project root and trained model
ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "artifacts" / "student_risk_model.joblib"

app = FastAPI(
    title="Student Performance Analytics API",
    description="Educational prototype for student risk analysis.",
    version="1.0.0",
)
@app.get("/metrics")
def get_metrics():
    metrics_path = ROOT / "reports" / "metrics.json"

    if not metrics_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Metrics file not found"
        )

    with open(metrics_path, "r", encoding="utf-8") as file:
        return json.load(file)
@app.get("/metrics")
def get_metrics():
    metrics_path = ROOT / "reports" / "metrics.json"

    if not metrics_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Metrics file not found"
        )

    with open(metrics_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Allow the local React development server to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StudentFeatures(BaseModel):
    school: str = Field(pattern="^(GP|MS)$")
    sex: str = Field(pattern="^(F|M)$")
    age: int = Field(ge=15, le=22)
    address: str = Field(pattern="^(U|R)$")
    famsize: str = Field(pattern="^(LE3|GT3)$")
    Pstatus: str = Field(pattern="^(T|A)$")

    Medu: int = Field(ge=0, le=4)
    Fedu: int = Field(ge=0, le=4)
    Mjob: str = Field(pattern="^(teacher|health|services|at_home|other)$")
    Fjob: str = Field(pattern="^(teacher|health|services|at_home|other)$")
    reason: str = Field(pattern="^(home|reputation|course|other)$")
    guardian: str = Field(pattern="^(mother|father|other)$")

    traveltime: int = Field(ge=1, le=4)
    studytime: int = Field(ge=1, le=4)
    failures: int = Field(ge=0, le=4)
    schoolsup: str = Field(pattern="^(yes|no)$")
    famsup: str = Field(pattern="^(yes|no)$")
    paid: str = Field(pattern="^(yes|no)$")
    activities: str = Field(pattern="^(yes|no)$")
    nursery: str = Field(pattern="^(yes|no)$")
    higher: str = Field(pattern="^(yes|no)$")
    internet: str = Field(pattern="^(yes|no)$")
    romantic: str = Field(pattern="^(yes|no)$")

    famrel: int = Field(ge=1, le=5)
    freetime: int = Field(ge=1, le=5)
    goout: int = Field(ge=1, le=5)
    Dalc: int = Field(ge=1, le=5)
    Walc: int = Field(ge=1, le=5)
    health: int = Field(ge=1, le=5)
    absences: int = Field(ge=0, le=100)


@app.get("/")
def home():
    return {
        "message": "Student Performance Analytics API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_exists": MODEL_PATH.exists(),
    }


@app.post("/predict")
def predict(student: StudentFeatures):
    if not MODEL_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail="Trained model not found. Run ml/src/train.py first.",
        )

    try:
        model = joblib.load(MODEL_PATH)
        features = pd.DataFrame([student.model_dump()])
        prediction = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0][1])

        return {
            "at_risk": bool(prediction),
            "risk_probability": round(probability, 4),
            "interpretation": (
                "Potential support may be useful."
                if prediction == 1
                else "The model did not flag this profile as at risk."
            ),
            "notice": (
                "Educational prototype only; not a diagnosis or "
                "a basis for consequential decisions."
            ),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {type(exc).__name__}",
        ) from exc