import pytest
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
import dataframes
from plotter import plotter
from random import random
import os 
import time


def calculator_init():
    theta = math.pi/6 #initial starting angle! 
    calc = calculator(0.0001,50000) #timestep and iterations for calculator 
    calc.get_balls(number = 1,positions= [[1 * math.sin(theta), -1 * math.cos(theta)]], velocities= [[0,0]], radii=[0.02], masses=[1], anchors= [[0,0]]) #create a single pendulum for simplicity
    results = calc.time_to_run(approximation='rk2', density=0) #do the calculation, using time to run to return both the collision results and the time results
    return results
    

def test_save_file():
    calculator_init()
    ''' save file creation ''' 
    assert os.path.isfile('system_states_over_time.npy'), "file of save data not collected"
    ''' save file length ''' 
    save_file = np.load('system_states_over_time.npy', allow_pickle=True)
    assert len(save_file) == 50000
    ''' save file component length '''
    save_file_component = save_file[0]
    assert len(save_file_component) == 2

def test_time_to_run():
    start_time = time.time()
    results = calculator_init()
    time_to_run_result = results[0]
    time_to_run_test = time.time()-start_time
    assert np.isclose(time_to_run_result, time_to_run_test)

def test_collision_results():
    ''' as testing a single pendulum, shouldn't be any collisions'''
    results = calculator_init()
    collision_info = results[1]
    assert len(collision_info) == 0