import math
import numpy as np 
from ball import ball
import matplotlib.pyplot as plt 
import copy
from itertools import combinations
import sys
import pandas as pd     
from calculator import calculator    
import json
#import config.json


class results:

    def __init__(self, number, start_positions, start_velocities, radii, masses, anchors, iterations):
        self.number = number
        self.start_positions = start_positions
        self.start_velocities = start_velocities
        self.radii = radii
        self.masses = masses
        self.anchors = anchors
        self.iterations = iterations
        #pd.set_option("display.max_rows", None, "display.max_columns", None)


     
    def collision_df(self, timesteps, approximations,  densities):
        '''
        Calculates the movement of the newtons cradle that is defined by the initialisation function, and a given timestep, approximation, and fluid density
        In order to test multiple timesteps, approximations, and densities, these can be entered as an array
        A dataframe will be printed that shows the number of the collisions, and the time at which they took place, for each defined "system"

        '''
        i = 0 
        for timestep in timesteps:
            for approximation in approximations:
                for fluid_density in densities:
                    calculating = calculator(timestep=timestep, iterations=self.iterations)
                    calculating.get_balls(number = self.number, positions = self.start_positions, velocities= self.start_velocities, radii = self.radii, masses= self.masses, anchors= self.anchors)
                    collision_results = calculating.calculate(approximation, fluid_density)
                    if i == 0:
                        number_columns = len(collision_results)
                        
                        columns = ['timestep', 'approximation', 'density']
                        for collision in range((number_columns - 1)): 
                            columns.append('Collision {}'.format(collision + 1))
                        
                    
                        data = [collision_results[0][0], collision_results[0][1], collision_results[0][2]]
                        for x in range(len(collision_results)):
                            if x == 0: 
                                continue
                            data.append(collision_results[x])

                        df = pd.DataFrame(data = [data], columns= columns)
                        i = 1
                        continue
                        

                    
                    number_columns = len(collision_results)
                    
                    columns = ['timestep', 'approximation', 'density']
                    for collision in range((number_columns - 1)): 
                        columns.append('Collision {}'.format(collision + 1))
                    
                
                    data = [collision_results[0][0], collision_results[0][1], collision_results[0][2]]
                    for x in range(len(collision_results)):
                        if x == 0: 
                            continue
                        data.append(collision_results[x])
                    #print('we made it here!')
                    

                    df2 = pd.DataFrame(data = [data], columns= columns)
                    #print(df2)
                    df = df.append(df2, ignore_index = True)
                        

        df = df.fillna('No Collision')            
        print(df)

    def time_to_run_df(self, timesteps, approximations,  densities):
        '''
        Calculates the movement of the newtons cradle that is defined by the initialisation function, and a given timestep, approximation, and fluid density
        In order to test multiple timesteps, approximations, and densities, these can be entered as an array
        A dataframe will be printed that shows the time taken to run each version of the "system"
        '''
        i = 0 
        for timestep in timesteps:
            for approximation in approximations:
                for fluid_density in densities:
                    calculating = calculator(timestep=timestep, iterations=self.iterations)
                    calculating.get_balls(number = self.number, positions = self.start_positions, velocities= self.start_velocities, radii = self.radii, masses= self.masses, anchors= self.anchors)
                    time = calculating.time_to_run(approximation, fluid_density)[0]
                    if i == 0:
                        df = pd.DataFrame(data= [[timestep, approximation, fluid_density, time]] , columns=['Timestep', 'Approximation', 'Fluid Density', 'Time to run'])
                        i += 1
                        continue
                    df2 = pd.DataFrame(data = [[timestep, approximation, fluid_density, time]], columns=['Timestep', 'Approximation', 'Fluid Density', 'Time to run'])
                    df = df.append(df2, ignore_index = True)
        print(df)

with open(r"code\config.json") as configuration:
    config = json.load(configuration)
initialisation = config['initialisation']
system = config['system']

'''
testing = results(initialisation['number'], initialisation['StartPositions'], initialisation['StartVelocities'], initialisation['radii'], initialisation['masses'], initialisation['anchors'], initialisation['iterations'])
testing.time_to_run_df(system['timesteps'], system['approximations'], system['densities'] )
'''
#print(config['initialisation'])
#print(config['system'])
#testing = results(number, startPositions, startVelocities, Radii, masses, anchors, iterations)
#testing.collision_df(timesteps, approximations, densities)
#testing.time_to_run_df(timesteps, approximations, densities)