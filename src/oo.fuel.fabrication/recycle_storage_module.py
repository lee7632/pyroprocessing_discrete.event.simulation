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

    def process_batch(self,facility,fuel_fabricator,batch,heel):
        """
        See class description
        """
        self.write_to_log(facility,'Recycling batch and heel\n\n\n')
        self.increment_operation_time(facility,self.time_delay)
        batch.add_weight(heel.weight)
        #######
        # The fuel fabricator monitors whether or not the recycle storage has accepted and processed materials
        # and then accounts for such to relay the information to the KMP's.  After that, it knows the heel
        # has been cleaned and can reset that given value.
        #######
        fuel_fabricator.expected_batch_weight = fuel_fabricator.expected_batch_weight + \
                fuel_fabricator.expected_heel_weight
        fuel_fabricator.expected_heel_weight = 0
