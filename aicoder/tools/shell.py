# aicoder/tools/shell.py
import subprocess
from pathlib import Path


def run_command(cmd: str, cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = proc.communicate()
    return proc.returncode, out, err
