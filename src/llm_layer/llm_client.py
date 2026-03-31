class LLMClient:
    def generate_explanation(self, context: dict) -> str:
        # TODO: Replace with real LLM API call
        return f"Transaction flagged due to {context['reason']}."