# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 20:20:40 2020

@author: Leon Kloker
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Pendulum:
    def __init__(self, dt, T, g, theta0, alpha0, theta1, alpha1):
        self.g = g
        self.dt = dt
        self.t = 0
        self.T = T
        self.theta = theta0
        self.theta_v = theta1
        self.alpha = alpha0
        self.alpha_v = alpha1
        self.E = self.energy()

    def euler_ex(self):
        theta_old = self.theta
        alpha_old = self.alpha
        theta_v_old = self.theta_v
        alpha_v_old = self.alpha_v

        self.theta += self.theta_v * self.dt
        self.alpha += self.alpha_v * self.dt
        theta_a, alpha_a = self.eq_motion(theta_old, alpha_old, theta_v_old, alpha_v_old)

        self.theta_v += self.dt * theta_a
        self.alpha_v += self.dt * alpha_a
        self.t += self.dt

    def runge_kutta(self):
        theta_a1, alpha_a1 = self.eq_motion(self.theta, self.alpha, self.theta_v, self.alpha_v)

        theta_2 = self.theta + self.dt/2 * self.theta_v
        alpha_2 = self.alpha + self.dt/2 * self.alpha_v
        theta_v2 = self.theta_v + self.dt/2 * theta_a1
        alpha_v2 = self.alpha_v + self.dt/2 * alpha_a1
        theta_a2, alpha_a2 = self.eq_motion(theta_2, alpha_2, theta_v2, alpha_v2)

        theta_3 = self.theta - self.dt*self.theta_v + 2*self.dt*theta_v2
        alpha_3 = self.alpha - self.dt*self.alpha_v + 2*self.dt*alpha_v2
        theta_v3 = self.theta_v - self.dt*theta_a1 + 2*self.dt*theta_a2
        alpha_v3 = self.alpha_v - self.dt*alpha_a1 + 2*self.dt*alpha_a2
        theta_a3, alpha_a3 = self.eq_motion(theta_3, alpha_3, theta_v3, alpha_v3)

        self.theta += self.dt * ((1/6)*self.theta_v + (2/3)*theta_v2 + (1/6)*theta_v3)
        self.alpha += self.dt * ((1/6)*self.alpha_v + (2/3)*alpha_v2 + (1/6)*alpha_v3)
        self.theta_v += self.dt * ((1/6)*theta_a1 + (2/3)*theta_a2 + (1/6)*theta_a3)
        self.alpha_v += self.dt * ((1/6)*alpha_a1 + (2/3)*alpha_a2 + (1/6)*alpha_a3)
        self.t += self.dt

    def velocity_verlet(self):
        theta_a, alpha_a = self.eq_motion(self.theta, self.alpha, self.theta_v, self.alpha_v)
        self.theta += self.theta_v*self.dt + 0.5 * self.dt**2 * theta_a
        self.alpha += self.alpha_v*self.dt + 0.5 * self.dt**2 * alpha_a
        self.theta_v += 0.5*self.dt*theta_a
        self.alpha_v += 0.5*self.dt*alpha_a

        theta_v2 = self.theta_v + 0.5 * self.dt*theta_a
        alpha_v2 = self.alpha_v + 0.5*self.dt*alpha_a
        theta_a, alpha_a = self.eq_motion(self.theta, self.alpha, theta_v2, alpha_v2)
        self.theta_v += 0.5*self.dt*theta_a
        self.alpha_v += 0.5*self.dt*alpha_a
        self.t += self.dt

    def eq_motion(self, theta, alpha, theta_v, alpha_v):
        theta_a = (self.g * (-2*np.sin(theta) + np.sin(theta + alpha) * np.cos(alpha))
                   + np.sin(alpha) * ((np.cos(alpha) + 1) * theta_v**2
                   + 2*theta_v * alpha_v + alpha_v**2)) / (3 + 2*np.cos(alpha) - (1+np.cos(alpha))**2)
        alpha_a = (-self.g * np.sin(theta+alpha) - theta_v**2 * np.sin(alpha) - theta_a * (1 + np.cos(alpha)))
        return theta_a, alpha_a

    def energy(self):
        energy = self.theta_v**2 + (self.theta_v + self.alpha_v)**2 / 2  + self.theta_v * ( self.theta_v + self.alpha_v) * np.cos(self.alpha) - self.g * (2* np.cos(self.theta) + np.cos(self.theta + self.alpha))
        return energy

    def cartesian_coordinates(self):
        x0 = -np.sin(self.theta)
        y0 = -np.cos(self.theta)
        x1 = x0 - np.sin(self.alpha + self.theta)
        y1 = y0 - np.cos(self.alpha + self.theta)

        return [x0,x1], [y0,y1]


if __name__ == '__main__':

    def animate(j):
        for i in range(0,int(0.01/DT)):
            pendel.runge_kutta()

        x, y = pendel.cartesian_coordinates()
        lines.set_xdata([0,x[0],x[1]])
        lines.set_ydata([0,y[0],y[1]])
        masses.set_offsets(np.array([x,y]).transpose())

        e = pendel.energy()
        energy.append(e)
        line.set_xdata(np.linspace(0,pendel.t,len(energy)))
        line.set_ydata(energy)
        if pendel.t >= pendel.T:
            pendel.T *= 2
            axis.set_xlim(0, pendel.T)

        axis.set_ylim(min(energy), max(energy))

        return masses, lines, line


    alpha = 0
    alpha_v = 1
    theta = np.pi
    theta_v = 0.
    g = 9.81
    DT = 0.01
    T = 5

    pendel = Pendulum(DT, T, g, theta, alpha, theta_v, alpha_v)

    #init of trajectory plot
    fig = plt.figure()
    x, y = pendel.cartesian_coordinates()
    lines = plt.plot([0,x[0],x[1]],[0,y[0],y[1]], 'k')[0]
    masses = plt.scatter(x,y, c='k')
    plt.xlim(-2.2, 2.2)
    plt.ylim(-2.2,2.2)

    #init of energy plot
    fig2 = plt.figure()
    e = pendel.energy()
    line = plt.plot(0, e, label='energy')[0]
    plt.legend()
    axis = fig2.axes[0]
    axis.set_xlim(0, pendel.T)
    axis.set_ylim(e-0.01, e+0.01)
    energy = [e]

    ani = animation.FuncAnimation(fig, animate, interval=10, blit=True)