import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_11_Heat_diffusion_on_a_2D_plate_o\project_11_Heat_diffusion_on_a_2D_plate_o.mp4'
FPS = 30
N_FRAMES = 150

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_title('Heat Diffusion on a 2D Plate')
ax.set_xlabel('x')
ax.set_ylabel('y')
im = ax.imshow(np.zeros((100, 100)), cmap='hot', interpolation='nearest')

def init():
    im.set_data(np.zeros((100, 100)))
    return im,

def update(frame):
    dx, dy = 0.05, 0.05
    u = np.zeros((102, 102))
    for i in range(1, 101):
        for j in range(1, 101):
            u[i, j] = (u[i+1, j] + u[i-1, j] + u[i, j+1] + u[i, j-1]) / 4
    u[25:76, 25:76] += np.random.normal(0.5, 0.1, (51, 51))
    im.set_data(u[1:-1, 1:-1])
    return im,

ani = FuncAnimation(fig, update, frames=N_FRAMES, init_func=init, interval=1000/FPS, blit=True)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')