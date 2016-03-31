########################################################################
# Malachi Tolman
# @tolman42
# rev.27.February.2016
########################################################################
#
# See class description
#
########################################################################
#
# Imports
#
########################################################################
import numpy as np
from facility_component_module import facility_component_class
from edge_transition_module import edge_transition_class
from product_storage_module import product_storage_class
from key_measurement_point_module import key_measurement_point_class as kmp_class

class final_storage_unit_class(facility_component_class):

    def __init__(self,facility):
        self.measured_inventory = 0
        self.edge = edge_transition_class(facility,0)
        self.product_storage = product_storage_class(facility)
        self.kmp = kmp_class(facility,2)
        facility_component_class.__init__(self, 0, 0, 0, "final storage unit", "manager")

    def process_batch(self,facility,batch):
        self.kmp.process_batch(facility,batch)
        self.edge.edge_transition(facility, batch, self.kmp, self.product_storage)
        self.kmp.update_measured_inventory(facility, self.product_storage, "add")
        self.product_storage.process_batch(facility,batch)

    def inspect(self):
        self.expected_weight.erase_expectations()
        self.expected_weight.add_weight(self.product_storage)
        self.expected_weight.add_weight(self.kmp)
        self.measured_inventory = self.product_storage.measured_inventory
