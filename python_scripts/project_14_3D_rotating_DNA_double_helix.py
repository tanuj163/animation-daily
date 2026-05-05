import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_14_3D_rotating_DNA_double_helix\project_14_3D_rotating_DNA_double_helix.mp4'
FPS = 30
N_FRAMES = 150

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)
ax.set_title('3D Rotating DNA Double Helix')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

theta = np.linspace(0, 2 * np.pi, 100)
t = np.linspace(0, 1, 100)
r = 1 + np.sin(6 * theta)

x = r * np.cos(theta) * t
y = r * np.sin(theta) * t
z = r * np.sin(4 * theta) * t

line, = ax.plot(x[:50], y[:50], z[:50], lw=2, color='blue', label='+')
line_neg, = ax.plot(x[50:], y[50:], z[50:], lw=2, color='red', label='-')

def init():
    line.set_data(np.array([]), np.array([]))
    line.set_3d_properties(np.array([]))
    line_neg.set_data(np.array([]), np.array([]))
    line_neg.set_3d_properties(np.array([]))
    return line, line_neg,

def update(frame):
    theta_frame = 2 * np.pi * frame / N_FRAMES
    x_pos = r * np.cos(theta + theta_frame) * t
    y_pos = r * np.sin(theta + theta_frame) * t
    z_pos = r * np.sin(4 * theta + theta_frame) * t

    x_neg = -x_pos
    y_neg = -y_pos
    z_neg = -z_pos

    line.set_data(x_pos[:50], y_pos[:50])
    line.set_3d_properties(z_pos[:50])

    line_neg.set_data(x_neg[50:], y_neg[50:])
    line_neg.set_3d_properties(z_neg[50:])

    return line, line_neg,

ani = FuncAnimation(fig, update, frames=N_FRAMES, init_func=init, interval=1000/FPS, blit=True)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')