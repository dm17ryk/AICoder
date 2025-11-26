import openai
from aicoder.config import API_KEY, MODEL_NAME

class LLMClient:
    def __init__(self):
        openai.api_key = API_KEY

    async def chat(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response.choices[0].message['content']
