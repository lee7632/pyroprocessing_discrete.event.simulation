########################################################################
# Malachi Tolman
# @tolman42
# rev.25.February.2016
########################################################################
#
# This program will simulate the fuel fabrication process.
#
# For now, it simply extracts a batch from the storage buffer, sends
# the batch to the melter where some of the material is left behind,
# goes to the trimmer, then gets stored in product storage.
#
# Key measurement points measure the weight of the batch between each
# component, and edge transitions carry the batch from component to 
# component.
#
# Variables for the most part are stored in the faciliy component in
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
from storage_buffer_module import storage_buffer_class
from edge_transition_module import edge_transition_class
from key_measurement_point_module import key_measurement_point_class as kmp_class
from melter_module import melter_class
from trimmer_module import trimmer_class
from product_storage_module import product_storage_class

######## 
# initialize objects to be used
######## 
facility = facility_command_class(global_vars.root_dir,'fuel.fabrication')
storage_buffer = storage_buffer_class(facility)
edge = edge_transition_class(facility,0)
kmp0 = kmp_class(facility,0)
melter= melter_class(facility)
kmp1 = kmp_class(facility,1) 
trimmer = trimmer_class(facility)
kmp2 = kmp_class(facility,2)
product_storage = product_storage_class(facility)


######
# Process the materials  
######
facility.write_to_log('Start facility operation\n')
facility.write_to_log('Starting campaign %i at time: %f days\n\n'%(facility.total_campaign, facility.operation_time))

batch = storage_buffer.batch_preparation(facility)
edge.edge_transition(facility)
kmp0.process_batch(facility,batch)
edge.edge_transition(facility)
melter.process_batch(facility,batch)
edge.edge_transition(facility)
kmp1.process_batch(facility,batch)
edge.edge_transition(facility)
trimmer.process_batch(facility,batch)
edge.edge_transition(facility)
kmp2.process_batch(facility,batch)
edge.edge_transition(facility)
product_storage.process_batch(facility,batch)
facility.end_of_campaign(storage_buffer,kmp0,kmp2,product_storage)

facility.close_files()
