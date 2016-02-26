########################################################################
# Malachi Tolman
# @tolman42
# rev.25.February.2016
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
# Currently, the simulation starts off with a fixed amount of unprocessed material in the buffer
# over the entire facility operation.
# Eventually materials will enter the storage buffer in differing quantities at different times.
#
########################################################################
import numpy as np
from facility_component_module import facility_component_class
from batch_module import batch_class

class storage_buffer_class(facility_component_class):

    def __init__(self,facility):
        self.batch_size = np.loadtxt(facility.process_states_dir+'/batch.inp')
        self.inventory = facility.initial_inventory
        self.time_delay = np.loadtxt(facility.process_states_dir+'/process.operation.time.inp',usecols=[1])[0]

    def batch_preparation(self,facility):
        self.write_to_log(facility,'Prepare batch in Storage Buffer for transfer: %.1f kg\n\n\n'%(self.batch_size))
        self.increment_operation_time(facility,self.time_delay)
        self.inventory = self.inventory - self.batch_size

        return batch_class(self.batch_size,self.batch_size)
        

