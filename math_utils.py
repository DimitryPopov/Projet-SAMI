import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

n = 3000

points = np.random.rand(n, 2) * 100

visite = [False] * n
chemin = []

courant = 0
chemin.append(courant)
visite[courant] = True

for _ in range(n - 1):
    dist_min = float('inf')
    prochain = None

    for i in range(n):
        if not visite[i]:
            d = np.linalg.norm(points[courant] - points[i])
            if d < dist_min:
                dist_min = d
                prochain = i

    courant = prochain
    chemin.append(courant)
    visite[courant] = True

chemin.append(chemin[0])

# --- ANIMATION ---

fig, ax = plt.subplots()
ax.scatter(points[:, 0], points[:, 1], color='red')
ax.set_title("TSP - Plus proche voisin (animé)")

line, = ax.plot([], [], color='blue')

x_data = []
y_data = []

def update(frame):
    i = frame
    p = points[chemin[i]]

    x_data.append(p[0])
    y_data.append(p[1])

    line.set_data(x_data, y_data)
    return line,

ani = FuncAnimation(
    fig,
    update,
    frames=len(chemin),
    interval=20,   # vitesse (ms)
    repeat=False
)

plt.show()