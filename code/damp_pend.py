import numpy as np
import math
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation
'''
Simple pendulum motion described by: d^2/dt^2(theta) + g/l * sin(theta) = 0

split into two, first orders, let theta = phi_1, d/dt(theta) = phi_2
this also splits the pendulum into a position and a velocity component

motion described by d/dt(phi_1) = phi_2, and d/dt(phi_2) = -g/l * sin(phi_1)
'''

phi_start = [0,0.5] #starting position and velocity - THIS HAS BIG IMPACT ON THE OUTCOME 
'''
definitions - experiment with changing these 
'''

g = 9.81
mass = 4
length = 3
dt = 0.05 
time_points = np.arange(0,10,dt) #this was changed so now the timestep between points was availible in an easier way
damping_constant = 2

'''
get the matrix(arrays) of the first order ODEs so that odeint can solve it
'''

def dphi_12_dt(phi_start, time_points, g, mass, damping_constant, legnth): #error thrown up that it only takes 4 positional arguments but 5 were given if the timepoints function isn't here
    phi_1 = phi_start[0]
    phi_2 = phi_start[1]
    dphi_1_dt = phi_2
    dphi_2_dt = - (g/length)*math.sin(phi_1) - (damping_constant/mass)*phi_2
    
    dphi_12_dt = [dphi_1_dt, dphi_2_dt]
    #print(dphi_12_dt)
    return dphi_12_dt


motion = odeint(dphi_12_dt, phi_start, time_points, args=(g, mass, damping_constant, length))

disp = motion[:,0]
vel = motion[:,1]

fig, ax = plt.subplots(ncols=1, nrows=3)
fig.suptitle('Plotting the pendulum motion and velocity of a simple pendulum')

ax[0].plot(time_points, disp, color = 'b')
ax[0].set(title = 'Pendulum position', xlabel = 'time', ylabel = 'displacement')
ax[0].grid()


ax[1].plot(time_points, vel, color = 'r')
ax[1].set(title = 'Pendulum velocity', xlabel = 'time', ylabel = 'velocity')
ax[1].grid()


ax[2].plot(time_points, motion[:,0], color = 'm', label = 'Displacement')
ax[2].plot(time_points, motion[:,1], color = 'c', label = 'Velocity')
ax[2].set(title = 'Superposition of both components', xlabel = 'time', ylabel = '')
ax[2].legend(loc = 'best')
ax[2].grid()
plt.show()



'''
setting up the points in spatial co-ordinates so they can be animated
'''
x0 = 0
y0 = 0
positions_x = []
positions_y = []
for time in time_points:
    for point in disp:
        x = x0 + length*math.sin(math.pi + point)
        y = y0 + length*math.cos(math.pi + point)
        positions_x.append(x)
        positions_y.append(y)






fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(111, autoscale_on = False , xlim = (-5,5), ylim = (-5,5) ) #the 111 is what defines the subplot - nrows, ncolums, and index 

line, = ax.plot([],[], 'o-')
time_template = 'time ={}s'
time_text = ax.text(0.05,0.9, '', transform=ax.transAxes)

def ani_init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text

def animate(i):
    plot_x = [0,positions_x[i]]
    plot_y = [0,positions_y[i]]

    line.set_data(plot_x,plot_y)
    time_text.set_text(time_template.format(i*dt))
    return line, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(positions_x)),  interval=25, blit=True, init_func=ani_init)

plt.show()

