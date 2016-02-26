########################################################################
# Malachi Tolman
# @tolman42
# rev.25.February.2016
########################################################################
#
# Key measurement points are vertexes which currently lie in between
# every other vertex.  They measure the weight of the batch, although
# some uncertainty is involved to account for realism.
#
########################################################################
import numpy as np
from facility_component_module import facility_component_class

class key_measurement_point_class(facility_component_class):
    """
    Each kmp should be specified separately where it lies along the
    system.  Each one will measure the weight of the batch as it comes in.
    It will then keep record of the latest measurement until another one is made
    (indicated by batch_weight),
    but it will also log the total weight that it has made since the facility 
    has started (indicated by system_weight).

    The kmp_indentifier is used for the log file and for getting the correct
    data from the input file.  It is zero indexed.
    """

    def __init__(self,facility,kmp_identifier):
        self.uncertainty = np.loadtxt(facility.kmps_dir+'/key.measurement.points.inp',usecols=[2])[kmp_identifier]
        self.time_delay = np.loadtxt(facility.kmps_dir+'/key.measurement.points.inp',usecols=[1])[kmp_identifier]
        self.identifier = kmp_identifier
        self.batch_weight = 0
        self.cumulative_weight = 0

    def process_batch(self,facility,batch):
        self.write_to_log(facility,'Measurement event at KMP: %i\n'%(self.identifier))

        self.batch_weight = batch.true_weight + self.uncertainty*np.random.randn()
        self.cumulative_weight = self.cumulative_weight+self.batch_weight
        self.increment_operation_time(facility,self.time_delay)

        self.write_to_log(facility,'Operation time %.4f (d) \nTrue quantity %.4f (kg) \nExpected quantity %.4f (kg) \nMeasured quantity %.4f (kg) \n\n\n'%(facility.operation_time, batch.true_weight, batch.expected_weight, self.batch_weight))
