# MATLAB AI Agent — Daily Animation Pipeline

Generates a MATLAB animation every day, validates it, uploads to YouTube,
and commits the code to GitHub — fully automated via Claude AI.

---

## What it does

| Step | Tool | Detail |
|------|------|--------|
| Pick project | `projects.txt` | Next uncompleted line |
| Generate code | Claude API | Writes complete .m script |
| Run & validate | MATLAB -batch | Headless; produces output.mp4 |
| Auto-retry | Claude API | Feeds MATLAB error back for self-correction (up to 3×) |
| Upload video | YouTube Data API | Title/description auto-generated |
| Push code | Git + GitHub | Commits .m file with day number |
| Log | `run_log.json` | Full record of every run |

---

## Prerequisites

- Python 3.11+
- MATLAB R2022b or newer (with a valid licence)
- Git installed and configured
- A GitHub repo already created and cloned locally
- A Google Cloud project with YouTube Data API v3 enabled

---

## Setup (one time)

### 1. Clone and install

```bash
git clone https://github.com/yourname/matlab-daily.git
cd matlab-daily
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.template .env
# Edit .env — fill in all values
```

### 3. Set up YouTube OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project → Enable **YouTube Data API v3**
3. Create **OAuth 2.0 credentials** → Desktop App type
4. Download as `credentials.json`, place in this folder
5. Run once manually to complete the browser consent:

```bash
python agent.py
# A browser window will open — log in and allow access
# Token is cached in youtube_token.json for future runs
```

### 4. Set up GitHub auth

**Option A — SSH (recommended):**
```bash
# Make sure your SSH key is added to GitHub
ssh -T git@github.com
```

**Option B — HTTPS with token:**
```bash
# Set GITHUB_TOKEN in .env (Personal Access Token with repo scope)
```

---

## Running manually

```bash
python agent.py
```

---

## Automating daily runs

### macOS/Linux — cron

```bash
crontab -e
# Run at 9 AM every day:
0 9 * * * cd /path/to/matlab-daily && /usr/bin/python3 agent.py >> cron.log 2>&1
```

### macOS — launchd (more reliable than cron)

Create `~/Library/LaunchAgents/com.matlab.agent.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.matlab.agent</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/path/to/matlab-daily/agent.py</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>9</integer>
    <key>Minute</key>
    <integer>0</integer>
  </dict>
  <key>WorkingDirectory</key>
  <string>/path/to/matlab-daily</string>
  <key>StandardOutPath</key>
  <string>/path/to/matlab-daily/launch.log</string>
  <key>StandardErrorPath</key>
  <string>/path/to/matlab-daily/launch_err.log</string>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.matlab.agent.plist
```

### Windows — Task Scheduler

```powershell
schtasks /create /tn "MatlabAgent" /tr "python C:\path\to\agent.py" /sc daily /st 09:00
```

### GitHub Actions (run on a remote server)

Create `.github/workflows/daily.yml`:

```yaml
name: Daily MATLAB Animation

on:
  schedule:
    - cron: '0 9 * * *'
  workflow_dispatch:

jobs:
  run:
    runs-on: self-hosted   # needs MATLAB on the runner
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install deps
        run: pip install -r requirements.txt
      - name: Run agent
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python agent.py
```

---

## Project structure

```
matlab-daily/
├── agent.py              # Main orchestrator
├── code_generator.py     # Claude API → MATLAB code
├── matlab_runner.py      # Run MATLAB -batch + validate output
├── youtube_upload.py     # Upload mp4 to YouTube
├── github_push.py        # Git commit + push
├── config.py             # All settings from .env
├── projects.txt          # 30 one-line project descriptions
├── requirements.txt
├── .env.template         # Copy to .env and fill in
├── credentials.json      # YouTube OAuth (you download this)
├── youtube_token.json    # Auto-created after first login
├── run_log.json          # Auto-created — full run history
├── outputs/              # Generated .mp4 videos
└── matlab_scripts/       # Generated .m files (committed to git)
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `MATLAB executable not found` | Set full path in `MATLAB_EXECUTABLE` in `.env` |
| MATLAB times out | Increase `MATLAB_TIMEOUT_SECONDS` or simplify the animation |
| YouTube auth loop | Delete `youtube_token.json` and re-run to re-authenticate |
| `git push` fails | Check SSH key or set `GITHUB_TOKEN` in `.env` |
| Video file too small | The script ran but didn't save — Claude will auto-retry |
