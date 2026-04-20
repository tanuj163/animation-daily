"""
code_generator.py — Generates Python animation code via a pluggable LLM backend.

Supported providers (set LLM_PROVIDER in .env):
  gemini  — Google Gemini API  (free tier: gemini-2.0-flash, 1500 req/day)
  ollama  — Local Ollama       (free, offline; needs `ollama pull codellama`)
  openai  — OpenAI API         (paid fallback)
"""

from config import Config

# ── Shared prompts ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert Python programmer specialising in scientific animations.

When given a one-line project description you MUST:
1. Write complete, self-contained Python code that creates an animation.
2. Save the animation as a .mp4 file to the EXACT path provided — copy verbatim.
3. Use matplotlib.animation.FuncAnimation with FFMpegWriter to save the video.
4. The animation must be at least 5 seconds at 30 fps (>=150 frames).
5. Use only these libraries (pre-installed): numpy, matplotlib, scipy.
6. Make the animation visually clear — proper title, axis labels, colourful styling.
7. Output ONLY raw Python code — no markdown fences, no explanations.

CRITICAL rules:
- DO NOT include any matplotlib.use() or backend setup — handled externally.
- DO NOT import matplotlib at the top — start directly with numpy/pyplot imports.
- Never call plt.show() — only save to file.
- Always close the figure at the end: plt.close('all')
- ALL array sizes used together must match exactly — double-check shapes.

Template to follow EXACTLY:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, FFMpegWriter

    OUTPUT_PATH = r'PASTE_EXACT_PATH_HERE'
    FPS = 30
    N_FRAMES = 150

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-2, 2)
    ax.set_title('Your Title')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    line, = ax.plot([], [], lw=2)

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        x = np.linspace(0, 2 * np.pi, 300)
        y = np.sin(x + frame * 0.1)
        line.set_data(x, y)
        return line,

    ani = FuncAnimation(fig, update, frames=N_FRAMES, init_func=init, interval=1000/FPS, blit=True)
    writer = FFMpegWriter(fps=FPS, bitrate=1800)
    ani.save(OUTPUT_PATH, writer=writer)
    plt.close('all')"""


def _build_user_prompt(description: str, output_video_path: str, previous_error: str | None) -> str:
    prompt = (
        f'Create a Python animation for: "{description}"\n\n'
        f"Save the output video to this EXACT path (copy verbatim as OUTPUT_PATH):\n"
        f"  {output_video_path}\n\n"
        f"Requirements:\n"
        f"- At least 5 seconds, 30 fps\n"
        f"- Clear title and axis labels\n"
        f"- Colourful and visually engaging\n"
        f"- Must run fully headless (no display, no plt.show())\n"
    )
    if previous_error:
        prompt += (
            f"\nIMPORTANT — previous version FAILED with this error. Fix it:\n"
            f"--- ERROR ---\n{previous_error[:1000]}\n-------------\n"
            f"Rewrite from scratch to avoid this error.\n"
        )
    return prompt


def _strip_fences(code: str) -> str:
    """Remove accidental markdown code fences."""
    if "```" in code:
        lines = code.splitlines()
        code = "\n".join(l for l in lines if not l.strip().startswith("```")).strip()
    return code


# ── Provider implementations ──────────────────────────────────────────────────

def _generate_gemini(user_prompt: str) -> str | None:
    """Call Google Gemini API using the new google-genai SDK."""
    import time

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("  [code_generator] Run: pip install google-genai")
        return None

    if not Config.GEMINI_API_KEY:
        print("  [code_generator] GEMINI_API_KEY not set. Get one at https://aistudio.google.com/app/apikey")
        return None

    client = genai.Client(api_key=Config.GEMINI_API_KEY)

    # Retry up to 3 times on 429 rate-limit with backoff
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=Config.GEMINI_MODEL,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    max_output_tokens=4096,
                    temperature=0.2,
                ),
            )
            return response.text.strip() or None

        except Exception as e:
            msg = str(e)
            if "429" in msg:
                wait = (attempt + 1) * 15   # 15s, 30s, 45s
                print(f"  [code_generator] Gemini rate-limited — waiting {wait}s before retry...")
                time.sleep(wait)
            else:
                print(f"  [code_generator] Gemini error: {e}")
                return None

    print("  [code_generator] Gemini: all retries exhausted on rate limit.")
    return None


def _generate_ollama(user_prompt: str) -> str | None:
    """
    Call local Ollama using the Anthropic SDK.
    Ollama v0.14+ speaks the Anthropic Messages API natively —
    no API key needed, no rate limits, fully offline.
    """
    try:
        import anthropic

        client = anthropic.Anthropic(
            base_url=Config.OLLAMA_BASE_URL,
            api_key="ollama",   # Ollama ignores this but SDK requires a value
        )

        response = client.messages.create(
            model=Config.OLLAMA_MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return response.content[0].text.strip() or None

    except Exception as e:
        msg = str(e)
        if "Connection" in msg or "connect" in msg.lower():
            print(
                f"  [code_generator] Ollama not reachable at {Config.OLLAMA_BASE_URL}.\n"
                f"  Start it with: ollama serve"
            )
        else:
            print(f"  [code_generator] Ollama error: {e}")
        return None


def _generate_openai(user_prompt: str) -> str | None:
    """Call OpenAI API (paid fallback)."""
    try:
        from openai import OpenAI

        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set.")

        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            max_tokens=4096,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
        )
        return response.choices[0].message.content.strip() or None

    except Exception as e:
        print(f"  [code_generator] OpenAI error: {e}")
        return None


# ── Public entry point ────────────────────────────────────────────────────────

_PROVIDERS = {
    "gemini": _generate_gemini,
    "ollama": _generate_ollama,
    "openai": _generate_openai,
}


def generate_python_code(
    description: str,
    output_video_path: str,
    previous_error: str | None = None,
) -> str | None:
    """
    Generate Python animation code using the configured LLM provider.
    Returns raw code string, or None on failure.
    """
    provider = Config.LLM_PROVIDER.lower()
    generator = _PROVIDERS.get(provider)

    if generator is None:
        print(
            f"  [code_generator] Unknown LLM_PROVIDER='{provider}'. "
            f"Valid options: {list(_PROVIDERS.keys())}"
        )
        return None

    print(f"  Using LLM provider: {provider} ({_model_label()})")
    user_prompt = _build_user_prompt(description, output_video_path, previous_error)
    code = generator(user_prompt)

    if code:
        code = _strip_fences(code)

    return code if code else None


def _model_label() -> str:
    p = Config.LLM_PROVIDER.lower()
    if p == "gemini":  return Config.GEMINI_MODEL
    if p == "ollama":  return Config.OLLAMA_MODEL
    if p == "openai":  return Config.OPENAI_MODEL
    return "?"