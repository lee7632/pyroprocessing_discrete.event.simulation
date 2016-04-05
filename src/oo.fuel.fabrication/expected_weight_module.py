########################################################################
# Malachi Tolman
# @tolman42
# rev.4.April.2016
########################################################################
#
# See class description
#
########################################################################
import pdb

class expected_weight_class:
    """
    This is a class that will be found in facility_component that gets implemented by basically every
    functional component of the facility.  How much weight of SNM each component will get will be
    passed to it through the edge transition along with the physical batch itself.  Components higher
    up the heirarchy will use an "update accountability" method to gather the expected 
    weight from each of the components
    its in charge of.

    Equipment should call one of the methods found here whenever it changes or does anything significant
    with the batch weight.

    #######
    # Variables 
    #######
    total_weight = the total amount of weight the component is expecting to contain at any given point
    in time.  This will be used extensively by storage units and "manager" components that will need
    to know how much SNM is contained among its branches during inspections.

    batch_weight = the expected weight that the batch being processed has.

    residual_weight = The amount of SNM being left in the equipment.  This applies to normal
    processing equipment that normally leave a little bit of material behind when passing the batch,
    and it applies to storage units who use this variable to keep track of their stored inventory (as opposed
    to the weight of the batch being passed in or out).
    """

    def __init__(self,total_weight,batch_weight,residual_weight):
        self.total_weight = total_weight 
        self.batch_weight = batch_weight
        self.residual_weight = residual_weight

    def update_total_weight(self):
        """
        Used by other methods to quickly update the total weight according to the current amount of expected
        residual and batch weights.
        """
        self.total_weight = self.batch_weight + self.residual_weight


    def equipment_batch_loss(self,amount_2_lose):
        """
        This method gets called by those processes which lose a given amount of SNM while processing the 
        batch.

        It updates the expected batch, residual, and total weight.
        """
        self.batch_weight = self.batch_weight - amount_2_lose
        self.residual_weight = self.residual_weight + amount_2_lose
        self.update_total_weight()

    def storage_batch_loss(self):
        """
        This method gets called when a storage unit loses a batch to the rest of the facility.

        Note that the storage unit will need to have set how much expected batch weight it has to subtract from.
        """
        self.residual_weight = self.residual_weight - self.batch_weight
        self.update_total_weight()

    def storage_batch_gain(self):
        """
        Use this method whenever a storage unit obtains a batch.  It will update the expected weight accordingly
        with respect to the expected batch weight passed in via the edge transition.

        Once the batch is processed, it is entirely in the residual weight with the previously processed batches, 
        thus the batch weight is reset to avoid double counting.
        """
        self.residual_weight = self.residual_weight + self.batch_weight
        self.batch_weight = 0
        self.update_total_weight()

    def batch_pass(self):
        """
        This method is called up by the edge transition to help pass the expected amount of batch weight
        in tandem with the physical batch itself.  It returns the expected batch weight it's passing, then
        resets the batch weight to zero since it no longer has such.
        """
        batch_2_pass = self.batch_weight
        self.batch_weight = 0
        self.update_total_weight()

        return batch_2_pass

    def batch_get(self,incoming_expected_batch_weight):
        """
        Like batch pass, this method is used by the edge transition to transfer the expected batch weight
        into the next object in the facility.
        """
        self.batch_weight = incoming_expected_batch_weight
        self.update_total_weight()

    def erase_expectations(self):
        """
        Used during inspections to ensure that the expected weight values are cleared before accumulating the
        expected weight of constituent parts.
        """
        self.batch_weight = 0
        self.residual_weight = 0
        self.update_total_weight()

    def add_weight(self, object1):
        """
        Primarily used during inspections to accumulate the expected weights of constituent parts.
        """
        self.batch_weight = self.batch_weight + object1.expected_weight.batch_weight
        self.residual_weight = self.residual_weight + object1.expected_weight.residual_weight
        self.update_total_weight()
