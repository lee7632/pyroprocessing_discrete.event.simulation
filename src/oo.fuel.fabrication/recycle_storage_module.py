########################################################################
# Malachi Tolman
# @tolman42
# rev.29.February.2016
########################################################################
#
# See class description
#
########################################################################
import numpy as np
from facility_component_module import facility_component_class

class recycle_storage_class(facility_component_class):
    """
    The recycle storage is the unit that takes in the batch and the heel when equipment failure occurs.
    It takes in the two and recycles them into a single batch to be sent back to the melter.

    When a system alarm is set off, it takes in only the heel, takes time to process it, then sends it back
    to the melter to go through the rest of the fuel fabrication process.
    
    As of thus far, it does not undergo any equipment failure, and it doesn't lose any material since it is
    responsible for recovring such.
    """

    def __init__(self,facility):
        self.time_delay = np.loadtxt(facility.process_states_dir+'/process.operation.time.inp',usecols=[1])[3]
        self.inventory = 0
        self.measured_inventory = 0
        facility_component_class.__init__(self, 0, 0, 0, "recycle storage", "storage")

    def process_batch(self,facility,fuel_fabricator,batch):
        """
        See class description
        """
        self.write_to_log(facility,'Recycling batch and heel\n\n\n')
        self.increment_operation_time(facility,self.time_delay)
        batch.weight = self.inventory
        self.expected_weight.batch_weight = self.expected_weight.residual_weight
        self.inventory = 0
        self.measured_inventory = 0
        self.expected_weight.storage_batch_loss()
        
    def store_batch(self,facility,batch):
        """
        This is called whenever the recycle storage receives a batch of any size (whether a full batch itself
        or just the heel cleaned out from the melter).  It stores the batch until it's called upon to process
        everything it has in storage.
        """
        self.write_to_log(facility,'Recycle storage receiving batch \n\n\n')
        self.increment_operation_time(facility,self.time_delay)
        self.inventory = self.inventory + batch.weight
        self.expected_weight.storage_batch_gain()
