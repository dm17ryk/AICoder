from aicoder.prompts.utils import build_prompt
from .base import BaseAgent

class DebuggerAgent(BaseAgent):
    """Agent that identifies bugs or issues from code and error context."""

    async def run(self, user_message: str) -> str:
        prompt = build_prompt("debugger", user_message, self.workspace)
        analysis = await self.llm.chat(prompt)
        return analysis
