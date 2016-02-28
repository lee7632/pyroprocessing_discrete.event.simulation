########################################################################
# Malachi Tolman
# @tolman42
# rev.25.February.2016
########################################################################
# 
# This is the storage facility for the batches of materials
# after they have been processed.
#
########################################################################
import numpy as np
from facility_component_module import facility_component_class
from batch_module import batch_class

class product_storage_class(facility_component_class):
    """
    This class keeps track of how much of the batch
    materials actually got processed along with
    how much was expected to get processed.
    """

    def __init__(self,facility):
        self.expected_campaign_inventory = 0
        self.true_campaign_inventory = 0
        self.expected_cumulative_inventory = 0 
        self.true_cumulative_inventory = 0
        self.time_delay = np.loadtxt(facility.process_states_dir+'/process.operation.time.inp',usecols=[1])[3]

    def process_batch(self,facility,batch):
        self.true_campaign_inventory = 0
        self.expected_campaign_inventory = 0
        self.write_to_log(facility,'Processing the final product \n\n\n')
        self.increment_operation_time(facility,self.time_delay)
        self.true_campaign_inventory = batch.true_weight
        self.expected_campaign_inventory = batch.expected_weight
        self.true_cumulative_inventory = self.true_cumulative_inventory + batch.true_weight
        self.expected_cumulative_inventory = self.expected_cumulative_inventory + batch.expected_weight

        #self.write_to_debug(facility,'Product storage processed batch\nTrue weight is %f \nexpected weight is %f \ntrue campaign inventory is %f \nexpected campaign inventory is %f \ntrue cumulative inventory is %f\nexpected cumulative inventory is %f\n\n\n'%(batch.true_weight, batch.expected_weight, self.true_campaign_inventory, self.expected_campaign_inventory, self.true_cumulative_inventory, self.expected_cumulative_inventory))
