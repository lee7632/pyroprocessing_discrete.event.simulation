########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.16.July.2015
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
# Eventually materials will enter the storage buffer in differing quantities at different times.
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
# (3): initialize parameters
# (4): write storage buffer process data 
# (5): storage buffer batch preparation process
# (6): close output files
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
    true_initial_inventory=0 #true inventory used for MUFc calculation
    expected_initial_inventory=0 #expected inventory used for MUFc calculation
###
    print 'Storage buffer initialization complete.'
###
    return(total_batch,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory,true_initial_inventory,expected_initial_inventory)
#
#########################################################################
#
#
#
#########################################################################
#
# (4): write storage buffer process data
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
# (5): storage buffer batch preparation process
#
#######
def storage_transfer(operation_time,total_batch,vertex_delay_time,true_quantity,expected_quantity,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory,true_initial_inventory,expected_initial_inventory):
#######
    print 'Prepare batch in Storage Buffer for transfer.',total_batch,'kg','\n\n'    
    operation_time=operation_time+vertex_delay_time
#
    true_quantity=total_batch
    expected_quantity=total_batch
#
    true_storage_inventory=true_storage_inventory-true_quantity
    expected_storage_inventory=expected_storage_inventory-expected_quantity
#
    true_system_inventory=true_system_inventory+true_quantity
    expected_system_inventory=expected_system_inventory+expected_quantity
#
    true_initial_inventory=true_quantity
    expected_initial_inventory=expected_quantity
###
    return(operation_time,true_quantity,expected_quantity,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory,true_initial_inventory,expected_initial_inventory)
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
# EOF
#
########################################################################
