# Repository Guidelines

This repository is being scaffolded; use these baseline rules as you add code and update them once the stack is fixed.

## Project Structure & Module Organization
- Keep production code in `src/` using language-appropriate package layout; mirror features with `tests/` alongside.
- Store helper scripts in `scripts/` (shell or Python) and keep docs in `docs/`. Place static assets in `assets/` and sample data in `examples/`.
- Use configuration files at the root (`.env.example`, `.tool-versions`, `.editorconfig`); avoid committing machine-specific secrets.

## Build, Test, and Development Commands
- Standardize on `make` (or `just`) wrappers; add targets such as `make setup` (install deps), `make lint`, `make test`, and `make dev` (run the app) and document flags here when added.
- Prefer reproducible installs: for Python use `python -m venv .venv && pip install -r requirements.txt`; for JS/TS use `pnpm install` or `npm ci`.
- Keep local run scripts executable (`scripts/dev.sh`, `scripts/serve.sh`); avoid embedding secrets or environment-specific paths.

## Coding Style & Naming Conventions
- Default to 4-space indentation for Python/shell and 2 spaces for JSON/YAML; use UTF-8, LF line endings, and include a trailing newline.
- Favor `snake_case` for file names and functions, `CamelCase` for classes, and `kebab-case` for CLI entry points.
- Run a formatter before commits (e.g., `black`/`isort` for Python, `prettier` for JS/TS) and pair with linters (`ruff`/`flake8`, `eslint`).
- Keep functions small and side-effect free; prefer dependency injection over global state.

## Testing Guidelines
- Mirror code paths under `tests/`; name files `test_<module>.py` or `<name>.spec.ts` depending on the stack.
- Write focused unit tests plus an integration path for each new feature; place fixtures in `tests/fixtures/`.
- Require tests for bug fixes and new behaviors; measure coverage locally (e.g., `pytest --cov`, `vitest --coverage`) and gate merges on failures.

## Commit & Pull Request Guidelines
- Commit messages are imperative and scoped (`Add lint target`, `Fix parser panic`); avoid batching unrelated changes.
- One logical change per PR; include a summary, motivation, test results, and linked issue.
- Add screenshots or logs for user-visible changes and call out migrations or breaking changes explicitly.
