"""
code_generator.py — Calls OpenAI Codex to generate Python animation code.
On retry, feeds the previous error back for self-correction.
"""

from openai import OpenAI
from config import Config

_client = OpenAI(api_key=Config.OPENAI_API_KEY)

SYSTEM_PROMPT = """You are an expert Python programmer specialising in scientific animations and visualisations.

When given a one-line project description you MUST:
1. Write complete, self-contained Python code that creates an animation.
2. Save the animation as an .mp4 file to the EXACT path provided — use that string verbatim.
3. Use matplotlib.animation.FuncAnimation with FFMpegWriter to save the video.
4. The animation must be at least 5 seconds at 30 fps (>=150 frames).
5. Use only these libraries (all pre-installed): numpy, matplotlib, scipy.
6. Make the animation visually clear — proper title, axis labels, colourful styling.
7. Output ONLY raw Python code — no markdown fences, no explanation text.

CRITICAL rules for headless execution:
- First line of code must be: import matplotlib; matplotlib.use('Agg')
- Never call plt.show() — only save to file.
- Never use any GUI backend or interactive feature.
- Always close the figure at the end: plt.close('all')

Template structure to follow:
    import matplotlib
    matplotlib.use('Agg')
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, FFMpegWriter

    fig, ax = plt.subplots(...)
    # ... setup ...

    def update(frame):
        # ... update plot for this frame ...
        return artists,

    ani = FuncAnimation(fig, update, frames=N_FRAMES, interval=1000/FPS, blit=True)
    writer = FFMpegWriter(fps=FPS, bitrate=1800)
    ani.save(OUTPUT_PATH, writer=writer)
    plt.close('all')"""


def _build_user_prompt(description: str, output_video_path: str, previous_error: str | None) -> str:
    prompt = f"""Create a Python animation for: "{description}"

Save the output video to this EXACT path (copy it verbatim as the OUTPUT_PATH string):
  {output_video_path}

Requirements:
- At least 5 seconds, 30 fps
- Clear title and axis labels
- Colourful and visually engaging
- Must run fully headless (no display, no plt.show())
"""
    if previous_error:
        prompt += f"""
IMPORTANT — the previous version FAILED with this error. Fix it:
--- ERROR ---
{previous_error[:1000]}
-------------
Rewrite the code from scratch to avoid this error.
"""
    return prompt


def generate_python_code(
    description: str,
    output_video_path: str,
    previous_error: str | None = None,
) -> str | None:
    """
    Ask OpenAI to generate Python animation code.
    Returns the raw code string, or None on API failure.
    """
    user_prompt = _build_user_prompt(description, output_video_path, previous_error)

    try:
        response = _client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            max_tokens=4096,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
        )
        code = response.choices[0].message.content.strip()

        # Strip accidental markdown fences
        if code.startswith("```"):
            lines = code.splitlines()
            code = "\n".join(
                line for line in lines
                if not line.strip().startswith("```")
            ).strip()

        return code if code else None

    except Exception as e:
        print(f"  [code_generator] OpenAI API error: {e}")
        return None
