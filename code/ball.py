import math 
import numpy as np 

class ball:
    '''
    class used to define the balls involved in the simulation
    '''


    def __init__(self, position = np.array([0,-1], dtype = float), velocity = np.array([0,0], dtype = float), radius = 1, mass = 1, anchor = np.array([0,0])):
        '''
        Initialisation function of the class:
        position, radius, mass and velocity all describe the ball itself
        anchor describes were the 'string' is attached, from which the length of the string is calculated 
        
        '''
        self.anchor = anchor
        self.position = position
        self.radius = radius
        self.mass = mass
        self.velocity = velocity
        

        self.length = np.linalg.norm(self.anchor - self.position)

    def euler_update(self, dv, dt):
        '''
        updates the position of the ball after a time dt, using the euler approximation
        '''
        self.position += self.velocity * dt
        self.velocity += dv
        #print('ball velocity was updated to {}'.format(self.velocity))

    def cromer_update(self, dv, dt):
        '''
        updates the position of the ball after a time dt, using the euler-cromer approximation
        '''
        self.velocity += dv
        self.position += self.velocity * dt

    def runge_kutta2(self, acceleration, dt):
        '''
        updates the position of the ball after a time dt, using the Runge-Kutta, second order approximation
        '''
        velocity_midpoint = self.velocity + 0.5 * dt * acceleration

        self.position += velocity_midpoint * dt
        self.velocity += dt * acceleration

    def overlap(self, incident):
        '''
        returns true if the the incident ball overlaps with self
        '''
        return np.hypot(*(self.position - incident.position)) <= self.radius + incident.radius

    def kinetic(self):
        '''returns kinetic energy of the ball'''
        ke = 0.5*self.mass*np.linalg.norm(self.velocity**2)
        return ke
    
    def potential(self):
        ''' returns potential energy of the ball ''' 
        lowest_point = self.anchor[1] - self.length
        h = self.position[1] - lowest_point
        mgh = self.mass * 9.81 * h
        return mgh
