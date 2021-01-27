import numpy as np
import math 
import random
from itertools import combinations
from matplotlib.patches import Circle
from matplotlib import animation
import matplotlib.pyplot as plt
#not sure entirely how to do this without particle ball class - it will be different to the final class, so kept contained in this file 
'''
generates a load of 2D particles that move around a 2D box, and sometimes smack each other.

a lot of credit to:
https://scipython.com/blog/two-dimensional-collisions/

few assumptions that will built in:
all of the particles have the same density - of 1 - and so mass = volume, or area in this case 
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
        return np.hypot(*(self.r - incident.r)) < self.radius + incident.radius

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
            if self.radius > x:
                self.r[0] = self.radius
            if  x > self.x_size - self.radius:
                self.r[0] = self.x_size - self.radius

        if not (self.radius < y < (self.y_size - self.radius)):
            vy = -vy
            if self.radius > y:
                self.r[1] = self.radius
            if  x > self.y_size - self.radius:
                self.r[1] = self.y_size - self.radius
        self.velocity = np.array([vx,vy])

    def draw(self, ax):
        circle = Circle(xy=self.r, radius=self.radius, **{'edgecolor': 'b', 'fill': False})
        ax.add_patch(circle)
        return circle

class sim:
    def __init__(self, x_size = 1, y_size = 1, number_of_particles = 3 , radii = [2,3,4]):
        self.x_size = x_size
        self.y_size = y_size


        self.get_particles(number_of_particles, radii)


    def get_particles(self, number, radius):
        '''
        'spawn' all the particles: number of particles and radii must be defined 
        radii can either be a number, or a list of numbers that is right length - every particle needs a radii, and no extra! 

        '''

        '''
        make sure the radius is in the form wanted, a list with a length of number of particles
        '''
        radius_list = []
        try: #check to see if radii is an array or a single number 
            radius.shape
            assert number == len(radius) #throws asserterror if the list isn't the right size
            radius_list = radius
        except AttributeError: #if it's a single number, make into a list of the same number 
            #print('oops')
            
            def make_radius_list(number):
                for i in range(number):
                    radius_list.append(radius)
            
            make_radius_list(number) 


        '''
        get the given number of particles with the given radius!
        '''
        self.particles = []
        self.number = number
        self.timestamps = []

        for i in range(len(radius_list)):
            #find a start position
            while True:
                r = np.array([self.x_size * random.random(), self.y_size * random.random()]) # generate a random starting point within the x and y size of the box
                v = np.array([self.x_size * random.random()/2 ,self.y_size * random.random()/2]) #generate a random starting velocity that scales with box size
                new = particle(r, v, radius_list[i], self.x_size, self.y_size)
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
                print('there was a collison!') #just for testing


    def update(self, repeats, dt):
        for repeat in np.arange(repeats):
            #print(repeat)
            for counter, particle in enumerate(self.particles):
                #print(counter)
                particle.update(dt)
                self.collisions()
                self.circles[counter].center = particle.r
            
            return self.circles
                #time = repeat * counter
                #self.timestamps.append(time)
                #print('particle number {}.'.format(counter), particle.velocity)
        #print('These are the timestamps',self.timestamps)

    def init_animation(self):
        '''
        Initialise the animation - setup all the circles
        '''
        self.circles = []
        for particle in self.particles:
            self.circles.append(particle.draw(self.ax))
        return self.circles
    
    def animate_func(self, i):
        '''
        function passed into matplotlib funcanimation. 
        '''
        self.update(10, 0.01) #change this to edit the repeats and tme 
        return self.circles

    def do_animation(self, save=False):
        '''
        actually do the animation, if save = True then saves the animation to disk
        '''

        fig, self.ax = plt.subplots()
        for s in ['top','bottom','left','right']:
            self.ax.spines[s].set_linewidth(2)
        self.ax.set_aspect('equal', 'box')
        self.ax.set_xlim(0, self.x_size)
        self.ax.set_ylim(0, self.y_size)
        self.ax.xaxis.set_ticks([])
        self.ax.yaxis.set_ticks([])
        anim = animation.FuncAnimation(fig, self.animate_func, init_func=self.init_animation,
                               frames=800, interval=2, blit=True)
        if save:
            anim.save('collision.mp4')
        else:
            plt.show()


test = sim(5,5,5,0.5)
test.do_animation(False)
