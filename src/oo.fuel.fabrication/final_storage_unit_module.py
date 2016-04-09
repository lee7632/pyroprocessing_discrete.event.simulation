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
    """
    This unit takes in the finished product from the fuel fabricator and keeps it in storage.  How much the unit
    knows has been stored is kept track via the weight measured by the kmp.

    #######
    # Variables 
    #######
    measured_inventory = Amount of SNM the storage buffer and kmp contain as measured by the kmp.  Only gets 
    updated via the update_accountability routine.

    edge = object that handles batch transitions between modules

    product_storage = module that stores the batch

    kmp = key measurement point paired with the storage buffer
    """
    def __init__(self,facility):
        self.measured_inventory = 0
        self.edge = edge_transition_class(facility,0)
        self.product_storage = product_storage_class(facility)
        self.kmp = kmp_class(facility,2)
        facility_component_class.__init__(self, 0, 0, 0, "final storage unit", "manager")

    def process_batch(self,facility,batch):
        """
        The kmp measured how much the batch weighs, then such is reported to the product storage after the
        batch has been passed in, but before it is processed by such.
        """
        self.kmp.process_batch(facility,batch)
        self.edge.edge_transition(facility, batch, self.kmp, self.product_storage)
        self.kmp.update_measured_inventory(facility, self.product_storage, "add")
        self.product_storage.process_batch(facility,batch)

    def update_accountability(self):
        """
        Update the unit expected and measured weight according to what's currently logged in the storage buffer
        and kmp.
        """
        self.expected_weight.erase_expectations()
        self.expected_weight.add_weight(self.product_storage)
        self.expected_weight.add_weight(self.kmp)
        self.measured_inventory = self.product_storage.measured_inventory

