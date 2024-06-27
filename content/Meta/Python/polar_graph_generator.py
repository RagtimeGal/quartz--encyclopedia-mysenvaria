import matplotlib.pyplot as plt
import numpy as np

# Create the figure and axis
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# Set the number of spokes and rings
num_spokes = 36
num_rings = 36

# Create the grid
theta = np.linspace(0, 2 * np.pi, num_spokes, endpoint=True)
radii = np.linspace(0, 1, num_rings)

# Draw the spokes
for angle in theta:
    ax.plot([angle, angle], [0, 1], color='black')

# Draw the rings
for radius in radii:
    ax.plot(theta, [radius]*num_spokes, color='black')

# Set the axis limits
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])

# Export the graph as a PNG image
plt.savefig("polar_graph.png")

# Show the graph (optional)
plt.show()
