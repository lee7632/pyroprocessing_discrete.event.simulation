########################################
**DES modeling for the pyroprocessing system**
########################################

########################################
**Discrete event simulation description**
<br>In DES, each 'event' is a 'vertex.'
<br>There are state changes and/or parameters associated with a vertex.
<br>State changes are assigning values to a variable or solving an equation.
<br>Parameters are variables needed to make the state change.
<br>DES steps discretely in time through each vertex via an 'edge.'
<br>At each vertex, the equations are run and the state variables change.
<br>The edges are dynamic and provide logical relationships between events.
<br>DES should readily lend itself to the modeling of batch systems like pyroprocessing.
<br>Python is a natural fir for DES due to its modularity.
########################################

########################################
**Fuel fabrication v1.0**
<br>This is a 'bare bones' build, just to get the model working.
<br>Many assumptions are made and listed in the comments.
########################################

########################################
**Fuel fabrication v1.1**
<br>Upgraded to simulate the melter failure with normal distribution.
########################################

########################################
**Fuel fabrication v1.2**
<br>Upgraded to simulate the melter failure with Weibull distribution.
<br>This version is ready for test cases. 
########################################

########################################
**Command and control v1.0**
<br>Controls directory creation and default input file transfers for all modules.
########################################
