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
        self.campaign_inventory = 0
        self.cumulative_inventory = 0
        self.expected_cumulative_inventory = 0
        self.time_delay = np.loadtxt(facility.process_states_dir+'/process.operation.time.inp',usecols=[1])[3]

    def process_batch(self,facility,last_kmp,batch):
        self.write_to_log(facility,'Processing the final product \n\n\n')
        self.increment_operation_time(facility,self.time_delay)
        self.campaign_inventory = batch.weight
        self.cumulative_inventory = self.cumulative_inventory + batch.weight
        self.expected_cumulative_inventory = self.expected_cumulative_inventory + last_kmp.expected_weight

        self.write_to_debug(facility,'Product storage processed batch at campaign %i\nlast kmp expected weight is %f\nnew cumulative expected weight is %f\n\n\n\n'%(facility.total_campaign, last_kmp.expected_weight, self.expected_cumulative_inventory))

        #self.write_to_debug(facility,'Product storage processed batch\nTrue weight is %f \nexpected weight is %f \ntrue campaign inventory is %f \nexpected campaign inventory is %f \ntrue cumulative inventory is %f\nexpected cumulative inventory is %f\n\n\n'%(batch.true_weight, batch.expected_weight, self.true_campaign_inventory, self.expected_campaign_inventory, self.true_cumulative_inventory, self.expected_cumulative_inventory))
