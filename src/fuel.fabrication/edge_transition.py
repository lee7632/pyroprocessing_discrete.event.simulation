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
def edge_transition(operation_time,equipment_failure_time_0,equipment_failure_time_1,edge_time_delay):
#######
    print 'Edge transition','\n\n'
    operation_time=operation_time+edge_time_delay
    equipment_failure_time_0=equipment_failure_time_0+edge_time_delay
    equipment_failure_time_1=equipment_failure_time_1+edge_time_delay
###
    return(operation_time,equipment_failure_time_0,equipment_failure_time_1)
########################################################################
#
# EOF
#
########################################################################
