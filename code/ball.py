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
        self.momentum =  velocity / mass


    def update(self, dt):
        '''
        updates the position of the ball after a time dt
        '''
        self.position += self.velocity * dt
        #print('ball velocity was updated to {}'.format(self.velocity))