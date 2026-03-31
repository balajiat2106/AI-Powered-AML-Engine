import logging
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from src.schemas.transaction import Transaction
from src.orchestration.pipeline import run_pipeline
from src.database.connection import engine, Base

# Create tables in Postgres on boot
Base.metadata.create_all(bind=engine)

# Configure base root python logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Powered AML Engine")

@app.post("/analyze")
async def analyze(tx: Transaction):
    try:
        # Pushing sync work into a thread pool guarantees we don't block the ASGI event loop
        result = await run_in_threadpool(run_pipeline, tx)
        return result
    except Exception as e:
        logger.error(f"Error processing transaction {tx.transaction_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal processing error")