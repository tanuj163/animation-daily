import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_06_Bouncing_ball_with_realistic_g\project_06_Bouncing_ball_with_realistic_g.mp4'
FPS = 30
N_FRAMES = 150

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, 10)
ax.set_ylim(-1, 1)
ax.set_title('Bouncing Ball with Realistic Gravity and Energy Loss')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Height (m)')
ball, = ax.plot([], [], 'ro', markersize=15)

def init():
    ball.set_data([], [])
    return ball,

def update(frame):
    g = 9.81
    dt = 0.033
    energy_loss_factor = 0.95

    if frame == 0:
        t0, h0 = 0, 1
        v0 = 0
    else:
        t0, h0, v0 = update.prev_state

    t = np.linspace(t0, t0 + dt, 2)
    x = np.linspace(h0 - v0 * dt / 2, h0 - v0 * dt / 2, 2)

    if h0 > 0 and (h0 - v0 * dt + 0.5 * g * dt**2 <= 0):
        v0 = -v0 * energy_loss_factor
        h0 = -(h0 - v0 * dt + 0.5 * g * dt**2)

    update.prev_state = t[-1], h0, v0

    ball.set_data(t, x)
    return ball,

update.prev_state = (0, 1, 0)

ani = FuncAnimation(fig, update, frames=N_FRAMES, init_func=init, interval=1000/FPS, blit=True)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')