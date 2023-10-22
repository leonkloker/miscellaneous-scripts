import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

class Simulation:
    def __init__(self, Time, dt, x, v, box, duration, rate, skin, fixed_rate=0, fmax=float('nan')):
        self.T_MAX = Time
        self.dt = dt
        self.t = 0
        self.x = x.copy()
        self.v = v.copy()
        self.box = box.copy()
        self.fmax = fmax
        self.dim = self.x.shape[0]
        self.n = self.x.shape[1]
        self.x0 = x.copy()

        self.f = np.zeros_like(self.x)
        self.r_matrix =np.zeros((self.n, self.n, self.dim))
        self.f_matrix = np.zeros_like(self.r_matrix)
        self.verlet = []
        self.skin = skin

        self.infected = np.zeros(self.n)
        self.duration = duration
        self.rate = rate
        self.fixed = np.array(np.where(np.random.random((1, self.n))<fixed_rate, 0, 1))
        self.fixed = np.repeat(self.fixed, self.dim, axis=0)

        self.cases = []
        self.recovered = []
        self.end = False

        self.reset()
        self.update_verlet()
        self.update_force()

    def update_verlet(self):
        #update the verlet list
        self.update_distance()
        self.x0 = self.x
        dist = np.tril(np.linalg.norm(self.r_matrix, axis=2))
        self.verlet = np.argwhere((dist < (1 + self.skin)) & (dist != 0))


    def vv_step(self):
        #velocity verlet integration step
        self.x = self.x + np.where(self.fixed != 0, self.dt*self.v + 0.5 * self.f * self.dt**2, 0)
        self.v = self.v + 0.5 * self.dt * self.f
        self.update_force()
        self.v = self.v + 0.5 * self.dt * self.f

        #increase time
        self.t += self.dt

        if np.max(np.linalg.norm(self.x - self.x0, axis=0)) > 0.5 * self.skin:
            self.update_verlet()

        self.update_disease()

        #elastic wall boundary conditions
        for i in range(self.dim):
            self.v[i,:] *= np.where(np.abs(self.x[i,:])>=(self.box[i]/2), -1, 1)

    def update_disease(self):
        #check for cured cases
        self.infected = np.where((self.t-self.duration > self.infected) & (self.infected >= 0), -2, self.infected)
        #save amount of cases
        self.cases.append(np.where(sim.infected != -1, 1, 0).sum())
        #save amount of recovered cases
        self.recovered.append(np.where(sim.infected == -2, 1, 0).sum())

        if self.recovered[-1] == self.n:
            self.end = True

    def update_distance(self):
        #compute distance of all particle pairs
        self.r_matrix = np.repeat([self.x.transpose()], self.n, axis=0)
        self.r_matrix -= np.transpose(self.r_matrix, axes=[1, 0, 2])

    def update_force(self):
        self.f = np.zeros((self.dim, self.n))

        for pair in self.verlet:
            r_vec = self.x[:,pair[1]]-self.x[:,pair[0]]
            r = np.linalg.norm(r_vec)
            f_ij = r_vec * self.force(r) / r
            self.f[:,pair[0]] -= f_ij
            self.f[:,pair[1]] += f_ij

            if r < 1:
                if (self.infected[pair[0]] >= 0) & (self.infected[pair[1]]==-1) & (np.random.random() < self.rate):
                    self.infected[pair[1]] = self.t
                if (self.infected[pair[1]] >= 0) & (self.infected[pair[0]]==-1) & (np.random.random() < self.rate):
                    self.infected[pair[0]] = self.t

        self.force_cutoff()

    def force(self, r):
        if r < 1:
            return 12*np.power(r, -12)
        else:
            return 0

    def force_cutoff(self):
        #cut force values which are to big if the system is still in the warmup
        if (not np.isnan(self.fmax)):
            F = np.linalg.norm(self.f, axis=0)
            if (np.array(np.where(self.fixed!=0, F, 0)) > self.fmax).sum() < 1:
                self.fmax = float('nan')
                print('warm-up time: '+str(self.t))
                self.reset()
            else:
                with np.errstate(all='ignore'):
                    self.f = np.multiply(self.f, np.where(F>self.fmax, self.fmax*np.power(F,-1), 1))

    def reset(self):
        self.infected = -np.ones(self.n)
        self.t = 0
        p0 = int(np.random.uniform(0, self.n-0.5))
        self.infected[p0] = self.t
        self.fixed[:,p0] = 1
        self.cases = []
        self.recovered = []


#number of particles
N = 100

#box size
BOX = np.array([50, 50])

#simulation time
T_MAX = 5

#integration time-step
DT = 0.001

#parameter for the average particle movement
T = 10

#maximum force during warm up
f_max = 200

#duration time of the disease
duration = 1.5

#infection probability during contact
infection_rate = 0.4

#percentage of particles, which dont move
fix_rate = 0.3

DIM = BOX.shape[0]

#random initialization of the particle positions
x = np.random.random((DIM,N)) - 0.5
for i in range(0, DIM):
    x[i,:] = x[i,:]*BOX[i]

#initialization of the particle velocities
v = np.random.normal(0, T, size=(DIM, N))

#set the simulation up
sim = Simulation(T_MAX, DT, x, v, BOX, duration, infection_rate, 0.5,  fix_rate, fmax=f_max)

#set the plot framework
fig = plt.figure()
col = np.where(sim.infected >= 0,'r', np.where(sim.infected == -2,'g','b'))
points = plt.scatter(x[0,:], x[1,:], s=8, c=col)
plot = fig.axes[0]
plot.set_xlim(-0.5*(1+sim.box[0]), (1+sim.box[0])*0.5)
plot.set_ylim(-0.5*(1+sim.box[1]), (1+sim.box[1])*0.5)

fig2 = plt.figure()
cases, = plt.plot([], 'k', label='overall cases')
cur, = plt.plot([], 'r', label='current cases')
rec, = plt.plot([], 'g', label='recovered cases')
axis = fig2.axes[0]
axis.set_ylim(ymin=0, ymax=N)
axis.set_xlim(xmin=0, xmax=T_MAX)
plt.legend(loc='upper left')

#when does the animation stop
def frames():
    while True:
        yield 1

#set new positions and colours
def animate(j):
    for i in range(0, int(0.01/DT)):
        sim.vv_step()

    if sim.t >= sim.T_MAX:
        sim.T_MAX = sim.T_MAX * 2.
        axis.set_xlim(xmin=0, xmax=sim.T_MAX)

    xdata = np.linspace(0,sim.t,len(sim.recovered))
    rec.set_xdata(xdata)
    rec.set_ydata(sim.recovered)
    cur.set_xdata(xdata)
    cur.set_ydata(np.array(sim.cases)-np.array(sim.recovered))
    cases.set_xdata(xdata)
    cases.set_ydata(sim.cases)
    points.set_offsets(sim.x.transpose())
    points.set_color(np.where(sim.infected >= 0, 'r', np.where(sim.infected == -2,'g','b')))
    return points, cases, cur, rec


ani = animation.FuncAnimation(fig, animate, frames=frames, interval=1, blit=True)
plt.show()

#start = time.time()
#ani.save('animation5.gif', writer='PillowWriter', fps=20);
#end = time.time()
#print('computation time: '+str(end-start))
