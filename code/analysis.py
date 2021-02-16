import numpy as np 
import matplotlib.pyplot as plt 
from calculator import calculator

class analysis:
    ''' a class of different analysis functions to check the accuracy of the simulation'''
    def __init__(self, data_name):
        file = data_name + '.npy'
        self.data = np.load(file, allow_pickle = True)

    def total_energy(self):
        ''' check the conservation of the entire systems total energy - pe + ke ''' 

    def total_energy_per_ball(self):
        ''' check the conservation of energy for each idividual ball'''



