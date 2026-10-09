
from pathlib import Path
import json

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
)
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.base import clone


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = ROOT / "data" / "student-mat.csv"
ARTIFACTS_DIR = ROOT / "artifacts"
REPORTS_DIR = ROOT / "reports"

ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}"
    )


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

df = pd.read_csv(DATA_PATH, sep=";")

# Target: 1 means at risk; 0 means not at risk.
y = (df["G3"] < 10).astype(int)

# Exclude all grade columns to avoid grade leakage.
X = df.drop(columns=["G1", "G2", "G3"])

print("Dataset shape:", df.shape)
print("\nAt-risk distribution:")
print(y.value_counts().rename(
    index={1: "At risk", 0: "Not at risk"}
))


# --------------------------------------------------
# 3. Define input features
# --------------------------------------------------

NUMERIC_FEATURES = [
    "age", "Medu", "Fedu", "traveltime", "studytime",
    "failures", "famrel", "freetime", "goout",
    "Dalc", "Walc", "health", "absences",
]

CATEGORICAL_FEATURES = [
    "school", "sex", "address", "famsize", "Pstatus",
    "Mjob", "Fjob", "reason", "guardian", "schoolsup",
    "famsup", "paid", "activities", "nursery", "higher",
    "internet", "romantic",
]

# Verify that all expected columns exist.
expected_features = NUMERIC_FEATURES + CATEGORICAL_FEATURES
missing_features = sorted(set(expected_features) - set(X.columns))

if missing_features:
    raise ValueError(f"Missing columns: {missing_features}")

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore")),
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, NUMERIC_FEATURES),
    ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
])


# --------------------------------------------------
# 4. Split data into training and testing sets
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# --------------------------------------------------
# 5. Define models
# --------------------------------------------------

models = {
    "Dummy Classifier": DummyClassifier(strategy="prior"),

    "Logistic Regression": LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42,
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    ),
}


# --------------------------------------------------
# 6. Cross-validation and test evaluation
# --------------------------------------------------

results = {}
best_model_name = None
best_cv_f1 = -1.0
best_pipeline = None

for name, model in models.items():
    print(f"\nTraining: {name}")

    pipeline = Pipeline([
        ("preprocessor", clone(preprocessor)),
        ("classifier", clone(model)),
    ])

    # Cross-validation uses training data only.
    cv_scores = cross_val_score(
        pipeline,
        X_train,
        y_train,
        cv=5,
        scoring="f1",
        n_jobs=1,
    )

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "cv_f1_mean": float(cv_scores.mean()),
        "cv_f1_std": float(cv_scores.std()),
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(
            precision_score(y_test, predictions, zero_division=0)
        ),
        "recall": float(
            recall_score(y_test, predictions, zero_division=0)
        ),
        "f1": float(
            f1_score(y_test, predictions, zero_division=0)
        ),
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
    }

    results[name] = metrics

    print("Cross-validation F1:", round(metrics["cv_f1_mean"], 3))
    print("Test metrics:", {
        key: round(value, 3)
        for key, value in metrics.items()
    })

    # Select using training cross-validation, not test scores.
    if metrics["cv_f1_mean"] > best_cv_f1:
        best_cv_f1 = metrics["cv_f1_mean"]
        best_model_name = name
        best_pipeline = pipeline


# --------------------------------------------------
# 7. Save best model and evaluation report
# --------------------------------------------------

model_path = ARTIFACTS_DIR / "student_risk_model.joblib"
metrics_path = REPORTS_DIR / "metrics.json"

joblib.dump(best_pipeline, model_path)

report = {
    "target": "at_risk = 1 if G3 < 10, otherwise 0",
    "excluded_features": ["G1", "G2", "G3"],
    "best_model_by_cv_f1": best_model_name,
    "best_cv_f1": float(best_cv_f1),
    "test_size": 0.20,
    "random_state": 42,
    "models": results,
}

metrics_path.write_text(
    json.dumps(report, indent=4),
    encoding="utf-8",
)

print("\n" + "=" * 50)
print("BEST MODEL:", best_model_name)
print("Saved model:", model_path)
print("Saved metrics:", metrics_path)

best_predictions = best_pipeline.predict(X_test)

print("\nClassification report for selected model:")
print(classification_report(
    y_test,
    best_predictions,
    target_names=["Not at risk", "At risk"],
    zero_division=0,
))
