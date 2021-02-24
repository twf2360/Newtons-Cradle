# What are all the brances in my project?
This markdown file is used to describe all of the branches that can be seen in this repository. They are listed in chronological order, with the most current ones at the top. 

### Main
Main is the "origin" branch. The most up to date, and working methods are all merged into main when they are completed. 

### df
DF branch is used to add a new functionality: saving important stuff to dataframes! 
### fix_collisions
This branch was made to hotfix the problems noticed about the collisions of the balls. It currently changes the code so that the y component of the velocity calculated after the collision is ignored and set to 0. This is obviously not a perfect solution, and will hopefuly be fixed at a later date.

### methods 
The goal of this branch is implement more approximations to the motion of the ball. This is due to the fact that the current method in main relies on the Euler-Cromer approximation. It is unknown whether the weird results seen is due to the problems with the Euler-Cromer approximations, and so as well as extending the complexity and accuracy of the code, this will also test this hypothesis. 

It was discovered that the weird results were due to problems with how the collisions were being handled, not the chosen approximation


### air_resistance
the air resistance branch has been merged into main, and is kept only as a record. This branch was use to add the formula for fluid resistance when the total forces on each ball were calculated. This branch also changed the calculation of the string tension into a seperate function. 

### analysis 
the air resistance branch has been merged into main, and is kept only as a record. The analysis branch was used to generate plotting functions, and especially plotting functions that were dependent on the energy of the system, in order to analyse it's accuracy. 

### adding_collisions 
The adding collisions branch has been merged into main, and is kept only as a record. This branch was used to scale up from a single pendulum to a Newton's Cradle

