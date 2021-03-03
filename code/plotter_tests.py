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
    assert (np.isclose(total[0] , (np.add(ke[0] , pe[0])))).all(), "total energy does not equal potential plus kinetic at the start"
    random_time = 50000 * random()
    random_time_int = math.floor(random_time)
    assert (np.isclose(total[random_time_int],  (np.add(ke[random_time_int]  ,pe[random_time_int])))).all(), "total energy does not equal potential plus kinetic at the a random point"


def test_energy_conservation():
    energies = plotter_init()
    total = energies[2]
    assert (np.isclose(total[0], total[50000]))
