# aicoder/app.py
from pathlib import Path
import signal
import sys

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Button, Input, Log, Static, Tree
from textual.binding import Binding
# Ensure package imports work when running as a script (python aicoder/app.py)
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR.parent))

from aicoder.core.agent import Agent
from aicoder.core.workspace import Workspace


class AICoderApp(App):
    CSS_PATH = "aicoder.css"
    BINDINGS = [  # Disable default 'q' binding
        Binding(
            "ctrl+q",
            "quit",
            "Quit",
            tooltip="Quit the app and return to the command prompt.",
            show=True,
            priority=True,
        ),
        Binding(
            "ctrl+b",
            "background_app",
            "Background",
            tooltip="Application will go to background",
            show=True,
            priority=True,
        ),
        Binding("ctrl+c", "help_quit", 
                show=False, system=True),
        Binding("ctrl+z", "help_bg", "Background the application", 
                show=False, system=True),
        Binding(
            "f5", 
            "run_agent", 
            "Run agent",
            tooltip="Run agent on last prompt"),
    ]

    def __init__(self, project_path: str | None = None, **kwargs):
        super().__init__(**kwargs)
        # Ignore terminal shortcuts that normally terminate/suspend apps
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        try:
            signal.signal(signal.SIGTSTP, signal.SIG_IGN)
        except AttributeError:
            # SIGTSTP may not exist on some platforms (e.g., Windows)
            pass
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
                self.chat_log = Log(id="chat_log")
                self.chat_input = Input(placeholder="Ask AICoder…", id="chat_input")
                self.actions_log = Log(id="actions_log")

                yield Static("Chat", classes="title")
                yield self.chat_log
                yield self.chat_input
                yield Static("Actions / Commands", classes="title")
                yield self.actions_log

        yield Footer()

    async def on_mount(self) -> None:
        # Заполняем дерево файлов
        self._build_file_tree(self.workspace.root, self.file_tree.root)
        self.file_tree.root.expand_all()

        # Фокус на инпут
        self.set_focus(self.chat_input)

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

    def action_help_bg(self) -> None:
        """Bound to ctrl+C to alert the user that it no longer quits."""
        self.notify(
            f"Press [b]ctrl+b[/b] to BG the app", 
            title="Do you want to go to BG?"
        )
        return

    def action_quit_app(self) -> None:
        """Exit the application via UI controls."""
        self.exit()

    def action_background_app(self) -> None:
        """Suspend the TUI until the user presses Enter in the terminal."""
        self.actions_log.write("Backgrounding app; press Enter in the terminal to resume…")
        # App.suspend() is a context manager with no arguments
        with self.suspend():
            input("AICoder paused. Press Enter to resume…")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle window/status buttons."""
        if event.button.id in {"btn_close", "btn_quit"}:
            self.action_quit_app()
        elif event.button.id in {"btn_minimize", "btn_background"}:
            self.action_background_app()
        elif event.button.id == "btn_run":
            self.action_run_agent()


if __name__ == "__main__":
    import sys
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."
    app = AICoderApp(project_path=project_path)
    app.run()
