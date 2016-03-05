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
    vertex (component to component), but also as the communication link between components.  The hierchical
    decomposition of the entire facility calls for individual components to be able to talk to each other
    to let the proceeding component know what it should expect to receive.

    It also causes the appropriate time delay for that particular transition.

    Edge transition input file allows for different time for different edges, thus
    the edge number is required to dilineate which edge is being created.

    Edge number is indexed by zero.
    """

    def __init__(self,facility,edge_number):
        self.time_delay = np.loadtxt(facility.edge_transition_dir+'/edge.transition.inp',
                usecols=[1])[edge_number]
        facility_component_class.__init__(self, 0, 0, 0, "edge transition", "manager")

    def edge_transition(self, facility, object1, object2):
        """
        This method is used to increment the time it takes to pass the physical batch from one object to the
        other.

        It also helps keep track of the expected amount of weight the batch will have from one object to the
        next.  If either object is a storage unit, then special procedures are taken to update the total
        expected weight and the measured inventory weight.
        """
        self.write_to_log(facility,'Edge transition: \nMoving batch from %s to %s \n\n'%(object1.description,
            object2.description))
        #######
        # Decrement total expected weight if batch is coming from a storage unit 
        #######
        if object1.object_type == "storage":
            object1.expected_weight.storage_batch_loss()
        #######
        # Pass the expected batch weight from one object to the next 
        #######
        object2.expected_weight.batch_get( object1.expected_weight.batch_pass() )
        #######
        # Update the measured inventory of the storage unit if a kmp is passing the batch into it.  If not,
        # then I'm not sure why an object is passing the batch into a storage unit (it needs to be measured first).
        #######
        if object2.object_type == "storage":
            if object1.object_type == "kmp":
                object2.measured_inventory = object2.measured_inventory + object1.measured_weight
            else:
                self.write_to_log(facility,'\n\n\n*******WARNING!!********\nATTEMPTING TO PASS A BATCH ' + \
                        'FROM AN OBJECT THAT IS NOT A KEY MEASUREMENT POINT INTO A STORAGE UNIT WILL ' + \
                        'YIELD UNRULY RESULTS!\n\n\n')
        self.increment_operation_time(facility,self.time_delay)
