########################################################################
# Malachi Tolman
# @tolman42
# rev.25.February.2016
########################################################################
#
# This object merely serves the purpose of incrementing the operation
# time the allotted amount when the batch gets passed from vertex
# to vertex. 
#
# Eventually I want it to serve as the actual liason, meaning that
# it will pass the batch to the next vertex and force the incoming
# vertex to process the batch.  That would be the most viable solution
# for creating the GUI that we talk of eventually happening.
#
########################################################################
import numpy as np
from facility_component_module import facility_component_class

class edge_transition_class(facility_component_class):
    """
    Class in charge of incrementing the correct time for a given edge transition.

    Edge transition input file allows for different time for different edges, thus
    the edge number is required to dilineate which edge is being created.

    Edge number is indexed by zero.
    """

    def __init__(self,facility_command,edge_number):
        self.time_delay = np.loadtxt(facility_command.edge_transition_dir+'/edge.transition.inp',usecols=[1])[edge_number]

    def edge_transition(self,facility_command):
        self.write_to_log(facility_command,'Edge transition \n\n\n')
        self.increment_operation_time(facility_command,self.time_delay)
