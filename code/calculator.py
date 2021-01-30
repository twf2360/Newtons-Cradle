import math
import numpy as np 
from ball import ball
import matplotlib.pyplot as plt 
import copy
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
                print('velocity at the start = {}'.format(ball.velocity))
                magAcceleration = (ball.velocity**2)/ball.length #calculate magnitude of  centripetal acceleration 
                angPos = math.atan((ball.position[0]- ball.anchor[0])/(-(ball.position[1] - ball.anchor[1]))) #angle of the ball compared to the anchor
                #print(angPos)
                stringTension = ((ball.mass*g_vector*math.cos(angPos)) + ball.mass*magAcceleration) * ball.length
                #print(stringTension)
                netForce = ball.mass*g_vector + stringTension
                #print(netForce)
                ball.velocity += (netForce*self.timestep/ball.mass)
                ball.update(self.timestep)
                

                time = i * self.timestep
                data_to_save = [time, copy.deepcopy(ball.position), copy.deepcopy(ball.velocity)]
                data.append(data_to_save)
                print('velocity at the end = {}'.format(ball.velocity))

                print('ball updated, position = {}, time = {}'.format(ball.position, time))


testing = calculator(0.1, 10)
testing.get_balls(1,[[0,-1]], [[1,0]], [[1]],[[1]],[[0,0]])
testing.calculate()

time_list = []
position_list = []
for i in data:
    #print(i)
    time_list.append(i[0])
    position_list.append(i[1])

print(data)

fig, ax = plt.subplots()
fig.suptitle('First Plot Test')

ax.plot(time_list, np.transpose(position_list)[0])
ax.set(xlabel = 'time', ylabel = 'x position of ball')
plt.show()
