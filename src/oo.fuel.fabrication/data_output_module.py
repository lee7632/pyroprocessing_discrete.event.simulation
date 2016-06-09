########################################################################
# Malachi Tolman
# @tolman42
# rev.12.April.2016
########################################################################
#
# See class description
#
########################################################################
import pdb

class data_output_class:
    """
    This class will contain functions that will be used for writing data to an output file.  Each facility
    component will have their own, because upon initialization, this class will contain the unique
    output directory for that given object.
    """

    def __init__(self, object_description, output_dir):
        self.output_file = open(output_dir + '/' + object_description + '.out','w+') 

    def write_to_data_output(self, message):
        self.output_file.write(message)

    def kmp_output(self, facility, kmp, batch):
        self.output_file.write('%.4f\t%i\t%.4f\t%.4f\t%.4f\n'%(facility.operation_time, 
            facility.total_campaign, batch.weight, kmp.expected_weight.batch_weight, kmp.measured_weight))

    def storage_output(self, facility, storage_object):
        self.output_file.write('%.4f\t%i\t%.4f\t%.4f\t%.4f\n'%(facility.operation_time, 
            facility.total_campaign, storage_object.inventory, storage_object.expected_weight.residual_weight,
            storage_object.measured_inventory))

    def processor_output(self, facility, processor, batch):
        self.output_file.write('%.4f\t%i\t%.4f\t%.4f\t%.4f\n'%(facility.operation_time, 
            facility.total_campaign, processor.heel.weight, processor.true_batch_loss, batch.weight))

    def failure_output(self, facility, processor, cdf, fail_check):
        self.output_file.write('%.4f\t%i\t%.4f\t%.4f\t%.4f\t%.4f\n'%(facility.operation_time, 
            facility.total_campaign, processor.time_of_last_failure, cdf, fail_check, processor.failure_count))

    def muf_output(self, facility):
        self.output_file.write('%.4f\t%i\t%.4f\t %.4f\t%.4f\t%.4f\t%.4f\t%.4f\n'%(facility.operation_time,
            facility.total_campaign, facility.fuel_fabricator.melter.heel.weight,
            facility.expected_muf, facility.measured_muf, facility.fuel_fabricator.true_campaign_muf,
            facility.fuel_fabricator.expected_campaign_muf, facility.fuel_fabricator.measured_campaign_muf))

