########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.14.July.2015
# v1.0
########################################################################
#
#
#
########################################################################
### Introduction
#
# Functions for the pyropocessing command and control main module.
#
########################################################################
#
#
#
####### imports
import os
import shutil
########################################################################
#
#
#
####### make simulation directories for input, output 
def make_simulation_dir(home_dir,subsystem,simulation_dir):
###
#
###
    print 'creating simulation directories'
###
#
### current directory is /src/command.and.control
#
    input_dir=home_dir+'\\input\\'+subsystem+'\\'+simulation_dir
    output_dir=home_dir+'\\output\\'+subsystem+'\\'+simulation_dir 
###
#
### make simulation directories
    os.makedirs(input_dir)
    os.makedirs(output_dir)
###
#
### make input subdirectories
    edge_transition_dir=make_subdirectory(input_dir,'edge_transition') 
    failure_distribution_dir=make_subdirectory(input_dir,'failure_distribution') 
    failure_equipment_dir=make_subdirectory(input_dir,'failure_equipment') 
    kmps_dir=make_subdirectory(input_dir,'kmps') 
    process_states_dir=make_subdirectory(input_dir,'process_states') 
    system_false_alarm_dir=make_subdirectory(input_dir,'system_false_alarm') 
#
    os.makedirs(edge_transition_dir)
    os.makedirs(failure_distribution_dir)
    os.makedirs(failure_equipment_dir)
    os.makedirs(kmps_dir)
    os.makedirs(process_states_dir)
    os.makedirs(system_false_alarm_dir)
###
#
### make output directories
    data_dir=make_subdirectory(output_dir,'data')
    figures_dir=make_subdirectory(output_dir,'figures')
#
    os.makedirs(data_dir)
    os.makedirs(figures_dir)
###
    return(input_dir,output_dir,edge_transition_dir,failure_distribution_dir,failure_equipment_dir,kmps_dir,process_states_dir,system_false_alarm_dir,data_dir,figures_dir)
#######
#
#
#
####### copy files from default directory to simulation directory
def copy_input_files(home_dir,input_dir,subsystem,simulation_dir,edge_transition_dir,failure_distribution_dir,failure_equipment_dir,kmps_dir,process_states_dir,system_false_alarm_dir):
###
#
###
    print 'copying default input files to '+simulation_dir
###
#
### move to default directory for input data
    default_dir=home_dir+'\\input\\'+subsystem+'\\'+'default'
    os.chdir(default_dir)
###
#
### copy input files from default directory to simulation directory
    copy_file('edge_transition',edge_transition_dir,default_dir)
    copy_file('failure_distribution',failure_distribution_dir,default_dir)
    copy_file('failure_equipment',failure_equipment_dir,default_dir)
    copy_file('kmps',kmps_dir,default_dir)
    copy_file('process_states',process_states_dir,default_dir)
    copy_file('system_false_alarm',system_false_alarm_dir,default_dir)
###
#
### copy readme file for input data
    shutil.copy('readme.md',input_dir)
###
    return()
#######
#
#
#
####### make readme file for the simulation
def make_readme(input_dir):
###
#
### move to simulation directory
    os.chdir(input_dir)
###
#
### open file
    readme_information=open('readme.md','w+')
###
#
### add statement
    readme_statement=raw_input('enter a readme statement for the simulation:')
###
#
### write to file
    readme_information.write(readme_statement)
#
### close file
    readme_information.close()
###
    return()
#######
#
#
#
####### write input and output directories WRITE ALL OF THEM INCLUDING OUTPUT
def write_simulation_dir(input_dir,output_dir):
###
#
### move up a level
# this file needs to be stored outside of the simulation_dir so the module file knows where to look in the first place
    os.chdir('..\\')
###
#
### open file
    simulation_dir_file=open('simulation.dir.inp','w+')
###
#
### write directories
    simulation_dir_file.write(input_dir+','+output_dir+'\\data'+','+output_dir+'\\figures')
###
#
### close file
    simulation_dir_file.close()
###
#
###
    return()
#######
#
#
#
####### make subdirectories
def make_subdirectory(working_dir,subdirectory):
###
#
### make subdirectory
    dummy_subdirectory=working_dir+'\\'+subdirectory
###
    return(dummy_subdirectory)
#######
#
#
#
####### copy input files from the default directory to the simulation directory
def copy_file(local_dir,destination_dir,default_dir):
###
#
### move to local subdirectory
    local_subdir=default_dir+'\\'+local_dir
    os.chdir(local_subdir)
###
#
### copy file
    for files in os.listdir(local_subdir):
	shutil.copy(files,destination_dir)
# end for
###
#
### return to default directory for input data 
    os.chdir(default_dir)
###
    return()
########################################################################
#
# EOF
#
########################################################################
