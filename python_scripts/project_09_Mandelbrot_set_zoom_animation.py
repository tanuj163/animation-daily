import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_09_Mandelbrot_set_zoom_animation\project_09_Mandelbrot_set_zoom_animation.mp4'
FPS = 30
N_FRAMES = 150

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(-2.0, 1.0)
ax.set_ylim(-1.5, 1.5)
ax.set_title('Mandelbrot Set Zoom Animation')
ax.set_xlabel('Re(z)')
ax.set_ylabel('Im(z)')

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n

def update(frame):
    ax.clear()
    ax.set_xlim(-2.0 * (frame / N_FRAMES), 1.0 * (frame / N_FRAMES))
    ax.set_ylim(-1.5 * (frame / N_FRAMES), 1.5 * (frame / N_FRAMES))
    
    x = np.linspace(-2, 1, 800)
    y = np.linspace(-1.5, 1.5, 800)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)
    
    for i in range(30):
        mask = abs(Z) < 2
        Z[mask] = Z[mask]**2 + C[mask]
    
    im = ax.imshow(np.log2(1 + np.abs(Z)), cmap='hot', interpolation='nearest')
    return [im]

ani = FuncAnimation(fig, update, frames=N_FRAMES, interval=1000/FPS)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')