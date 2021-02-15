''' a class used to plot the results saved by the calculator '''
import numpy as np 
import matplotlib as plt 
from calculator import calculator

class plotter:
    def __init__(self, data_name, number):
        file = data_name + '.npy'
        self.data = np.load(file, allow_pickle = True)
        self.number = number

    def enumeration(self):
        '''results with [[ball1 time 0, ball2 time 0], [ball1 time 1, ball2 time 1]] '''
        lists = [ [] for i in range(self.number)]
        print(lists)
        print(self.data)
        for i in range(len(lists)):
            for j in range(self.number):
                lists[i].append(self.data[i][1][j].position)
    
            

test = plotter('data_testing', 2)
test.enumeration()