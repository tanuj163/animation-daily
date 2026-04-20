import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_03_Lorenz_attractor_3D_trajectory\project_03_Lorenz_attractor_3D_trajectory.mp4'
FPS = 30
N_FRAMES = 150

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-20, 20)
ax.set_ylim(-30, 30)
ax.set_zlim(-30, 30)
ax.set_title('Lorenz Attractor')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

def lorenz(x, y, z, s=10, r=28, b=2.667):
    dx = s * (y - x)
    dy = r * x - y - x * z
    dz = x * y - b * z
    return dx, dy, dz

x, y, z = [1], [1], [1]
dt = 0.05

def update(frame):
    global x, y, z, dt
    dx, dy, dz = lorenz(x[-1], y[-1], z[-1])
    x.append(x[-1] + dx * dt)
    y.append(y[-1] + dy * dt)
    z.append(z[-1] + dz * dt)
    line.set_data(np.array(x), np.array(y))
    line.set_3d_properties(np.array(z))
    return line,

line, = ax.plot([], [], [], lw=2, color='r')

ani = FuncAnimation(fig, update, frames=N_FRAMES, interval=1000/FPS, blit=True)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')