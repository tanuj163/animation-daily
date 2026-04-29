import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_12_Spiral_galaxy_particle_simulat\project_12_Spiral_galaxy_particle_simulat.mp4'
FPS = 30
N_FRAMES = 150

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_title('Spiral Galaxy Particle Simulation')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_aspect('equal')

theta = np.linspace(0, 10 * np.pi, N_FRAMES)
r = theta / (2 * np.pi)  # Radius increases linearly with time

line, = ax.plot([], [], 'o', lw=2, markersize=2)

def init():
    line.set_data([], [])
    return line,

def update(frame):
    x = r[frame] * np.cos(theta[:frame + 1])
    y = r[frame] * np.sin(theta[:frame + 1])
    line.set_data(x, y)
    return line,

ani = FuncAnimation(fig, update, frames=N_FRAMES, init_func=init, interval=1000/FPS, blit=True)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')