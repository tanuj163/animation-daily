"""
config.py — All settings loaded from environment variables or .env file.
Copy .env.template to .env and fill in your values before running.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ── OpenAI ───────────────────────────────────────────────────────────────
    OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
    # gpt-4o is the recommended default; swap for o4-mini to reduce cost
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")

    # ── Python ───────────────────────────────────────────────────────────────
    # Timeout for each generated animation script
    PYTHON_TIMEOUT_SECONDS: int = int(os.getenv("PYTHON_TIMEOUT_SECONDS", "120"))

    # ── YouTube ──────────────────────────────────────────────────────────────
    # Path to credentials.json downloaded from Google Cloud Console
    YOUTUBE_CLIENT_SECRETS_FILE: str = os.getenv(
        "YOUTUBE_CLIENT_SECRETS_FILE", "credentials.json"
    )
    # Token is cached here after first OAuth login
    YOUTUBE_TOKEN_FILE: str = os.getenv("YOUTUBE_TOKEN_FILE", "youtube_token.json")
    # "public", "private", or "unlisted"
    YOUTUBE_PRIVACY: str = os.getenv("YOUTUBE_PRIVACY", "public")

    # ── GitHub ───────────────────────────────────────────────────────────────
    GITHUB_REPO_LOCAL_PATH: str = os.getenv("GITHUB_REPO_LOCAL_PATH", ".")
    GITHUB_REPO_URL: str = os.getenv("GITHUB_REPO_URL", "https://github.com/yourname/matlab-daily")
    GITHUB_BRANCH: str = os.getenv("GITHUB_BRANCH", "main")

    # ── Agent behaviour ──────────────────────────────────────────────────────
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    # Minimum valid video size in bytes (~10 KB)
    MIN_VIDEO_BYTES: int = int(os.getenv("MIN_VIDEO_BYTES", "10240"))
