"""
matlab_runner.py — Runs a .m script in headless MATLAB batch mode
and validates that the output video was created successfully.
"""

import subprocess
import os
from pathlib import Path
from config import Config


def run_matlab(script_path: str) -> tuple[bool, str, str]:
    """
    Execute a MATLAB script in -batch mode.

    Returns:
        (success: bool, stdout: str, stderr: str)
    """
    script = Path(script_path).resolve()
    if not script.exists():
        return False, "", f"Script not found: {script}"

    # MATLAB -batch runs the script and exits; errors cause non-zero exit code
    # We use run('full/path.m') so MATLAB can find the file regardless of cwd
    cmd = [
        Config.MATLAB_EXECUTABLE,
        "-batch",
        f"run('{script}');",
    ]

    # Some systems need this to avoid display errors in headless environments
    env = os.environ.copy()
    env.setdefault("DISPLAY", ":0")  # Ignored if no X server; harmless on macOS/Windows

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=Config.MATLAB_TIMEOUT_SECONDS,
            env=env,
        )
        success = result.returncode == 0
        return success, result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        return False, "", f"MATLAB timed out after {Config.MATLAB_TIMEOUT_SECONDS}s"

    except FileNotFoundError:
        return (
            False,
            "",
            f"MATLAB executable not found: '{Config.MATLAB_EXECUTABLE}'. "
            f"Set MATLAB_EXECUTABLE in your .env file.",
        )


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
