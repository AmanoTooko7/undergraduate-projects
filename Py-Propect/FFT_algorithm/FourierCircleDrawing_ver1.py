#此程序来源于GPT，目的用于实现用傅里叶画人物图，为版本一

# Step 1: Load image and extract coordinates of edge points
import numpy as np
import cv2

# Load image and convert to grayscale
img = cv2.imread('bart_simpson.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 100, 200)

# Find contours and extract coordinates of contour with largest perimeter
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
perimeters = [cv2.arcLength(contour, True) for contour in contours]
largest_contour = contours[np.argmax(perimeters)]
pts = np.squeeze(largest_contour)

# Step 2: Center the coordinates around (0,0)
center = np.mean(np.minmax(pts, axis=0), axis=0)
pts = pts - center

# Step 3: Downsample the coordinates by keeping only every 5th point
shortest = np.arange(0, len(pts), 5)
pts = pts[shortest]

# Step 4: Compute the Fourier coefficients
from numpy.fft import fft

def cf(z, m):
    """Compute Fourier coefficients up to order m for a given set of points"""
    n = len(z)
    return fft(z)/n * np.exp(-2j*np.pi*m/n*np.arange(n))

z = pts[:,0] + 1j*pts[:,1]
m = 300
cn = cf(z, m)

# Step 5: Compute the circles at each time step
def toPt(z):
    """Convert a complex number to a tuple of (x,y) coordinates"""
    return np.array([z.real, z.imag])

r = np.abs(cn)
theta = np.angle(cn)
index = np.concatenate(([m+1], np.r_[m+2:2*m+2], np.r_[1:m+1][::-1]))
tab = [toPt(cn[j]*np.exp(1j*(j-m-1)*np.arange(0,2*np.pi,2*np.pi/(2*m+1)))) for j in index]

def compute_circles(t):
    """Compute the positions and radii of the circles at time t"""
    p = np.cumsum(tab, axis=0)
    circles = [(p[i], r[index[i]]) for i in range(2*m+1)]
    return circles

# Step 6: Generate the animation frames
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(figsize=(5,5))
ax.set_aspect('equal')

def update(t):
    ax.clear()
    circles = compute_circles(t)
    for c in circles:
        circle = plt.Circle(c[0][t], c[1], fill=False)
        ax.add_artist(circle)
    ax.plot(*p[t].T, color='black')
    ax.scatter(*p[t][-1], color='black', s=10)
    ax.set_xlim(-200, 100)
    ax.set_ylim(-200, 200)

ani = FuncAnimation(fig, update, frames=np.linspace(0, 4*np.pi, 100), interval=50)
ani.save('homer.gif', writer='imagemagick', fps=20)
