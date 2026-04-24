import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_07_Rotating_3D_surface_plot_of_a_\project_07_Rotating_3D_surface_plot_of_a_.mp4'
FPS = 30
N_FRAMES = 150

fig, ax = plt.subplots(subplot_kw={'projection': '3d'}, figsize=(8, 5))
ax.set_xlim(-2 * np.pi, 2 * np.pi)
ax.set_ylim(-2 * np.pi, 2 * np.pi)
ax.set_zlim(-2, 2)
ax.set_title('Rotating 3D Surface Plot of a Mathematical Function')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

x = np.linspace(-2 * np.pi, 2 * np.pi, 100)
y = np.linspace(-2 * np.pi, 2 * np.pi, 100)
x, y = np.meshgrid(x, y)
z = np.sin(np.sqrt(x**2 + y**2))

surface = ax.plot_surface(x, y, z, cmap='viridis')

def init():
    surface.set_array(None)
    return surface,

def update(frame):
    surface._offsets3d = (x.ravel(), y.ravel(), np.sin(np.sqrt(x**2 + y**2) + frame * 0.1))
    return surface,

ani = FuncAnimation(fig, update, frames=N_FRAMES, init_func=init, interval=1000/FPS, blit=True)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')