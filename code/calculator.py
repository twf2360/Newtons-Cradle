import math
import numpy as np 
from ball import ball
import matplotlib.pyplot as plt 
import copy
import matplotlib.animation as animation
from itertools import combinations
'''
I realised that the previous version, using the ODE solver, probably wouldn't be all the applicable moving forward
Trying a forces method instead to model the pendulum motion.

This will be much easier to combine with the collisions 

credit to: https://www.wired.com/2016/10/modeling-pendulum-harder-think/
'''
g_scalar = -9.8
g_vector = np.array([0,-9.81])
data = []
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
        for i in np.arange(number):
            spawnedBall = ball(position= np.array(positions[i], dtype = float),velocity= np.array(velocities[i], dtype = float), radius= np.array(radii[i], dtype = float), mass = masses[i], anchor= anchors[i])
            self.ball_list.append(spawnedBall)
        return self.ball_list

    
    def calculate(self):
        '''
        calculate the movement of the ball 
        '''
        for i in np.arange(self.iterations):
            for ball in self.ball_list: 
                pairs = combinations(range(self.number), 2)
                for i,j in pairs:
                    if self.ball_list[i].overlap(self.ball_list[j]):
                        print('There was a collsison')
                        ball1, ball2 = self.ball_list[i], self.ball_list[j]
                        totalMass = ball1.mass + ball2.mass

                        pos1, pos2 = ball1.position, ball2.position
                        distance = np.linalg.norm(pos1 - pos2)**2

                        v1_before = ball1.velocity
                        v2_before = ball2.velocity

                        v1_after = v1_before - (2*ball1.mass / totalMass) (np.dot(v1_before-v2_before, pos1- pos2) / distance) * (pos1- pos2)
                        v2_after = v2_before - (2*ball2.mass / totalMass) (np.dot(v2_before-v1_before, pos2- pos1) / distance) * (pos2 - pos1)

                        ball1.velocity = v1_after
                        ball2.velocity = v2_after

                    
                print('no collision, current position ={}'.format(ball.position))
                magAcceleration = (np.linalg.norm(ball.velocity)**2)/ball.length #calculate magnitude of  centripetal acceleration

                angPos = math.atan((ball.position[0] - ball.anchor[0])/((ball.position[1] - ball.anchor[1]))) #angle of the ball compared to the anchor

                stringTension_scalar = ((ball.mass*g_scalar*math.cos(angPos)) + ball.mass*magAcceleration) #calculate magnitude of string tension
                stringTension_vector = stringTension_scalar * (np.array((ball.position-ball.anchor)/ball.length)) #acts along the direction of the string towards the centre

                netForce = ball.mass*g_vector + stringTension_vector

                ball.velocity += (netForce*self.timestep/ball.mass)
                ball.update(self.timestep)
                

                time = i * self.timestep
                data_to_save = [time, copy.deepcopy(ball.position), copy.deepcopy(ball.velocity)]
                data.append(data_to_save)
                
               


testing = calculator(0.01, 1000)
testing.get_balls(number =1, positions= [[0,-1]], velocities= [[0.1,0]], radii= [1], masses= [1], anchors= [[0,0]])
testing.calculate()


time_list = []
position_list = []
for i in data:
    time_list.append(i[0])
    position_list.append(i[1])


'''
plot x against time to check the expected pattern of motion
'''

fig, ax = plt.subplots()

fig.suptitle('x position against time')

ax.plot(time_list, np.transpose(position_list)[0])
ax.set(xlabel = 'time', ylabel = 'x position of ball')
plt.show()


