from aicoder.config import API_KEY, MODEL_NAME

try:
    import openai
except ImportError:
    openai = None


class LLMClient:
    def __init__(self):
        if openai is not None:
            openai.api_key = API_KEY

    async def chat(self, prompt: str) -> str:
        """Send a prompt to the LLM; returns a placeholder if the SDK is missing."""
        if openai is None:
            return "OpenAI SDK not installed. Install `pip install openai` or plug in a client."

        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message["content"]
