"""
youtube_upload.py — Uploads a video to YouTube using the YouTube Data API v3.

First run: opens a browser for OAuth consent and caches the token.
Subsequent runs: uses the cached token silently.

Setup:
  1. Go to https://console.cloud.google.com
  2. Create a project, enable "YouTube Data API v3"
  3. Create OAuth 2.0 credentials (Desktop app type)
  4. Download credentials.json and set YOUTUBE_CLIENT_SECRETS_FILE in .env
"""

import os
import json
from pathlib import Path

import google.oauth2.credentials
import google_auth_oauthlib.flow
import google.auth.transport.requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from config import Config

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


def _get_authenticated_service():
    """Return an authenticated YouTube service, refreshing or re-authorising as needed."""
    token_path = Path(Config.YOUTUBE_TOKEN_FILE)
    creds = None

    if token_path.exists():
        creds = google.oauth2.credentials.Credentials.from_authorized_user_file(
            str(token_path), SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            if not Path(Config.YOUTUBE_CLIENT_SECRETS_FILE).exists():
                raise FileNotFoundError(
                    f"YouTube credentials not found: {Config.YOUTUBE_CLIENT_SECRETS_FILE}\n"
                    "Download it from Google Cloud Console and set YOUTUBE_CLIENT_SECRETS_FILE in .env"
                )
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                Config.YOUTUBE_CLIENT_SECRETS_FILE, SCOPES
            )
            # Opens browser on first run; run this once interactively to cache the token
            creds = flow.run_local_server(port=0)

        token_path.write_text(creds.to_json())

    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)


def upload_to_youtube(
    video_path: str,
    title: str,
    description: str,
    tags: list[str],
) -> tuple[str | None, str | None]:
    """
    Upload a video to YouTube.

    Returns:
        (youtube_url: str | None, error: str | None)
    """
    if not Path(video_path).exists():
        return None, f"Video file not found: {video_path}"

    try:
        youtube = _get_authenticated_service()

        body = {
            "snippet": {
                "title": title[:100],           # YouTube max title length
                "description": description[:5000],
                "tags": tags,
                "categoryId": "28",             # Science & Technology
            },
            "status": {
                "privacyStatus": Config.YOUTUBE_PRIVACY,
                "selfDeclaredMadeForKids": False,
            },
        }

        media = MediaFileUpload(
            video_path,
            chunksize=-1,       # Single upload (simpler for short clips)
            resumable=True,
            mimetype="video/mp4",
        )

        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media,
        )

        print(f"  Uploading {Path(video_path).name} ({Path(video_path).stat().st_size / 1e6:.1f} MB)...")
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                pct = int(status.progress() * 100)
                print(f"  Upload progress: {pct}%", end="\r")

        video_id = response["id"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"\n  Upload complete: {url}")
        return url, None

    except HttpError as e:
        return None, f"YouTube API error {e.resp.status}: {e.content.decode()}"
    except Exception as e:
        return None, str(e)
