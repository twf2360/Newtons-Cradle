import numpy as np
import math
from scipy.integrate import odeint
import matplotlib.pyplot as plt
'''
Simple pendulum motion described by: d^2/dt^2(theta) + g/l * sin(theta) = 0

split into two, first orders, let theta = phi_1, d/dt(theta) = phi_2
this also splits the pendulum into a position and a velocity component

motion described by d/dt(phi_1) = phi_2, and d/dt(phi_2) = -g/l * sin(phi_1)
'''

phi_start = [0,3] #two arbitrary values, experiment the effect of changing these

'''
definitions - experiment with changing these 
'''

g = 9.81
mass = 1
length = 3
time_points = np.linspace(0,100,1000) 

'''
get the matrix(arrays) of the first order ODEs so that odeint can solve it
'''

def dphi_12_dt(phi_start, time_points, g, mass, legnth): #error thrown up that it only takes 4 positional arguments but 5 were given if the timepoints function isn't here
    phi_1 = phi_start[0]
    phi_2 = phi_start[1]
    dphi_1_dt = phi_2
    dphi_2_dt = - (g/length)*math.sin(phi_1)
    
    dphi_12_dt = [dphi_1_dt, dphi_2_dt]
    #print(dphi_12_dt)
    return dphi_12_dt


motion = odeint(dphi_12_dt, phi_start, time_points, args=(g,mass, length))
#print(motion)

fig, ax = plt.subplots(ncols=3, nrows=1)
fig.suptitle('Plotting the pendulum motion and velocity of a simple pendulum')

ax[0].plot(time_points, motion[:,0], color = 'm')
ax[0].set(title = 'Pendulum position', xlabel = 'time', ylabel = 'displacement')
ax[0].grid()


ax[1].plot(time_points, motion[:,1], color = 'c')
ax[1].set(title = 'Pendulum velocity', xlabel = 'time', ylabel = 'velocity')
ax[1].grid()


ax[2].plot(time_points, motion[:,0], color = 'm', label = 'Displacement')
ax[2].plot(time_points, motion[:,1], color = 'c', label = 'Velocity')
ax[2].set(title = 'Superposition of both components', xlabel = 'time', ylabel = '')
ax[2].legend(loc = 'best')
plt.show()

