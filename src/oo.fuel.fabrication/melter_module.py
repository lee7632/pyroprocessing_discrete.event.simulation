########################################################################
# Malachi Tolman
# @tolman42
# rev.25.February.2016
########################################################################
#
# For now the melter does everything to include melting down the
# batch of materials and solidifying them into rods. 
#
# As of thus far, this is the only point along the process where some
# of the material gets left behind in the entire system.  An given
# amount is expected to get left behind, thus such is accounted for
# in the batch.  But the true amount left behind is randomized 
# with a given uncertainty, and the melter itself will keep track
# of how much that actual amount (true_accumulated_loss) is.
#
########################################################################
import numpy as np
from facility_component_module import facility_component_class

class melter_class(facility_component_class):
    """
    As mentioned above, when this class processes a batch, some
    of the materials get left behind.  However, this is to be
    expected and is accounted for each time by
    expected_batch_loss, and the cumulative effect of this
    over time is expected via expected_accumulated_loss.

    The actual amount lost each batch is randomly selected
    from an upper and lower bound given by the input file.
    The cumulative effect of this is stored in
    true_accumulated_loss.
    """

    def __init__(self,facility):
        self.expected_batch_loss = np.loadtxt(facility.process_states_dir+'/melter.loss.fraction.inp',usecols=[1])[0]
        self.batch_loss_bounds = np.loadtxt(facility.process_states_dir+'/melter.loss.fraction.inp',usecols=[1])[1:3] #upper bound and lower bound of the true material loss
        self.time_delay = np.loadtxt(facility.process_states_dir+'/process.operation.time.inp',usecols=[1])[1]
        self.expected_accumulated_loss = 0
        self.true_accumulated_loss = 0

    def process_batch(self,facility,batch):
        self.write_to_log(facility,'Alloy melting\n')
        self.increment_operation_time(facility,self.time_delay)
        
        ######
        # Calculate and assign true losses 
        ######
        self.true_batch_loss = (self.batch_loss_bounds[0] - self.batch_loss_bounds[1]) * \
                np.random.random_sample() + self.batch_loss_bounds[0]
        batch.true_weight = batch.true_weight - self.true_batch_loss
        self.true_accumulated_loss = self.true_accumulated_loss + self.true_batch_loss
        ######
        # Assign expected losses 
        ######
        batch.expected_weight = batch.expected_weight - self.expected_batch_loss
        self.expected_accumulated_loss = self.expected_accumulated_loss + self.expected_batch_loss
        ######
        # Log progress 
        ######
        self.write_to_log(facility,'Failure status:  False \n\n\n')

