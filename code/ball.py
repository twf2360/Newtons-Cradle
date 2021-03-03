import math 
import numpy as np 

class ball:
    '''
    class used to define the balls involved in the simulation.
    This class is used by all of the other classes:
        - calculator.py uses the update functions (euler_update, cromer_update, and runge_kutta2) to update the positions and velocities of the balls based on the accelerations it calculated
        - calculator.py requires the position, velocity, mass, and anchor points of the balls to calculate the change in acceleration
        - calculator.py uses the overlap function to determine when a collision between balls has taken place

        - plotter.py uses the position attribute of the ball object to plot the balls position over time 
        - plotter.py uses the energy functions - kinetic and potential - to plot the energy of the system over time 

    '''


    def __init__(self, position = np.array([0,-1], dtype = float), velocity = np.array([0,0], dtype = float), radius = 1, mass = 1, anchor = np.array([0,0])):
        '''
        Initialisation function of the class:
        position, radius, mass and velocity attributes all describe the ball itself
        anchor attribute describe where the 'string' is attached, from which the length of the string is calculated 

        radius, mass, and anchor should not be changed at any point

        all of the inputs that can be entered as lists are turned into numpy arrays for easier manipulation
        
        '''
        self.anchor = np.array(anchor) 
        self.position = np.array(position)
        self.radius = radius
        self.mass = mass
        self.velocity = np.array(velocity)
        

        self.length = np.linalg.norm(self.anchor - self.position)

    def euler_update(self, dv, dt):
        '''
        updates the position of the ball after a time dt, using the euler approximation

        dt = the timestep between iterations used by the calculator 
        dv = the change in velocity that has been calculated using the calculator
        '''
        self.position += self.velocity * dt
        self.velocity += dv


    def cromer_update(self, dv, dt):
        '''
        updates the position of the ball after a time dt, using the euler-cromer approximation

        dt = the timestep between iterations used by the calculator 
        dv = the change in velocity that has been calculated using the calculator
        '''
        self.velocity += dv
        self.position += self.velocity * dt

    def runge_kutta2(self, acceleration, dt):
        '''
        updates the position of the ball after a time dt, using the Runge-Kutta, second order approximation

        dt = the timestep between iterations used by the calculator 
        acceleration = the acceleration at a given moment that has been calculated using the calculator
        '''
        velocity_midpoint = self.velocity + 0.5 * dt * acceleration

        self.position += velocity_midpoint * dt
        self.velocity += dt * acceleration

    def overlap(self, incident):
        '''
        input incident must also be a ball object 
        returns true if an incident ball overlaps with the current ball.
        '''
        return np.hypot(*(self.position - incident.position)) <= self.radius + incident.radius

    def kinetic(self):
        '''
        returns kinetic energy of the ball at a given moment 
        '''
        ke = 0.5*self.mass*np.linalg.norm(self.velocity**2)
        return ke
    
    def potential(self):
        ''' 
        returns potential energy of the ball at a given moment 
        
        Assumes constant acceleration due to gravity, and that the simulation is taking place on Earth's surface.
        '''
        lowest_point = self.anchor[1] - self.length
        h = self.position[1] - lowest_point
        mgh = self.mass * 9.81 * h
        return mgh
