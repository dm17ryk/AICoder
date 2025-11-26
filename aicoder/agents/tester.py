from aicoder.prompts.utils import build_prompt
from aicoder.mcp_tools.shell import run_command
from .base import BaseAgent

class TesterAgent(BaseAgent):
    """Agent that validates code by running tests or generating test cases."""

    async def run(self, user_message: str) -> str:
        prompt = build_prompt("tester", user_message, self.workspace)
        _ = await self.llm.chat(prompt)
        code, out, err = run_command("pytest", self.workspace.root)
        result = out + err
        if code != 0:
            return f"Tests failed (exit {code}):\n{result}"
        return f"Tests passed (exit {code}):\n{result}"
