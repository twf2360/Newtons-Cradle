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

''' ADD KE AND PE HERE ''' 

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


'''
in order to test the functions of the plotter class, data must be collected to plot
In order to test the simplest aspects - such as that total energy = pe+ke, and conservation of energy, the simulation of a single ball - a simple pendulum - will be tested
'''


def plotter_init():
    theta = math.pi/6 #initial starting angle! 
    get_results = calculator(0.0001,50000)
    get_results.get_balls(number = 1,positions= [[1 * math.sin(theta), -1 * math.cos(theta)]], velocities= [[0,0]], radii=[0.02], masses=[1], anchors= [[0,0]])
    get_results.calculate(approximation='cromer', density=0)
    plot = plotter('system_states_over_time', 1)
    
    ke_by_time = plot.total_kinetic_energy()
    pe_by_time = plot.total_potential_energy()
    total_e_by_time = plot.total_energy()
    return [ke_by_time, pe_by_time, total_e_by_time]

def test_energy_addition():
    ''' use is close due to errors in floating point maths'''
    energies = plotter_init()
    ke = energies[0]
    pe = energies[1]
    total = energies[2]
    assert (math.isclose(total[0] == (ke[0] + pe[0]))).all(), "total energy does not equal potential plus kinetic at the start"
    random_time = 50000 * random()
    random_time_int = math.floor(random_time)
    assert (math.isclose(total[random_time_int],  (ke[random_time_int] + pe[random_time_int]))).all(), "total energy does not equal potential plus kinetic at the a random point"


def test_energy_conservation():
    energies = plotter_init()
    total = energies[2]
    assert (math.isclose(total[0], total[50000])).all()


