########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.20.October.2015
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
########################################################################
#
#
#
####### start command and control
print 'Starting the command and control module for the pyroprocessing system.'
#######
#
####### set the root and lib directory
root_dir='/home/usr/borrelli/pyroprocessing_discrete.event.simulation'
lib_dir=root_dir+'/lib'
#
print 'root dir is: ',root_dir
print 'root dir is hard coded into each of the mainflow files'
raw_input('hit a key to continue or break to change root dir')
#######
#
####### set the simulation directory
simulation_dir=raw_input('set the simulation directory name: ')
#######
#
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
