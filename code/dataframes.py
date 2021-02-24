import math
import numpy as np 
from ball import ball
import matplotlib.pyplot as plt 
import copy
from itertools import combinations
import sys
import pandas as pd     
from calculator import calculator     

class results:

    def __init__(self, number, start_positions, start_velocities, radii, masses, anchors, iterations):
        self.number = number
        self.start_positions = start_positions
        self.start_velocities = start_velocities
        self.radii = radii
        self.masses = masses
        self.anchors = anchors
        self.iterations = iterations
        pd.set_option("display.max_rows", None, "display.max_columns", None)


     
    def use_calculator(self, timesteps, approximations,  densities):
        i = 0 
        for timestep in timesteps:
            for approximation in approximations:
                for fluid_density in densities:
                    calculating = calculator(timestep=timestep, iterations=self.iterations)
                    calculating.get_balls(number = self.number, positions = self.start_positions, velocities= self.start_velocities, radii = self.radii, masses= self.masses, anchors= self.anchors)
                    important_results = calculating.calculate(approximation, fluid_density)
                    if i == 0:
                        number_columns = len(important_results)
                        
                        columns = ['timestep', 'approximation', 'density']
                        for collision in range((number_columns - 1)): 
                            columns.append('Collision {}'.format(collision + 1))
                        
                    
                        data = [important_results[0][0], important_results[0][1], important_results[0][2]]
                        for i in range(len(important_results)):
                            if i == 0: 
                                continue
                            data.append(important_results[i])

                        df = pd.DataFrame(data = [data], columns= columns)
                        

                    else:
                        number_columns = len(important_results)
                        
                        columns = ['timestep', 'approximation', 'density']
                        for collision in range((number_columns - 1)): 
                            columns.append('Collision {}'.format(collision + 1))
                        
                    
                        data = [important_results[0][0], important_results[0][1], important_results[0][2]]
                        for i in range(len(important_results)):
                            if i == 0: 
                                continue
                            data.append(important_results[i])

                        df2 = pd.DataFrame(data = [data], columns= columns)
                        df.append(df2, ignore_index = True)
                        

                    i += 1
        print(df)


iterations = 60000
number = 2
startPositions = [[-1.2,0], [0,-1]]
startVelocities =[[0,0],[0,0]]
Radii = [0.1,0.1]
masses = [2,2]
anchors = [[-0.2,0],[0,0]]

testing = results(number, startPositions, startVelocities, Radii, masses, anchors, iterations)

timesteps = [0.00005]
approximations = ['cromer', 'rk2']
densities = [0]

testing.use_calculator(timesteps, approximations, densities)

'''

timestep = 0.00005
iterations = 60000
number = 3
startPositions = [[-1.2,0], [0,-1], [0.2, -1]]
startVelocities =[[0,0],[0,0], [0,0]]
Radii = [0.1,0.1, 0.1]
masses = [1,1,1]
anchors = [[-0.2,0],[0,0],[0.2,0]]
approximation = 'rk2'
density = '1.225' #density of the fluid through which the ball is travelling - SET TO 0 TO MODEL FOR NO RESISTANCE

testing = calculator(timestep, iterations)

testing.get_balls(number, startPositions,startVelocities,Radii,masses,anchors)
testing.calculate(approximation, density)

np.save('data_testing.npy', data, allow_pickle = True)
'''
'''

timestep = 0.00001
iterations = 500000
number = 2
startPositions = [[-1.2,0], [0,-1]]
startVelocities =[[0,0],[0,0]]
Radii = [0.1,0.1]
masses = [2,2]
anchors = [[-0.2,0],[0,0]]
air = 'on'
approximation = 'cromer'
testing = calculator(timestep, iterations, air)

testing.get_balls(number, startPositions,startVelocities,Radii,masses,anchors)
testing.calculate(approximation)

np.save('data_testing.npy', data, allow_pickle = True)
'''