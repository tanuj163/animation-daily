import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_02_Lissajous_figures_morphing_thr\project_02_Lissajous_figures_morphing_thr.mp4'
FPS = 30
N_FRAMES = 150

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_title('Lissajous Figures Morphing through Phase Angles')
ax.set_xlabel('x')
ax.set_ylabel('y')
line, = ax.plot([], [], lw=2, color='blue')

def init():
    line.set_data([], [])
    return line,

def update(frame):
    t = np.linspace(0, 2 * np.pi, 300)
    phase_angle = frame * (np.pi / N_FRAMES)
    x1 = np.sin(t)
    y1 = np.cos(t + phase_angle)
    x2 = np.sin(2 * t)
    y2 = np.cos(2 * t - phase_angle)
    ratio = frame / N_FRAMES
    line.set_data((x1, x2), (y1, y2))
    return line,

ani = FuncAnimation(fig, update, frames=N_FRAMES, init_func=init, interval=1000/FPS, blit=True)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')