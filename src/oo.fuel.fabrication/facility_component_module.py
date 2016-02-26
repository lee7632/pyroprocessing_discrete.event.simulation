########################################################################
# Malachi Tolman
# @tolman42
# 18.February.2016
########################################################################
#
# This class contains methods that essentially ever component of the
# facility will use.  All of them will inherit this class, it's just
# an easier way of getting methods written that one would have to write 
# several times otherwise.
#
########################################################################
#
# Imports
#
import numpy

class facility_component_class:
    """
    This class will get inherited by most other classes used in fuel fabrication.
    """

    def write_to_log(self,facility_command,message):
        facility_command.log_file.write(message)

    def increment_operation_time(self,facility_command,time_added):
        """
        This function increases the operation time by the desired amount indicated by time_added;
        it then logs the incremented operation time in the designated output file.

        inputs: facility class, amount of time to increase operation time (float)
        """
        #print 'funtion called, \noperation time is %.4f\ntime to add is %.4f\n'%(facility_command.operation_time,time_added)
        facility_command.operation_time = facility_command.operation_time + time_added
        facility_command.system_time_output.write('%.4f\n'%(facility_command.operation_time))
        facility_command.campaign_output.write('%.4f\t%i\n'%(facility_command.operation_time,facility_command.total_campaign))
        #print 'operation time is now %.4f\n\n'%(facility_command.operation_time)
        
