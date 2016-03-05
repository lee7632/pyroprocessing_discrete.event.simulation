########################################################################
# Malachi Tolman
# @tolman42
# rev.29.February.2016
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
        self.expected_loss = np.loadtxt(facility.process_states_dir+ \
                '/melter.loss.fraction.inp',usecols=[1])[0] \
                #Amount of material the personnel expect the melter to lose each time it processes a batch 
        self.batch_loss_bounds = np.loadtxt(facility.process_states_dir+'/melter.loss.fraction.inp',usecols=[1])[1:3] #upper bound and lower bound of the true material loss
        self.process_time_delay = np.loadtxt(facility.process_states_dir+ \
                '/process.operation.time.inp',usecols=[1])[1] \
                #amount of time it takes to process the batch uninterrupted
        self.heel = batch_class(0)
        self.failure_rate = np.loadtxt(facility.failure_equipment_dir+'/melter.failure.data.inp',usecols=[1]) \
                #how often the melter is expected to fail (actual time selected from a weibull distribution
        self.maintenance_time_delay = np.loadtxt(facility.failure_equipment_dir+ \
                '/melter.failure.data.inp',usecols=[2]) \
                #How long it takes to repair the melter after a failure
        self.cleaning_time_delay = np.loadtxt(facility.failure_equipment_dir+ \
                '/melter.failure.data.inp',usecols=[2]) \
                #Amount of time it takes to remove the heel from the melter
        self.time_of_last_failure = 0
        facility_component_class.__init__(self, 0, 0, 0, "melter", "processor")

    def process_batch(self,facility,batch):
        """
        The melter looses some of the SNM during this process.  Such is selected from a uniform distribution
        dictated by the bounds from the input file.
        """
        self.write_to_log(facility,'Alloy melting\n')
        self.increment_operation_time(facility,self.process_time_delay)
         
        did_fail = self.check_equipment_failure(facility)
        if did_fail:
            self.write_to_log(facility,'Failure status:  True \n\n\n')
        else:
            self.write_to_log(facility,'Failure status:  False \n\n\n')
            ######
            # Calculate and assign weight losses 
            ######
            true_batch_loss = (self.batch_loss_bounds[0] - self.batch_loss_bounds[1]) * \
                    np.random.random_sample() + self.batch_loss_bounds[0]
            batch.weight = batch.weight - true_batch_loss
            self.expected_weight.equipment_batch_loss(self.expected_loss)
            #######
            # Everything lost in batch is accumulated in the heel 
            #######
            self.heel.add_weight(true_batch_loss)
            
        return did_fail

    def clean_heel(self,facility):
        """
        The accumulated SNM leftover from all previous campaigns (the heel) is cleaed out and returned.
        """
        self.write_to_log(facility,'Cleaning the heel\n\n')
        self.increment_operation_time(facility,self.cleaning_time_delay)
        #######
        # Create new batch instance, because the assignment variable only copies the pointer, not the 
        # object itself.
        #######
        cleaned_out_heel = batch_class(self.heel.weight) 
        #######
        # A little bit of variable shuffle to make sure that the edge transition with the heel occurs as expected
        #######
        self.expected_weight.batch_weight = self.expected_weight.residual_weight
        self.heel.weight = 0
        self.expected_weight.residual_weight = 0
        self.expected_weight.update_total_weight

        return cleaned_out_heel 

    def repair(self,facility):
        """
        Repair and maintain the melter after a failure has occurred.
        """
        self.write_to_log(facility,'Repairing melter\n\n')
        self.increment_operation_time(facility,self.maintenance_time_delay)

