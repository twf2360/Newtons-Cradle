import numpy as np
import math 



class Ball:
    '''
    A class used to define each of the balls in the newtons cradle

    '''
    def __init__(self, x, y, velX, velY, accelX, accelY, radius, mass): #could be later expanded to include how each ball is displayed?
        self.position = np.array([x,y], dtype=float)
        self.velocity = np.array([velX,velX], dtype=float)
        self.acceleration = np.array([accelX, accelY], dtype=float)
        self.radius = radius
        self.mass = mass
    
    def __repr__(self):
        print('This is a currently unwritten representation functuion.')

    def kineticEnergy(self):
        '''
        Used to return the kinetic energy of a ball so that the conservation of energy can be checked 
        '''
        v = np.linalg.norm(self.velocity)
        m = self.mass 
        return 0.5*m*v**2
