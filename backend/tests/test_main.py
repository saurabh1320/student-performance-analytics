
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_predict():
    student_data = {
        "school": "GP",
        "sex": "F",
        "age": 17,
        "address": "U",
        "famsize": "GT3",
        "Pstatus": "T",
        "Medu": 3,
        "Fedu": 2,
        "Mjob": "other",
        "Fjob": "other",
        "reason": "course",
        "guardian": "mother",
        "traveltime": 1,
        "studytime": 2,
        "failures": 0,
        "schoolsup": "no",
        "famsup": "yes",
        "paid": "no",
        "activities": "yes",
        "nursery": "yes",
        "higher": "yes",
        "internet": "yes",
        "romantic": "no",
        "famrel": 4,
        "freetime": 3,
        "goout": 3,
        "Dalc": 1,
        "Walc": 2,
        "health": 4,
        "absences": 2
    }

    response = client.post("/predict", json=student_data)

    assert response.status_code == 200

    result = response.json()

    assert "at_risk" in result
    assert isinstance(result["at_risk"], bool)

    assert "risk_probability" in result
    assert 0 <= result["risk_probability"] <= 1

    assert "interpretation" in result
    assert "notice" in result
