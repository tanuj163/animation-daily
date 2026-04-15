"""
github_push.py — Commits a file and pushes it to GitHub.

Assumes:
  - Git is installed and on PATH
  - The repo at GITHUB_REPO_LOCAL_PATH has a remote 'origin' already set up
  - Either SSH keys or a stored credential handle authentication
    (or GITHUB_TOKEN is set for HTTPS remotes)
"""

import subprocess
import os
from pathlib import Path
from config import Config


def _git(args: list[str], cwd: str, env: dict | None = None) -> tuple[bool, str]:
    """Run a git command in the given directory. Returns (success, output)."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env or os.environ.copy(),
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def push_to_github(
    file_path: str,
    commit_message: str,
    repo_path: str,
) -> tuple[str | None, str | None]:
    """
    Stage a file, commit it, and push to origin.

    Returns:
        (commit_sha: str | None, error: str | None)
    """
    repo = Path(repo_path).resolve()
    if not repo.exists():
        return None, f"Repo path not found: {repo}"

    file_abs = Path(file_path).resolve()

    # Make path relative to repo for git add
    try:
        rel_path = file_abs.relative_to(repo)
    except ValueError:
        # File is outside the repo — copy it in
        dest = repo / "matlab_scripts" / file_abs.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(file_abs.read_bytes())
        rel_path = dest.relative_to(repo)

    env = os.environ.copy()
    # If using HTTPS with a token, inject it into the remote URL via env
    if token := env.get("GITHUB_TOKEN"):
        # git credential helper via env — works for https remotes
        env["GIT_ASKPASS"] = "echo"
        env["GIT_USERNAME"] = "x-access-token"
        env["GIT_PASSWORD"] = token

    # Pull latest to avoid push conflicts
    ok, out = _git(["pull", "--rebase", "origin", Config.GITHUB_BRANCH], str(repo), env)
    if not ok:
        print(f"  [github] Warning: pull failed (continuing): {out}")

    # Stage the file
    ok, out = _git(["add", str(rel_path)], str(repo))
    if not ok:
        return None, f"git add failed: {out}"

    # Check if there's actually anything staged
    ok, status = _git(["diff", "--cached", "--stat"], str(repo))
    if not status.strip():
        return None, "Nothing to commit — file unchanged."

    # Commit
    ok, out = _git(["commit", "-m", commit_message], str(repo))
    if not ok:
        return None, f"git commit failed: {out}"

    # Push
    ok, out = _git(["push", "origin", Config.GITHUB_BRANCH], str(repo), env)
    if not ok:
        return None, f"git push failed: {out}"

    # Get the commit SHA
    ok, sha = _git(["rev-parse", "--short", "HEAD"], str(repo))
    return sha if ok else "unknown", None
