########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.03.August.2015
# v1.0
########################################################################
#
#
#
########################################################################
#
# Functions for the pyropocessing command and control main module.
#
########################################################################
#
# imports
#
import os
import shutil
#
########################################################################
#
# function list
#
# (1): make data directories
# (2): copy files from lib directory to home directory
# (3): make readme file for the simulation
# (4): write directory paths for subsystem module 
# (5): make subdirectories
# (6): copy input files from the default directory to the simulation directory
# (7): write home directory information for pyroprocessing simulation
#
########################################################################
#
#
#
########################################################################
#
# (1): make data directories
#
#######
def make_data_dir(home_dir,subsystem):
#######
#
###
    print 'creating data directories'
#
###
    os.chdir(home_dir)
    os.makedirs(subsystem)
#
    input_dir=home_dir+'/'+subsystem+'/input'
    output_dir=home_dir+'/'+subsystem+'/output' 
#
### make simulation directories
    os.makedirs(input_dir)
    os.makedirs(output_dir)
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
#
### make output directories
    data_dir=make_subdirectory(output_dir,'data')
    figures_dir=make_subdirectory(output_dir,'figures')
#
    os.makedirs(data_dir)
    os.makedirs(figures_dir)
#
### make output subdirectories
    system_odir=make_subdirectory(data_dir,'system')
    material_flow_odir=make_subdirectory(data_dir,'material.flow')
    inventory_odir=make_subdirectory(data_dir,'inventory')
    false_alarm_odir=make_subdirectory(data_dir,'false.alarm')
    kmps_odir=make_subdirectory(data_dir,'kmps')
    muf_odir=make_subdirectory(data_dir,'muf')
    equipment_failure_odir=make_subdirectory(data_dir,'equipment.failure')
#
    system_gdir=make_subdirectory(figures_dir,'system')
    material_flow_gdir=make_subdirectory(figures_dir,'material.flow')
    inventory_gdir=make_subdirectory(figures_dir,'inventory')
    false_alarm_gdir=make_subdirectory(figures_dir,'false.alarm')
    kmps_gdir=make_subdirectory(figures_dir,'kmps')
    muf_gdir=make_subdirectory(figures_dir,'muf')
    equipment_failure_gdir=make_subdirectory(figures_dir,'equipment.failure')
#
    os.makedirs(system_odir)
    os.makedirs(material_flow_odir)
    os.makedirs(inventory_odir)
    os.makedirs(false_alarm_odir)
    os.makedirs(kmps_odir)
    os.makedirs(muf_odir)
    os.makedirs(equipment_failure_odir)
#
    os.makedirs(system_gdir)
    os.makedirs(material_flow_gdir)
    os.makedirs(inventory_gdir)
    os.makedirs(false_alarm_gdir)
    os.makedirs(kmps_gdir)
    os.makedirs(muf_gdir)
    os.makedirs(equipment_failure_gdir)
###
    return(input_dir,output_dir,edge_transition_dir,failure_distribution_dir,failure_equipment_dir,kmps_dir,process_states_dir,system_false_alarm_dir,data_dir,figures_dir,system_odir,material_flow_odir,inventory_odir,false_alarm_odir,kmps_odir,muf_odir,equipment_failure_odir,system_gdir,material_flow_gdir,inventory_gdir,false_alarm_gdir,kmps_gdir,muf_gdir,equipment_failure_gdir)
########################################################################
#
# (2): copy files from lib directory to simulation directory
#
#######
def copy_input_files(lib_dir,input_dir,subsystem,simulation_dir,edge_transition_dir,failure_distribution_dir,failure_equipment_dir,kmps_dir,process_states_dir,system_false_alarm_dir):
#######
#
###
    default_dir=lib_dir+'/'+subsystem
    os.chdir(default_dir)
#
### copy input files from lib directory to simulation directory
    copy_file('edge_transition',edge_transition_dir,default_dir)
    copy_file('failure_distribution',failure_distribution_dir,default_dir)
    copy_file('failure_equipment',failure_equipment_dir,default_dir)
    copy_file('kmps',kmps_dir,default_dir)
    copy_file('process_states',process_states_dir,default_dir)
    copy_file('system_false_alarm',system_false_alarm_dir,default_dir)
#
### copy readme file for input data
    shutil.copy('readme.md',input_dir)
###
    return()
########################################################################
#
# (3): make readme file for the simulation
#
#######
def make_readme(home_dir):
#######
#
### move to simulation directory
    os.chdir(home_dir)
#
### open file
    readme_information=open('readme.md','w+')
#
### add statement
    readme_statement=raw_input('enter a readme statement for the simulation: ')
#
### write to file
    readme_information.write(readme_statement)
#
### close file
    readme_information.close()
###
    return()
########################################################################
#
# (4): write directory paths for subsystem module 
#
#######
def write_simulation_dir(root_dir,subsystem,input_dir,output_dir,edge_transition_dir,failure_distribution_dir,failure_equipment_dir,kmps_dir,process_states_dir,system_false_alarm_dir,data_dir,figures_dir,system_odir,material_flow_odir,inventory_odir,false_alarm_odir,kmps_odir,muf_odir,equipment_failure_odir,system_gdir,material_flow_gdir,inventory_gdir,false_alarm_gdir,kmps_gdir,muf_gdir,equipment_failure_gdir):
#######
#
### move to subsystem directory
# the file has to be located here so the subsystem.py knows where to look
    os.chdir(root_dir+'/simulation/meta.data') 
#
### open file
    simulation_dir_filename=subsystem+'_simulation.dir.inp'
    simulation_dir_file=open(simulation_dir_filename,'w+')
#
### write directories
    simulation_dir_file.write(input_dir+','+output_dir+','+edge_transition_dir+','+failure_distribution_dir+','+failure_equipment_dir+','+kmps_dir+','+process_states_dir+','+system_false_alarm_dir+','+data_dir+','+figures_dir+','+system_odir+','+material_flow_odir+','+inventory_odir+','+false_alarm_odir+','+kmps_odir+','+muf_odir+','+equipment_failure_odir+','+system_gdir+','+material_flow_gdir+','+inventory_gdir+','+false_alarm_gdir+','+kmps_gdir+','+muf_gdir+','+equipment_failure_gdir)
#
### close file
    simulation_dir_file.close()
###
    return()
########################################################################
#
# (5): make subdirectories
#
#######
def make_subdirectory(working_dir,subdirectory):
#######
#
### make subdirectory
    dummy_subdirectory=working_dir+'/'+subdirectory
###
    return(dummy_subdirectory)
########################################################################
#
# (6): copy input files from the default directory to the simulation directory
#
#######
def copy_file(local_dir,destination_dir,default_dir):
#######
#
### move to local subdirectory
    local_subdir=default_dir+'/'+local_dir
    os.chdir(local_subdir)
#
### copy file
    for files in os.listdir(local_subdir):
	shutil.copy(files,destination_dir)
# end for
#
### return to default directory for input data 
    os.chdir(default_dir)
###
    return()
########################################################################
#
# (7): write home directory information for pyroprocessing simulation
#
#######
def write_home_dir(root_dir,lib_dir,simulation_dir):
#######
#
### check for simulation directory 
#
    os.chdir(root_dir)
    dir_check=os.path.isdir(root_dir+'/simulation') 
#
    if(dir_check==False):
	os.makedirs('simulation')
# end
#
### set home directory where all the simulation data will go
    home_dir=root_dir+'/simulation/'+simulation_dir
#
### store directory path information
    os.chdir('simulation')
#
    dir_check=os.path.isdir('meta.data')
#
    if(dir_check==False):
	os.makedirs('meta.data') #this directory will store the simulation directory information for process modules
# end
    os.makedirs(simulation_dir)
    os.chdir('meta.data')
#
    home_dir_file=open('home.dir.inp','w+')
    home_dir_file.write(home_dir)
    home_dir_file.close()
###
    return(home_dir)
########################################################################
#
# EOF
#
########################################################################
