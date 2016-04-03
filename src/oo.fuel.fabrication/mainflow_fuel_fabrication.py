########################################################################
# Malachi Tolman
# @tolman42
# rev.27.February.2016
########################################################################
#
# This program will simulate the fuel fabrication process.
#
# True to the system diagram, U and TRU will get fed into the fuel
# fabricator.  It then processes the SNM (special nuclear material)
# into metal slugs that are stored in product storage.  One batch that moves
# from the storage buffer through the system to product storage counts
# as a single campaign.  Once that occurs, a brief end of campaign
# inspection is held.
#
# Variables for the most part are stored in the facility component in
# charge of operations pertaining to that state variable, altough
# some variables important to the whole facility are stored in
# the facility_command module that is passed from component to component.
#
########################################################################
#
# Imports
#
########################################################################
import numpy as np
import global_vars
from facility_command_module import facility_command_class
from storage_unit_module import storage_unit_class
from edge_transition_module import edge_transition_class
from fuel_fabricator_module import fuel_fabricator_class
from final_storage_unit_module import final_storage_unit_class
from key_measurement_point_module import key_measurement_point_class as kmp_class

np.random.seed(0)

######## 
# initialize objects to be used
######## 
facility = facility_command_class(global_vars.root_dir,'fuel.fabrication')
storage_unit = storage_unit_class(facility)
edge = edge_transition_class(facility,0)
fuel_fabricator = fuel_fabricator_class(facility)
final_storage_unit = final_storage_unit_class(facility) 


######
# Process the materials  
######
facility.write_to_log('Start facility operation\n')
while facility.operation_time <= facility.total_operation_time:
    facility.write_to_log('Starting campaign: %i at time:  %.4f  days \n\n' \
            %(facility.total_campaign, facility.operation_time))
    
    batch = storage_unit.batch_preparation(facility)
    edge.edge_transition(facility, batch, storage_unit.kmp, fuel_fabricator.melter)
    fuel_fabricator.process_batch(facility,batch)
    edge.edge_transition(facility, batch, fuel_fabricator.trimmer, final_storage_unit.kmp)
    final_storage_unit.process_batch(facility,batch)
    facility.end_of_campaign(storage_unit,fuel_fabricator,final_storage_unit, batch)
    
facility.close_files()
