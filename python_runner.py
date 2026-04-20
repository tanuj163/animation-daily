"""
python_runner.py — Runs a generated .py animation script in a subprocess
and validates that the output video was created successfully.

Automatically injects an ffmpeg path-finder preamble before every script
so FFMpegWriter works regardless of whether ffmpeg is on PATH.
"""

import subprocess
import sys
import shutil
from pathlib import Path
from config import Config

# This preamble is prepended to every generated script before execution.
# It locates ffmpeg and tells matplotlib where to find it.
_FFMPEG_PREAMBLE = '''import matplotlib
matplotlib.use('Agg')
import matplotlib as _mpl
_mpl.rcParams['animation.ffmpeg_path'] = r'C:\\ffmpeg\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe'

'''


def run_python(script_path: str) -> tuple[bool, str, str]:
    """
    Prepend ffmpeg detection preamble, then execute the animation script.

    Returns:
        (success: bool, stdout: str, stderr: str)
    """
    script = Path(script_path).resolve()
    if not script.exists():
        return False, "", f"Script not found: {script}"

    # Read generated code, strip any duplicate matplotlib.use('Agg') at top
    original = script.read_text(encoding="utf-8")
    # Remove leading backend/use lines — our preamble handles them
    lines = original.splitlines()
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped in ("import matplotlib", "matplotlib.use('Agg')", 'matplotlib.use("Agg")'):
            continue
        cleaned_lines.append(line)
    patched = _FFMPEG_PREAMBLE + "\n".join(cleaned_lines)

    # Write patched version to a temp file alongside the original
    temp_path = script.with_suffix(".tmp.py")
    temp_path.write_text(patched, encoding="utf-8")

    try:
        result = subprocess.run(
            [sys.executable, str(temp_path)],
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

    finally:
        temp_path.unlink(missing_ok=True)   # Always clean up temp file


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