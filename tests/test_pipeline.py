from src.schemas.transaction import Transaction
from src.orchestration.pipeline import run_pipeline

def test_pipeline():
    tx = Transaction(
        transaction_id="test_tx",
        user_id="user",
        amount=5000,
        country="US",
        timestamp="2026-01-01T10:00:00"
    )

    result = run_pipeline(tx)
    assert "decision" in result