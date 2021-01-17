import math 
import numpy as np 

class ball:

    def __init__(self, length = 1, theta = math.pi/2, radius = 0.01, mass = 1):
        '''
        Initialisation function of the class - the length of the pendulum, angle between the pendulum and the vertical, radius, and mass
        '''
        self.length = length
        self.theta = theta
        self.radius = radius
        self.mass = mass
