**pyroprocessing_command_functions.py**
<br>
(1): make simulation directories
<br>
(2): copy files from default directory to simulation directory
<br>
(3): make readme file for the simulation
<br>
(4): write directory paths for subsystem module 
<br>
(5): make subdirectories
<br>
(6): copy input files from the default directory to the simulation directory
<br>
(7): write home directory information for pyroprocessing simulation
<br><br><br>
**io_functions.py**
<br>
(1): get simulation directories
<br><br>
input regime
<br>
(2a): read system operation input data
<br>
(2b): read storage buffer input data
<br>
(2c): read melter input data
<br>
(2d): read system false alarm input data
<br>
(2e): read edge transition input data
<br>
(2f): read kmp input data
<br><br>
output regime
<br>
(3a): open system output files
<br>
(3b): open material flow output files
<br>
(3c): open inventory output files
<br>
(3d): open system false alarm output files
<br>
(3e): open kmp output files
<br>
(3f): open melter failure output files
<br>
(3g): open muf output files
<br><br>
initialization regime
<br>
(4a): initialize system parameters
<br>
(4b): initialize material flow parameters
<br>
(4c): initialize inventory parameters
<br>
(4d): initialize system false alarm parameters
<br>
(4e): initialize melter failure parameters
<br>
(4f): initialize muf parameters
<br><br>
data writing regime
<br>
(5a): write system operation 
<br>
(5b): write material flow
<br>
(5c): write inventory
<br>