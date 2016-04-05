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

class edge_transition_class(facility_component_class):
    """
    The edge transition serves as both the physical means by which the nuclear materials travels from vertex to 
    vertex (component to component), but also as the communication link between components.  In spite of the
    facility being set up in a hierchical decomposition, this is the one liason that allows components
    to communicate laterally with each other.

    It also causes the appropriate time delay for that particular transition.

    Edge transition input file allows for different time for different edges, thus
    the edge number is required to dilineate which edge is being created.

    Edge number is indexed by zero.

    #######
    # Variables 
    #######
    time_delay = amount of time in days it takes for this specific edge to move the batch.
    """

    def __init__(self,facility,edge_number):
        self.time_delay = np.loadtxt(facility.edge_transition_dir+'/edge.transition.inp',
                usecols=[1])[edge_number]
        facility_component_class.__init__(self, 0, 0, 0, "edge transition", "manager")

    def edge_transition(self, facility, batch, object1, object2):
        """
        This method is used to increment the time it takes to pass the physical batch from one object to the
        other.

        It also helps keep track of the expected amount of weight the batch will have from one object to the
        next. 

        Take special note that when an object passes the batch (both physical and expected weight), it resets
        its own expected batch weight to zero.
        """
        self.write_to_log(facility,'Edge transition: \nMoving %s from %s to %s \n\n'%(batch.description, 
            object1.description, object2.description))

        object2.expected_weight.batch_get( object1.expected_weight.batch_pass() )

        self.increment_operation_time(facility,self.time_delay)
