# Newtons_Cradle - PHYS389 Project
<img src="https://www.lancaster.ac.uk/media/lancaster-university/content-assets/images/fst/logos/Physicslogo.svg" width="350" height="95">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
phys389-2021-project-twf2360 created by GitHub Classroom

Writing a program that simulates, and hopefully animates, a Newton's cradle, for module PHYS389 at Lancaster University. 
### About PHYS389: Computer Modelling
PHYS389 is intented to build upon previous Computer Modelling techniques from PHYS281, and introduce more advanced programming techniques than those used in the previous Computer Modelling Module, PHYS281. These more advanced techniques could be more sophisticated class methods, such as inheritcance. Alternatively, the system could be more complicated than the PHYS281, consisting of more complicated motion - such as random, or choatic motion. Additionally, as an addition to PHYS281, a testing system should be implemented, using libraries such as PyTest. This is a large portion of the final grade, and it is important that it is included

### Personal Project 
As two of the recommended projects were a force damped pendulum, or a double pendulum. To add to this, I decided to try to code a Newton's Cradke. Ideally, the 'pendulum motion' shown by the balls on the end of the pendulum will also show damped behviour. 
The aim is to not only write a program to simulate and animate a newtons cradle, but to be able to anaylse the simulation and test it's accuracy. I would also like to be able adaptable to user inputs, in this case those inputs being number of balls, and the string length. As there is an analytic solution for pendulum motion with a small angle approximation, this should not be used - instead there should be numerical calculations at a given time interval in order to obtain an approximation to real motion. From this, the effect of changing the time intervals can be analysed. Whilst the original plan was to use an ODE solver, instead all of the forces on each ball will be evaluated at every given moment. Due to the time scale of this project, there is a very high possibility that not all of these goals will be possible. The focus should be on the analysis of the simulation, over the adaptability to user inputs.
Furthermore, There is a possibility that a Newton's Cradle is not a choatic enough system. Should this be the case, the code will be changed to a double pendulum. 

### Milestones 
There are various milestones that will help to document my progress! 
1. Simulate a simple pendulum
    - Done using ODEINT
    - Need to ensure that the 'forces' method works
    - Succesfully animated 
2. Extend to a damped pendulum
    - Done using ODEINT
    - Succesfully animated
3. Model Collisons 
    - Done 
    - Successfully animated
4. Extend to a Newtons Cradle
    - Done, but more testing needing to be done to prove it works 
    - Plotting function needs updating 
