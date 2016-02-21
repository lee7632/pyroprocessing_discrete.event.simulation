########################################################################
# Malachi Tolman
# @tolman42
# 18.February.2016
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
from facility_component_module import facility_component_class
from facility_vars_module import facility_vars_class as facility_vars
#
########################################################################
#
#
#
#######

class storage_buffer_class(facility_component_class):

    def batch_preparation(self,facility_vars,time_delay,batch,true_quantity,expected_quantity,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory,true_initial_inventory,expected_initial_inventory):

        #log_file.write('Prepare batch in Storage Buffer for transfer: %.1f kg\n\n'%(batch))
        self.write_to_log(facility_vars,'Prepare batch in Storage Buffer for transfer: %.1f kg\n\n'%(batch))
        #operation_time=operation_time+time_delay
        self.increment_operation_time(facility_vars,time_delay)
        true_quantity=batch
        expected_quantity=batch
        true_storage_inventory=true_storage_inventory-true_quantity
        expected_storage_inventory=expected_storage_inventory-expected_quantity
        true_system_inventory=true_system_inventory+true_quantity
        expected_system_inventory=expected_system_inventory+expected_quantity
        true_initial_inventory=true_quantity
        expected_initial_inventory=expected_quantity
        
        return(true_quantity,expected_quantity,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory,true_initial_inventory,expected_initial_inventory)

    def close_files(batch_output,true_storage_inventory_output,expected_storage_inventory_output,true_system_inventory_output,expected_system_inventory_output):
        batch_output.close()
        campaign_output.close()
        true_storage_inventory_output.close()
        expected_storage_inventory_output.close()
        true_system_inventory_output.close()
        expected_system_inventory_output.close()
        
        return(batch_output,true_storage_inventory_output,expected_storage_inventory_output,true_system_inventory_output,expected_system_inventory_output)
    
########################################################################
#
# EOF
#
########################################################################
