import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_13_Spring-mass-damper_system_osci\project_13_Spring-mass-damper_system_osci.mp4'
FPS = 30
N_FRAMES = 150

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_title('Spring-Mass-Damper System Oscillation')
ax.set_xlabel('Position (m)')
ax.set_ylabel('Velocity (m/s)')
line_pos, = ax.plot([], [], lw=2, color='blue', label='Mass Position')
line_vel, = ax.plot([], [], lw=2, color='red', label='Mass Velocity')
ax.legend()

def init():
    line_pos.set_data([], [])
    line_vel.set_data([], [])
    return line_pos, line_vel,

def update(frame):
    t = frame / FPS
    x = np.sin(t)
    v = np.cos(t) * (1 - 0.5 * t)
    line_pos.set_data([t], [x])
    line_vel.set_data([t], [v])
    return line_pos, line_vel,

ani = FuncAnimation(fig, update, frames=N_FRAMES, init_func=init, interval=1000/FPS, blit=True)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')