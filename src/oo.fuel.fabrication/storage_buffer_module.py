########################################################################
# Malachi Tolman
# @tolman42
# rev.4.April.2016
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
    """
    The storage buffer contains the materials to be processed by the fuel fabrication subsystem.
    Uranium, TRUs with REPFs, and Zr arrive in the buffer at different times in different quantities.
    Fuel fabrication processes this material into a metal alloy fuel slug with a prescribed batch size.

    Currently, the simulation starts off with a fixed amount of unprocessed material in the buffer
    over the entire facility operation.
    Eventually materials will enter the storage buffer in differing quantities at different times.

    #######
    # Variables 
    #######
    batch_size = weight of batch in kg that the storage buffer will make each time

    inventory = actual amount of SNM that the storage buffer is holding in kg

    measured_inventory = the amount of SNM that the storage buffer thinks it has according to what is reported
    by the kmp.

    time_delay = amount of time it takes the storage buffer to create a batch
    """

    def __init__(self,facility,initial_inventory):
        self.batch_size = np.loadtxt(facility.process_states_dir+'/batch.inp')
        self.inventory = initial_inventory
        self.measured_inventory = initial_inventory 
        self.time_delay = np.loadtxt(facility.process_states_dir+'/process.operation.time.inp',usecols=[1])[0]
        facility_component_class.__init__(self, self.inventory, self.batch_size, self.inventory, 
                "storage buffer", "storage")

    def batch_preparation(self,facility):
        """
        The storage buffer takes some SNM from its inventory, creates it into a batch, then passes such on
        to the next part.
        """
        self.write_to_log(facility,'Prepare batch in Storage Buffer for transfer: %.1f kg \n\n\n'%(self.batch_size))
        self.increment_operation_time(facility,self.time_delay)
        self.inventory = self.inventory - self.batch_size
        #######
        # This variable must be set in order for the edge transition to function properly 
        # since it is the first facility component to create the batch
        #######
        self.expected_weight.batch_weight = self.batch_size
        self.expected_weight.storage_batch_loss()

        return batch_class(self.batch_size,"batch")

    def inspect(self,facility):
        """
        Routine called when an alaram is set off.  This represents the personnel inspecting the storage buffer
        to verify how much SNM is actually there.  This updates the expected and measured weights.
        """
        self.write_to_log(facility,'\nInspecting storage buffer: \n' + \
                'Expected weight was %.4f\nMeasured weight was %.4f \n' %(self.expected_weight.total_weight,
                    self.measured_inventory))
        self.expected_weight.residual_weight = self.inventory
        self.expected_weight.update_total_weight()
        self.measured_inventory = self.inventory
        self.write_to_log(facility,
                '\nExpected weight now is %.4f \nMeasured weight now is %.4f\n'%(self.expected_weight.total_weight,
                    self.measured_inventory))
