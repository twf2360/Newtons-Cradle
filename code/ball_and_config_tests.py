''' IDEAS! 
CHECK KE + PE = TOTAL E 
CHECK STARTING E = INITIAL E
check the config is correct
check the time to run is correct?
check the balls made are expected
'''

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

'''
The tests below are for the ball class. They test that a ball is initialised with the correct parameters, and that potential energy and kinetic energy are correctly calculated
'''

def ball_initialisation(position, velocity, radius, mass, anchor):
    test_ball = ball(position, velocity,radius,mass,anchor )
    return test_ball

def test_ball_initalisation_position():
    ball = ball_initialisation(position=[0,0], velocity=[0,0],radius= 1, mass = 1,anchor= [0,1])
    assert (ball.position == [0,0]).all() 


def test_ball_initalisation_velocity():
    ball = ball_initialisation(position=[0,0], velocity=[0,0],radius= 1, mass = 1,anchor= [0,1])
    assert (ball.velocity == [0,0]).all()

def test_ball_initalisation_radius():
    ball = ball_initialisation(position=[0,0], velocity=[0,0],radius= 1, mass = 1,anchor= [0,1])
    assert ball.radius == 1

def test_ball_initalisation_mass():
    ball = ball_initialisation(position=[0,0], velocity=[0,0],radius= 1, mass = 1,anchor= [0,1])
    assert ball.mass == 1


def test_ball_initalisation_anchor():
    ball = ball_initialisation(position=[0,0], velocity=[0,0],radius= 1, mass = 1,anchor= [0,1])
    assert (ball.anchor == [0,1]).all()

def test_ball_energies():
    ball = ball_initialisation(position=[0,0], velocity=[0,0],radius= 1, mass = 1,anchor= [0,1])
    assert ball.kinetic == 0, "kinetic energy should be 0"
    assert ball.potential == 0, "potential energy should be 0"


 

'''
the next group of tests are for the the configuration file. This ensures that there is a dictionary that defines the configuration, and that it contains all of the needed parameters 

'''
def inital_config():
    with open(r"code\config.json") as configuration:
        config = json.load(configuration)
    return config

def test_ensure_dict():
    config = inital_config()
    assert type(config) == dict

def test_for_initialisation_config():
    config = inital_config()
    assert type(config['initialisation']) == dict

def test_for_system_config():
    config = inital_config()
    assert type(config['system']) == dict

def test_keys_exist():
    config = inital_config()
    system = config['system']
    initial = config['initialisation']
    assert all(key in initial for key in(('iterations', 'number', 'StartPositions', 'StartVelocities', 'masses', 'radii', 'anchors'))) , "missing key for initialisation config"
    assert all(key in system for key in('timesteps', 'approximations', 'densities')) , "missing key for system config"



