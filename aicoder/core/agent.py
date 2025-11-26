# aicoder/core/agent.py
from dataclasses import dataclass
from typing import AsyncIterator

from aicoder.core.workspace import Workspace
from aicoder.llm.client import LLMClient


@dataclass
class AgentStep:
    type: str  # "llm" | "command" | "command_result"
    text: str | None = None
    command: str | None = None
    output: str | None = None


class Agent:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.llm = LLMClient()

    async def handle_user_message(self, text: str) -> AsyncIterator[AgentStep]:
        # Пока без сложного планирования: просто шлём в LLM
        # Позже сюда добавятся tools, chain-of-thought и т.д.
        prompt = self._build_prompt(text)
        response = await self.llm.chat(prompt)

        yield AgentStep(type="llm", text=response)

    def _build_prompt(self, user_text: str) -> str:
        # Тут можно подмешивать контекст проекта: список файлов, AGENTS.md и т.д.
        return f"Ты AICoder, ИИ-помощник-программист. Пользователь говорит:\n{user_text}\n"
