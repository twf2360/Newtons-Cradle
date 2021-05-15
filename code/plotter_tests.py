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
    get_results.calculate(approximation='rk2', density=0)
    plot = plotter('system_states_over_time', 1)
    
    ke_by_time = plot.total_kinetic_energy()
    pe_by_time = plot.total_potential_energy()
    total_e_by_time = plot.total_energy()
    return [ke_by_time, pe_by_time, total_e_by_time]

def test_list_lengths():
    '''
    lots of lists are created by the plotter class, and the length of them should be known, as it should be the number of iterations in a lot of case
    '''

    ''' as testing class attributes, not results, need to call a new class instance'''

    theta = math.pi/6 #initial starting angle! 
    get_results = calculator(0.0001,50000)
    get_results.get_balls(number = 1,positions= [[1 * math.sin(theta), -1 * math.cos(theta)]], velocities= [[0,0]], radii=[0.02], masses=[1], anchors= [[0,0]])
    get_results.calculate(approximation='rk2', density=0)
    plot = plotter('system_states_over_time', 1)

    assert len(plot.timelist) == 50000
    assert len(plot.total_ke_list) == 50000
    assert len(plot.total_pe_list) == 50000
    assert len(plot.total_energy_by_time) == 50000
    assert len(plot.potential_energy_by_time) == 50000
    assert len(plot.kinetic_energy_by_time) == 50000
    assert len(plot.list_position_by_time) == 50000

    

def test_energy_addition():
    '''
    test to ensure that the when adding kinetic and potential energy to get total energy, that the addition is done correctly
    '''
    ''' use is close due to errors in floating point maths'''
    energies = plotter_init()
    ke = energies[0]
    pe = energies[1]
    total = energies[2]
    assert (np.isclose(total[0] , (np.add(ke[0] , pe[0])))).all(), "total energy does not equal potential plus kinetic at the start"
    random_time = 50000 * random()
    random_time_int = math.floor(random_time)
    assert (np.isclose(total[random_time_int],  (np.add(ke[random_time_int]  ,pe[random_time_int])))).all(), "total energy does not equal potential plus kinetic at the a random point"


def two_ball_init():
    '''
    some of the results rely on the tota energy of the system, and therefore this is to check that these things are caluclated correctly with a more complicated system
    '''
    theta = math.pi/6 #initial starting angle! 
    get_results = calculator(0.0001,50000)
    get_results.get_balls(number = 2,positions= [[1 * math.sin(theta), -1 * math.cos(theta)], [0,-0.4]], velocities= [[0,0], [0,0]], radii=[0.02,0.02], masses=[1,1], anchors= [[0,0], [0.4]])
    get_results.calculate(approximation='rk2', density=0)
    plot = plotter('system_states_over_time', 2)
    return plot

def test_two_ball_energy():
    '''
    testing that the total energy of the system is calculated correctly - kinetic plus potential. 
    '''
    plot = two_ball_init()
    ke = plot.total_kinetic_energy 
    pe = plot.total_potential_energy
    total = plot.total_energy()
    
    ke_plus_pe = ke + pe 
    assert np.isclose(ke_plus_pe[0], total[0]).all(), "total energy not equal to kinetic plus potential at start" 
    random_time = 50000 * random()
    random_time_int = math.floor(random_time)
    assert np.isclose(ke_plus_pe[random_time_int], total[random_time_int]).all(), "total energy not equal to kinetic plus potential at random time"

