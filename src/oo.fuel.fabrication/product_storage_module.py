########################################################################
# Malachi Tolman
# @tolman42
# rev.25.February.2016
########################################################################
# 
# See class description
#
########################################################################
import numpy as np
from facility_component_module import facility_component_class
from batch_module import batch_class

class product_storage_class(facility_component_class):
    """
    The product storage is the facility component that stores the final product of the entire pyroprocessing
    facility. It keeps tabs on how much it is holding onto via the update from the kmp paired with it.  It 
    also keeps track of the cumulative expected weight passed in from the other components, since such is
    used at the end of campaign inspections.

    #######
    # Variables 
    #######
    inventory = actual amount of SNM that the storage buffer is holding in kg

    measured_inventory = the amount of SNM that the storage buffer thinks it has according to what is reported
    by the kmp.

    time_delay = amount of time it takes the storage buffer to create a batch
    """

    def __init__(self,facility):
        self.inventory = 0
        self.measured_inventory = 0
        self.time_delay = np.loadtxt(facility.process_states_dir+'/process.operation.time.inp',usecols=[1])[3]
        facility_component_class.__init__(self, 0, 0, 0, "product storage", "storage")

    def process_batch(self,facility,batch):
        """
        The final product is added to the inventory, and the expected weight is updated.
        """
        self.write_to_log(facility,'Processing the final product \n\n\n')
        self.increment_operation_time(facility,self.time_delay)
        self.inventory = self.inventory + batch.weight
        self.expected_weight.storage_batch_gain()

    def inspect(self,facility):
        """
        Routine called when an alaram is set off.  This represents the personnel inspecting the storage buffer
        to verify how much SNM is actually there.  This updates the expected and measured weights.
        """
        self.write_to_log(facility,'\nInspecting product storage: \n' + \
                'Expected weight was %.4f\nMeasured weight was %.4f \n' %(self.expected_weight.total_weight,
                    self.measured_inventory))
        self.expected_weight.residual_weight = self.inventory
        self.expected_weight.update_total_weight()
        self.measured_inventory = self.inventory
        self.write_to_log(facility,
                '\nExpected weight now is %.4f \nMeasured weight now is %.4f\n\n'%(self.expected_weight.total_weight,
                    self.measured_inventory))
