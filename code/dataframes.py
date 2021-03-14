import math
import numpy as np 
from ball import ball
import matplotlib.pyplot as plt 
import copy
from itertools import combinations
import sys
import pandas as pd     
from calculator import calculator    
from plotter import plotter
import json


class results:
    '''
    This is a class that accesses functions from within the calculator class, and prints the results using pandas dataframes
    The calculator class is accessed multiple times, so that results can be compared

    The results class contains four class methods:
        - collision_df generates a dataframe for all of the collisions that take place for every possible configuration described in the config file 
        - time_to_run_df generates a dataframe for the time to run each configuration described in the config file
        - conservation_df generates a dataframe that investigates the conservation of energy of each system configuration

        - all_three_dfs generates all three of the previously defined functions. The reason these methods are combined is so that the calculator class does not have to perform
        repeat calculations - this dramatically shortens the time taken to generate the dataframes. Becuase of this, all_three_dfs is the class method that is called by main.py

        
    '''

    def __init__(self, number, start_positions, start_velocities, radii, masses, anchors, iterations):
        '''
        All of the paramaters needed by the calculator class have to be defined. 
        All of the parameters throughout the initialisation function are constant throughout all of the different tests - these paramaters are held as a control
        to compare the effect of changing all of the other parameters
        '''
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
        In order to test multiple timesteps, approximations, and densities, these must be entered as an array
        A dataframe will be printed that shows the number of the collisions, and the time at which they took place, for each defined "system"

        '''
        i = 0 #this is used as the initial creation of the dataframe requires slightly different inputs than appending all of the other rows, therefore after the initial creation, i is set to 1
        
        for timestep in timesteps: # loops over all of the different system configurations in order to run the simulation for every possible config
            for approximation in approximations:
                for fluid_density in densities:
                    
                    
                    calculating = calculator(timestep=timestep, iterations=self.iterations) # initialises the calculator class with the selected timestep
                    calculating.get_balls(number = self.number, positions = self.start_positions, velocities= self.start_velocities, radii = self.radii, masses= self.masses, anchors= self.anchors)  #set up the calculator with the correct conditions defined by the initialisation config
                    collision_results = calculating.calculate(approximation, fluid_density) #calculate the movement using the current approximation and density 
                    if i == 0: #if the dataframe has not yet been created
                        
                        number_columns = len(collision_results) #the number of additional columns (other than the system configuration) is the number of collisions plus the system config, which is the length of this list
                        
                        columns = ['timestep', 'approximation', 'density'] #the system config are the first three columns 
                        
                        for collision in range((number_columns - 1)): #the -1 is because the first term in the number_columns list is the config information, and doens't correspond to a collision
                            columns.append('Collision {}'.format(collision + 1)) #this adds an extra colummn for each collision
                        
                    
                        data = [collision_results[0][0], collision_results[0][1], collision_results[0][2]] #these three items are the timestep, approximation, and density config of the system respectively
                        #the data list represents a row of the data that is going to be added to the bottom of the overall dataframe
                        for x in range(len(collision_results)): 
                            if x == 0: # want to skip the first term in the collision results list as this is the system config, not a collision
                                continue
                            data.append(collision_results[x]) #for all other terms, add the collision information to the current data list

                        df = pd.DataFrame(data = [data], columns= columns)
                        i = 1 #the dataframe has now been created so i is set to 1 to avoid passing the if statement this block is contained in
                        continue
                        

                    ''' the process as above is repeated to obtain the next row of data (the results for the next configuration), however the next row is saved to a dataframe called df2, instead of df '''
                    number_columns = len(collision_results)
                    
                    columns = ['timestep', 'approximation', 'density']
                    for collision in range((number_columns - 1)): 
                        columns.append('Collision {}'.format(collision + 1))
                    
                
                    data = [collision_results[0][0], collision_results[0][1], collision_results[0][2]]
                    for x in range(len(collision_results)):
                        if x == 0: 
                            continue
                        data.append(collision_results[x])
                
                    

                    df2 = pd.DataFrame(data = [data], columns= columns) #this dataframe just contains the row of results for the current system configuration
                    
                    df = df.append(df2, ignore_index = True) #it then gets appended to the total dataframe, which contains all of the previous system configuration results 
                        

        df = df.fillna('No Collision')  #some systems won't have has as many collisions as others (eg for a smaller timestep) but it looks much nicer to say no collision that to have NaN       
        print(df)
        df.to_csv('collisions.csv') #save the df as a csv file

    def time_to_run_df(self, timesteps, approximations,  densities):
        '''
        Calculates the movement of the newtons cradle that is defined by the initialisation function, and a given timestep, approximation, and fluid density
        In order to test multiple timesteps, approximations, and densities, these must be entered as an array, even if only of one value
        A dataframe will be printed that shows the time taken to run each version of the "system"
        '''
        i = 0 #as in collisions df, the first row is created differently to the rest of the rows and so this is used to identify if a row has been made previosuly 
        ''' loops across all possible system configuratuons'''
        
        for timestep in timesteps:
            for approximation in approximations:
                for fluid_density in densities:
                    ''' the next 2 lines initialise the calculator class using the initial conditions from the config file and the timestep for this given simulation'''
                    calculating = calculator(timestep=timestep, iterations=self.iterations) 
                    calculating.get_balls(number = self.number, positions = self.start_positions, velocities= self.start_velocities, radii = self.radii, masses= self.masses, anchors= self.anchors)
                    
                    time = calculating.time_to_run(approximation, fluid_density)[0] #returns the time to run for running each system configuration
                    if i == 0: #if no row of data has been made 
                        df = pd.DataFrame(data= [[timestep, approximation, fluid_density, time]] , columns=['Timestep', 'Approximation', 'Fluid Density', 'Time to run']) #create the first row of data 
                        i += 1 #now there has been a row of data made 
                        
                        continue
                    df2 = pd.DataFrame(data = [[timestep, approximation, fluid_density, time]], columns=['Timestep', 'Approximation', 'Fluid Density', 'Time to run']) #create a new dataframe for each individual simulation
                    df = df.append(df2, ignore_index = True) #append it to the overall simulation
        print(df)
        df.to_csv('time_to_run.csv')

    def conservation_of_energy_df(self, timesteps, approximations, densities):
        '''
        return a dataframe showing the difference between the minimum and maximum of total energy for each system configuration
        used to compare system configurations 
        '''
        first_column = True
        for timestep in timesteps:
            for approximation in approximations:
                for density in densities:
                    calculating = calculator(timestep=timestep, iterations=self.iterations)
                    calculating.get_balls(number = self.number, positions = self.start_positions, velocities= self.start_velocities, radii = self.radii, masses= self.masses, anchors= self.anchors)
                    results = calculating.time_to_run(approximation, fluid_density)
                    plot_class_call = plotter('system_states_over_time.npy', self.number)
                    energy_list = plot_class_call.total_energy()
                    energy_min= min(energy_list)
                    energy_max= max(energy_list)
                    energy_diff= energy_max - energy_min
                    energy_start = energy_list[0]
                    energy_variation_as_fraction = energy_diff/energy_start
                    energy_variation_as_percentage = energy_variation_as_fraction * 100
                    
                    if first_column:
                        conservation_df = pd.DataFrame(data=[timestep, approximation, density, energy_diff, energy_variation_as_percentage], columns=['timstep','approximation', 'density', 'difference in minimum and maximum energy', 'energy difference as a oercentage of initial energy']) 
                        first_column = False
                        continue 
                    conservation_df_new_row = pd.DataFrame(data=[timestep, approximation, density, energy_diff, energy_variation_as_percentage], columns=['timstep','approximation', 'density', 'difference in minimum and maximum energy', 'energy difference as a oercentage of initial energy'])
                    conservation_df.append(conservation_df_new_row, ignore_index = True)
                
        conservation_df.to_csv('conservation.csv')

    def all_three_dfs(self, timesteps, approximations, densities):
        '''
        generates three dataframes, one to describe the number of collisions in the simulation of every configuration, one detailing the time taken to run each simulation, and one investigating the conservation of energy for each simulation
        the dataframes are then saved to disk as collisions.csv, time_to_run.csv and conservation.csv 
         
        '''
        first_column = True 
        
        for timestep in timesteps:
            for approximation in approximations:
                for fluid_density in densities:
                    calculating = calculator(timestep=timestep, iterations=self.iterations)
                    calculating.get_balls(number = self.number, positions = self.start_positions, velocities= self.start_velocities, radii = self.radii, masses= self.masses, anchors= self.anchors)
                    results = calculating.time_to_run(approximation, fluid_density)
                    time = results[0]
                    collision_results = results[1]

                    plot_class_call = plotter('system_states_over_time.npy', self.number)
                    energy_list = plot_class_call.total_energy()
                    
                    energy_min= min(energy_list)
                    energy_max= max(energy_list)
                    energy_diff= energy_max - energy_min
                    energy_start = energy_list[0]
                    energy_variation_as_fraction = energy_diff/energy_start
                    energy_variation_as_percentage = energy_variation_as_fraction * 100
                    

                    if first_column:
                        ''' initialise the time dataframe'''
                        time_df = pd.DataFrame(data= [[timestep, approximation, fluid_density, time]] , columns=['Timestep (s)', 'Approximation', 'Fluid Density (kg/m^3)', 'Time to run (s)'])
                        
                        ''' initialise the energy conservation dataframe ''''
                        conservation_df = pd.DataFrame(data=[timestep, approximation, density, energy_diff, energy_variation_as_percentage], columns=['Timestep (s)','Approximation', 'Fluid Density (kg/m^3)', 'Difference in minimum and maximum energy (J)', 'Energy difference as a percentage of initial energy (%)']) 

                        ''' initialise the collision results dataframe ''' 
                        number_of_columns = len(collision_results)
                        
                        columns = ['Timestep (s)', 'Approximation', 'Fluid Density (kg/m^3)']
                        for collision in range((number_of_columns - 1)): 
                            columns.append('Collision {}'.format(collision + 1))
                        
                        ''' extract the system information - timestep, approximation, and density - from the collision results'''
                        collision_data = [collision_results[0][0], collision_results[0][1], collision_results[0][2]]
                        
                        ''' append the information about all of the collision results to the new list, collision_data, that will become each row of the dataframe'''
                        for x in range(len(collision_results)):
                            if x == 0: #the first item in collision_results is the system information, which was added manually and so is skipped
                                continue
                            collision_data.append(collision_results[x]) #append the collision information to the list for the new row

                        collision_df = pd.DataFrame(data = [collision_data], columns= columns)
                        first_column = False
                        continue
                    ''' create the new row of time results, and add this row into the dataframe'''
                    time_df_new_row = pd.DataFrame(data = [[timestep, approximation, fluid_density, time]], columns=['Timestep (s)', 'Approximation', 'Fluid Density (kg/m^3)', 'Time to run (s)'])
                    time_df = time_df.append(time_df_new_row, ignore_index = True)

                    '''create the new row of energy conservation results, and add to the dataframe '''
                    conservation_df_new_row = pd.DataFrame(data=[timestep, approximation, density, energy_diff, energy_variation_as_percentage], columns=['Timestep (s)','Approximation', 'Fluid Density (kg/m^3)', 'Difference in minimum and maximum energy (J)', 'Energy difference as a percentage of initial energy (%)'])
                    conservation_df.append(conservation_df_new_row, ignore_index = True)
                

                    ''' create the new row of collision results and add to the dataframe. New row is generated using the same process to generate the first row'''
                    number_of_columns = len(collision_results)
                    
                    columns = ['Timestep (s)', 'Approximation', 'Fluid Density (kg/m^3)']
                    for collision in range((number_of_columns - 1)): 
                        columns.append('Collision {}'.format(collision + 1))
                    
                
                    collision_data = [collision_results[0][0], collision_results[0][1], collision_results[0][2]]
                    for x in range(len(collision_results)):
                        if x == 0: 
                            continue
                        collision_data.append(collision_results[x])
                
                    collision_df_new_row = pd.DataFrame(data = [collision_data], columns= columns)
                    collision_df = collision_df.append(collision_df_new_row, ignore_index = True)

                    
        
        time_df.to_csv('time_to_run.csv')
        collision_df = collision_df.fillna('No Collision')            
        collision_df.to_csv('collisions.csv')
        conservation_df.to_csv('conservation.csv')
