import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

OUTPUT_PATH = r'C:\Users\tgupta\Downloads\MatLabAutoV2\New folder\outputs\project_04_Double_pendulum_chaotic_motion\project_04_Double_pendulum_chaotic_motion.mp4'
FPS = 30
N_FRAMES = 150

def double_pendulum(theta1, theta2, l1, l2, m1, m2):
    g = 9.81
    dt = 0.05
    
    alpha1 = -g * (2*m1 + m2) * np.sin(theta1) - m2 * g * np.sin(theta1 - 2*theta2) - 2 * np.sin(theta1 - theta2) * m2 * ((l2**2 * theta2**2 * np.cos(theta1 - theta2)) + (l1 * theta1**2 * np.cos(theta1 - theta2) - dt**2 * l1 * np.sin(theta1 - theta2)))
    alpha1 /= l1 * (2*m1 + m2 - m2*np.cos(2*theta1 - 2*theta2))
    
    alpha2 = 2 * np.sin(theta1 - theta2) * ((l1 * theta1**2 * np.cos(theta1 - theta2) + g * (m1 + m2)*np.sin(theta1)) - dt**2 * l2 * m2 * np.sin(theta1 - theta2))
    alpha2 /= l2 * (2*m1 + m2 - m2*np.cos(2*theta1 - 2*theta2))

    return alpha1, alpha2

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)
ax.set_title('Double Pendulum Chaotic Motion')
ax.set_xlabel('x')
ax.set_ylabel('y')

theta1 = np.pi/4
theta2 = -np.pi/6
l1 = 1.0
l2 = 1.0
m1 = 1.0
m2 = 1.0

line, = ax.plot([], [], 'o-', lw=2)
pendulum1, = ax.plot([], [], 'ro')
pendulum2, = ax.plot([], [], 'bo')

def init():
    line.set_data([], [])
    pendulum1.set_data([], [])
    pendulum2.set_data([], [])
    return line, pendulum1, pendulum2,

def update(frame):
    global theta1, theta2
    alpha1, alpha2 = double_pendulum(theta1, theta2, l1, l2, m1, m2)
    theta1 += alpha1 * 0.05
    theta2 += alpha2 * 0.05
    
    x1 = np.array([0, l1 * np.sin(theta1)])
    y1 = np.array([0, -l1 * np.cos(theta1)])
    
    x2 = np.array([x1[1], x1[1] + l2 * np.sin(theta2)])
    y2 = np.array([y1[1], y1[1] - l2 * np.cos(theta2)])
    
    line.set_data(np.concatenate((x1, x2)), np.concatenate((y1, y2)))
    pendulum1.set_data(x1, y1)
    pendulum2.set_data(x2, y2)
    
    return line, pendulum1, pendulum2,

ani = FuncAnimation(fig, update, frames=N_FRAMES, init_func=init, interval=1000/FPS, blit=True)
writer = FFMpegWriter(fps=FPS, bitrate=1800)
ani.save(OUTPUT_PATH, writer=writer)
plt.close('all')