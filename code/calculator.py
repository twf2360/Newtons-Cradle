import math
import numpy as np 
from ball import ball
import matplotlib.pyplot as plt 
import copy
import matplotlib.animation as animation
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
                #print('velocity at the start = {}'.format(ball.velocity))
                print(ball.mass)
                magAcceleration = (np.linalg.norm(ball.velocity)**2)/ball.length #calculate magnitude of  centripetal acceleration

                angPos = math.atan((ball.position[0] - ball.anchor[0])/((ball.position[1] - ball.anchor[1]))) #angle of the ball compared to the anchor
                #print(angPos)
                stringTension_scalar = ((ball.mass*g_scalar*math.cos(angPos)) + ball.mass*magAcceleration) 
                stringTension_vector = stringTension_scalar * (np.array((ball.position-ball.anchor)/ball.length))

                netForce = ball.mass*g_vector + stringTension_vector
                #print(netForce)
                ball.velocity += (netForce*self.timestep/ball.mass)
                ball.update(self.timestep)
                

                time = i * self.timestep
                data_to_save = [time, copy.deepcopy(ball.position), copy.deepcopy(ball.velocity)]
                data.append(data_to_save)
                #print('velocity at the end = {}'.format(ball.velocity))

                #print('ball updated, position = {}, time = {}'.format(ball.position, time))


testing = calculator(0.01, 1000)
testing.get_balls(1,[[0,-1]], [[0.1,0]], [1],[1],[[0,0]])
testing.calculate()

time_list = []
position_list = []
for i in data:
    #print(i)
    time_list.append(i[0])
    position_list.append(i[1])


fig, ax = plt.subplots()

fig.suptitle('First Plot Test')

ax.plot(time_list, np.transpose(position_list)[0])
ax.set(xlabel = 'time', ylabel = 'x position of ball')
plt.show()



'''
there appears to be a singularity in the code so i want to animate it to see if i can see what happens.
'''
'''
fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on = False) #the 111 is what defines the subplot - nrows, ncolums, and index 

line, = ax.plot([],[], 'o-')
time_template = 'time ={}s'
time_text = ax.text(0.05,0.9, '', transform=ax.transAxes)
def ani_init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text
positions_x = np.transpose(position_list)[0]
positions_y = np.transpose(position_list)[1]
def animate(i):
    plot_x = [0,positions_x[i]]
    plot_y = [0,positions_y[i]]

    line.set_data(plot_x,plot_y)
    time_text.set_text(time_template.format(i*0.01))
    return line, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(positions_x)),  interval=25, blit=True, init_func=ani_init)

plt.show()
'''