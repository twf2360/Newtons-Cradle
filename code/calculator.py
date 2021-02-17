import math
import numpy as np 
from ball import ball
import matplotlib.pyplot as plt 
import copy
import matplotlib.animation as animation
from itertools import combinations
import sys
'''
I realised that the previous version, using the ODE solver, probably wouldn't be all the applicable moving forward
Trying a forces method instead to model the pendulum motion.

This will be much easier to combine with the collisions 

credit to: https://www.wired.com/2016/10/modeling-pendulum-harder-think/
'''
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



    def calculate(self):
        '''
        calculate the movement of the ball 
        '''
        def air_resistance(ball):
            ''' calculates the force of air resistance on the ball'''
            air_density = 1.225
            drag_coefficient = 0.5 #just googled the drag co-efficent of a sphere
            cross_sec_area = math.pi * ball.radius**2
            if not np.any(ball.velocity):
                return [0,0]
            velocity = ball.velocity
            speed = np.linalg.norm(velocity)
            vel_direction = velocity / speed

            force_scalar = 0.5 * air_density * speed**2 *drag_coefficient * cross_sec_area
            force_vector = (-force_scalar) * vel_direction # - as it always acts against the direction of the velocity
            return force_vector

        def collision(ball1, ball2):
            '''
            calculate the change in velocities if there's a collision
            '''
            totalMass = ball1.mass + ball2.mass

            pos1, pos2 = ball1.position, ball2.position
            distance = np.linalg.norm(pos1 - pos2)**2
            v1_before = ball1.velocity
            v2_before = ball2.velocity

            v1_after = v1_before - (2*ball1.mass / totalMass) * (np.dot(v1_before-v2_before, pos1- pos2) / distance) * (pos1 - pos2)
            v2_after = v2_before - (2*ball2.mass / totalMass) * (np.dot(v2_before-v1_before, pos2- pos1) / distance) * (pos2 - pos1)

            ball1.velocity = v1_after
            ball2.velocity = v2_after

            #print('ball 1 velocity after collision = {}, ball 2 velocity afer collision = {} \nball 1 position = {}, ball 2 position = {}'.format(ball1.velocity, ball2.velocity, ball1.position, ball2.position))


        def stringtension(ball):
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

        def movement(ball):
            '''
            calculate the change in velocity with no collision
            '''
            tension_force = stringtension(ball)
            air_resistance_force = air_resistance(ball) 

            netForce = ball.mass*g_vector + tension_force + air_resistance_force
            acceleration = (netForce/ball.mass)
            velocity_change = acceleration * self.timestep
            ball.velocity += velocity_change




        for i in np.arange(self.iterations):
            for ball in self.ball_list: 
                while True: #probably a much cleaner way to do this somehow 
                    pairs = combinations(range(self.number), 2)
                    for x,y in pairs:
                        if self.ball_list[x].overlap(self.ball_list[y]):
                            #print('There was a collsison at iteration {}'.format(i))
                            collision(self.ball_list[x], self.ball_list[y])
                            break
                    #print(i)
                    movement(ball)
                    #print(ball.position)
                    break   
                ball.update(self.timestep)
                
            time = i * self.timestep
 
            data_to_save = [time, copy.deepcopy(self.ball_list)]
            data.append(data_to_save)
                
               


timestep = 0.0005
iterations = 10000
number = 2
startPositions = [[-2,0], [0,-1]]
startVelocities =[[0,0],[0,0]]
Radii = [0.5,0.5]
masses = [1,1]
anchors = [[-1,0],[0,0]]
testing = calculator(timestep, iterations)

testing.get_balls(number, startPositions,startVelocities,Radii,masses,anchors)
testing.calculate()

np.save('data_testing.npy', data, allow_pickle = True)

