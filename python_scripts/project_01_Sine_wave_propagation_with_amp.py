import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_01_Sine_wave_propagation_with_amp.mp4'
FPS = 30
N_FRAMES = 150

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)
ax.set_title('Sine Wave Propagation with Amplitude and Frequency Sweep')
ax.set_xlabel('Position (x)')
ax.set_ylabel('Amplitude (y)')
line, = ax.plot([], [], lw=2, color='blue')

def init():
    line.set_data([], [])
    return line,

def update(frame):
    t = np.linspace(0, 2 * np.pi, 300)
    amplitude = frame / 50 + 1
    frequency = (frame / N_FRAMES) * 10 + 1
    y = amplitude * np.sin(frequency * t)
    line.set_data(t, y)
    return line,

ani = FuncAnimation(fig, update, frames=N_FRAMES, init_func=init, interval=1000/FPS, blit=True)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')