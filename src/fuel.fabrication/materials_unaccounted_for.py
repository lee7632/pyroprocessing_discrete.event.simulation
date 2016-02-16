########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.27.October.2015
########################################################################
# 
# Materials unaccounted for
# 
########################################################################
#
# A mass balance is conducted after a fuel campaign or on an equipment failure, and then as part of post-failure inspection for restart.
# The materials unaccounted for (muf) is the difference resulting from the mass balance.
# The mass balance is never going to be zero because of equipment material losses.
# The muf is then compared to expected material losses to test for false alarm.
#
########################################################################
#
# imports
#
import numpy 
#
########################################################################
#
# function list
#
# (1): system mass balance
#
########################################################################
#
#
#
########################################################################
#
# (1): system mass balance
# 
#
###
def system_mass_balance(operation_time,melter_failure_time,trimmer_failure_time,time_delay,true_quantity,expected_quantity,measured_quantity,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,true_muf,expected_muf,measured_muf,log_file):
### 
    operation_time=operation_time+time_delay
    melter_failure_time=melter_failure_time+time_delay
    trimmer_failure_time=trimmer_failure_time+time_delay
#
###
    true_mufc=0
    expected_mufc=0
    measured_mufc=0
    true_final_inventory=true_quantity
    expected_final_inventory=expected_quantity
    measured_final_inventory=measured_quantity
###
#
### compute MUF for campaign 
    true_mufc=abs(true_initial_inventory-true_final_inventory)
    expected_mufc=abs(expected_initial_inventory-expected_final_inventory)
    measured_mufc=abs(measured_initial_inventory-measured_final_inventory)
#
### compute system MUF for total system operation
#    if (melter_failure_event==False):
    true_muf=abs(true_system_inventory-true_processed_inventory)
    expected_muf=abs(expected_system_inventory-expected_processed_inventory)
    measured_muf=abs(measured_system_inventory-measured_processed_inventory)
#    else:
#       true_muf=abs(true_system_inventory-true_processed_inventory-true_final_inventory)
#	expected_muf=abs(expected_system_inventory-expected_processed_inventory-expected_final_inventory)
#       measured_muf=abs(measured_system_inventory-measured_processed_inventory-measured_final_inventory)
# end if    

    # print 'Facility inspection','\n','Operation time','%.4f'%operation_time,'(d)','\n'
    # print 'True storage buffer inventory','%.4f'%true_storage_inventory,'(kg)','\n','Expected storage buffer inventory','%.4f'%expected_storage_inventory,'(kg)','\n','Measured storage buffer inventory','%.4f'%measured_storage_inventory,'(kg)','\n'
    # print 'True processed inventory','%.4f'%true_processed_inventory,'(kg)','\n','Expected processed inventory','%.4f'%expected_processed_inventory,'(kg)','\n','Measured processed inventory','%.4f'%measured_processed_inventory,'(kg)','\n'
    # print 'True system inventory','%.4f'%true_system_inventory,'(kg)','\n','Expected system inventory','%.4f'%expected_system_inventory,'(kg)','\n','Measured system inventory','%.4f'%measured_system_inventory,'(kg)','\n'    
    # print 'True campaign MUF','%.4f'%true_mufc,'(kg)','\n','Expected campaign MUF','%.4f'%expected_mufc,'(kg)','\n','Measured campaign MUF','%.4f'%measured_mufc,'(kg)','\n'
    # print 'True system MUF','%.4f'%true_muf,'(kg)','\n','Expected system MUF','%.4f'%expected_muf,'(kg)','\n','Measured system MUF','%.4f'%measured_muf,'(kg)','\n'
    log_file.write('Facility inspection \nOperation time %.4f (d)\n\n'%(operation_time))
    log_file.write('True storage buffer inventory %.4f (kg) \nExpected storage buffer inventory %.4f (kg) \nMeasured storage buffer inventory %.4f (kg)\n\n'%(true_storage_inventory,expected_storage_inventory,measured_storage_inventory))
    log_file.write('True processed inventory %.4f (kg) \nExpected processed inventory %.4f (kg) \nMeasured processed inventory %.4f (kg) \n\n'%(true_processed_inventory,expected_processed_inventory,measured_processed_inventory))
    log_file.write('True system inventory %.4f (kg) \nExpected system inventory %.4f (kg) \nMeasured system inventory %.4f (kg) \n\n'%(true_system_inventory,expected_system_inventory,measured_system_inventory))
    log_file.write('True campaign MUF %.4f (kg) \nExpected campaign MUF %.4f (kg)\nMeasured campaign MUF %.4f (kg) \n\n'%(true_mufc,expected_mufc,measured_mufc))
    log_file.write('True system MUF %.4f (kg)\nExpected system MUF %.4f (kg) \nMeasured system MUF %.4f (kg)\n\n\n'%(true_muf,expected_muf,measured_muf))
###
    return(operation_time,melter_failure_time,trimmer_failure_time,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc)
########################################################################
#
# EOF
#
########################################################################
