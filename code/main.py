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

class main:
    '''
    the main class for running the simulation. Main integrates all of the other classes 
    '''
    
    def __init__(self):
        '''
        upon initialisation, config.json is opened and the configuration is "read in"
        '''
        with open(r"code\config.json") as configuration:
            config = json.load(configuration)
        self.initialisation = config['initialisation']
        self.system = config['system']
        self.number = self.initialisation['number']

    def get_plots(self):
        sys_config = np.array((self.system.values())) #the plotter function takes the system configuration as an argument in order to display on the plots
        timesteps = self.system['timesteps']
        approximations = self.system['approximations']
        densities = self.system['densities']
        for timestep in timesteps:
            for approximation in approximations:
                for density in densities:
                    calculating = calculator(timestep=timestep, iterations=self.iterations)
                    calculating.get_balls(number = self.number, positions = self.start_positions, velocities= self.start_velocities, radii = self.radii, masses= self.masses, anchors= self.anchors)
                    plots = plotter('system_states_over_time', self.number)
                    plots.plot_x_vs_y(sys_config, show = False)
                    plots.energy_plot(sys_config, show = False, kinetic = True, kinetic = True, kinetic = True)

    def get_dfs(self):
        get_results = results(self.initialisation['number'], self.initialisation['StartPositions'], self.initialisation['StartVelocities'], self.initialisation['radii'], self.initialisation['masses'], self.initialisation['anchors'], self.initialisation['iterations'])
        get_results.time_to_run_df(self.system['timesteps'], self.system['approximations'], self.system['densities'])
        get_results.collision_df(self.system['timesteps'], self.system['approximations'], self.system['densities'])

    def main(self, plots = True, dataframes = True):
        '''
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

            
