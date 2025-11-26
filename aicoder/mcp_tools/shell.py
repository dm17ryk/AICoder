import subprocess
from pathlib import Path


def run_command(cmd: str, cwd: Path) -> tuple[int, str, str]:
    """Execute a shell command in the given working directory. Returns (exit_code, stdout, stderr)."""
    proc = subprocess.Popen(
        cmd, cwd=str(cwd), shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    out, err = proc.communicate()
    return proc.returncode, out, err
