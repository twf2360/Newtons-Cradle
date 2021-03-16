from typing import Tuple
from plotter import plotter
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
from dataframes import results

''' there will be a way to make this faster, as currently plots runs the calculator through, and then collision dfs does it again, and then time to run dfs does it again '''
''' fixed the dfs part '''

class main:
    '''
    the main class for running the simulation. It is intended that a user only interacts with this file, and the config json
    Main integrates all of the other classes in order to produce dataframes, and plots, for all of the possible configurations listed in config.json
    note: this can lead to a lot of plots saved - each config saves two plots (paths and energies). 
    '''
    
    def __init__(self):
        '''
        upon initialisation, config.json is opened and the configuration is "read in" from config.json 
        the two keys from the overarching dictionary within config are seperated out for ease of future use (initialisation and system)
        '''
        with open(r"code\config.json") as configuration:
            self.config = json.load(configuration)
        
        self.initialisation = self.config['initialisation'] #initialisation dictionary extracted from total config dict
        self.system = self.config['system'] #system dictionary extracted from total config dict
        self.number = self.initialisation['number'] #the number of balls is also further extracted from the config dictionary

    def get_plots(self):
        '''
        generates plots for all of the possible configurations in the config file using the plotter and calculator class 
        two plots are generated for each configuration, one of the individual ball paths and one of the potential, kinetic, and total energy of the system [not individual balls]
        plots are saved using the following naming convention:
            energy plots: energy_plot_timestep_{}_approximation_{}_density_{}
            path plots: energy_plot_timestep_{}_approximation_{}_density_{}
            where {} contains the system configuration for that variable. 
        '''
        timesteps = self.system['timesteps'] #extract the list of timestep configs
        approximations = self.system['approximations'] #extract the list of approximation congifs
        densities = self.system['densities'] #extract the list of density configs 
        
        '''loop of each of the individual aspect lists in order to iterate over every possible config '''
        for timestep in timesteps:
            for approximation in approximations:
                for density in densities:
                    print(timestep, approximation, density)
                    calculating = calculator(timestep=timestep, iterations=self.initialisation['iterations']) #initialise the calculator class using the selected timestep
                    calculating.get_balls(self.initialisation['number'], self.initialisation['StartPositions'], self.initialisation['StartVelocities'], self.initialisation['radii'], self.initialisation['masses'], self.initialisation['anchors']) #set up the calculator with the correct conditions defined by the initialisation config
                    calculating.calculate(approximation, density) #calculate the movement using the current approximation and density 
                    
                    plots = plotter('system_states_over_time', self.number) #read in the calculated data so that it can be plotted 
                    plots.plot_x_vs_y([timestep, approximation, density], show = False) #ploy the paths of the balls, just save the plot instead of showing it 
                    plots.energy_plot([timestep, approximation, density], show = False, kinetic = True, total=  True, potential=  True) #plot the energy of the balls, just save the plot instead of showing it
                    print('\n \n \n')

    def get_dfs(self):
        '''
        generates the results dataframes for all of the possible configurations. Uses the results class within dataframes.py which in itself accesses the calculator class
        generates two dataframes that are saved as csv files, not printed: collisions.csv and time_to_run.csv
        
        time_to_run.csv contains the system configuration settings (timestep, approximation, and density) and how long it took to run that simulation
        collisions.csv contains the system configuration settings (timestep, approximation, and density) and the the number of, and at what time all of the collisions took place
        
        note: if the configuration only contains one ball, there will be no collisions, and therefore collisions.csv will only contain the system settings
        '''
        get_results = results(self.initialisation['number'], self.initialisation['StartPositions'], self.initialisation['StartVelocities'], self.initialisation['radii'], self.initialisation['masses'], self.initialisation['anchors'], self.initialisation['iterations']) # initialises the results class in dataframes.py
        get_results.all_three_dfs(self.system['timesteps'], self.system['approximations'], self.system['densities']) #uses the collision_and_time_seperate_df class method to obtain the dataframes and save them to disk
        

    def main(self, plots = True, dataframes = True):
        '''
        The main function is used to access the plots and dataframes function if they are wanted. This is the only function that should be "ran" by a user

        depending on the inputs (see below) other class methods within the main class are ran, in order to generate the plots or dataframes required.

        inputs:
        plots (boolean) : if plots is set to true then the plots of the defined simulation will be saved 
        dataframes (boolean): if dataframes is set to true then the dataframes showing time to run, and collision information are saved. 
        '''
        
        if dataframes and (not plots):
            self.get_dfs()
        
        if plots and (not dataframes):
            self.get_plots()

        if plots and dataframes:
            self.get_plots()
            self.get_dfs()


''' example of how to run the simulation'''
test = main()
test.main(plots= True, dataframes= True)