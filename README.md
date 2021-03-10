# Newtons_Cradle - PHYS389 Project
<img src="https://www.lancaster.ac.uk/media/lancaster-university/content-assets/images/fst/logos/Physicslogo.svg" width="350" height="95">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
phys389-2021-project-twf2360 created by GitHub Classroom

Writing a program that simulates, and hopefully animates, a Newton's cradle, for module PHYS389 at Lancaster University. 
## About PHYS389: Computer Modelling
PHYS389 is intented to build upon previous Computer Modelling techniques from PHYS281, and introduce more advanced programming techniques than those used in the previous Computer Modelling Module, PHYS281. These more advanced techniques could be more sophisticated class methods, such as inheritcance. Alternatively, the system could be more complicated than the PHYS281, consisting of more complicated motion - such as random, or choatic motion. Additionally, as an addition to PHYS281, a testing system should be implemented, using libraries such as PyTest. This is a large portion of the final grade, and it is important that it is included

## Personal Project 
As two of the recommended projects were a force damped pendulum, or a double pendulum. To add to this, I decided to try to code a Newton's Cradle simulation. Ideally, the 'pendulum motion' shown by the balls on the end of the pendulum will also show damped behviour. 
The aim is to not only write a program to simulate and animate a Newton's Cradle, but to be able to anaylse the simulation and test it's accuracy. I would also like to be able adaptable to various configurations, in this case those configurations being number of balls, and the string length, starting positions, and more. As there is an analytic solution for pendulum motion with a small angle approximation, this should not be used - instead there should be numerical calculations at a given time interval in order to obtain an approximation to real motion. From this, the effect of changing the time intervals can be analysed. The original plan was to use an ODE solver, however issues arose when trying to combine the ODE solver for pendulum motion, and the collision calculations. Instead all of the forces on each ball will be evaluated at every given moment. Due to the time scale of this project, there is a very high possibility that not all of these goals will be possible. The focus should be on the analysis of the simulation, over animation. 
Furthermore, There is a possibility that a Newton's Cradle is not a choatic enough system. Should this be the case, the code will be changed to a double pendulum. 

## How To Use This Repo:

### Required Python Packages
The simulation requires certain python packages for many of the calculations. The documentation for importing python modules can be found [here](https://pip.pypa.io/en/stable/)
Required modules:
 - NumPy
 - Matplotlib
 - math
 - copy
 - itertools 
 - pandas
 - json 
 - time 
 - os
 - PyTest

### How To Run a Simulation
Once the "code" folder has been downloaded and unpacked, two files require user changing in order to run a simulation:
##### config.json:
config.json defines the system configurations that are to be simulated. System configurations must be entered as values to the keys already shown in config.json. There will key:value pairs already entered in the downloaded file.
> only certain system configurations are possible, as will be described in "What Systems Can Be Simulated" 
##### main.py 
main.py is the file that reads the configurations descirbed in config.json, and accesses all of the other classes contained in this repo in order to run the simulation. In order to run the simulation, an instance of the main class should be created, and then the class function main should be run. Main takes two inputs, plots and dataframes. These inputs should be set to true or false, depending on whether a use wants the plots, or the dataframes of the results of the simulation should be saved to disk
> an example of creating an instance of the class and calling the correct class method will be present at the bottom of the main.py file
### What Systems Can Be Simulated   
Due to limitations withon the code, only certain systems can be simulated. Any number of balls can be defined within config.json, however it must be ensured that the number of parameters (eg, the number of start positions) is consistent with the number of balls. However, there are only three possible approximations of motion that can be modeled, the Euler, Euler-Cromer, and Runge-Kutta second order. These approximations can be chosen by entering the strings "euler", "cromer", and "rk2" as the values to the approximations key within config.json. Any other strings will not be recognised, and these are case sensitive. The pre-downloaded config.json contains all three possible approximations of motion in the configuration file, and it is recommended that this is only changed by deleting unwanted approximations, and not adding to the list. 


### Repo File Tree Explained 
The folder titled "learning" can be ignored. It contains three more simple scripts that were written in order to understand the concepts behind the Newton's Cradle. These concepts are simple pendulums, damped pendulums, and collisions.

The "txt" folder contains two files, notes.md, and branches.md. Notes is a personal to-do list, that will be used to document the progress of the project, and keep track of any ideas for future improvement. As the use of Git/GitHub is being assessed for the PHYS389 module, I did not want to delete any of the previous branches. Therefore, branches.md contains information on each of the branches, why they were created, and what they were used for.

The "code" folder contains all of the code that is used to run, and test the simulation:
    
  - config.json should be changed to the configuration that you are looking to test. "initialisation" contains the number of balls, as well as all of the required information about them. This information includes their masses, radii, starting position and velocity, and the point at which they are anchored too.  "system" is used to define the different systems that you want to test. Therefore, multiple different approximations, timesteps, and fluid densities can be defined
    
  - ball.py defines the ball objects. Each ball object is described by the paramaters mentioned in the config file. Ball.py also contains multiple different approximations of motion, which can be chosen when updating the balls position and velocity. There are also functions that return the kinetic and potential energy of the ball
    
  - calculator.py calculates the motion of the system. It saves the state of the system (the ball objects, the approximation being used, the density of the fluid through which the balls are moving and the time), to disk, in a file called "system_states_over_time.npy". There is also a function used to calculate the time taken to run the calculator, should this be required
   
  - plotter.py reads in a file with a given name, and when the number of balls used in that simulation is defined, it can be used to plot the energy of, or positions of balls withing the system over time 
    
  - dataframes.py uses calculator.py to calculate the motion of the system for every system defined in the config file. It can then be used to print dataframes for the time at which all of the collisions took place for each system, or the time taken to run the calculator for each system

  - main.py accesses all of the other classes, and is to be ran by a user after they have defined the system configuration in the config.json file.

  - plotter_tests.py, ball_and_config_tests.py, and calculator_tests all use the PyTest framework to test the respective files that are contained within the name. 



