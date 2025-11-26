from aicoder.prompts.utils import build_prompt
from .base import BaseAgent

class BuilderAgent(BaseAgent):
    """Agent that generates new or updated code based on the user's request."""

    async def run(self, user_message: str) -> str:
        prompt = build_prompt("builder", user_message, self.workspace)
        code_suggestion = await self.llm.chat(prompt)
        return code_suggestion
