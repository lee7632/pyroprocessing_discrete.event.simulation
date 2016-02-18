########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.23.October.2015
########################################################################
# 
# Edge transitions occur between each vertex.
# State variables do not change on the edges.
# 
########################################################################
#
# imports
#
########################################################################
#
# function list
#
# (1): edge transition
#
########################################################################
#
#
#
########################################################################
#
#
# (1): edge transition
#
#######

from facility_module import Facility_Class

class Edge_Transition_Class(Facility_Class):

    def edge_transition(self,operation_time,equipment_failure_time_0,equipment_failure_time_1,edge_time_delay,log_file):

        #print 'Edge transition','\n\n'
        #log_file.write('Edge transition \n\n')
        self.write_to_log('Edge transition \n\n')
        #operation_time=operation_time+edge_time_delay
        self.increment_operation_time(edge_time_delay)
        equipment_failure_time_0=equipment_failure_time_0+edge_time_delay
        equipment_failure_time_1=equipment_failure_time_1+edge_time_delay

        return(self.operation_time,equipment_failure_time_0,equipment_failure_time_1)

########################################################################
#
# EOF
#
########################################################################
