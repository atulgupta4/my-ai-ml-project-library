
from audit import initialize_audit_db, log_prediction
import uuid

initialize_audit_db()

log_prediction(
    request_id=str(uuid.uuid4()),
    model_name="credit-risk-logistic-regression",
    model_version="1",
    run_id="442519574eba4901bfc49514bb027143",
    probability=0.42,
    threshold=0.30,
    decision="MANUAL_REVIEW",
    latency_ms=2.15
)

print("Audit record inserted successfully!")
