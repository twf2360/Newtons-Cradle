import math
import numpy as np 
from ball import ball
import matplotlib.pyplot as plt 
'''
I realised that the previous version, using the ODE solver, probably wouldn't be all the applicable moving forward
Trying a forces method instead to model the pendulum motion.

This will be much easier to combine with the collisions 

credit to: https://www.wired.com/2016/10/modeling-pendulum-harder-think/
'''
g_scalar = 9.8
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
                magAcceleration = (ball.velocity**2)/ball.length #calculate magnitude of  centripetal acceleration 
                angPos = math.atan((ball.position[0]- ball.anchor[0])/(ball.position[1] - ball.anchor[1])) #angle of the ball compared to the anchor
                stringTension = ((ball.mass*g_vector*math.cos(angPos)) + ball.mass*magAcceleration) * ball.length
                netForce = ball.mass*g_vector + stringTension
                ball.momentum += netForce*self.timestep
                ball.velocity = ball.momentum/ball.mass
                ball.update(self.timestep)
                print('ball updated, position = {}'.format(ball.position))

                time = i * self.timestep
                data_to_save = [time, ball.position, ball.velocity]
                data.append(data_to_save)


testing = calculator(0.1, 10)
testing.get_balls(1,[[0,-1]], [[1,0]], [[1]],[[1]],[[0,0]])
testing.calculate()

fig, ax = plt.subplots()
fig.suptitle('First Plot Test')

ax.plot(data[0], data[1])
ax.set()
