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
    if a discrepancy has occurred (aside from an actual inspection).  It needs confirmation from the system
    component governing it (i.e. fuel fabricator) as to what the expected weigh of the measured batch is, because
    this quantity changes depending on the situation (whether or not a failure or inspection has occurred.  Also
    is it getting a whole batch, or just the heel?).

    Each kmp should be specified separately where it lies along the
    system.  Each one will measure the weight of the batch as it comes in.
    It will then keep record of the latest measurement until another one is made
    (indicated by measured_weight),
    but it will also log the total weight that it has made since the facility 
    has started (indicated by cumulative_weight).

    The kmp_indentifier is used for the log file and for getting the correct
    data from the input file.  It is zero indexed.
    """

    def __init__(self,facility,kmp_identifier):
        self.uncertainty = np.loadtxt(facility.kmps_dir+'/key.measurement.points.inp',usecols=[2])[kmp_identifier]
        self.time_delay = np.loadtxt(facility.kmps_dir+'/key.measurement.points.inp',usecols=[1])[kmp_identifier]
        self.identifier = kmp_identifier
        self.measured_weight = 0
        self.cumulative_weight = 0
        self.expected_weight = 0

    def process_batch(self,facility,batch,expected_weight):
        """
        See class description
        """
        self.write_to_log(facility,'Measurement event at KMP: %i\n'%(self.identifier))

        self.expected_weight = expected_weight
        self.measured_weight = batch.weight + self.uncertainty*np.random.randn()
        self.cumulative_weight = self.cumulative_weight+self.measured_weight
        self.increment_operation_time(facility,self.time_delay)

        self.write_to_log(facility,'Operation time %.4f (d) \nTrue quantity %.4f (kg) \nExpected quantity %.4f (kg) \nMeasured quantity %.4f (kg) \n\n\n'%(facility.operation_time, batch.weight, self.expected_weight, self.measured_weight))
