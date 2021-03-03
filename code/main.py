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

class main:
    
    def __init__(self):
        with open(r"code\config.json") as configuration:
            config = json.load(configuration)
            self.initialisation = config['initialisation']
            self.system = config['system']

    def main(self, plots = True, dataframes = True):
         

        if dataframes and (not plots):
            
            get_results = results(self.initialisation['number'], self.initialisation['StartPositions'], self.initialisation['StartVelocities'], self.initialisation['radii'], self.initialisation['masses'], self.initialisation['anchors'], self.initialisation['iterations'])
            get_results.time_to_run_df(self.system['timesteps'], self.system['approximations'], self.system['densities'])

        if plots and (not dataframes):
            '''
            need to change from show to save, and make sure the saves won't overwrite. 
            '''
