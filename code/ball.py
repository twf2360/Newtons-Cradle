import math 
import numpy as np 

class ball:
    '''
    class used to define the balls involved in the simulation
    '''


    def __init__(self, position = np.array([0,0], dtype = float), velocity = np.array([0,0], dtype = float), radius = 1, length = 1, mass = 1, anchor = np.array([0,1])):
        '''
        Initialisation function of the class:
        position, radius, mass and velocity all describe the ball itself
        length describes the distance from the ball to the top, the length of the 'string'
        anchor describes were the 'string' is attached
        
        '''
        self.length = length
        self.position = position
        self.radius = radius
        self.mass = mass
        self.velocity = velocity


    def update(self, dt):
        '''
        updates the position of the ball after a time dt
        '''
        self.position += self.velocity * dt