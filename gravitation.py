# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 20:43:33 2020

@author: Leon Kloker
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d.art3d import juggle_axes

class mass:
    def __init__(self, dt, T, gamma, m, r0, phi0, theta0, r1 , phi1, theta1):
        self.gamma = gamma
        self.m = m
        self.dt = dt
        self.t = 0
        self.T = T
        self.theta = theta0
        self.theta_v = theta1
        self.phi = phi0
        self.phi_v = phi1
        self.r = r0
        self.r_v = r1
        self.E = self.energy()
        
    def euler_ex(self):
        r_a, phi_a, theta_a = self.eq_motion(self.r, self.phi, self.theta, self.r_v, self.phi_v, self.theta_v)
        
        self.r += self.r_v * self.dt
        self.theta += self.theta_v * self.dt
        self.phi += self.phi_v * self.dt
        
        self.r_v += self.dt * r_a
        self.theta_v += self.dt * theta_a
        self.phi_v += self.dt * phi_a       
        self.t += self.dt
    
    def velocity_verlet(self):
        r_a, phi_a, theta_a = self.eq_motion(self.r, self.phi, self.theta, self.r_v, self.phi_v, self.theta_v)
        
        self.r += self.r_v * self.dt + 0.5*self.dt**2 * r_a
        self.phi += self.phi_v * self.dt + 0.5*self.dt**2 * phi_a
        self.theta += self.theta_v * self.dt + 0.5*self.dt**2 * theta_a
        
        self.r_v += 0.5 * self.dt * r_a
        self.theta_v += 0.5 * self.dt * theta_a
        self.phi_v += 0.5 * self.dt * phi_a
        
        r_v = self.r_v + 0.5 * self.dt * r_a
        phi_v = self.phi_v + 0.5 * self.dt * phi_a
        theta_v = self.theta_v + 0.5 * self.dt * theta_a
        
        r_a, phi_a, theta_a = self.eq_motion(self.r, self.phi, self.theta, r_v, phi_v, theta_v)
        
        self.r_v += 0.5 * self.dt * r_a
        self.theta_v += 0.5 * self.dt * theta_a
        self.phi_v += 0.5 * self.dt * phi_a
        self.t += self.dt
        
    def eq_motion(self, r, phi, theta, r_v, phi_v, theta_v):
        r_a = theta_v**2 * r + r * phi_v**2 * np.sin(theta)**2 - self.gamma / r**2
        phi_a = phi_v**2 * np.cos(theta) * np.sin(theta) - 2* r_v * phi_v / r
        theta_a = -2 * phi_v * ( theta_v * np.cos(theta)/np.sin(theta) + r_v/r)
        return r_a, phi_a, theta_a
    
    def energy(self):
        energy = 0.5 * self.m * (self.r_v**2 + self.r**2 * self.theta_v**2 + self.r**2 * self.phi_v**2 * np.sin(self.theta)**2) - self.gamma *self.m / self.r
        return energy
        
    def cartesian_coordinates(self):
        x = self.r * np.sin(self.theta) * np.cos(self.phi)
        y = self.r * np.sin(self.theta) * np.sin(self.phi)
        z = self.r * np.cos(self.theta)       
        return x,y,z
    
if __name__ == '__main__':
    
    dt = 1
    T = 100
    G = 6.6743 * 10**-20
    M = 5.9723 * 10**24
    m = 1.
    r = 7000
    phi = 0.
    theta = np.pi/2
    r_v = 0.
    phi_v = 2*np.sqrt(G*M/r**3)
    theta_v = 0.
    
    sat = mass(dt, T, G*M, m, r, phi, theta, r_v, phi_v, theta_v)
    
    def animate(j):
        for i in range(0,int(5/dt)):
            sat.velocity_verlet()
        
        x, y, z = sat.cartesian_coordinates()
        #masses.set_offsets([[0,0,0],[x,y,z]])
        masses.set_offsets([[0,0],[x,z]])
        e = sat.energy()
        energy.append(e)
        line.set_xdata(np.linspace(0, sat.t, len(energy)))
        line.set_ydata(energy)
        
        if (x >= ax.get_xlim()).sum() > 0:
            ax.set_xlim(2*ax.get_xlim()[0],2*ax.get_xlim[1])
            
        if z >= ax.get_ylim():
            ax.set_ylim(ax.get_ylim()*2)
            
        if sat.t >= sat.T:
            sat.T *= 2
            axis.set_xlim(0, sat.T)
        
        #axis.set_ylim(min(energy), max(energy))
        
        return masses, line
    
    
    #init of trajectory plot
    fig = plt.figure()
    ax = plt.subplot(111)
    #ax = p3.Axes3D(fig)
    x, y, z = sat.cartesian_coordinates()   
    masses = ax.scatter([0,x],[0,z], linewidth=1, c=['k','r'])
    #ax.scatter(0, 0, 0, linewidth=8, c='k')
    ax.set_xlim(-3*r,3*r)  
    ax.set_ylim(-3*r,3*r)
    #ax.set_zlim3d(-3*r,3*r)
    plt.show()
        
    #init of energy plot
    fig2 = plt.figure()
    e = sat.energy()
    line = plt.plot(0, e, label='energy')[0]
    plt.legend()
    axis = fig2.axes[0]
    axis.set_xlim(0, sat.T)
    axis.set_ylim(e-1000, e+1000)
    energy = []
    energy.append(e)
    
    ani = animation.FuncAnimation(fig, animate, interval=10, blit=True)
    plt.show()
    
    
    
    