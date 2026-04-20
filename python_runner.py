"""
python_runner.py — Runs a generated .py animation script in a subprocess
and validates that the output video was created successfully.
"""

import subprocess
import sys
from pathlib import Path
from config import Config


def run_python(script_path: str) -> tuple[bool, str, str]:
    """
    Execute a Python animation script in a subprocess.

    Uses the same Python interpreter that is running the agent so all
    installed packages (numpy, matplotlib, scipy) are available.

    Returns:
        (success: bool, stdout: str, stderr: str)
    """
    script = Path(script_path).resolve()
    if not script.exists():
        return False, "", f"Script not found: {script}"

    try:
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            timeout=Config.PYTHON_TIMEOUT_SECONDS,
        )
        success = result.returncode == 0
        return success, result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        return False, "", f"Script timed out after {Config.PYTHON_TIMEOUT_SECONDS}s"

    except Exception as e:
        return False, "", str(e)


def validate_output(video_path: str) -> tuple[bool, str]:
    """
    Check that the output video file was created and has a reasonable size.

    Returns:
        (valid: bool, message: str)
    """
    p = Path(video_path)

    if not p.exists():
        return False, f"Output file not found: {video_path}"

    size = p.stat().st_size
    if size < Config.MIN_VIDEO_BYTES:
        return False, (
            f"Output file too small ({size} bytes < {Config.MIN_VIDEO_BYTES} min). "
            f"The video may be empty or corrupt."
        )

    return True, f"OK ({size / 1024:.1f} KB)"
