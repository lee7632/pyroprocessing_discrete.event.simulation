########################################################################
# Malachi Tolman
# @tolman42
# rev.27.February.2016
########################################################################
#
# See class description
#
########################################################################
import numpy as np
from facility_component_module import facility_component_class
from batch_module import batch_class

class melter_class(facility_component_class):
    """
    The melter takes the U and TRU, melts them with zirconium, and injects the melted alloy into quartz molds
    that will cool as they are passed onto the trimmer.

    As of thus far, this is the only component in the entire facility where some of the material gets left
    behind.  This is to be expected, and that is accounted for with expected_batch_loss from the input file.
    
    The actual amount lost each batch is randomly selected as a uniform distribution
    from an upper and lower bound given by the input file.
    The cumulative effect of this is stored in the heel.

    The heel is made of the same stuff as the batch, thus comes from the same object.  Whenever an alarm
    is set off, or it there is an equipment failure, the heel gets sent to the recycle storage to be accounted
    for and eventually reprocessed.

    This is also the only component thus far that can experience equipment failure.  Such will essentially
    initiate the same routine as an alarm, but more operation time will pass to account for equipment maintenance.
    """

    def __init__(self,facility):
        self.expected_batch_loss = np.loadtxt(facility.process_states_dir+'/melter.loss.fraction.inp',usecols=[1])[0]
        self.batch_loss_bounds = np.loadtxt(facility.process_states_dir+'/melter.loss.fraction.inp',usecols=[1])[1:3] #upper bound and lower bound of the true material loss
        self.time_delay = np.loadtxt(facility.process_states_dir+'/process.operation.time.inp',usecols=[1])[1] \
                #amount of time it takes to process the batch uninterrupted
        self.heel = batch_class(0,0)
        self.failure_rate = np.loadtxt(facility.failure_equipment_dir+'/melter.failure.data.inp',usecols=[1]) \
                #how often the melter is expected to fail (actual time selected from a weibull distribution
        self.maintenance_time = np.loadtxt(facility.failure_equipment_dir+'/melter.failure.data.inp',usecols=[2]) \
                #How long it takes to repair the melter after a failure
        self.cleaning_time = np.loadtxt(facility.failure_equipment_dir+'/melter.failure.data.inp',usecols=[2]) \
                #Amount of time it takes to remove the heel from the melter
        self.time_of_last_failure = 0

    def process_batch(self,facility,batch):
        self.write_to_log(facility,'Alloy melting\n')
        self.increment_operation_time(facility,self.time_delay)
        
        ######
        # Calculate and assign true losses 
        ######
        true_batch_loss = (self.batch_loss_bounds[0] - self.batch_loss_bounds[1]) * \
                np.random.random_sample() + self.batch_loss_bounds[0]
        batch.true_weight = batch.true_weight - true_batch_loss
        ######
        # Assign expected losses 
        ######
        batch.expected_weight = batch.expected_weight - self.expected_batch_loss
        #######
        # Everything lost in batch is accumulated in the heel 
        #######
        self.heel.add_weight(true_batch_loss,self.expected_batch_loss)

        did_fail = self.check_equipment_failure(facility)

        ######
        # Log progress 
        ######
        if did_fail:
            self.write_to_log(facility,'Failure status:  True \n\n\n')
        else:
            self.write_to_log(facility,'Failure status:  True \n\n\n')

        return did_fail


    def check_equipment_failure(self,facility):
        """
        This method calculates the probability of an equipment failure by running the time through a cumulative
        distribution function from the Weibull distribution.

        Currently, beta (or k, depeding on who's syntax you use) is set to be 1.  That is the value
        used when the actual failure distribution is unknown, and then eta (or lambda) represents a general
        guess of the rate of failure

        Whether or not an actual failure occurs is determined by whether or not the calculated probability is 
        greater than a randomly selected number between 0-1 from a uniform distribution.
        """
        #######
        # Initialize the boolean 
        #######
        did_fail = False
        #######
        # The time used to calculate the probability is the time that has passed since the last failure. 
        #######
        time = facility.operation_time - self.time_of_last_failure
        #######
        # The cumulative distribution function caclulated according to time 
        #######
        cdf = 1 - np.exp(-time / self.failure_rate)
        fail_check = np.random.rand()
        self.write_to_debug(facility,'time to calc is %f \nfail rate is %f \ncdf is %f \nfail check is %f \n\n\n' \
                %(time, self.failure_rate,cdf,fail_check))
        if cdf > fail_check:
            did_fail = True
            self.time_of_last_failure = facility.operation_time

        return did_fail

