''' a class used to plot the results saved by the calculator '''
import numpy as np 
import matplotlib.pyplot as plt 
from calculator import calculator

class plotter:
    def __init__(self, data_name, number):
        file = data_name + '.npy'
        self.data = np.load(file, allow_pickle = True)
        self.number = number

    def enumeration(self):
        '''results with [[ball1 time 0, ball2 time 0], [ball1 time 1, ball2 time 1]] '''
        self.lists = [ [] for i in range(len(self.data))]
        self.timelist = []
        for i in range(len(self.lists)):
            for j in range(self.number):
                self.lists[i].append(self.data[i][1][j].position)
            self.timelist.append(self.data[i][0])


    def plot(self):
        self.enumeration()
        #print(self.lists)
        fig, ax = plt.subplots()
        fig.suptitle('overall title!')
        for x in range(self.number):
            transpose = np.transpose(self.lists)[x]
            print(transpose[x])
            ax.plot(self.timelist, transpose[x], label = 'ball {}'.format(x+1))

        ax.set(xlabel = 'time list', ylabel = 'x_position of balls')
        ax.legend()
        plt.show()
        

            

test = plotter('data_testing', 2)
test.plot()