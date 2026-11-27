
import sqlite3
from datetime import datetime, timezone

AUDIT_DB = "logs/credit_risk_audit.db"


def initialize_audit_db():
    print("initialize db")
    conn = sqlite3.connect(AUDIT_DB)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS prediction_audit (
            request_id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            model_name TEXT NOT NULL,
            model_version TEXT NOT NULL,
            run_id TEXT,
            default_probability REAL NOT NULL,
            decision_threshold REAL NOT NULL,
            decision TEXT NOT NULL,
            latency_ms REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def log_prediction(
    request_id,
    model_name,
    model_version,
    run_id,
    probability,
    threshold,
    decision,
    latency_ms
):
    conn = sqlite3.connect(AUDIT_DB)

    conn.execute("""
        INSERT INTO prediction_audit (
            request_id,
            timestamp,
            model_name,
            model_version,
            run_id,
            default_probability,
            decision_threshold,
            decision,
            latency_ms
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        request_id,
        datetime.now(timezone.utc).isoformat(),
        model_name,
        model_version,
        run_id,
        probability,
        threshold,
        decision,
        latency_ms
    ))

    conn.commit()
    conn.close()
