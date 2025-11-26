import subprocess
from pathlib import Path

def git_status(cwd: Path):
    return subprocess.check_output(['git', 'status'], cwd=str(cwd), text=True)
