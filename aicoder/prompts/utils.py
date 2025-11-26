from pathlib import Path
from aicoder.core.workspace import Workspace

TEMPLATES_DIR = Path(__file__).parent


def load_prompt_template(name: str) -> str:
    """Load the prompt template text for the given role (or 'base')."""
    path = TEMPLATES_DIR / f"{name}.txt"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def build_prompt(role: str, user_message: str, workspace: Workspace) -> str:
    """Construct a prompt by combining base, role-specific instructions, and project context."""
    base_prompt = load_prompt_template("base")
    role_prompt = load_prompt_template(role)
    context_info = build_context(workspace)

    prompt_parts: list[str] = []
    if base_prompt:
        prompt_parts.append(base_prompt.strip())
    if role_prompt:
        prompt_parts.append(role_prompt.strip())
    if context_info:
        prompt_parts.append(context_info.strip())

    prompt_parts.append(f"User request:\n{user_message}")
    return "\n\n".join(prompt_parts)


def build_context(workspace: Workspace) -> str:
    """Return lightweight project context (top-level files)."""
    try:
        files = [str(p.relative_to(workspace.root)) for p in workspace.root.iterdir() if p.is_file()]
    except Exception:
        files = []
    if not files:
        return ""
    return "Project files:\n" + "\n".join(files)
