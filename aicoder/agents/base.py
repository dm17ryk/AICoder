from aicoder.llm.client import LLMClient
from aicoder.core.workspace import Workspace


class BaseAgent:
    """Base class providing workspace access and a shared LLM client."""

    def __init__(self, workspace: Workspace):
        self.workspace = workspace
        self.llm = LLMClient()

    async def run(self, user_message: str) -> str:
        """Execute agent logic; to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the run method")
