"""
config.py — All settings loaded from environment variables or .env file.
Copy .env.template to .env and fill in your values before running.

Supported LLM providers (set LLM_PROVIDER in .env):
  gemini  — Google Gemini API (has a free tier; recommended)
  ollama  — Local Ollama instance (completely free, needs GPU/CPU)
  openai  — OpenAI API (paid)
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ── LLM Provider ─────────────────────────────────────────────────────────
    # Options: "gemini" | "ollama" | "openai"
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")

    # ── Gemini (free tier available) ─────────────────────────────────────────
    # Get a free key at: https://aistudio.google.com/app/apikey
    # Free tier: gemini-2.0-flash — 1,500 requests/day, 1M tokens/min
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    # ── Ollama (local / completely free) ─────────────────────────────────────
    # Install: https://ollama.com  then: ollama pull codellama
    # Good code models: codellama, deepseek-coder, qwen2.5-coder, llama3
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "codellama")

    # ── OpenAI (paid, kept for backward compat) ───────────────────────────────
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")

    # ── Python ───────────────────────────────────────────────────────────────
    PYTHON_TIMEOUT_SECONDS: int = int(os.getenv("PYTHON_TIMEOUT_SECONDS", "120"))

    # ── YouTube ──────────────────────────────────────────────────────────────
    YOUTUBE_CLIENT_SECRETS_FILE: str = os.getenv(
        "YOUTUBE_CLIENT_SECRETS_FILE", "credentials.json"
    )
    YOUTUBE_TOKEN_FILE: str = os.getenv("YOUTUBE_TOKEN_FILE", "youtube_token.json")
    YOUTUBE_PRIVACY: str = os.getenv("YOUTUBE_PRIVACY", "public")

    # ── GitHub ───────────────────────────────────────────────────────────────
    GITHUB_REPO_LOCAL_PATH: str = os.getenv("GITHUB_REPO_LOCAL_PATH", ".")
    GITHUB_REPO_URL: str = os.getenv("GITHUB_REPO_URL", "https://github.com/yourname/animation-daily")
    GITHUB_BRANCH: str = os.getenv("GITHUB_BRANCH", "main")

    # ── Agent behaviour ──────────────────────────────────────────────────────
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    MIN_VIDEO_BYTES: int = int(os.getenv("MIN_VIDEO_BYTES", "10240"))
