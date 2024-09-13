import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import random

# ---------------- Simulation Parameters ---------------- #
WIDTH = 10.0  # Width of the box
HEIGHT = 10.0  # Height of the box
N_PARTICLES = 100  # Total number of particles
PROPORTION_RED = 0.1  # Initial proportion of red particles
PARTICLE_RADIUS = 0.1  # Radius of each particle
P_RED_ON_COLLISION = 0.3  # Probability to turn green to red upon collision with red
V_MEAN = 5.0  # Average speed (Maxwell-Boltzmann)
MASS = 1.0  # Mass of each particle (assuming unit mass for simplicity)
COOLDOWN_MEAN = 10.0  # Average cooldown time for red particles

DT = 0.01  # Time step
MAX_TIME = 50.0  # Maximum simulation time

# ---------------- Particle Initialization ---------------- #
class Particle:
    def __init__(self, position, velocity, is_red=False):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.is_red = is_red
        self.cooldown_timer = 0.0  # Time remaining in red state

def initialize_particles():
    particles = []
    # Initialize positions without overlapping
    attempts = 0
    max_attempts = 10000
    while len(particles) < N_PARTICLES and attempts < max_attempts:
        pos = np.array([random.uniform(0, WIDTH), random.uniform(0, HEIGHT)])
        overlap = False
        for p in particles:
            # Compute minimum image distance considering periodic boundaries
            delta = pos - p.position
            delta[0] -= WIDTH * np.round(delta[0] / WIDTH)
            delta[1] -= HEIGHT * np.round(delta[1] / HEIGHT)
            if np.linalg.norm(delta) < 2 * PARTICLE_RADIUS:
                overlap = True
                break
        if not overlap:
            # Initialize velocity from Maxwell-Boltzmann distribution
            # Gaussian distribution for each velocity component
            vx = np.random.normal(0, V_MEAN / np.sqrt(2))
            vy = np.random.normal(0, V_MEAN / np.sqrt(2))
            vel = np.array([vx, vy])
            particles.append(Particle(pos, vel))
        attempts += 1
    if attempts == max_attempts:
        raise Exception("Failed to initialize particles without overlap. Try reducing N_PARTICLES or PARTICLE_RADIUS.")
    
    # Assign initial red particles
    n_red = int(PROPORTION_RED * N_PARTICLES)
    red_indices = random.sample(range(N_PARTICLES), n_red)
    for idx in red_indices:
        particles[idx].is_red = True
        particles[idx].cooldown_timer = np.random.exponential(scale=COOLDOWN_MEAN)
    return particles

# ---------------- Collision Handling ---------------- #
def handle_collision(p1, p2):
    # Vector between centers
    delta_pos = p1.position - p2.position
    # Apply minimum image convention for periodic boundaries
    delta_pos[0] -= WIDTH * np.round(delta_pos[0] / WIDTH)
    delta_pos[1] -= HEIGHT * np.round(delta_pos[1] / HEIGHT)
    dist = np.linalg.norm(delta_pos)
    if dist == 0:
        # Prevent division by zero
        dist = 1e-8
    # Normal vector
    n = delta_pos / dist
    # Relative velocity
    delta_v = p1.velocity - p2.velocity
    # Velocity along the normal
    vn = np.dot(delta_v, n)
    if vn > 0:
        # Particles are moving away from each other
        return
    # Compute impulse scalar
    impulse = (2 * vn) / (MASS + MASS)  # Assuming equal mass
    # Update velocities to simulate elastic collision
    p1.velocity -= impulse * MASS * n
    p2.velocity += impulse * MASS * n

    # State change
    if p1.is_red and not p2.is_red:
        if random.random() < P_RED_ON_COLLISION:
            p2.is_red = True
            p2.cooldown_timer = np.random.exponential(scale=COOLDOWN_MEAN)
    elif p2.is_red and not p1.is_red:
        if random.random() < P_RED_ON_COLLISION:
            p1.is_red = True
            p1.cooldown_timer = np.random.exponential(scale=COOLDOWN_MEAN)

# ---------------- Periodic Boundary Conditions ---------------- #
def apply_periodic_boundary(p):
    p.position[0] = p.position[0] % WIDTH
    p.position[1] = p.position[1] % HEIGHT

# ---------------- Simulation Initialization ---------------- #
particles = initialize_particles()

# For plotting proportions over time
time_history = []
green_history = []
red_history = []

# ---------------- Visualization Setup ---------------- #
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ---------------- Particle Animation Setup ---------------- #
ax1.set_xlim(0, WIDTH)
ax1.set_ylim(0, HEIGHT)
ax1.set_aspect('equal')
ax1.set_title('Particle Simulation')
particles_plot = ax1.scatter([], [], s=(PARTICLE_RADIUS*800), c=[], facecolors='k', edgecolors='k')

# ---------------- Proportion Plot Setup ---------------- #
ax2.set_xlim(0, MAX_TIME)
ax2.set_ylim(0, 1)
line_green, = ax2.plot([], [], 'g-', label='Green')
line_red, = ax2.plot([], [], 'r-', label='Red')
ax2.set_xlabel('Time')
ax2.set_ylabel('Proportion')
ax2.set_title('Proportion of Particles')
ax2.legend()
ax2.grid(True)

# ---------------- Animation Functions ---------------- #
def init():
    # Initialize scatter plot with empty data but correct shape
    particles_plot.set_offsets(np.empty((0, 2)))  # 2D empty array
    particles_plot.set_color([])  # Empty color list
    particles_plot.set_facecolors([])  # Empty face color list

    # Initialize proportion plot
    time_history.clear()
    green_history.clear()
    red_history.clear()
    line_green.set_data([], [])
    line_red.set_data([], [])

    return particles_plot, line_green, line_red

def animate(frame):
    global particles, time_history, green_history, red_history
    current_time = frame * DT
    if current_time > MAX_TIME:
        anim.event_source.stop()

    # Update positions
    for p in particles:
        p.position += p.velocity * DT
        apply_periodic_boundary(p)

    # Detect and handle collisions
    # Using a simple pairwise check; for better performance with many particles, consider spatial partitioning
    for i in range(N_PARTICLES):
        for j in range(i+1, N_PARTICLES):
            p1 = particles[i]
            p2 = particles[j]
            delta_pos = p1.position - p2.position
            # Apply minimum image convention for periodic boundaries
            delta_pos[0] -= WIDTH * np.round(delta_pos[0] / WIDTH)
            delta_pos[1] -= HEIGHT * np.round(delta_pos[1] / HEIGHT)
            dist = np.linalg.norm(delta_pos)
            if dist < 2 * PARTICLE_RADIUS:
                handle_collision(p1, p2)

    # Update cooldown timers and handle state transitions
    for p in particles:
        if p.is_red:
            p.cooldown_timer -= DT
            if p.cooldown_timer <= 0:
                p.is_red = False
                p.cooldown_timer = 0.0

    # Record proportions
    n_red = sum(p.is_red for p in particles)
    n_green = N_PARTICLES - n_red
    time_history.append(current_time)
    green_history.append(n_green / N_PARTICLES)
    red_history.append(n_red / N_PARTICLES)

    # Update particle plot
    x = [p.position[0] for p in particles]
    y = [p.position[1] for p in particles]
    colors = ['red' if p.is_red else 'green' for p in particles]
    particles_plot.set_offsets(np.c_[x, y])
    particles_plot.set_facecolors(colors)
    particles_plot.set_color(colors)
    

    # Update proportion plot
    line_green.set_data(time_history, green_history)
    line_red.set_data(time_history, red_history)
    ax2.set_xlim(0, max(MAX_TIME, current_time + DT))

    return particles_plot, line_green, line_red

# ---------------- Run Animation ---------------- #
anim = animation.FuncAnimation(
    fig, animate, init_func=init,
    frames=int(MAX_TIME / DT), interval=20, blit=True
)

plt.tight_layout()
plt.show()
