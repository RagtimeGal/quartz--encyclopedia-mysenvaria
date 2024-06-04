## Import Libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

## Define parameters
plane_radius = 8757.84
treaty_radius = 0.53 * plane_radius
initial_treaty_tilt_angle = np.radians(7.25)
treaty_height, treaty_eccentricity = 3844, 0.017
years_per_rotation, total_days_in_year, minutes_in_day, start_day, start_year, current_frame = 2.7, 360, 24 * 60, 0, 0, 0
# Calc
R = np.sqrt(0.27 * plane_radius**2 + treaty_height**2)
theta = np.linspace(0, 2 * np.pi, 1000)
plane_x_circumference, plane_y_circumference = plane_radius * np.cos(theta), plane_radius * np.sin(theta)

## Initialize the plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
plt.subplots_adjust(bottom=0.25)
# Make the figure full screen
figManager = plt.get_current_fig_manager()
figManager.window.state('zoomed')
# Slider setup
speed_slider = Slider(plt.axes([0.2, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow'), 'Speed', 0.1, 20.0, valinit=7.5, valstep=0.1)
# Setup helper function to set limits and labels
def set_limits_labels(ax, title, xlabel, ylabel, legend_location='best'):
    ax.set_xlim(-plane_radius * 1.3, plane_radius * 1.3)
    ax.set_ylim(-plane_radius * 1.3, plane_radius * 1.3)
    ax.set_aspect('equal', adjustable='box')
    ax.legend(loc=legend_location)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
# Top-down view (Area of Influence)
extent_of_plane, = ax1.plot(plane_x_circumference, plane_y_circumference, color='blue', label="Extent of Plane")
orbit_center_vline, = ax1.plot([], [], color='black', label="Orbital Rotation")
orbit_center_hline, = ax1.plot([], [], color='green', label="Orbital Inclination")
orbit_line_top_down, = ax1.plot([], [], color='red', label="Treaty's Orbit")
point_top_down, = ax1.plot([], [], 'o', color='yellow', label="Harmonic Treaty")
influence_circle, = ax1.plot([], [], '--', color='yellow', label="Area of Influence")
day_text_top_down = ax1.text(0.05, 0.95, '', transform=ax1.transAxes, fontsize=12, verticalalignment='top')
set_limits_labels(ax1, "Harmonic Treaty Orbital Model (Top-Down View)", "X", "Y", legend_location='lower left')
# Side view (Area of Influence)
plane_line_side, = ax2.plot(np.linspace(-plane_radius, plane_radius, 1000), np.zeros_like(plane_x_circumference), color='blue', label="Plane")
orbit_center_side, = ax2.plot([], [], 'o', color='red', label="Orbit Center")  # Changed marker type
orbit_line_side_view, = ax2.plot([], [], color='red', label="Treaty's Orbit")
point_side_view, = ax2.plot([], [], 'o', color='yellow', label="Harmonic Treaty")
influence_sphere_side, = ax2.plot([], [], '--', color='yellow', label="Area of Influence")
day_text_side_view = ax2.text(0.05, 0.95, '', transform=ax2.transAxes, fontsize=12, verticalalignment='top')
set_limits_labels(ax2, "Harmonic Treaty Orbital Model (Side View)", "X", "Z")

## Animation Function
def update(frame):
    global current_frame
    speed_multiplier = np.exp(speed_slider.val) - 1
    current_frame += speed_multiplier
    frame = int(current_frame)
    
    current_day = (start_day + frame // minutes_in_day) % total_days_in_year
    current_time = frame % minutes_in_day
    current_year = start_year + (start_day + frame // minutes_in_day) // total_days_in_year
    
    A = initial_treaty_tilt_angle
    T = total_days_in_year
    phi = 135  # Peak at day 135

    tilt_angle = A * np.sin(2 * np.pi * (current_day - phi) / T + np.pi / 2)
    
    a = treaty_radius
    b = a * np.sqrt(1 - treaty_eccentricity)
    
    # Orbit of Harmonic Treaty completing every 24 hours
    treaty_orbit_angle = 2 * np.pi * current_time / minutes_in_day
    x_orbit = a * np.cos(treaty_orbit_angle)
    y_orbit = b * np.sin(treaty_orbit_angle)
    z = treaty_height * np.sin(2 * np.pi * current_time / minutes_in_day) * np.sin(tilt_angle)
    
    # Rotational angle of the orbit completing every 2.7 years
    cumulative_time = ((current_year - start_year) * total_days_in_year + current_day) / total_days_in_year
    rotational_angle = 2 * np.pi * cumulative_time / years_per_rotation
    
    x_rotated = x_orbit * np.cos(rotational_angle) - y_orbit * np.sin(rotational_angle)
    y_rotated = x_orbit * np.sin(rotational_angle) + y_orbit * np.cos(rotational_angle)

    ## Projection
    # Project to top-down view (Area of Influence)
    point_top_down.set_data([x_rotated], [y_rotated])
    # Project to side view (Area of Influence)
    point_side_view.set_data([x_rotated], [z + treaty_height])
    
    # Update intersection circle (Area of Influence)
    height_diff = abs(z + treaty_height)
    influence_radius = np.sqrt(R**2 - height_diff**2) if height_diff <= R else 0
    influence_circle.set_data(x_rotated + influence_radius * np.cos(theta), y_rotated + influence_radius * np.sin(theta)) if influence_radius > 0 else influence_circle.set_data([], [])
    
    # Update side view (Area of Influence)
    influence_x_side = x_rotated + R * np.cos(theta)
    influence_z_side = z + treaty_height + R * np.sin(theta)
    influence_sphere_side.set_data(influence_x_side, influence_z_side)
    
    # Update orbit lines (Area of Influence)
    treaty_x_orbit = a * np.cos(theta)
    treaty_y_orbit = b * np.sin(theta)
    orbit_line_x_top_down = treaty_x_orbit * np.cos(rotational_angle) - treaty_y_orbit * np.sin(rotational_angle)
    orbit_line_y_top_down = treaty_x_orbit * np.sin(rotational_angle) + treaty_y_orbit * np.cos(rotational_angle)
    orbit_line_top_down.set_data(orbit_line_x_top_down, orbit_line_y_top_down)
    
    orbit_x_side = a * np.cos(theta) * np.cos(rotational_angle) - b * np.sin(theta) * np.sin(rotational_angle)
    orbit_z_side = treaty_height + treaty_height * np.sin(theta) * np.sin(tilt_angle)
    orbit_line_side_view.set_data(orbit_x_side, orbit_z_side)
    
    # Update rotary symbol
    length = 0.1 * plane_radius
    angle = np.pi / 2  # 90 degrees for the + symbol
    x_vline = [0, length * np.cos(rotational_angle)]
    y_vline = [0, length * np.sin(rotational_angle)]
    x_hline = [0, length * np.cos(rotational_angle + angle)]
    y_hline = [0, length * np.sin(rotational_angle + angle)]
    orbit_center_vline.set_data(x_vline, y_vline)
    orbit_center_hline.set_data(x_hline, [0, 0])
    orbit_center_side.set_data([0], [treaty_height])
    
    # Update text
    day_text_top_down.set_text(f'Year: {current_year}, Day: {current_day + 1}, Time: {current_time // 60}:{current_time % 60}')
    
    return (point_top_down, influence_circle, point_side_view, influence_sphere_side, 
            day_text_top_down, day_text_side_view, orbit_line_top_down, orbit_line_side_view,
            extent_of_plane, orbit_center_vline, orbit_center_hline, plane_line_side, orbit_center_side)

## Animation and Display
ani = FuncAnimation(fig, update, frames=np.arange(0, total_days_in_year * minutes_in_day), blit=True, interval=10)
plt.show()
