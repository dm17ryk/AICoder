# aicoder/core/workspace.py
from pathlib import Path


class Workspace:
    def __init__(self, root: Path):
        self.root = root

    def read_file(self, relative: str) -> str:
        path = self.root / relative
        return path.read_text(encoding="utf-8")

    def write_file(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.write_text(content, encoding="utf-8")
