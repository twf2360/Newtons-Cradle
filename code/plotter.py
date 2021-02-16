''' a class used to plot the results saved by the calculator '''
import numpy as np 
import matplotlib.pyplot as plt 
from calculator import calculator

class plotter:
    def __init__(self, data_name, number):
        file = data_name + '.npy'
        self.data = np.load(file, allow_pickle = True)
        self.number = number

    def organise_by_ball(self):
        '''results with [[ball1.position time 0, ball1.position time 1,...], [ball2.position time 0, ball2.position time 1,....], ....] '''
        self.organise_by_time()
        lists_array = np.array(self.lists)
        self.organised_by_ball = lists_array.transpose(1,0,2)

        

    def organise_by_time(self):
        '''results with [[ball1.position time 0, ball2.position time 0, ....], [ball1.position time 1, ball2.position time 1,....]] '''
        self.lists = [ [] for i in range(len(self.data))]
        self.timelist = []
        
        for i in range(len(self.lists)):
            for j in range(self.number):
                self.lists[i].append(self.data[i][1][j].position)
            self.timelist.append(self.data[i][0])

    
    def plot_x_positions_vs_time(self):
        self.organise_by_ball()
        fig, ax = plt.subplots()
        fig.suptitle("x postions of Newton's Cradle Balls vs Time")
        for ball in range(self.number):
            total_positions = self.organised_by_ball[ball]
            x_positions = []
            for position in range(len(total_positions)):
                x_positions.append(total_positions[position][0])
    
            ax.plot(self.timelist, x_positions , label = 'ball {}'.format(ball+1))

        ax.set(xlabel = 'time list', ylabel = 'x position of balls')
        ax.legend()
        plt.show()
        

    def plot_y_positions_vs_time(self):
        self.organise_by_ball()
        fig, ax = plt.subplots()
        fig.suptitle("y postions of Newton's Cradle Balls vs Time")
        for ball in range(self.number):
            total_positions = self.organised_by_ball[ball]
            y_positions = []
            for position in range(len(total_positions)):
                y_positions.append(total_positions[position][1])
    
            ax.plot(self.timelist, y_positions , label = 'ball {}'.format(ball+1))

        ax.set(xlabel = 'time list', ylabel = 'x position of balls')
        ax.legend()
        plt.show()
        

test = plotter('data_testing', 2)
test.plot_y_positions_vs_time()