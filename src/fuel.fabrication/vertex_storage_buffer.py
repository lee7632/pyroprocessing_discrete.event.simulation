########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.16.February.2015
########################################################################
# 
# Storage buffer vertex
# 
########################################################################
#
# The storage buffer contains the materials to be processed by the fuel fabrication subsystem.
# Uranium, TRUs with REPFs, and Zr arrive in the buffer at different times in different quantities.
# Fuel fabrication processes this material into a metal alloy fuel slug with a prescribed batch size.
#
########################################################################
#
# Currently, the simulation starts off with a fixed amount of unprocessed material in the buffer over the entire facility operation.
#
########################################################################
#
# imports
#
import os
#
########################################################################
#
# function list
#
# (1): read input data
# (2): open output files
# (3): initialize parameters
# (4): write system and material flow data
# (5): storage buffer preparation
# (6): close output files
#
########################################################################
#
#
#
########################################################################
#
# (1): read input data
#
#######
def input_parameters(home_dir,input_dir,output_data_dir):
#######
#
### go to input file directory
    os.chdir(input_dir)
###
#
### open data files
    batch=numpy.loadtxt('process_states\\batch.inp') #batch size
    unprocessed_storage_inventory=numpy.loadtxt('process_states\\unprocessed.storage.inventory.inp') #total quantity of material in storage buffer at T = 0
###
#
### go back to home directory
    os.chdir(home_dir)
###
    print 'Storage buffer parameters loaded.','\n'
###
    return(batch,unprocessed_storage_inventory)
#
########################################################################
#
#
#
########################################################################
#
# (2): open output files
#
#######
def open_output_files(home_dir,output_data_dir):
#######
#
### change directory
    os.chdir(output_data_dir)
###
#
### open files: the functions for writing data to the files explain what is in each of them since the variables are listed
    true_storage_inventory_output=open('process_states\\true.storage.inventory.out','w+')
    expected_storage_inventory_output=open('process_states\\expected.storage.inventory.out','w+')
    true_system_inventory_output=open('process_states\\true.system.inventory.out','w+')
    expected_system_inventory_output=open('process_states\\expected.system.inventory.out','w+')
    batch_output=open('process_states\\total.batch.out','w+')
###
#
### return to home directory
    os.chdir(home_dir)
###
    return(true_storage_inventory_output,expected_storage_inventory_output,true_system_inventory_output,expected_system_inventory_output,batch_output)
#
########################################################################
#
#
#
########################################################################
#
# (3): initialize parameters
#
#######
def initialize_parameters(unprocessed_storage_inventory):
#######
#
    total_batch=1 #total batches processed over facility operation
    true_storage_inventory=unprocessed_storage_inventory #true quantity of unprocessed material over facility operation
    expected_storage_inventory=unprocessed_storage_inventory #expected quantity of unprocessed material over facility operation
    true_system_inventory=0 #true quantity of material transferred out of storage buffer over facility operation
    expected_system_inventory=0 #expected quantity of material transferred out of storage buffer over facility operation
###
    print 'Storage buffer initialization complete.'
###
    return(total_batch,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory)
#
#########################################################################
#
#
#
#########################################################################
#
# (4): write system and material flow data
#
#######
def write_output(operation_time,total_batch,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory,batch_output,true_storage_inventory_output,expected_storage_inventory_output,true_system_inventory_output,expected_system_inventory_output):
#######
#
    batch_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%i'%total_batch)+'\n')
    true_storage_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_storage_inventory)+'\n')
    expected_storage_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_storage_inventory)+'\n')
    true_system_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_system_inventory)+'\n')
    expected_system_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_system_inventory)+'\n')
###
    return(batch_output,true_storage_inventory_output,expected_storage_inventory_output,true_system_inventory_output,expected_system_inventory_output)
#
########################################################################
#
#
#
########################################################################
#
# (5): storage buffer preparation
#
#######
def storage_transfer(operation_time,total_batch,delay,true_quantity,expected_quantity,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory):
#######
    print 'Prepare batch in Storage Buffer for transfer.',total_batch,'kg','\n\n'    
    operation_time=operation_time+delay
#
    true_quantity=total_batch
    expected_quantity=total_batch
#
    true_storage_inventory=true_storage_inventory-true_quantity
    expected_storage_inventory=expected_storage_inventory-expected_quantity
#
    true_system_inventory=true_system_inventory+true_quantity
    expected_system_inventory=expected_system_inventory+expected_quantity
###
    return(operation_time,true_quantity,expected_quantity,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory)
########################################################################
#
#
#
########################################################################
#
# (6): close output files
#
#######
def close_files(batch_output,true_storage_inventory_output,expected_storage_inventory_output,true_system_inventory_output,expected_system_inventory_output):
#######
#
    batch_output.close()
    campaign_output.close()
    true_storage_inventory_output.close()
    expected_storage_inventory_output.close()
    true_system_inventory_output.close()
    expected_system_inventory_output.close()
###
    return(batch_output,true_storage_inventory_output,expected_storage_inventory_output,true_system_inventory_output,expected_system_inventory_output)
#
########################################################################
#
#      EOF
#
########################################################################
