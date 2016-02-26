########################################################################
# Malachi Tolman
# @tolman42
# rev.25.February.2016
########################################################################
#
# The trimmer segments the rods into useable chunks
#
########################################################################
import numpy as np
from facility_component_module import facility_component_class

class trimmer_class(facility_component_class):
    """
    For now, all the trimmer does is pass along the batch
    unchanged.
    """

    def __init__(self,facility):
        self.time_delay = np.loadtxt(facility.process_states_dir+'/process.operation.time.inp',usecols=[1])[2]

    def process_batch(self,facility,batch):
        self.write_to_log(facility,'Slug trimming\n')
        self.increment_operation_time(facility,self.time_delay)
        
        self.write_to_log(facility,'Failure status: False \n\n\n')

