########################################################################
# Malachi Tolman
# @tolman42
# rev.25.February.2016
########################################################################
#
# This module will represent the batch of materials prepared in the
# storage buffer that will get passed from module to module.  
#
########################################################################

class batch_class:

    def __init__(self,true_weight,expected_weight):
        self.true_weight = true_weight
        self.expected_weight = expected_weight
