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
# (1): mass balance
#
########################################################################
#
#
#
########################################################################
#
# (1): mass balance
# 
#
###
def mass_balance(operation_time,time_delay,storage_inventory_start,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_quantity,expected_quantity,measured_quantity,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_muf,expected_muf,measured_muf,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,melter_failure_event,true_system_inventory,expected_system_inventory,measured_system_inventory):
### 
    operation_time=operation_time+delay
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
### compute MUFc
    true_mufc=abs(true_initial_inventory-true_final_inventory)
    expected_mufc=abs(expected_initial_inventory-expected_final_inventory)
    measured_mufc=abs(measured_initial_inventory-measured_final_inventory)
#
### compute system MUF
    if (melter_failure_event==False):
        true_muf=abs(true_system_inventory-true_processed_inventory)
        expected_muf=abs(expected_system_inventory-expected_processed_inventory)
        measured_muf=abs(measured_system_inventory-measured_processed_inventory)
    else:
        true_muf=abs(true_system_inventory-true_processed_inventory-true_final_inventory)
        expected_muf=abs(expected_system_inventory-expected_processed_inventory-expected_final_inventory)
        measured_muf=abs(measured_system_inventory-measured_processed_inventory-measured_final_inventory)
# end if    

    print 'Facility inspection','\n','Operation time','%.4f'%operation_time,'(d)','\n'
    print 'True storage buffer inventory','%.4f'%true_storage_inventory,'(kg)','\n','Expected storage buffer inventory','%.4f'%expected_storage_inventory,'(kg)','\n','Measured storage buffer inventory','%.4f'%measured_storage_inventory,'(kg)','\n'
    print 'True processed inventory','%.4f'%true_processed_inventory,'(kg)','\n','Expected processed inventory','%.4f'%expected_processed_inventory,'(kg)','\n','Measured processed inventory','%.4f'%measured_processed_inventory,'(kg)','\n'
    print 'True system inventory','%.4f'%true_system_inventory,'(kg)','\n','Expected system inventory','%.4f'%expected_system_inventory,'(kg)','\n','Measured system inventory','%.4f'%measured_system_inventory,'(kg)','\n'    
    print 'True campaign MUF','%.4f'%true_mufc,'(kg)','\n','Expected campaign MUF','%.4f'%expected_mufc,'(kg)','\n','Measured campaign MUF','%.4f'%measured_mufc,'(kg)','\n'
    print 'True system MUF','%.4f'%true_muf,'(kg)','\n','Expected system MUF','%.4f'%expected_muf,'(kg)','\n','Measured system MUF','%.4f'%measured_muf,'(kg)','\n'
###
    return(operation_time,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc)
########################################################################
#
#
#
####### (k): recycle storage
# Metal alloy is removed from the melter and moved to recycle on failure
###
#
###
def recycle_storage(operation_time,delay):
###
    print 'Material transferred to Recycle','\n\n'
    operation_time=operation_time+delay
###
    return(operation_time)
########################################################################
#
#
#
####### (m): Failure test
# Tests for a failure in equipment
# This is meant to be generalized for multiple equipment 
###
#
# failure control should be its own module
###
def failure_test(operation_time,equipment_failure_number,equipment_failure_type,equipment_failure_probability,failure_event,equipment_failure_counter,melter_process_counter):
###
#
###
# currently there is only a single general failure
# this needs to be the same to compare designs
# the failure analysis will have to be its own module later on
###
#
###
    print 'Failure test'
    print 'Number of failure types:',equipment_failure_number
    print 'Failure type:',equipment_failure_type[0]
    print 'Failure probability:','%.4f'%equipment_failure_probability[0],'\n'
###
#
###
# the old failure test just sampled from the standard normal distribution 
# if the corresponding probability range contained the prescribed frequency then a failure occurred
#
#    failure_test=0
#    lower_failure_test=0
#    upper_failure_test=0
#    lower_failure_pdf=0
#    upper_failure_pdf=0
#
#    failure_test=numpy.random.randn()    
#    lower_failure_test=failure_test-1
#    upper_failure_test=failure_test+1
#    lower_failure_pdf=scipy.stats.norm.pdf(lower_failure_test)
#    upper_failure_pdf=scipy.stats.norm.pdf(upper_failure_test)
#    print 'Test range:','%.4f'%lower_failure_test,'%.4f'%upper_failure_test
#    print 'Probability range:','%.4f'%lower_failure_pdf,'%.4f'%equipment_failure_probability[0],'%.4f'%upper_failure_pdf
#    if (lower_failure_pdf<=equipment_failure_probability[0]<=upper_failure_pdf):     
#        print 'Failure'
#        failure_event=True
#        equipment_failure_counter=equipment_failure_counter+1
#        print 'Failure #:',equipment_failure_counter,'\n\n'
#    elif (upper_failure_pdf<=equipment_failure_probability[0]<=lower_failure_pdf):
#        print 'Failure'
#        failure_event=True
#        equipment_failure_counter=equipment_failure_counter+1
#        print 'Failure #:',equipment_failure_counter,'\n\n'    
#    else:
#        print 'No failure','\n\n'
#        failure_event=False
###
#
### there is a failure every 1/equipment_failure_probability day
# this is a 'forced failure' where a failure occurs at about the same time for different designs
    print operation_time,equipment_failure_counter+1,operation_time*equipment_failure_probability[0]
###
    return(failure_event,equipment_failure_counter)
########################################################################
#
#
#
####### (n): End of campaign reset
# Advance the counters
###
#
###
def end_of_campaign(total_campaign,total_batch):
###
    print 'Campaign',total_campaign,'complete.','\n\n'
    total_campaign=total_campaign+1
    total_batch=total_batch+1
###
    return(total_campaign,total_batch)
########################################################################
#
#
#
####### (n): End of campaign reset weight
# Zero out the weights
###
#
###
def reset_weight():
###
    true_weight=0
    expected_weight=0
    measured_weight=0
###
    return(true_weight,expected_weight,measured_weight)
########################################################################
#
#
#
########################################################################
#
# (N): close output files
#
#######
def close_files(time_output,campaign_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_kmp0,true_kmp1,true_kmp2,true_kmp3,true_kmp4,expected_kmp0,expected_kmp1,expected_kmp2,expected_kmp3,expected_kmp4,measured_kmp0,measured_kmp1,measured_kmp2,measured_kmp3,measured_kmp4,true_heel,expected_heel,measured_heel,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output):
#######
    time_output.close()
    campaign_output.close()
    measured_storage_inventory_output.close()
    true_weight_output.close()
    expected_weight_output.close()
    measured_weight_output.close()
    true_muf_output.close()
    expected_muf_output.close()
    measured_muf_output.close()
    true_mufc_output.close()
    expected_mufc_output.close()
    measured_mufc_output.close()    
    true_processed_inventory_output.close()
    expected_processed_inventory_output.close()
    measured_processed_inventory_output.close()
    total_melter_failure_output.close()
    true_heel.close()
    expected_heel.close()
    measured_heel.close()
    measured_system_inventory_output.close()
    melter_process_counter_output.close()
    trimmer_process_counter_output.close()
###
    return(time_output,campaign_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_kmp0,true_kmp1,true_kmp2,true_kmp3,true_kmp4,expected_kmp0,expected_kmp1,expected_kmp2,expected_kmp3,expected_kmp4,measured_kmp0,measured_kmp1,measured_kmp2,measured_kmp3,measured_kmp4,true_heel,expected_heel,measured_heel,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#
########################################################################
#
#
#
#
#
#
####### (s): Melter cleaning procedure
# Cleans out the heel from the melter when there is a failure
# Sends the heel to the Recycle Storage and combines with the batch
# Heel must be measured at KMP3 if it is active
###
#
###
def melter_cleaning(operation_time,delay):
###
    print 'Melter cleaning','\n\n'
    operation_time=operation_time+delay
###
    return(operation_time)
########################################################################
#
#
#
####### (t): Maintenance
# Maintenance is performed on the equipment
# Currently this is only for the melter
###
#
###
def maintenance_melter(operation_time,delay,true_weight,expected_weight,measured_weight,accumulated_true_crucible,accumulated_expected_crucible,accumulated_measured_crucible,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,true_muf,expected_muf,measured_muf):
###
    print 'Performing maintenance','\n\n'
    operation_time=operation_time+delay
#
    true_initial_inventory=true_weight+true_muf
    expected_initial_inventory=expected_weight+expected_muf
    measured_initial_inventory=measured_weight+measured_muf
#
    true_weight=true_weight+accumulated_true_crucible
    expected_weight=expected_weight+accumulated_expected_crucible
    measured_weight=measured_weight+accumulated_measured_crucible
#
    accumulated_true_crucible=0
    accumulated_expected_crucible=0
    accumulated_measured_crucible=0
###
    return(operation_time,true_weight,expected_weight,measured_weight,accumulated_true_crucible,accumulated_expected_crucible,accumulated_measured_crucible,true_initial_inventory,expected_initial_inventory,measured_initial_inventory)
########################################################################
#
# EOF
#
########################################################################
