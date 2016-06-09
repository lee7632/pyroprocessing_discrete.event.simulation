########################################################################
# Malachi Tolman
# @tolman42
# rev.4.April.2016
########################################################################
#
# See class description
#
########################################################################
import numpy as np
from facility_component_module import facility_component_class
from batch_module import batch_class
from data_output_module import data_output_class

class melter_class(facility_component_class):
    """
    The melter takes the U and TRU, melts them with zirconium, and injects the melted alloy into quartz molds
    that will cool as they are passed onto the trimmer.

    As of thus far, this is the only component in the entire facility where some of the material gets left
    behind.  This is to be expected, and that is accounted for with expected_batch_loss from the input file.
    
    The actual amount lost each batch experiences is randomly selected as a uniform distribution
    from an upper and lower bound given by the input file.
    The cumulative effect of this is stored in the heel.

    The heel is made of the same stuff as the batch, thus comes from the same object.  Whenever an alarm
    is set off, or if there is an equipment failure, the heel gets sent to the recycle storage to be accounted
    for and eventually reprocessed.

    This is also the only component thus far that can experience equipment failure.  Such will essentially
    initiate the same routine as an alarm, but more operation time will pass to account for equipment maintenance.

    #######
    # Variables 
    #######
    expected_loss = amount of SNM in kg that is expected to be left behind in the heel each time a batch is
    processed.

    batch_loss_bounds = upper and lower bounds used when calculating the actual amount of SNM left in the heel
    when a batch is processed.

    process_time_delay = the amount of time in days it takes to process the batch uninterrupted.

    heel = object that keeps track how much SNM has accumulated in the melter.  Same class as batch.

    failure_rate = average frequency that the melter will fail in units of 1/days.

    maintenance_time_delay = amount of time in days it takes to maintain the melter after it has experienced
    a failure.

    cleaning_time_delay = amount of time it takes to clean the heel out of the melter.

    time_of_last_failure = the operation time clocked (in days) when the melter last failed.  This is used
    to keep track of how long its been since parts have been replaced, thus how likely it is for a failure to
    occur again.

    true_batch_loss = variable that stores the true amount of batch loss.  Such is calculated as a uniform
    distribution between the bounds, but it needs to be stored so that the managing unit can view and use
    such.

    failure_count = number of times this component has failed.

    failure_data_output = object that handles the opening and writing to a file exclusively for variables
    that deal with the equipment failure check.
    """
    def __init__(self,facility):
        self.expected_loss = np.loadtxt(facility.process_states_dir+ \
                '/melter.loss.fraction.inp',usecols=[1])[0] 
        self.batch_loss_bounds = np.loadtxt(facility.process_states_dir+'/melter.loss.fraction.inp',
                usecols=[1])[1:3] 
        self.process_time_delay = np.loadtxt(facility.process_states_dir+ \
                '/process.operation.time.inp',usecols=[1])[1] 
        self.heel = batch_class(0,"heel")
        self.failure_rate = np.loadtxt(facility.failure_equipment_dir+'/melter.failure.data.inp',usecols=[1]) 
        self.maintenance_time_delay = np.loadtxt(facility.failure_equipment_dir+ \
                '/melter.failure.data.inp',usecols=[2]) 
        self.cleaning_time_delay = np.loadtxt(facility.failure_equipment_dir+ \
                '/melter.failure.data.inp',usecols=[2]) 
        self.time_of_last_failure = 0
        self.true_batch_loss = 0
        self.failure_count = 0
        self.failure_data_output = data_output_class("melter_failure_data", facility.equipment_failure_odir)
        facility_component_class.__init__(self, 0, 0, 0, "melter", "processor", facility.material_flow_odir)

    def process_batch(self,facility,batch):
        """
        The melter looses some of the SNM during this process.  Such is selected from a uniform distribution
        dictated by the bounds from the input file.

        If the melter fails, then the state variables are not changed, and news of such gets passed back
        to the fuel fabricator

        #######
        # Return 
        #######
        True = melter did fail.  Need to run the failure routine.

        False = melter did not fail.  Fuel fabricator may continue running as normal.
        """
        self.write_to_log(facility,'Alloy melting\n')
        self.increment_operation_time(facility,self.process_time_delay)
         
        did_fail = self.check_equipment_failure(facility)
        if did_fail:
            self.write_to_log(facility,'Failure status:  True \n\n\n')
            facility.melter_did_fail = True
        else:
            self.write_to_log(facility,'Failure status:  False \n\n\n')
            ######
            # Calculate and assign weight losses 
            ######
            self.true_batch_loss = (self.batch_loss_bounds[0] - self.batch_loss_bounds[1]) * \
                    np.random.random_sample() + self.batch_loss_bounds[1]
            batch.weight = batch.weight - self.true_batch_loss
            self.expected_weight.equipment_batch_loss(self.expected_loss)
            #######
            # Everything lost in batch is accumulated in the heel 
            #######
            self.heel.add_weight(self.true_batch_loss)
    
        self.data_output.processor_output(facility, self, batch)

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
        cleaned_out_heel = batch_class(self.heel.weight,"heel")
        #######
        # A little bit of variable shuffle to make sure that the edge transition with the heel occurs as expected
        #######
        self.expected_weight.batch_weight = self.expected_weight.residual_weight
        self.heel.weight = 0
        self.expected_weight.residual_weight = 0
        self.expected_weight.update_total_weight

        self.data_output.processor_output(facility, self, cleaned_out_heel)

        return cleaned_out_heel 

    def repair(self,facility):
        """
        Repair and maintain the melter after a failure has occurred.
        """
        self.write_to_log(facility,'Repairing melter\n\n')
        self.increment_operation_time(facility,self.maintenance_time_delay)

