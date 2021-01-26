import numpy as np
import math 
import random
#not sure entirely how to do this without particle ball class - it will be different to the final class, so kept contained in this file 
'''
generates a load of particles that move around a box.
a lot of credit to:
https://scipython.com/blog/two-dimensional-collisions/

few other assumptions that will built in:
all of the particles have the same density - of 1 - and so mass = volume 
'''
class particle:
    '''
    set up the particles that are used in the simulation
    '''
    
    def __init__(self, r = np.array([0,0], dtype = float), velocity = np.array([0,0], dtype = float), radius = 1):
        self.velocity = velocity
        self.r = r 
        self.radius = radius
    
    def overlap(self, incident):
        '''
        returns true if incident particle overlaps with self particle
        '''
        return np.hypot(*(self.r - incident.r)) < self.radius - incident.radius

    def update(self, dt):
        '''
        updates the position of the particle after a time dt
        '''
        self.r += self.velocity * dt


class sim:
    def __init__(self, x_size, y_size, number_of_particles, radii):
        self.x_size = x_size
        self.y_size = y_size

    def get_particles(self, number, radii):

        '''
        make sure the radius is in the form wanted
        '''

        try: #check to see if radii is an array or a single number 
            radii.shape()
            assert number == len(radii)
        except TypeError: #if it's a single number, make into a list of the same number 
            def radius_list_generator(number, radii):
                for i in range(number):
                    yield radii
            
                radii = radius_list_generator(number, radii) 

        '''
        get the given number of particles with the given radius!
        '''
        self.particles = []
        self.number = number

        for i in enumerate(radii):
            #find a start position
            while True:
                r = [self.x_size * random.random(), self.y_size * random.random()] # generate a random starting point within the x and y size of the box
                v = [random.random(), random.random()] #generate a random starting velocity 
                new = particle(r, v, radii[i])
                for collider in self.particles: #check that it doesnt spawn inside a different particle:
                    if collider.overlap(new):
                        break
                else:
                     self.particles.append(new)
                     break



