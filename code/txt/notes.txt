This page is just to keep track of things that need doing, and random thoughts:
        - slightly unsure about how the collisions program will deal with corners, however that won't be relevant to the larger project anyway
        - the original ODEINT solutions have been discarded.
    

- to do:
    - simple pend   (done)
    - animate simple pend (done)
    - damped pend + animate (done)
    - collisions + animate (done)
    - combine (in progress)
        - currently changing from a ODE based method to a forces based method for calculating momenta
            - this will make combining much easier (done)
        - plot to check if results are sensible (done, animation needs more work)
        - add an enumerate so that balls have a label?
        - there may be an issue if the timestep is too high in calculating overlaps
            - currently -> 0.01 doesn't work, 0.001 does
        -put the collision handler, and the calculator without collisions, in seperate functions (done)


    - find things to analyse (consv of momentum, energy, how changing time step effects things etc)
    - ensure that enough "advanced coding methods" are present
        - read up on what counts as advanced coding methods 
            -Abstract classes, inheritance?


Feels like it's worth writing up about using np.seterr, and try except statements to find what values of ball.position and ball.anchor were causing the runtime warning for overflow
