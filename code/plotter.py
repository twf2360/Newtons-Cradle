''' a class used to plot the results saved by the calculator ''' '''RENAME THE DATA VARAIBLE'''
import numpy as np 
import matplotlib.pyplot as plt 
from calculator import calculator
import os

class plotter:
    '''
    the plotter class is used to plot various different results that have been calculated by the calculator class
    although it does not call on any functions from the calculator class, it relies on the calculations being completed so that it can read in the results
    '''
    def __init__(self, data_name, number):
        '''
        Initialisation function of the class:
        inputs:
        data_name: the stem of an npy file that contains the saved data from the calculator 
        number: the number of balls involved in the simulation
        '''
        file = data_name + '.npy'
        self.data= []
        self.data = np.load(file, allow_pickle = True)
        self.number= number
        os.remove(file) #this was added to debug why there were multiple overlaying plots
        
        
        

    def organise_by_ball_positon(self):
        '''
        The data that is read in by the calculator class is in a certain form [[time0, [ball1, ball2,....], [time1, [ball1, ball2,....]]]
        this is however not always the most useful form for plotting uses. Therefore, both of the organise_by_ functions change the organisation of the read in array
        these organisation functions are then used by the plotting function.
        '''
        '''results with [[ball1.position time 0, ball1.position time 1,...], [ball2.position time 0, ball2.position time 1,....], ....] '''
        self.organise_by_time_position()
        self.position_organised_by_ball = []
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
        '''
        this function is used to plot the x positions of all of the balls against time 
        '''
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
        '''
        used to plot the y position value of the balls against time 
        '''
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
        
    def plot_x_vs_y(self, system_config, show = False):
        '''
        plot the x position of all of the balls against the y position of the same ball.
        
        show (boolean) is set to True if you wish to see (and save) the plots, or False just to just save them
        system_config (array_like) is the system configuration that is being plotted - the timestep, approximation, and density

        this is used plot the path of the balls as a visual check that they are following the expected path
        
        '''
        timestep = system_config[0]
        approximation = system_config[1]
        density = system_config[2]
        txt = "system paramaters: timestep = {}, approximation = {}, fluid density = {}".format(timestep, approximation, density)
        config_name = 'timestep_{}'.format(timestep) + '_approximation_{}_'.format(approximation) + 'density_{}'.format(density) 
        plot_name = 'path_plot_' + config_name +'.jpeg'
        
        self.organise_by_ball_positon()
        fig, ax = plt.subplots(figsize= [15,8])
        
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
        ax.set_xlim([-0.8, 0.6])
        ax.set_ylim([-1.2,-0.7])
        ax.legend(loc='lower left')
        fig.text(.5, .05, txt, ha='center')
        if show:
            plt.show()
        plt.subplots_adjust(bottom=0.15)
        plt.savefig(plot_name)
        
    def kinetic_energy_by_time(self):
        '''
        similar to the organise_by_ functions, this function is used to organise the data that is read in into a certain form so that it can be plotted
        this function is by all of the plots that require kinetic energy
        '''
        '''results with [[ball1.ke time 0, ball2.ke time 0, ....], [ball1.ke time 1, ball2.ke time 1,....]] '''
        self.list_ke_by_time = [ [] for i in range(len(self.data))]
        self.timelist = []
        
        for i in range(len(self.list_ke_by_time)):
            for j in range(self.number):
                ke = self.data[i][1][j].kinetic()
                self.list_ke_by_time[i].append(ke)
            self.timelist.append(self.data[i][0])
        
    
    def potential_energy_by_time(self):
        '''
        similar to the organise_by_ functions, this function is used to organise the data that is read in into a certain form so that it can be plotted
        this function is by all of the plots that require potential energy
        '''
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
        '''
        this function turns [[ball1.ke time 0, ball2.ke time 0, ....], [ball1.ke time 1, ball2.ke time 1,....]] into [totalke time0, total ke time1,.....]
        so the total kinetic energy of the system can then be plotted
        '''

        self.kinetic_energy_by_time()
        self.total_ke_list = [[] for i in range(len(self.list_ke_by_time))] #generate an empty list of the correct size
        
        for time in range(len(self.list_ke_by_time)):
            total_ke = 0 #at the each time section, reset ke to 0 so it can be calculated
            for ball in range(len(self.list_ke_by_time[time])):
                total_ke += self.list_ke_by_time[time][ball] #add up all the kinetc energies of each ball at that time
            self.total_ke_list[time].append(total_ke)


        return self.total_ke_list
        
       
    def total_potential_energy(self):
        '''
        this function turns [[ball1.pe time 0, ball2.pe time 0, ....], [ball1.pe time 1, ball2.pe time 1,....]] into [totalpe time0, total pe time1,.....]
        so the total kinetic energy of the system can then be plotted
        '''
        self.potential_energy_by_time()
        self.total_pe_list = [[] for i in range(len(self.list_pe_by_time))] #generate empty list of the correct size
        for time in range(len(self.list_pe_by_time)):
            total_pe = 0 #at the each time section, reset pe to 0 so it can be calculated
            for ball in range(len(self.list_pe_by_time[time])):
                total_pe += self.list_pe_by_time[time][ball] #add up all the potential energies of each ball at that time
            self.total_pe_list[time].append(total_pe)

        return self.total_pe_list
        
        
    
    def total_energy(self):
        '''
        this function adds the total kinetic energy list to the total potential energy list, so that the total energy of the system can be plotted
        this allows a check for total energy conservation
        '''
    
        ''' when air reistance is set to "on", energy will not be conservered ''' 
        self.total_potential_energy()
        self.total_kinetic_energy()
        self.total_energy_by_time = np.add(self.total_pe_list , self.total_ke_list)
        return self.total_energy_by_time

    def energy_plot(self, system_config, show = False, kinetic = False, potential = False, total = False) :
        '''
        plot the change in different energies in the system at different times 

        system_config (array_like) is the system configuration that is being plotted - the timestep, approximation, and density

        show (boolean) is set to True if you wish to see (and save) the plots, or False just to just save them

        if any of kinetic, potential, and total are set to True, then the graph of that energy over time will be plotted  
        These functions only plot the enegyies of the whole system - not individual balls

        '''

        timestep = system_config[0]
        approximation = system_config[1]
        density = system_config[2]
        txt = "system configuration: timestep = {}, approximation = {}, fluid density = {}".format(timestep, approximation, density)
        config_name = 'timestep_{}'.format(timestep) + '_approximation_{}_'.format(approximation) + 'density_{}'.format(density) 
        plot_name = 'energy_plot_' + config_name +'.jpeg'
        
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
            fig.text(.5, .05, txt, ha='center')
            if show:
                plt.show()

        if total and ((not kinetic) or (not potential)):
            self.total_energy()
            fig, ax = plt.subplots(nrows=1, ncols=1)
            ax.plot(self.timelist, self.total_energy_by_time)
            ax.set(xlabel = 'time', ylabel = 'total energy of the system')
            ax.grid()
            fig.suptitle('Total energy change with time of the total system')
            fig.text(.5, .05, txt, ha='center')
            if show:
                plt.show()
        
        if kinetic != potential: #i think this will give me an exclusive or
            if kinetic:
                self.total_kinetic_energy()
                fig, ax = plt.subplots(nrows=1, ncols=1)
                ax.plot(self.timelist, self.total_ke_list)
                ax.set(xlabel = 'time', ylabel = 'kinetic energy of the system')
                ax.grid()
                fig.suptitle('kinetic energy of the system against time')
                fig.text(.5, .05, txt, ha='center')
                plt.show()
            if potential:
                self.total_potential_energy()
                fig, ax = plt.subplots(nrows=1, ncols=1)
                ax.plot(self.timelist, self.total_pe_list)
                ax.set(xlabel = 'time', ylabel = 'potential energy of the system')
                ax.grid()
                fig.suptitle('potential energy of the system against time')
                fig.text(.5, .05, txt, ha='center')
                if show:
                    plt.show()

        if kinetic and potential and total:
            self.total_energy()
            
            fig, ax = plt.subplots(nrows=1, ncols=3, figsize= [25,10])
            ax[0].plot(self.timelist, self.total_ke_list)
            ax[0].set(xlabel = 'time', ylabel = 'kinetic energy of the system')
            ax[0].grid()

            ax[1].plot(self.timelist, self.total_pe_list)
            ax[1].set(xlabel = 'time', ylabel = 'Potential energy of the system')
            ax[1].grid()

            ax[2].plot(self.timelist, self.total_energy_by_time)
            ax[2].set(xlabel = 'time', ylabel = 'Total energy of the system')
            ax[2].set_ylim([0,3])
            ax[2].grid()
            m, b = np.polyfit(self.timelist, self.total_energy_by_time, 1)
            fit = m*self.timelist + b
            ax[2].plot(self.timelist, fit , linestyle = 'dashed')
                
            fig.suptitle('energy time depencies of the total system')
            fig.text(.5, .05, txt, ha='center')
            if show:
                plt.show()
            plt.subplots_adjust(bottom=0.15)
            plt.savefig(plot_name)
            




    
'''
test = plotter('system_states_over_time', 1)
#test.plot_y_positions_vs_time()
#test.plot_x_positions_vs_time()
test.plot_x_vs_y()
test.energy_plot(kinetic=True, potential=True, total=True)

'''