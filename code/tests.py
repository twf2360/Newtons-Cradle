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
import plotter

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

def inital_config():
    with open(r"code\config.json") as configuration:
        config = json.load(configuration)
    return config

def ensure_dict():
    config = inital_config()
    assert type(config) == dict

def test_for_initialisation_config():
    config = inital_config()
    assert type(config['initialisation']) == dict

def test_for_system_config():
    config = inital_config()
    assert type(config['system']) == dict

