import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_10_Projectile_motion_with_air_res\project_10_Projectile_motion_with_air_res.mp4'
FPS = 30
N_FRAMES = 150

g = 9.81
m = 1.0  # mass of the projectile
c_d = 0.1  # drag coefficient
v_0 = 20  # initial velocity
theta = np.pi / 4  # launch angle
x_0, y_0 = 0, 0  # initial position

t_max = v_0 * np.sin(theta) / g + 1  # approximate maximum time for projectile motion
dt = t_max / N_FRAMES
time_points = np.linspace(0, t_max, N_FRAMES)

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(-5, 25)
ax.set_ylim(-5, 20)
ax.set_title('Projectile Motion with Air Resistance')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
line, = ax.plot([], [], lw=2, color='blue')

def init():
    line.set_data([], [])
    return line,

def update(frame):
    t = time_points[frame]
    x = x_0 + v_0 * np.cos(theta) * t - 0.5 * c_d * m / (2 * m) * v_0**2 * np.cos(theta)**2 * t**2
    y = y_0 + v_0 * np.sin(theta) * t - 0.5 * g * t**2
    line.set_data([x_0, x], [y_0, y])
    return line,

ani = FuncAnimation(fig, update, frames=N_FRAMES, init_func=init, interval=int(1000 / FPS), blit=True)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')