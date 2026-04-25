import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_08_Wave_interference_patterns_fro\project_08_Wave_interference_patterns_fro.mp4'
FPS = 30
N_FRAMES = 150

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-2 * np.pi, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)
ax.set_title('Wave Interference Patterns from Two Point Sources')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.grid(True)

source1 = (-np.pi, 0)
source2 = (np.pi, 0)
interference_pattern, = ax.plot([], [], lw=2, color='blue')

def init():
    interference_pattern.set_data([], [])
    return interference_pattern,

def update(frame):
    x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
    y_source1 = np.sin(x - source1[0])
    y_source2 = np.sin(x - source2[0])
    y_interference = y_source1 + y_source2
    interference_pattern.set_data(x, y_interference)
    return interference_pattern,

ani = FuncAnimation(fig, update, frames=N_FRAMES, init_func=init, interval=1000/FPS, blit=True)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')