import random
from ParticleFunctions import *


class Particle: #a particle class for each particle.
    def __init__(self, x, y, vx, vy): #initializes the particle with the location,the velocity, and an optional mass, default is 1.
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.locations = [(x,y)]
        self.velocities = [(vx,vy)]
        self.anim = []


class Particle_Array: # a master class for all the particles.
    def __init__(self, N, x_min, x_max, y_min, y_max, vx_max, vy_max): #initializes an array with N particles, within a given range, and a given max speed.
        self.array = []
        self.times = []
        #appends the array N times with a random location within the range and a random velocity within the range
        while len(self.array) < N:
            p1 = (random.uniform(x_min, x_max), random.uniform(y_min, y_max))
            for p in self.array:
                if distance(p1[0], p1[1], p.x, p.y) < 2:
                    break
            self.array.append(Particle(p1[0], p1[1], random.uniform(-vx_max, vx_max), random.uniform(-vy_max, vy_max)))
    def step(self, time):# steps each particle with its vlocity * the accepted time, which is the time until next collision
        for p in self.array:
            p.x += time * p.vx
            p.y += time * p.vy
            p.locations.append((p.x,p.y))
            p.velocities.append((p.vx,p.vy))
        self.times.append(time)

    def velocity_change2(self, p1, p2, ux1, uy1, ux2, uy2):# a function that changes the velocity of particle1 and particle2 to the target velocities
        self.array[self.array.index(p1)].vx = ux1
        self.array[self.array.index(p1)].vy = uy1
        self.array[self.array.index(p2)].vx = ux2
        self.array[self.array.index(p2)].vy = uy2

    def velocity_change1(self, p ,ux, uy):# a function that changes the velocity of a given particle to the target velocity
        self.array[p].vx = ux
        self.array[p].vy = uy
