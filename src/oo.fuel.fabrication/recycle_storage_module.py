########################################################################
# Malachi Tolman
# @tolman42
# rev.29.February.2016
########################################################################
#
# See class description
#
########################################################################
import pdb
import numpy as np
from facility_component_module import facility_component_class
from batch_module import batch_class

class recycle_storage_class(facility_component_class):
    """
    The recycle storage is the unit that takes in the batch and the heel when equipment failure occurs.
    It takes in the two and recycles them into a single batch to be sent back to the melter.

    It also indefinitely holds onto SNM whenever an alarm is triggered.

    When a system alarm is set off, it takes in only the heel, takes time to process it, then sends it back
    to the melter to go through the rest of the fuel fabrication process.
    
    As of thus far, it does not undergo any equipment failure, and it doesn't lose any material since it is
    responsible for recovring such.
    """

    def __init__(self,facility):
        self.time_delay = np.loadtxt(facility.process_states_dir+'/process.operation.time.inp',usecols=[1])[3]
        self.inventory = 0
        self.measured_inventory = 0
        facility_component_class.__init__(self, 0, 0, 0, "recycle_storage", "storage", facility.inventory_odir)

    def process_batch(self,facility,batch):
        """
        Here the recycle storage recycles all of its stored materials into one batch.

        --NOTE--
        A batch must be passed in becuase I ran into coding problems when creating a new batch class here
        and trying to return such.  The address change does not carry over from function to function for
        some weird reason, thus the batch being passed in is a coding work around.
        """
        self.write_to_log(facility,'Recycling batch and heel\n\n\n')
        self.increment_operation_time(facility,self.time_delay)
        batch.weight = 0
        batch.add_weight( self.inventory )
        batch.description = "recycled batch"
        self.expected_weight.batch_weight = self.expected_weight.residual_weight
        self.inventory = 0
        self.expected_weight.storage_batch_loss()
        self.measured_inventory = 0

        self.data_output.storage_output(facility, self)
        
    def store_batch(self,facility,batch):
        """
        This takes the batch and puts it into temporary storage.  Under the current code structure,
        everything in here soon gets sent either back into the melter (in the case of equpiment failure)
        or gets shipped back into the storage buffer (as is the case with facility alarms).
        """
        self.write_to_log(facility,'Storing %s in recycle storage \n\n\n' %(batch.description))
        self.increment_operation_time(facility,self.time_delay)
        self.inventory = self.inventory + batch.weight
        self.expected_weight.storage_batch_gain()

        self.data_output.storage_output(facility, self)
