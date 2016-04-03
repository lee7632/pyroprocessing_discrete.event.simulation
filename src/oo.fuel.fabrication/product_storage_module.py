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
    facility.  For now, I'm assuming that it also speaks with the fuel fabricator to know how much SNM the fuel
    fabricator is expecting to be delivered across the edge transition.  The product storage will then keep
    track of this cumulative expected weight, since it can't tell how much true weight is actually inside.
    """

    def __init__(self,facility):
        self.inventory = 0
        self.measured_inventory = 0
        self.time_delay = np.loadtxt(facility.process_states_dir+'/process.operation.time.inp',usecols=[1])[3]
        facility_component_class.__init__(self, 0, 0, 0, "product storage", "storage")

    def process_batch(self,facility,batch):
        self.write_to_log(facility,'Processing the final product \n\n\n')
        self.increment_operation_time(facility,self.time_delay)
        self.inventory = self.inventory + batch.weight
        self.expected_weight.storage_batch_gain()

    def inspect(self,facility):
        self.write_to_log(facility,'\nInspecting product storage: \n' + \
                'Expected weight was %f\nMeasured weight was %f \n' %(self.expected_weight.total_weight,
                    self.measured_inventory))
        self.expected_weight.residual_weight = self.inventory
        self.expected_weight.update_total_weight()
        self.measured_inventory = self.inventory
        self.write_to_log(facility,
                '\nExpected weight now is %f \nMeasured weight now is %f\n'%(self.expected_weight.total_weight,
                    self.measured_inventory))
