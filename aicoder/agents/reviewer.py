from aicoder.prompts.utils import build_prompt
from .base import BaseAgent

class ReviewerAgent(BaseAgent):
    """Agent that reviews code for quality and correctness."""

    async def run(self, user_message: str) -> str:
        prompt = build_prompt("reviewer", user_message, self.workspace)
        feedback = await self.llm.chat(prompt)
        return feedback
