########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.15.July.2015
# v1.0
########################################################################
#
#
#
########################################################################
### Introduction
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
print 'Make sure the home_dir was coded into this file.'
raw_input('Hit a key to continue or break to code the home_dir ')
#######
#
####### set the root directory
root_dir=raw_input('set the root directory. use "\\\\" if on Windows: ')
#######
#
####### set the simulation directory
simulation_dir=raw_input('set the simulation directory: ')
#######
#
####### set the home directory
home_dir='C:\\root\git\\pyroprocessing_discrete.event.simulation'
command_and_control.write_home_dir(root_dir,home_dir)
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
input_dir,output_dir,edge_transition_dir,failure_distribution_dir,failure_equipment_dir,kmps_dir,process_states_dir,system_false_alarm_dir,data_dir,figures_dir,system_odir,material_flow_odir,inventory_odir,false_alarm_odir,kmps_odir,muf_odir,melter_failure_odir,system_gdir,material_flow_gdir,inventory_gdir,false_alarm_gdir,kmps_gdir,muf_gdir,melter_failure_gdir=command_and_control.make_simulation_dir(home_dir,'fuel.fabrication',simulation_dir)
###
#
### copy default input files to new simulation directory
command_and_control.copy_input_files(home_dir,input_dir,'fuel.fabrication',simulation_dir,edge_transition_dir,failure_distribution_dir,failure_equipment_dir,kmps_dir,process_states_dir,system_false_alarm_dir)
###
#
### make readme file
command_and_control.make_readme(input_dir)
###
#
### write directory paths for subsystem module 
command_and_control.write_simulation_dir(home_dir,'fuel.fabrication',input_dir,output_dir,edge_transition_dir,failure_distribution_dir,failure_equipment_dir,kmps_dir,process_states_dir,system_false_alarm_dir,data_dir,figures_dir,system_odir,material_flow_odir,inventory_odir,false_alarm_odir,kmps_odir,muf_odir,melter_failure_odir,system_gdir,material_flow_gdir,inventory_gdir,false_alarm_gdir,kmps_gdir,muf_gdir,melter_failure_gdir)
###
#
###
# eventual control panel for facility design
###
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
