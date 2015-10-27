########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.21.October.2015
########################################################################
# 
# Key measurement points (KMPs) are located based on the system diagram.
# Location can change based on design, but there should be a diagram for each design.
# 
########################################################################
#
# Assumptions
#
# No false alarms at KMPs.
# No state variable changes at KMPs.
#
########################################################################
#
# imports
import numpy
#
########################################################################
#
# function list
#
# (1): kmp measurement
# (5): close output files
#
########################################################################
#
#
#
#########################################################################
#
# (1): kmp measurement
#
#######
def kmp_measurement(operation_time,equipment_failure_time_0,equipment_failure_time_1,kmp_delay_time,uncertainty,threshold,true_quantity,expected_quantity,measured_inventory,measured_system_inventory,kmp_identifier):
#######
#
###    
    print 'Measurement event at KMP:',kmp_identifier
    operation_time=operation_time+kmp_delay_time
    equipment_failure_time_0=equipment_failure_time_0+kmp_delay_time
    equipment_failure_time_1=equipment_failure_time_1+kmp_delay_time
    measured_quantity=0
###
#
### measurement module
    if (kmp_identifier==0): #storage transfer
        measured_quantity=true_quantity+uncertainty*numpy.random.randn()
        measured_inventory=measured_inventory-measured_quantity
        measured_system_inventory=measured_system_inventory+measured_quantity
#
        measured_initial_inventory=measured_quantity #used for MUFc calculations
#
    elif (kmp_identifier==1): #trimmer
        measured_quantity=true_quantity+uncertainty*numpy.random.randn()
#
    elif (kmp_identifier==2): #product storage
        measured_quantity=true_quantity+uncertainty*numpy.random.randn()
        measured_inventory=measured_inventory+measured_quantity
#
    elif (kmp_identifier==3): #recycle transfer for failure
        measured_quantity=true_quantity+uncertainty*numpy.random.randn()
#
    elif (kmp_identifier==-3): #transfer back from recycle to melter
        measured_quantity=true_quantity+uncertainty*numpy.random.randn()
# end
###
    print 'Operation time','%.4f'%operation_time,'(d)','\n','True quantity','%.4f'%true_quantity,'(kg)','\n','Expected quantity','%.4f'%expected_quantity,'(kg)','\n','Measured quantity','%.4f'%measured_quantity,'(kg)','\n\n'
###
    if (kmp_identifier==0):
        return(operation_time,equipment_failure_time_0,equipment_failure_time_1,measured_quantity,measured_inventory,measured_initial_inventory,measured_system_inventory)
    else:
        return(operation_time,equipment_failure_time_0,equipment_failure_time_1,measured_quantity,measured_inventory)
########################################################################
#
#
#
########################################################################
#
# (5): close output files
#
#######
def close_files(true_kmp,expected_kmp,measured_kmp):
#######
    true_kmp.close()
    expected_kmp.close()
    measured_kmp.close()
###
    return(true_kmp,expected_kmp,measured_kmp)
########################################################################
#
# EOF
#
########################################################################
