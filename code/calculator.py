import math
import numpy as np 
from ball import ball
import matplotlib.pyplot as plt 
import copy
import matplotlib.animation as animation
from itertools import combinations
import sys
import pandas as pd
from time import time
g_scalar = 9.81
g_vector = np.array([0,-9.81])
data = []
np.seterr(over='raise')
class calculator:
    '''

    A class used to calculate the motion of the ball, save the movement of the balls to disk so that they can later be read in
    takes the number of iterations, and the timesteps between iterations as arguments
    '''

    def __init__(self, timestep, iterations):
        '''
        initalistation function of the class 
        timestep = the difference in time between the updates of the balls position
        iterations = the number of timesteps ran through
        '''
        self.timestep = timestep
        self.iterations = iterations 
        self.ball_list = []
        
        
       
    


    def get_balls(self, number, positions, velocities, radii, masses, anchors):
        self.number = number
        
        for i in np.arange(self.number):
            spawnedBall = ball(position= np.array(positions[i], dtype = float),velocity= np.array(velocities[i], dtype = float), radius= np.array(radii[i], dtype = float), mass = masses[i], anchor= anchors[i])
            self.ball_list.append(spawnedBall)
        
        
        return self.ball_list



    
    def fluid_resistance(self,ball, density):
        ''' calculates the force of fluid resistance on the ball, density of the fluid must be defined'''
        fluid_density = density #1.225
        drag_coefficient = 0.5 #just googled the drag co-efficent of a sphere
        cross_sec_area = math.pi * ball.radius**2
        if not np.any(ball.velocity):
            return [0,0]
        velocity = ball.velocity
        speed = np.linalg.norm(velocity)
        vel_direction = velocity / speed

        force_scalar = 0.5 * fluid_density * speed**2 *drag_coefficient * cross_sec_area
        force_vector = (-force_scalar) * vel_direction # - as it always acts against the direction of the velocity
        return force_vector

    def collision(self, ball1, ball2):
        '''
        calculate the change in velocities if there's a collision
        '''
        totalMass = ball1.mass + ball2.mass

        pos1, pos2 = ball1.position, ball2.position
        distance = np.linalg.norm(pos1 - pos2)**2
        v1_before = ball1.velocity
        v2_before = ball2.velocity

        v1_after = v1_before - (2*ball1.mass / totalMass) * (np.dot((v1_before-v2_before), (pos1- pos2)) / distance) * (pos1 - pos2)
        v2_after = v2_before - (2*ball2.mass / totalMass) * (np.dot((v2_before-v1_before) ,(pos2- pos1)) / distance) * (pos2 - pos1)

        ''' this is where things arguably get very dodgy''' 
        ''' there were some major issues with the y direction acting very weirdly during collisions, so now that has been artificially set to 0'''
        ''' this can be thought of as the strings holding the balls having an infinitely large spring constant '''

        v1_x = v1_after[0]
        v2_x = v2_after[0] 

        v1_y = 0
        v2_y = 0

        ball1.velocity = np.array([v1_x, v1_y], dtype= float)
        ball2.velocity = np.array([v2_x, v2_y], dtype = float)

        #print(' \n ball 1 velocity after collision = {}, ball 2 velocity afer collision = {} \nball 1 position = {}, ball 2 position = {}  \n'.format(ball1.velocity, ball2.velocity, ball1.position, ball2.position))
        #print(' v1 before = {}, v1 after = {} \n v2 before = {}, v2 after = {} \n r1 before = {}, r1 after = {} \n  r2 before = {}, r2 after = {} \n \n'.format(v1_before, v1_after, v2_before, v2_after, pos1, ball1.position, pos2, ball2.position))

    def stringtension(self,ball):
        ''' calculates the force on the ball due to the string tension '''
        magAcceleration = (np.linalg.norm(ball.velocity)**2)/ball.length #calculate magnitude of  centripetal acceleration

        delta_x = np.abs((ball.position[0] - ball.anchor[0]))
        delta_y = np.abs((ball.position[1] - ball.anchor[1]))

        to_anchor = ball.anchor - ball.position  
        normalisation = np.linalg.norm(to_anchor)
        #print(to_anchor)
        
        if (not np.isnan(delta_x)) and (delta_x != 0) and (not np.isnan(delta_y)) and (delta_y != 0):
            ''' this to avoid the possibility of any divide by 0 errors if the ball is at 0 or 90 degrees to the vertical '''
            #print(ball.position[1] - ball.anchor[1])
            angPos = math.atan(delta_x/delta_y) #angle of the ball compared to the anchor
            #print(angPos)
        
        elif (np.isnan(delta_y)) or (delta_y == 0):
            angPos = (math.pi/2)
            #print('dy = {}'.format(delta_y))
            
        else:
            angPos = 0
            #print('dx = {}'.format(delta_x))

        stringTension_scalar = ((ball.mass*g_scalar*math.cos(angPos)) + ball.mass*magAcceleration) #calculate magnitude of string tension
        stringTension_vector = stringTension_scalar * (np.array((to_anchor)/normalisation))

        return stringTension_vector

    def calculate_acceleration(self, ball, density):
        '''
        calculate the acceleration of the ball if there is no collision
        '''
        tension_force = self.stringtension(ball)

        air_resistance_force = self.fluid_resistance(ball, density) 


        netForce = ball.mass*g_vector + tension_force + air_resistance_force
        acceleration = (netForce/ball.mass)
        return acceleration
        


    def calculate(self, approximation, density):
        '''
        calculate the movement of the ball, with a chosen approximation
        '''
        important_info = []
        fluid_density = density
        important_info.append([self.timestep ,approximation, fluid_density])
        if not approximation.lower() in ('cromer', 'euler', 'rk2'):
            print('approximation not recognised, must be cromer, euler, or RK')
            sys.exit()
        for i in np.arange(self.iterations):
            for ball in self.ball_list: 
                while True: #probably a much cleaner way to do this somehow 
                    pairs = combinations(range(self.number), 2)
                    for x,y in pairs:
                        if self.ball_list[x].overlap(self.ball_list[y]):
                            if self.ball_list[x].velocity or self.ball_list[y].velocity == [0,0]:
                                self.collision(self.ball_list[x], self.ball_list[y])
                                continue
                            print('There was a collsison at iteration {}'.format(i))
                            self.collision(self.ball_list[x], self.ball_list[y])
                            important_info.append('iteration {}, time {}s'.format(i, self.timestep*i )) #add the balls that collide? 
                            #important_info.append([i, {'incedent ball velocity after':self.ball_list[x].velocity}, {'target ball velocity after': self.ball_list[y].velocity}])
                            break
                    acceleration = self.calculate_acceleration(ball, fluid_density)
                    delta_v = acceleration * self.timestep  # calculate the change in velocity over the timestep
                    
                    break   
                if approximation.lower() == 'euler':
                    ball.euler_update(delta_v, self.timestep)
                
                if approximation.lower() == 'cromer':
                    ball.cromer_update(delta_v, self.timestep) 
                
                if approximation.lower() == 'rk2':
                    ball.runge_kutta2(acceleration, self.timestep)
            time = i * self.timestep
            data_to_save = [time, copy.deepcopy(self.ball_list)]
            data.append(data_to_save)

        return important_info

    def time_to_run(self, approximation, density):
            start_time = time()
            self.calculate(approximation, density)
            time_to_run = start_time - time()
            return time_to_run



        
