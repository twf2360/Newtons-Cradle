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
                magAcceleration = (np.linalg.norm(ball.velocity)**2)/ball.length #calculate magnitude of  centripetal acceleration

                angPos = math.atan((ball.position[0] - ball.anchor[0])/((ball.position[1] - ball.anchor[1]))) #angle of the ball compared to the anchor

                stringTension_scalar = ((ball.mass*g_scalar*math.cos(angPos)) + ball.mass*magAcceleration) 
                stringTension_vector = stringTension_scalar * (np.array((ball.position-ball.anchor)/ball.length))

                netForce = ball.mass*g_vector + stringTension_vector

                ball.velocity += (netForce*self.timestep/ball.mass)
                ball.update(self.timestep)
                

                time = i * self.timestep
                data_to_save = [time, copy.deepcopy(ball.position), copy.deepcopy(ball.velocity)]
                data.append(data_to_save)
                
               


testing = calculator(0.01, 1000)
testing.get_balls(number =1, positions= [[0,-1]], velocities= [[0.1,0]], radii= [1], masses= [1], anchors= [[0,0]])
testing.calculate()



'''
all of the below are just used for plotting - these will eventually be put into their own class, allowing stuff to be saved
in a dataframe etc. For now, The splurge
'''
'''
the below is just to get certain lists that can then be plotted later on
'''

time_list = []
position_list = []
for i in data:
    time_list.append(i[0])
    position_list.append(i[1])


'''
plot x against time to check the expected pattern of motion
'''
'''
fig, ax = plt.subplots()

fig.suptitle('x position against time')

ax.plot(time_list, np.transpose(position_list)[0])
ax.set(xlabel = 'time', ylabel = 'x position of ball')
plt.show()
'''

'''
animation! This needs some work due to the "zoom out" issue
'''
'''

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on = True) #the 111 is what defines the subplot - nrows, ncolums, and index 

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

'''
plot x and y position - not sure of this 
'''
'''

fig, ax = plt.subplots()

fig.suptitle('x-y position of ball')

ax.plot(np.transpose(position_list)[0], np.transpose(position_list)[1])
ax.set(xlabel = 'x position of ball', ylabel = 'y position of ball')
plt.show()
'''

'''
plot x and y against time on seperate graphs against time 
'''
fig, ax = plt.subplots(ncols= 2, nrows= 1)

ax[0].set(xlabel = 'time', ylabel = 'x position', title = 'x-position against time')
ax[0].plot(time_list, np.transpose(position_list)[0], color = 'm')

ax[1].set(xlabel = 'time', ylabel = 'y position', title = 'y-position against time')
ax[1].plot(time_list, np.transpose(position_list)[1], color = 'r')


plt.show()

