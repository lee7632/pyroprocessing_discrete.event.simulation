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

class trimmer_class(facility_component_class):
    """
    The trimmer takes the quartz molds from the melter and sheers them to produce the metal slug of SNM
    hidden there-in.  The quartz is processed as waste material, and the metal slugs are sent into
    product storage, as they are the final product of the entire pyroprocessing system, much less the
    fuel fabrication process.

    For now, the trimmer doesn't experience equipment failure, nor does it lose any material during
    it's batch processing time.  It simply accepts the batch from kmp1 (from the melter), increments
    the operation time accordingly, then passes the product along to product storage.
    """

    def __init__(self,facility):
        self.time_delay = np.loadtxt(facility.process_states_dir+'/process.operation.time.inp',usecols=[1])[2]
        facility_component_class.__init__(self, 0, 0, 0, "trimmer", "processor")

    def process_batch(self,facility,batch):
        """
        See class description
        """
        self.write_to_log(facility,'Slug trimming\n')
        self.increment_operation_time(facility,self.time_delay)
        
        self.write_to_log(facility,'Failure status:  False \n\n\n')

