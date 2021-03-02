''' a class used to plot the results saved by the calculator ''' '''RENAME THE DATA VARAIBLE'''
import numpy as np 
import matplotlib.pyplot as plt 
from calculator import calculator

class plotter:
    def __init__(self, data_name, number):
        file = data_name + '.npy'
        self.data = np.load(file, allow_pickle = True)
        self.number= number
        

    def organise_by_ball_positon(self):
        '''results with [[ball1.position time 0, ball1.position time 1,...], [ball2.position time 0, ball2.position time 1,....], ....] '''
        self.organise_by_time_position()
        lists_array = np.array(self.list_position_by_time)
        self.position_organised_by_ball = lists_array.transpose(1,0,2)

        

    def organise_by_time_position(self):
        '''results with [[ball1.position time 0, ball2.position time 0, ....], [ball1.position time 1, ball2.position time 1,....]] '''
        self.list_position_by_time = [ [] for i in range(len(self.data))]
        self.timelist = []
        
        for i in range(len(self.list_position_by_time)):
            for j in range(self.number):
                self.list_position_by_time[i].append(self.data[i][1][j].position)
            self.timelist.append(self.data[i][0])

    
    def plot_x_positions_vs_time(self):
        self.organise_by_ball_positon()
        fig, ax = plt.subplots()
        fig.suptitle("x postions of Newton's Cradle Balls vs Time")
        for ball in range(self.number):
            total_positions = self.position_organised_by_ball[ball]
            x_positions = []
            for position in range(len(total_positions)):
                x_positions.append(total_positions[position][0])
    
            ax.plot(self.timelist, x_positions , label = 'ball {}'.format(ball+1))

        ax.set(xlabel = 'time list', ylabel = 'x position of balls')
        ax.legend()
        plt.show()
        

    def plot_y_positions_vs_time(self):
        self.organise_by_ball_positon()
        fig, ax = plt.subplots()
        fig.suptitle("y postions of Newton's Cradle Balls vs Time")
        for ball in range(self.number):
            total_positions = self.position_organised_by_ball[ball]
            y_positions = []
            for position in range(len(total_positions)):
                y_positions.append(total_positions[position][1])
    
            ax.plot(self.timelist, y_positions , label = 'ball {}'.format(ball+1))

        ax.set(xlabel = 'time list', ylabel = 'x position of balls')
        ax.legend()
        plt.show()
        
    def plot_x_vs_y(self):
        self.organise_by_ball_positon()
        fig, ax = plt.subplots()
        fig.suptitle("x vs y positions")
        for ball in range(self.number):
            total_positions = self.position_organised_by_ball[ball]
            x_positions = []
            y_positions = []
            for position in range(len(total_positions)):
                x_positions.append(total_positions[position][0])
                y_positions.append(total_positions[position][1])
            ax.plot(x_positions, y_positions, label = 'ball {}'.format(ball+1))

        ax.set(xlabel ='x positions', ylabel = 'y positions')
        ax.legend()
        plt.show()

    def kinetic_energy_by_time(self):
        '''results with [[ball1.ke time 0, ball2.ke time 0, ....], [ball1.ke time 1, ball2.ke time 1,....]] '''
        self.list_ke_by_time = [ [] for i in range(len(self.data))]
        self.timelist = []
        
        for i in range(len(self.list_ke_by_time)):
            for j in range(self.number):
                ke = self.data[i][1][j].kinetic()
                self.list_ke_by_time[i].append(ke)
            self.timelist.append(self.data[i][0])
        
    
    def potential_energy_by_time(self):
        '''results with [[ball1.pe time 0, ball2.pe time 0, ....], [ball1.pe time 1, ball2.pe time 1,....]] '''
        ''' in order to calculate the potential energy, the "ground" height is the y position of the ball when directly underneath it's anchor '''
        self.list_pe_by_time = [ [] for i in range(len(self.data))]
        self.timelist = []
        for i in range(len(self.list_pe_by_time)):
            for j in range(self.number):
                pe = self.data[i][1][j].potential()
                self.list_pe_by_time[i].append(pe)
            self.timelist.append(self.data[i][0])
        
       



    def total_kinetic_energy(self):
        ''' check the conservation of the entire systems kinetic energy ke ''' 

        self.kinetic_energy_by_time()
        #print(self.list_ke_by_time)
        self.total_ke_list = [[] for i in range(len(self.list_ke_by_time))]
        for time in range(len(self.list_ke_by_time)):
            total_ke = 0 #at the each time section, reset ke to 0 so it can be calculated
            for ball in range(len(self.list_ke_by_time[time])):
                total_ke += self.list_ke_by_time[time][ball] #add up all the kinetc energies of each ball at that time
            self.total_ke_list[time].append(total_ke)
        #self.total_ke_list = self.total_ke_list
        return self.total_ke_list
        
       
    def total_potential_energy(self):
        ''' check the conservation of the entire systems potenital energy pe ''' 
    
        self.potential_energy_by_time()
        self.total_pe_list = [[] for i in range(len(self.list_pe_by_time))]
        for time in range(len(self.list_pe_by_time)):
            total_pe = 0 #at the each time section, reset pe to 0 so it can be calculated
            for ball in range(len(self.list_pe_by_time[time])):
                total_pe += self.list_pe_by_time[time][ball] #add up all the kinetc energies of each ball at that time
            self.total_pe_list[time].append(total_pe)
        return self.total_pe_list
        
        
    
    def total_energy(self):
        ''' check the conservation of the entire systems total energy - pe + ke ''' 
        ''' when air reistance is set to "on", energy will not be conservered ''' 
        self.total_potential_energy()
        self.total_kinetic_energy()
        self.total_energy_by_time = np.add(self.total_pe_list , self.total_ke_list)
        return self.total_energy_by_time

    def energy_plot(self, kinetic = False, potential = False, total = False):
        if kinetic and potential and (not total):
            self.total_potential_energy()
            self.total_kinetic_energy()
            fig, ax = plt.subplots(nrows=1, ncols=2)
            ax[0].plot(self.timelist, self.total_ke_list)
            ax[0].set(xlabel = 'time', ylabel = 'kinetic energy of the system')
            ax[0].grid()

            ax[1].plot(self.timelist, self.total_pe_list)
            ax[1].set(xlabel = 'time', ylabel = 'Potential energy of the system')
            ax[1].grid()
            
            fig.suptitle('Kinetic and potential energy time depence of the total system')
            plt.show()

        if total and ((not kinetic) or (not potential)):
            self.total_energy()
            fig, ax = plt.subplots(nrows=1, ncols=1)
            ax.plot(self.timelist, self.total_energy_by_time)
            ax.set(xlabel = 'time', ylabel = 'total energy of the system')
            ax.grid()
            fig.suptitle('Total energy change with time of the total system')
            plt.show()
        
        if kinetic != potential: #i think this will give me an exclusive or
            if kinetic:
                self.total_kinetic_energy()
                fig, ax = plt.subplots(nrows=1, ncols=1)
                ax.plot(self.timelist, self.total_ke_list)
                ax.set(xlabel = 'time', ylabel = 'kinetic energy of the system')
                ax.grid()
                fig.suptitle('kinetic energy of the system against time')
                plt.show()
            if potential:
                self.total_potential_energy()
                fig, ax = plt.subplots(nrows=1, ncols=1)
                ax.plot(self.timelist, self.total_pe_list)
                ax.set(xlabel = 'time', ylabel = 'potential energy of the system')
                ax.grid()
                fig.suptitle('potential energy of the system against time')
                plt.show()

        if kinetic and potential and total:
            self.total_energy()
            fig, ax = plt.subplots(nrows=1, ncols=3)
            ax[0].plot(self.timelist, self.total_ke_list)
            ax[0].set(xlabel = 'time', ylabel = 'kinetic energy of the system')
            ax[0].grid()

            ax[1].plot(self.timelist, self.total_pe_list)
            ax[1].set(xlabel = 'time', ylabel = 'Potential energy of the system')
            ax[1].grid()

            ax[2].plot(self.timelist, self.total_energy_by_time)
            ax[2].set(xlabel = 'time', ylabel = 'Total energy of the system')
            ax[2].grid()
                
            fig.suptitle('energy time depencies of the total system')
            plt.show()



    def total_energy_per_ball(self):
        ''' check the conservation of energy for each idividual ball'''
    
'''
test = plotter('data_testing', 2)
#test.plot_y_positions_vs_time()
#test.plot_x_positions_vs_time()
test.plot_x_vs_y()
test.energy_plot(kinetic=True, potential=True, total=True)

'''