import logging
from src.features.feature_builder import build_features
from src.risk_engine.inference.model import RiskModel
from src.rules_engine.rules import apply_rules
from src.explainability.shap_explainer import explain
from src.llm_layer.llm_client import LLMClient
from src.llm_layer.rag import enrich_with_policy
from src.decision_engine.decision import make_decision
from src.audit.logger import log_event

logger = logging.getLogger(__name__)

model = RiskModel()
llm = LLMClient()

def run_pipeline(tx):
    try:
        features = build_features(tx)
        risk_score = model.predict(features)
        rule_flags = apply_rules(tx, features)
        
        # LLM enrichment could fail (e.g., API timeout), trap this specific error
        try:
            explanation = explain(features, risk_score)
            context = enrich_with_policy(explanation)
            narrative = llm.generate_explanation(context)
        except Exception as e:
            logger.error(f"LLM Enrichment failed for {tx.transaction_id}: {str(e)}")
            narrative = "Enrichment unavailable due to internal service error."

        decision = make_decision(risk_score)

        audit_data = {
            "tx_id": tx.transaction_id,
            "risk_score": risk_score,
            "rules": rule_flags,
            "decision": decision,
            "narrative": narrative
        }

        # Keep audit failures from breaking the whole request execution
        try:
            log_event(audit_data)
        except Exception as e:
            logger.error(f"Audit stream failed: {str(e)}")

        return audit_data
    except Exception as e:
        logger.error(f"Critical Pipeline Failure for transaction {tx.transaction_id}: {str(e)}")
        raise RuntimeError(f"AML Engine processing failed: {str(e)}")