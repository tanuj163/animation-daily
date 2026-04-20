"""
MATLAB AI Agent — Main Orchestrator
Picks today's project, generates MATLAB code via Claude, runs it,
validates the output video, uploads to YouTube, and pushes to GitHub.
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

from config import Config
from code_generator import generate_python_code
from python_runner import run_python, validate_output
from youtube_upload import upload_to_youtube
from github_push import push_to_github

LOG_FILE = Path("run_log.json")
PROJECTS_FILE = Path("projects.txt")
OUTPUT_DIR = Path("outputs")
CODE_DIR = Path("python_scripts")


def load_projects() -> list[str]:
    if not PROJECTS_FILE.exists():
        raise FileNotFoundError(f"projects.txt not found — create it with 30 project lines.")
    lines = [l.strip() for l in PROJECTS_FILE.read_text().splitlines() if l.strip()]
    return lines


def load_log() -> list[dict]:
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text())
    return []


def save_log(log: list[dict]):
    LOG_FILE.write_text(json.dumps(log, indent=2))


def get_todays_project(projects: list[str], log: list[dict]) -> tuple[int, str]:
    """Return the next unfinished project (index, description)."""
    completed_indices = {entry["project_index"] for entry in log if entry.get("success")}
    for i, project in enumerate(projects):
        if i not in completed_indices:
            return i, project
    raise ValueError("All 30 projects completed! Add more to projects.txt.")


def run_pipeline(project_index: int, description: str) -> dict:
    """Full pipeline for one project. Returns a log entry dict."""
    print(f"\n{'='*60}")
    print(f"Project #{project_index + 1}: {description}")
    print(f"{'='*60}\n")

    OUTPUT_DIR.mkdir(exist_ok=True)
    CODE_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().isoformat()
    script_name = f"project_{project_index+1:02d}_{description[:30].replace(' ','_').replace('/','')}.py"
    script_path = CODE_DIR / script_name
    video_path = OUTPUT_DIR / script_name.replace(".py", ".mp4")

    log_entry = {
        "project_index": project_index,
        "description": description,
        "timestamp": timestamp,
        "success": False,
        "script_path": str(script_path),
        "video_path": str(video_path),
        "youtube_url": None,
        "github_commit": None,
        "error": None,
        "attempts": 0,
    }

    # ── Step 1: Generate MATLAB code (up to 3 retries) ──────────────────────
    matlab_code = None
    last_error = None

    for attempt in range(1, Config.MAX_RETRIES + 1):
        log_entry["attempts"] = attempt
        print(f"[{attempt}/{Config.MAX_RETRIES}] Generating MATLAB code via Claude...")

        matlab_code = generate_python_code(
            description=description,
            output_video_path=str(video_path.resolve()),
            previous_error=last_error,
        )

        if not matlab_code:
            last_error = "Claude returned empty code."
            print(f"  Empty response — retrying...")
            continue

        script_path.write_text(matlab_code)
        print(f"  Saved to {script_path}")

        # ── Step 2: Run MATLAB ───────────────────────────────────────────────
        print(f"  Running Python...")
        success, stdout, stderr = run_python(str(script_path))

        if not success:
            last_error = stderr or stdout
            print(f"  Script error:\n{last_error[:500]}")
            print(f"  Feeding error back to Claude for retry...")
            continue

        # ── Step 3: Validate output ──────────────────────────────────────────
        valid, msg = validate_output(str(video_path))
        if not valid:
            last_error = msg
            print(f"  Validation failed: {msg}")
            continue

        print(f"  Video validated: {video_path}")
        break
    else:
        log_entry["error"] = f"Failed after {Config.MAX_RETRIES} attempts. Last error: {last_error}"
        print(f"\nPipeline FAILED: {log_entry['error']}")
        return log_entry

    # ── Step 4: Upload to YouTube ────────────────────────────────────────────
    print(f"\nUploading to YouTube...")
    yt_title = f"MATLAB Animation: {description.title()} | Day {project_index + 1}/30"
    yt_desc = (
        f"Day {project_index + 1} of 30 daily MATLAB animations.\n\n"
        f"Today: {description}\n\n"
        f"Generated with Claude AI + MATLAB. Code on GitHub: {Config.GITHUB_REPO_URL}"
    )
    yt_tags = ["MATLAB", "animation", "simulation", "engineering", "AI", "coding"]

    yt_url, yt_error = upload_to_youtube(
        video_path=str(video_path),
        title=yt_title,
        description=yt_desc,
        tags=yt_tags,
    )

    if yt_error:
        print(f"  YouTube upload failed: {yt_error}")
        log_entry["error"] = f"YouTube: {yt_error}"
    else:
        print(f"  Uploaded: {yt_url}")
        log_entry["youtube_url"] = yt_url

    # ── Step 5: Push to GitHub ───────────────────────────────────────────────
    print(f"\nPushing to GitHub...")
    commit_msg = f"Day {project_index+1:02d}: {description}"
    commit_sha, gh_error = push_to_github(
        file_path=str(script_path),
        commit_message=commit_msg,
        repo_path=Config.GITHUB_REPO_LOCAL_PATH,
    )

    if gh_error:
        print(f"  GitHub push failed: {gh_error}")
        log_entry["error"] = (log_entry.get("error") or "") + f" | GitHub: {gh_error}"
    else:
        print(f"  Committed: {commit_sha}")
        log_entry["github_commit"] = commit_sha

    log_entry["success"] = (yt_url is not None) or (commit_sha is not None)
    return log_entry


def main():
    print("MATLAB AI Agent starting...")

    projects = load_projects()
    log = load_log()

    project_index, description = get_todays_project(projects, log)

    entry = run_pipeline(project_index, description)

    log.append(entry)
    save_log(log)

    print(f"\n{'='*60}")
    if entry["success"]:
        print(f"SUCCESS — Day {project_index + 1}/30 complete")
        print(f"  YouTube : {entry.get('youtube_url', 'N/A')}")
        print(f"  GitHub  : {entry.get('github_commit', 'N/A')}")
    else:
        print(f"FAILED — {entry.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()