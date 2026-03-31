from src.schemas.transaction import Transaction
from src.orchestration.pipeline import run_pipeline

if __name__ == "__main__":
    tx = Transaction(
        transaction_id="tx_001",
        user_id="user_123",
        amount=15000,
        country="IR",
        timestamp="2026-01-01T14:00:00"
    )

    result = run_pipeline(tx)
    print(result)