import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_05_Fourier_series_approximating_a\project_05_Fourier_series_approximating_a.mp4'
FPS = 30
N_FRAMES = 150

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)
ax.set_title('Fourier Series Approximating a Square Wave')
ax.set_xlabel('x')
ax.set_ylabel('y')

square_wave, = ax.plot([], [], 'k-', label='Square Wave', linewidth=2)
approximations = [ax.plot([], [], 'r--', lw=0.8)[0] for _ in range(5)]

def init():
    square_wave.set_data([], [])
    for approx in approximations:
        approx.set_data([], [])
    return square_wave, *approximations

def update(frame):
    x = np.linspace(0, 2 * np.pi, 300)
    y_square = np.sign(np.sin(x))
    square_wave.set_data(x, y_square)

    n_terms = frame
    y_approx = np.zeros_like(x)
    for k in range(1, n_terms + 1):
        y_approx += (4 / (k * np.pi)) * np.sin(k * x) * np.cos((k - 0.5) * np.pi * k)

    for i, approx in enumerate(approximations):
        if i < n_terms:
            approx.set_data(x[:300], y_approx[:300])
        else:
            approx.set_data([], [])

    return square_wave, *approximations

ani = FuncAnimation(fig, update, frames=N_FRAMES, init_func=init, interval=1000/FPS, blit=True)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')