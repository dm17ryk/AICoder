from aicoder.prompts.utils import build_prompt
from .base import BaseAgent

class FixerAgent(BaseAgent):
    """Agent that fixes code issues or applies necessary changes."""

    async def run(self, user_message: str) -> str:
        prompt = build_prompt("fixer", user_message, self.workspace)
        solution = await self.llm.chat(prompt)
        return solution
