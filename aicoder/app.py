# aicoder/app.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, TextLog, Tree, Static
from textual.containers import Horizontal, Vertical
from pathlib import Path

from aicoder.core.agent import Agent
from aicoder.core.workspace import Workspace


class AICoderApp(App):
    CSS_PATH = "aicoder.css"
    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("f5", "run_agent", "Run agent on last prompt"),
    ]

    def __init__(self, project_path: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self.workspace = Workspace(Path(project_path or ".").resolve())
        self.agent = Agent(self.workspace)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal():
            # Левая колонка: файлы проекта
            self.file_tree = Tree("Project", id="file_tree")
            yield self.file_tree

            # Правая колонка: чат и лог
            with Vertical():
                self.chat_log = TextLog(id="chat_log")
                self.chat_input = Input(placeholder="Ask AICoder…", id="chat_input")
                self.actions_log = TextLog(id="actions_log")

                yield Static("Chat", classes="title")
                yield self.chat_log
                yield self.chat_input
                yield Static("Actions / Commands", classes="title")
                yield self.actions_log

        yield Footer()

    async def on_mount(self) -> None:
        # Заполняем дерево файлов
        self._build_file_tree(self.workspace.root, self.file_tree.root)
        await self.file_tree.expand_all()

        # Фокус на инпут
        await self.set_focus(self.chat_input)

    def _build_file_tree(self, path: Path, node) -> None:
        for child in sorted(path.iterdir()):
            label = child.name
            new_node = node.add(label, data=child)
            if child.is_dir():
                self._build_file_tree(child, new_node)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        if not text:
            return

        self.chat_log.write(f"[user] {text}")
        event.input.value = ""

        # Запускаем агента на этот запрос
        async for step in self.agent.handle_user_message(text):
            # step может быть: текст модели, команда, результат команды и т.п.
            if step.type == "llm":
                self.chat_log.write(f"[aicoder] {step.text}")
            elif step.type == "command":
                self.actions_log.write(f"$ {step.command}")
            elif step.type == "command_result":
                self.actions_log.write(step.output)

    def action_run_agent(self) -> None:
        # F5 можно привязать к повтору последнего промпта или какой-то спец-команде
        pass


if __name__ == "__main__":
    import sys
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."
    app = AICoderApp(project_path=project_path)
    app.run()
