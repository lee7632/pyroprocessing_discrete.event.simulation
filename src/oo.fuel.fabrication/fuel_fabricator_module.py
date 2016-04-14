########################################################################
# Malachi Tolman
# @tolman42
# rev.4.April.2016
########################################################################
#
# See class description
#
########################################################################
#
# Imports
#
########################################################################
import pdb
import numpy as np
from facility_component_module import facility_component_class
from edge_transition_module import edge_transition_class
from key_measurement_point_module import key_measurement_point_class as kmp_class
from melter_module import melter_class
from trimmer_module import trimmer_class
from recycle_storage_module import recycle_storage_class

class fuel_fabricator_class(facility_component_class):
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

    #######
    # Variables 
    #######
    edge = module that keeps track of the expected batch weight as it gets passed from object to object

    kmp = modules that measure the weight of the batch between pertinent vertexes.

    melter = module that melts down the batch and pours such into a crucible. It is at this point that
    some SNM is left behind, thus changing the state variable.  This is also the only component thus far
    that can experince a failure.

    trimmer = module that sheers the crucibles to reveal the cooled slugs inside.  This currently does
    nothing more than run the clock (no state variables are changed).

    recycle_storage = module that both recycle the batch and heel together when a failure has occurred and
    also indefinitely stores the heel whenever an alarm is set off.

    expected_campaign_muf = expected amount of SNM left in a given campaign determined ahead of time
    as to what any given component should lose in a campaign

    measured_campaign_muf = measured amount of the batch left behind.  Found by taking the difference
    amongst the pertinent kmps.

    true_campaign_muf = actual amount of SNM left behind for this campaign
    """


    def __init__(self,facility):
        """
        The fabricator initializes all of the objects that are its own constituents.  That includes the melter,
        trimmer, recycle storage, four kmp's, and the edge transitions between such.

        The expected batch and heel weights are changed everytime a component that changes those state variables
        processes a batch.  
        """
        self.edge = edge_transition_class(facility,0)
        self.kmp = []
        for n in range(4):
            self.kmp.append(kmp_class(facility,n))
        self.melter= melter_class(facility)
        self.trimmer = trimmer_class(facility)
        self.recycle_storage = recycle_storage_class(facility)
        self.expected_campaign_muf = 0
        self.measured_campaign_muf = 0
        self.true_campaign_muf = 0
        facility_component_class.__init__(self, 0, 0, 0, "fuel_fabricator", "manager", None)

    def update_accountability(self):
        """
        Method that makes each child unit update their known inventory of expected weight and measured weight
        from their own children units.
        """
        self.expected_weight.erase_expectations()
        self.expected_weight.add_weight(self.melter)
        self.expected_weight.add_weight(self.trimmer)
        self.expected_weight.add_weight(self.kmp[1])
        self.expected_weight.add_weight(self.kmp[3])
        self.expected_weight.add_weight(self.recycle_storage)

    def process_batch(self,facility,batch):
        """
        After getting the batch from storage, the fuel fabricator turns it into useable metal slugs as
        described in the class description.

        If the melter experiences a failure while processing the batch, the failure routine is called.
        """
        #######
        # When the melter processes a batch,
        # it returns a boolean to indicate whether it
        # experienced an equpiment failure or not
        #######
        if self.melter.process_batch(facility,batch):
            self.equipment_failure(facility,batch)
        self.edge.edge_transition(facility,batch, self.melter,self.kmp[1])
        self.kmp[1].process_batch(facility,batch)
        self.edge.edge_transition(facility,batch, self.kmp[1],self.trimmer)
        self.trimmer.process_batch(facility,batch)

    def calculate_campaign_muf(self, previous_kmp):
        """
        This is called by the facility to calculate the campaign MUF.  The kmp that measured the batch
        before passing it onto the fuel fabricator needs to be passed in here to calculate the measured
        MUF.
        """
        self.expected_campaign_muf = self.melter.expected_loss
        self.measured_campaign_muf = previous_kmp.measured_weight - self.kmp[1].measured_weight
        self.true_campaign_muf = self.melter.true_batch_loss

    def equipment_failure(self,facility,batch):
        """
        The routine that occurs when the melter fails.  The batch is sent to the recycle storage, then the heel
        is cleaned and sent to recycle storage, both are recycled into one batch, and then that batch gets
        sent back into the normal process.
        """
        did_fail = True
        while did_fail:
            self.write_to_log(facility,
                    'Melter failed at time %.4f, begin failure routine\n\n'%(facility.operation_time))
            self.edge.edge_transition(facility,batch, self.melter,self.kmp[3])
            self.kmp[3].process_batch(facility,batch)
            self.edge.edge_transition(facility,batch, self.kmp[3],self.recycle_storage)
            self.kmp[3].update_measured_inventory(facility, self.recycle_storage, "add")
            self.recycle_storage.store_batch(facility,batch)
            heel = self.melter.clean_heel(facility)
            self.edge.edge_transition(facility,heel,self.melter,self.kmp[3]) 
            self.kmp[3].process_batch(facility,heel)
            self.edge.edge_transition(facility,heel,self.kmp[3],self.recycle_storage)
            self.kmp[3].update_measured_inventory(facility, self.recycle_storage, "add")
            self.recycle_storage.store_batch(facility,heel)
            self.melter.repair(facility)
            self.recycle_storage.process_batch(facility,batch)
            self.edge.edge_transition(facility,batch, self.recycle_storage,self.kmp[3])
            self.kmp[3].process_batch(facility,batch)
            self.edge.edge_transition(facility,batch, self.kmp[3],self.melter)
            did_fail = self.melter.process_batch(facility,batch)

    def inspect(self,facility):
        """
        Method that gets called whenever an alarm is set off.  The melter is cleaned out, and the heel
        moved to recycle storage for the mass balance.
        """
        self.write_to_log(facility,'\nPreparing fuel fabricator for facility inspection: \n')
        heel = self.melter.clean_heel(facility)
        self.edge.edge_transition(facility,heel,self.melter,self.kmp[3])
        self.kmp[3].process_batch(facility,heel)
        self.edge.edge_transition(facility,heel,self.kmp[3],self.recycle_storage)
        self.kmp[3].update_measured_inventory(facility,self.recycle_storage, "add")
        self.recycle_storage.store_batch(facility,heel)
