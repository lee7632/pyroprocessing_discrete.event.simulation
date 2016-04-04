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

class key_measurement_point_class(facility_component_class):
    """
    Key measurement points are the only points along the system that can actually weigh the materials and determine
    if a discrepancy has occurred (aside from an actual inspection).  How much weight should be detected is passed
    to it from the previous object via the edge transition.  Thus it relies on the previous component to recognize
    how much it expected to have changed the weight of the batch.

    Each kmp should be specified separately where it lies along the
    system.  Each one will measure the weight of the batch as it comes in.
    It will then keep record of the latest measurement until another one is made
    (indicated by measured_weight).

    It can (and should) report to the storage buffer that it is linked to if such is the case.  In this manner,
    the storage component keeps track of how much SNM it actually contains via the measurements made by
    its own kmp.  This process is governed by the managing unit in charge of each.

    The kmp_indentifier is used for the log file and for getting the correct
    data from the input file.  It is zero indexed.

    #######
    # Variables 
    #######

    uncertainty = standard deviation of noise that gets added to each measurement to simulate realistic 
    equipment uncertainty when measuring the weight.

    time_delay = time in days that the kmp takes to make the measurement

    alarm_threshold = weight in kg that will make the kmp sound an alarm when the difference between
    expected and measured weight is at least that much.

    identifier = integer number labeling which kmp the object is.  Used in getting input data from files and
    also keeping track in the log file.

    measured_weight = the weight of the batch most recently measured in kg
    """

    def __init__(self,facility,kmp_identifier):
        self.uncertainty = np.loadtxt(facility.kmps_dir+'/key.measurement.points.inp',usecols=[2])[kmp_identifier]
        self.time_delay = np.loadtxt(facility.kmps_dir+'/key.measurement.points.inp',usecols=[1])[kmp_identifier]
        self.alarm_threshold = np.loadtxt(facility.kmps_dir+'/key.measurement.points.inp',
                usecols=[4])[kmp_identifier]
        self.identifier = kmp_identifier
        self.measured_weight = 0
        facility_component_class.__init__(self, 0, 0,0, "key measurement point %i"%(kmp_identifier), "kmp")

    def process_batch(self,facility,batch):
        """
        See class description
        """
        self.write_to_log(facility,'Measurement event at KMP: %i\n'%(self.identifier))

        self.measured_weight = batch.weight + self.uncertainty*np.random.randn()
        self.increment_operation_time(facility,self.time_delay)

        self.write_to_log(facility,'Operation time %.4f (d) \nTrue quantity %.4f (kg) \nExpected quantity %.4f (kg) \nMeasured quantity %.4f (kg) \n\n\n'\
                %(facility.operation_time, batch.weight, self.expected_weight.batch_weight, self.measured_weight))
        if abs(self.measured_weight - self.expected_weight.batch_weight) > self.alarm_threshold:
            self.write_to_log(facility,
                    '\nMISSING SNM DETECTED in %s!  CONDUCT INSPECTION IMMEDIATELY!\n\n\n'%(self.description))
            facility.kmp_alarm(batch, self)

    def update_measured_inventory(self, facility, storage_buffer, action):
        """
        This method should be called by the managing unit everytime a kmp processes a batch and passes that 
        batch to or from a storage component.  It is only through this method that the storage units can 
        update how much cumulative inventory they have gained.

        The final argument "action" should be a string either saying "add" or "subtract" so that the managing
        unit and kmp know what to do.
        """
        if action == "add":
            storage_buffer.measured_inventory = storage_buffer.measured_inventory + self.measured_weight
        elif action == "subtract":
            storage_buffer.measured_inventory = storage_buffer.measured_inventory - self.measured_weight
        else:
            self.write_to_log(facility,'************** WARNING!! ***************\n' + \
                    'Key measurement point %i incorrectly asked to update the measured inventory of %s.\n' \
                     %(self.kmp_identifier, storage_buffer.description) + \
                    "Please make sure that final argument of update inventory reads either 'add' or 'subtract'")

