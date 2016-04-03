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
        self.recycle_expected_weight = 0
        self.recycle_batches = []
        facility_component_class.__init__(self, 0, 0, 0, "recycle storage", "storage")

    def process_batch(self,facility,batch):
        """
        This is the recycling part of the recycle storage, if you indicate which batches need to be processed,
        it will take those out of storage, put them into one batch, and return such.

        Note the it will store all of the batches into the first one passed in the array.  I wanted to pass back
        a new batch, but Python is a bit of a pill when it comes to manipulating object references.

        Note that it can only take the expected weight to be the actual weight.  This is more a convenient work
        around to make things function under the moment, but I'm going to assume that this particular storage unit
        has radiation detection to determine how much there actually is.  Although I will be updating the measured
        inventory via the kmp as usual.
        """
        self.write_to_log(facility,'Recycling batch and heel\n\n\n')
        self.increment_operation_time(facility,self.time_delay)
        for batch_to_recycle in self.recycle_batches:
            if batch_to_recycle.description != batch.description:
                batch.add_weight(batch_to_recycle.weight)
        self.expected_weight.batch_weight = self.recycle_expected_weight
        self.recycle_expected_weight = 0
        self.expected_weight.storage_batch_loss()
        self.recycle_batches = []
        batch.description = "recycled batch"
        
    def hold_batch(self,facility,batch):
        """
        This method cues up any number of desired batches.  They will stay in the cue until the recyle storage
        process them all.  Then it will combine all held batches into the first batch in the cue to be passed
        back to kmp3.
        """
        self.write_to_log(facility,'Recycle storage receiving batch \n\n\n')
        self.increment_operation_time(facility,self.time_delay)
        self.recycle_batches.append(batch)
        self.recycle_expected_weight = self.recycle_expected_weight + self.expected_weight.batch_weight
        self.expected_weight.storage_batch_gain()

    def store_batch(self,facility,batch):
        """
        This is called when you want to store the batch indefinitely.  For now, such occurs when a weight
        discrepancy occurs and one wants to conduct an entire facility inspection.
        """
        self.write_to_log(facility,'Storing %s in recycle storage \n\n\n' %(batch.description))
        self.increment_operation_time(facility,self.time_delay)
        self.inventory = self.inventory + batch.weight
        self.expected_weight.storage_batch_gain()

    def inspect(self,facility):
        self.write_to_log(facility,'\nInspecting recycle storage: \n' + \
                'Expected weight was %f\nMeasured weight was %f \n' %(self.expected_weight.total_weight,
                    self.measured_inventory))
        self.expected_weight.residual_weight = self.inventory
        self.expected_weight.update_total_weight()
        self.measured_inventory = self.inventory
        self.write_to_log(facility,
                '\nExpected weight now is %f \nMeasured weight now is %f\n'%(self.expected_weight.total_weight,
                    self.measured_inventory))
