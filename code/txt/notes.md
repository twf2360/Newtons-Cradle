
# Notes 

This page is just to keep track of things that need doing, and random thoughts that could be useful:
        
    

- to do:
    - simple pend   :white_check_mark:

    - animate simple pend :white_check_mark:

    - damped pend + animate :white_check_mark:

    - collisions + animate :white_check_mark:

    - combine :construction: (in progress)

        - change from a ODE based method to a forces based method for calculating momenta :white_check_mark:
        
        - plot results :white_check_mark:

        - Analyse the plot results :construction:
            - there may be an issue if the timestep is too high in calculating overlaps
                - currently 0.01 doesn't work, 0.001 does. 0.0001 is usually used thrroughout the testing process
            - first few collisions work, things get weird after :confused:
                - not due to approximation
                - not due to overly large radii 
                - this has been fixed with a bit of a hotfix, but it works! 
                    - needs more analysis
            - The total energy plot doesn't appear to be a simple addition of the ke and pe 
                - perfect idea for a unit test! 
                - this is due to errors with floating point maths. It is only very very small variations :neutral_face:
        
        - put the collision handler, and the calculator without collisions, in seperate functions :white_check_mark:

        - within plotter class, ensure that the test is run first? 

    - Air resistance seems to have far too great an impact
        - modelled using fluid resistance, and the units of damping co-efficent weren't correct
        - the energy response to damping is as expected
 
    - find things to analyse (consv of momentum, energy, how changing time step effects things etc) :construction:
        - added kinetic, potential and total energy to plotter and they can be anaylsed
    
    - ensure that enough "advanced coding methods" are present :construction:
        - read up on what counts as advanced coding methods 
            - Abstract classes, inheritance?

    - add pytests :construction:
        - tried to contain it within a seperate folder, althought I had some major issues with importing the other classes
    
    - add config file :white_check_mark: 
        - unable to comment within the file which is annoying - the reason for the weird position number is because it starts at an angle of 30 deg
    
    - Dataframes :construction:
        - collision data frame :white_check_mark:
        - time to run dataframe :white_check_mark:
            - add the number of the balls that are colliding into plots, or dataframes?
        - save dfs to disk?
    
    - add "main.py" which is used to run the code? :white_check_mark:

    - add non-elastic collisions? 

    - update docstrings and readme to include main, and the changes made to plotter :white_check_mark:

    - add a change of mass possibility somewhere?
    
    - animate? 

Feels like it's worth writing up about using np.seterr, and try except statements to find what values of ball.position and ball.anchor were causing the runtime warning for overflow
This was a divide by 0 error, which is now solved! 
