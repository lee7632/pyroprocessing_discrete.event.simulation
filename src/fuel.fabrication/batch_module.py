########################################################################
# Malachi Tolman
# @tolman42
# 18.February.2016
########################################################################
#
# This module will represent the batch of materials prepared in the
# storage buffer that will get passed from module to module.  
#
########################################################################
#
# Imports
import numpy as np

class batch_class:
    """
    This class represents the batch of materials that gets passed
    from module to module.  It simply is a bundle of variables
    that will get acted upon by each vertex in the system.

    It will get initialized in the storage_buffer module, since
    that is the vertex that creates the batch.  Then it gets passed
    along the system.  It's used up once it reaches the product
    storage, then it will get reinitialized by storage_buffer once
    a new campaign starts.
    """

    def __init__(self,true_quantity,expected_quantity,measured_quantity):
        self.true_quantity = true_quantity
        self.expected_quantity = expected_quantity
        self.measured_quantity = measured_quantity
