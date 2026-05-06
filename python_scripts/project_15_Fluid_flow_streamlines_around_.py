import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_15_Fluid_flow_streamlines_around_\project_15_Fluid_flow_streamlines_around_.mp4'
FPS = 30
N_FRAMES = 150

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(-2, 2)
ax.set_ylim(-1, 1)
ax.set_title('Fluid Flow Streamlines Around a Cylinder')
ax.set_xlabel('x')
ax.set_ylabel('y')

# Create the cylinder
theta = np.linspace(0, 2 * np.pi, 100)
x_cylinder = np.cos(theta)
y_cylinder = np.sin(theta)

# Initial streamline positions
x_streamlines = np.linspace(-1.5, 1.5, 30)
y_streamlines = np.zeros_like(x_streamlines)

def init():
    ax.plot(x_cylinder, y_cylinder, 'b-', lw=2)  # Plot the cylinder
    for i in range(len(x_streamlines)):
        line, = ax.plot([], [], lw=1.5)
    return ax.lines + (line,) * len(x_streamlines)

def update(frame):
    for i, x0 in enumerate(x_streamlines):
        y0 = -y_streamlines[i]
        x = np.linspace(x0, 2 * np.pi, 100)
        y = y0 + np.sin(x) / (x ** 2 + y0 ** 2)
        ax.lines[i].set_data(x, y)
    return ax.lines

ani = FuncAnimation(fig, update, frames=N_FRAMES, init_func=init, interval=1000/FPS, blit=True)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')