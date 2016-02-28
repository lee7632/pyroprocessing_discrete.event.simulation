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
import global_vars
from edge_transition_module import edge_transition_class
from key_measurement_point_module import key_measurement_point_class as kmp_class
from melter_module import melter_class
from trimmer_module import trimmer_class

class fuel_fabricator_class:
    """
    The fuel fabricator is the final stage of the pyroprocessor.
    It takes in a batch of U and TRU, melts them in with zirconium,
    injects the entire melted alloy into a quartz crucible, let's the
    metal cool, and then breaks the quartz mold in order to produce metal
    slugs of SNM (special nuclear material).
   
    However, some of the SNM gets left behind in the melting process each
    time, which slowly accumulates into a "heel".  Eventually, the heel
    builds up so much, that the key measurement points (KMP's) detect a 
    large enough discrepancy between what's been processed and what's
    supposed to be there and initiate a system alarm.
    
    If the alarm is triggered, then the melter is cleaned, and the heel
    is accounted for and sent to the recycle storage facility to get 
    processed.

    Currently, the melter is set to be the only component that can experience an equipment failure.
    If this happens, the batch and heel are sent to the recycle storage, then put together in one
    batch to be processed as normal.  In the mean time, operation time is lost while the melter undergoes
    maintenance.
    """


    def __init__(self,facility):
        """
        The fabricator initializes all of the objects that are its own constituents.  That includes the melter,
        trimmer, recycle storage, four kmp's, and the edge transitions between such.
        """
        self.edge = edge_transition_class(facility,0)
        self.kmp0 = kmp_class(facility,0)
        self.melter= melter_class(facility)
        self.kmp1 = kmp_class(facility,1) 
        self.trimmer = trimmer_class(facility)
        self.kmp2 = kmp_class(facility,2)


    def process_batch(self,facility,batch):
        """
        See the class description
        """
        self.kmp0.process_batch(facility,batch)
        self.edge.edge_transition(facility)
        #######
        # When the melter processes a batch,
        # it returns a boolean to indicate whether it
        # experienced an equpiment failure or not
        #######
        if self.melter.process_batch(facility,batch):
            print 'Melter Failure!'
        self.edge.edge_transition(facility)
        self.kmp1.process_batch(facility,batch)
        self.edge.edge_transition(facility)
        self.trimmer.process_batch(facility,batch)
        self.edge.edge_transition(facility)
        self.kmp2.process_batch(facility,batch)

