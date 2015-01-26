########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.05.December.2014
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
####### set the simulation directory
simulation_dir=raw_input('set the simulation directory:')
#######
#
####### set the home directory
# The rest of the directory changes are relative to the home directory.
home_dir='C:\\ftp\git\\pyroprocessing_discrete.event.simulation\\src\\command.and.control'
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
input_dir,output_dir=command_and_control.make_simulation_dir('fuel.fabrication',simulation_dir)
###
#
### reset home directory
os.chdir(home_dir)
#
### copy default input files to new simulation directory
command_and_control.copy_input_files('fuel.fabrication',simulation_dir)
###
#
### reset home directory
os.chdir(home_dir)
###
#
### make readme file
command_and_control.make_readme(input_dir)
###
#
### write input and output directories
command_and_control.write_simulation_dir(input_dir,output_dir)
###
#
### reset home directory
os.chdir(home_dir)
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
# end modules
#
########################################################################
#
#
#
########################################################################
#
# EOF
#
########################################################################
