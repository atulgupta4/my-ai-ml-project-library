
import sqlite3

import pytest
from fastapi.testclient import TestClient

import app as api
import audit


# Synthetic customer record for testing
CUSTOMER_PAYLOAD = {
    "X1": 20000,
    "X2": 2,
    "X3": 2,
    "X4": 1,
    "X5": 35,
    "X6": 2,
    "X7": 2,
    "X8": 0,
    "X9": 0,
    "X10": 0,
    "X11": 0,
    "X12": 15000,
    "X13": 14000,
    "X14": 13000,
    "X15": 12000,
    "X16": 11000,
    "X17": 10000,
    "X18": 0,
    "X19": 1000,
    "X20": 1000,
    "X21": 1000,
    "X22": 1000,
    "X23": 1000
}


@pytest.fixture
def client(tmp_path, monkeypatch):

    # Use a temporary database for each test
    test_db = tmp_path / "test_audit.db"

    monkeypatch.setattr(audit, "AUDIT_DB", str(test_db))

    audit.initialize_audit_db()

    return TestClient(api.app)


def test_health_endpoint(client):

    response = client.get("/health")

    assert response.status_code == 200

    result = response.json()

    assert result["status"] == "healthy"
    assert result["model"] == "credit-risk-logistic-regression"
    assert result["model_version"] == "1"


def test_prediction_endpoint(client):

    response = client.post(
        "/predict",
        json=CUSTOMER_PAYLOAD
    )

    assert response.status_code == 200

    result = response.json()

    assert 0 <= result["default_probability"] <= 1

    assert result["decision"] in [
        "LOW_RISK",
        "MANUAL_REVIEW"
    ]

    assert result["request_id"] is not None

    # Verify decision against configured threshold
    if result["default_probability"] >= 0.30:
        assert result["decision"] == "MANUAL_REVIEW"
    else:
        assert result["decision"] == "LOW_RISK"


def test_prediction_is_audited(client):

    response = client.post(
        "/predict",
        json=CUSTOMER_PAYLOAD
    )

    assert response.status_code == 200

    request_id = response.json()["request_id"]

    # Verify audit record exists
    conn = sqlite3.connect(audit.AUDIT_DB)

    record = conn.execute(
        """
        SELECT request_id, default_probability, decision
        FROM prediction_audit
        WHERE request_id = ?
        """,
        (request_id,)
    ).fetchone()

    conn.close()

    assert record is not None
    assert record[0] == request_id
    assert 0 <= record[1] <= 1
    assert record[2] in ["LOW_RISK", "MANUAL_REVIEW"]


def test_invalid_request_returns_422(client):

    # Missing required customer features
    invalid_payload = {
        "X1": 20000,
        "X2": 2
    }

    response = client.post(
        "/predict",
        json=invalid_payload
    )

    assert response.status_code == 422
