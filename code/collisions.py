import numpy as np
import math 
import random
from itertools import combinations
#not sure entirely how to do this without particle ball class - it will be different to the final class, so kept contained in this file 
'''
generates a load of 2D particles that move around a 2D box, and sometimes smack each other.
a lot of credit to:
https://scipython.com/blog/two-dimensional-collisions/

few other assumptions that will built in:
all of the particles have the same density - of 1 - and so mass = volume 
collisions are all perfectly elastic - momentum and kinetic energy conserved
these govern the equations of motion used to handle all the collisions between particles
'''
class particle:
    '''
    set up the particles that are used in the simulation
    '''
    
    def __init__(self, r = np.array([0,0], dtype = float), velocity = np.array([0,0], dtype = float), radius = 1, x_size =1, y_size=1):
        self.velocity = velocity
        self.r = r 
        self.radius = radius
        self.x_size = x_size
        self.y_size = y_size
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
        '''
        make sure the particles bounce off the walls 
        little worried about corners! 

        '''
        x,y = self.r[0], self.r[1]
        vx, vy = self.velocity[0], self.velocity[1]
        
        if not (self.radius < x < (self.x_size - self.radius)):
            vx = -vx # this makes me a little uncomfortable, probably a cleaner way of doing this 
        if not (self.radius < y < (self.y_size - self.radius)):
            vy = -vy

class sim:
    def __init__(self, x_size = 1, y_size = 1, number_of_particles = 3 , radii = [2,3,4]):
        self.x_size = x_size
        self.y_size = y_size

        self.get_particles(number_of_particles, radii)


    def get_particles(self, number, radii):
        '''
        'spawn' all the particles: number of particles and radii must be defined 
        radii can either be a number, or a list of numbers that is right length - every particle needs a radii, and no extra! 

        '''

        '''
        make sure the radius is in the form wanted
        '''

        try: #check to see if radii is an array or a single number 
            radii.shape()
            assert number == len(radii) #throws asserterror if the list isn't the right size
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
                new = particle(r, v, radii[i], self.x_size, self.y_size)
                for collider in self.particles: #check that it doesnt spawn inside a different particle:
                    if collider.overlap(new):
                        break
                else:
                     self.particles.append(new)
                     break


    def collisions(self): 
        '''
        handles collsions between two particles - this is where the code diverts more from the example, so may be prone to breaking...

        it was very prone to breaking so followed the example better! 

        '''
        
        
        def calculate_velocities(particle1,particle2):
            '''
            calculate the velocities after the collision 
            '''
            mass1, mass2 = particle1.radius ** 2, particle2.radius** 2 #assuming uniform density etc - mass is just the volume - or area in this case - pi not included for simplicity
            totalMass = mass1 + mass2

            pos1, pos2 = particle1.r, particle2.r
            distance = np.linalg.norm(pos1 - pos2)**2 

            v_before_1 = particle1.velocity
            v_before_2 = particle2.velocity
                
            v_after_1 = v_before_1 - (2*mass2 / totalMass) * (np.dot(v_before_1-v_before_2, pos1- pos2) / distance) * (pos1- pos2)
            v_after_2 = v_before_2 - (2*mass1 / totalMass) * (np.dot(v_before_2-v_before_1, pos2-pos1) / distance) * (pos2 - pos1)
                
            particle1.velocity = v_after_1
            particle2.velocity = v_after_2
                    
        pairs = combinations(range(self.number),2) #need to check all possible particles
        for i,j in pairs:
            if self.particles[i].overlap(self.particles[j]): #check if they overlap
                calculate_velocities(self.particles[i], self.particles[j]) #if they do overlap, then calculate the change in velocity


