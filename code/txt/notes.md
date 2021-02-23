
# Notes 

This page is just to keep track of things that need doing, and random thoughts:
        - slightly unsure about how the collisions program will deal with corners, however that won't be relevant to the larger project anyway
        - the original ODEINT solutions have been discarded.
    

- to do:
    - simple pend   :white_check_mark:
    - animate simple pend :white_check_mark:
    - damped pend + animate :white_check_mark:
    - collisions + animate :white_check_mark:
    - combine :construction: (in progress)
        - change from a ODE based method to a forces based method for calculating momenta :white_check_mark:
            - this will make combining much easier 
        - plot results :white_check_mark:
        - Analyse the plot results :construction:
            - there may be an issue if the timestep is too high in calculating overlaps
                - currently -> 0.01 doesn't work, 0.001 does
            - first few collisions work, things get weird after :confused:
                - Possible solution!!! Is it due to the fact that EC is doesn't conserve energy?
                - second possible solution - maybe due to the large size of the radii in previous iterations?
        
        -put the collision handler, and the calculator without collisions, in seperate functions :white_check_mark:

    - Air resistance seems to have far too great an impact
        - it has been modelled using fluid resistance, co-efficnet maybe be too high, or  wrong units 
        - however, the energy response to damping is as expected 
    - find things to analyse (consv of momentum, energy, how changing time step effects things etc) :construction:
        - added kinetic and potential energy to plotter and they can be anaylses
    - ensure that enough "advanced coding methods" are present
        - read up on what counts as advanced coding methods 
            -Abstract classes, inheritance?


Feels like it's worth writing up about using np.seterr, and try except statements to find what values of ball.position and ball.anchor were causing the runtime warning for overflow
This was a divide by 0 error, which is now solved! 
