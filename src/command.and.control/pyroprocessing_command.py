########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.5.March.2015
# v1.2
########################################################################
#
# 
#
########################################################################
#
# Command and control module for the entire pyrprocessing system (eventually).
# This file will set up all the input/output directories and allow for input parameter editing (eventually).
#
########################################################################
#
#
#
####### imports
import os
import shutil
import pyroprocessing_command_functions as command_and_control

def edit_global_vars(file_to_change, dir_of_file, new_root_dir, new_simulation_dir):
    """
    This function rewrites the file_to_change (must include the complete directory in the name from root)
    with a new root directory and simulation directory.

    This is used to streamline running a mainflow program from any folder after a new root directory for
    the source code is determined.
    """
    with open(file_to_change,'r') as input_file, open(dir_of_file + '/new_temp.txt','w') as output_file:
        for line in input_file:
            if line[0:10] == 'root_dir =' or line[0:9] == 'root_dir=':
                output_file.write('root_dir = "%s"\n'%(new_root_dir))
            elif line[0:16] == 'simulation_dir =' or line[0:15] == 'simulation_dir=':
                output_file.write('simulation_dir = "%s/simulation/%s"\n'%(new_root_dir, new_simulation_dir))
            else:
                output_file.write(line)
    shutil.move(dir_of_file + '/new_temp.txt', file_to_change)




########################################################################
#
#
#
####### start command and control
print 'Starting the command and control module for the pyroprocessing system.'
#######
#
####### set the root and lib directory
root_dir= os.getcwd()
#
print 'root dir is: ',root_dir
change_directory_input = raw_input('Would you like to change the root directory (y/n)? ')
#
did_change_root_dir = False
if change_directory_input == 'y':
    root_dir = raw_input('Please enter the desired root directory ')
    did_change_root_dir = True
    
lib_dir=root_dir+'/lib'
#######
#
####### set the simulation directory
simulation_dir=raw_input('set the simulation directory name: ')
#######
#
if did_change_root_dir:
    print '\nChanging global variables in %s'%(root_dir)
    edit_global_vars(root_dir + '/global_vars.py',
            root_dir, root_dir, simulation_dir)



####### set the home directory where all the simulation data will go 
home_dir=command_and_control.write_home_dir(root_dir,lib_dir,simulation_dir)
#######
#
#
#
########################################################################
#
# fuel fabrication module
#
########################################################################
#
#
#
### set the file trees
input_dir,output_dir,edge_transition_dir,failure_distribution_dir,failure_equipment_dir,kmps_dir,process_states_dir,system_false_alarm_dir,data_dir,figures_dir,system_odir,material_flow_odir,inventory_odir,false_alarm_odir,kmps_odir,muf_odir,equipment_failure_odir,system_gdir,material_flow_gdir,inventory_gdir,false_alarm_gdir,kmps_gdir,muf_gdir,equipment_failure_gdir=command_and_control.make_data_dir(home_dir,'fuel.fabrication')
#
### copy lib input files to home directory
command_and_control.copy_input_files(lib_dir,input_dir,'fuel.fabrication',simulation_dir,edge_transition_dir,failure_distribution_dir,failure_equipment_dir,kmps_dir,process_states_dir,system_false_alarm_dir)
#
### make readme file
command_and_control.make_readme(home_dir)
#
### write directory paths for subsystem module 
command_and_control.write_simulation_dir(root_dir,'fuel.fabrication',input_dir,output_dir,edge_transition_dir,failure_distribution_dir,failure_equipment_dir,kmps_dir,process_states_dir,system_false_alarm_dir,data_dir,figures_dir,system_odir,material_flow_odir,inventory_odir,false_alarm_odir,kmps_odir,muf_odir,equipment_failure_odir,system_gdir,material_flow_gdir,inventory_gdir,false_alarm_gdir,kmps_gdir,muf_gdir,equipment_failure_gdir)
#
#
#


########################################################################
#
# end fuel fabrication module
#
########################################################################
#
# EOF
#
########################################################################
