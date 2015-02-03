########################################################################
# R.A.Borrelli
# @TheDoctorRAB 
# rev.02.February.2015
# v1.2
########################################################################
#
# v1.0: Basic structure to compute inventory; make material flow work
# v1.1: Add edge travel time; clean up variables and dummys
# v1.2: Weibull distrubution applied to melter failure
#
########################################################################
# 
# Most of the general comments have been removed from the code and sent to the documentation folder.
# Comment files are in markdown so they can be viewed in github or related readers.
#
########################################################################
#
# This is the control file that governs the fuel fabrication subsystem in the commercial pyroprocessing facility.
# Each vertex in the fuel fabrication system is its own module, including maintenance.
# The fuel fabrication subsystem itself is its own module for the full commerical pyroprocessing facility.
#
########################################################################
#
#
#
########################################################################
#
# imports
#
import numpy
import io_functions as io
import failure_analysis_weibull as melter_weibull
#
########################################################################
# 
#
#
########################################################################
#
# get simulation directories 
#
home_dir,input_dir,output_data_dir,output_figure_dir=io.get_simulation_dir()
#
########################################################################
#
#
#
########################################################################
#
# read input data
#
batch,crucible_fraction,edge_time,facility_operation,melter_failure_false_alarm_threshold,end_of_campaign_false_alarm_threshold,melter_failure_inspection_time,campaign_inspection_time,kmp_measurement_uncertainty,kmp_time,kmp_measurement_threshold,maximum_kmp,melter_failure_number,melter_failure_type,melter_failure_probability,melter_failure_maintenance_time,melter_cleaning_time,process_time,storage_inventory_start,weibull_beta_melter,weibull_eta_melter=io.input_parameters(home_dir,input_dir,output_data_dir)
#
########################################################################
#
#
#
########################################################################
#
# open output files 
#
time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,end_of_campaign_false_alarm_counter_output,melter_failure_false_alarm_counter_output,true_kmp0,true_kmp1,true_kmp2,true_kmp3,true_kmp4,expected_kmp0,expected_kmp1,expected_kmp2,expected_kmp3,expected_kmp4,measured_kmp0,measured_kmp1,measured_kmp2,measured_kmp3,measured_kmp4,true_heel,expected_heel,measured_heel,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output,melter_probability_density_function_output,melter_unreliability_function_output=io.open_output_files(home_dir,output_data_dir)
#
########################################################################
#
#
#
########################################################################
#
# initialize parameters
#
operation_time,melter_failure_time,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,total_campaign,total_batch,melter_failure_counter,true_weight,expected_weight,measured_weight,true_crucible,expected_crucible,measured_crucible,accumulated_true_crucible,accumulated_expected_crucible,accumulated_measured_crucible,melter_true_muf,melter_expected_muf,melter_measured_muf,melter_true_mufc,melter_expected_mufc,melter_measured_mufc,end_of_campaign_false_alarm_counter,melter_failure_false_alarm_counter,end_of_campaign_false_alarm,melter_failure_false_alarm,melter_failure_event,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,end_of_campaign_false_alarm_test,melter_failure_false_alarm_test,melter_process_counter,trimmer_process_counter,melter_probability_density_function_evaluate,melter_probability_density_function_failure_evaluate,melter_unreliability_function_evaluate,melter_unreliability_function_failure_evaluate=io.initialize_parameters(storage_inventory_start)
#
########################################################################
#
#
#
########################################################################
#
# calculations for TIME=0
#
melter_probabbility_density_function_evaluate=melter_weibull.somethingfunction(operation_time,weibull_beta_melter,weibull_eta_melter)
melter_unreliability_function_evaluate=melter_weibuill.somethingfunction(operation_time,weibull_beta_melter,weibull_eta_melter)
#
melter_probability_density_function_failure_evaluate=melter_weibull.somethingfunction(failure_time,weibull_beta_melter,weibull_eta_melter)
melter_unreliability_function_failure_evaluate=melter.weibull.somethingfunction(failure_time,weibull_beta_melter,weibull_eta_melter)
#
########################################################################
####### main process loop
print 'Start facility operation.'
###
#
###
while(operation_time<=facility_operation):
    print 'Starting campaign:',total_campaign,'\n'
###
#
####### calculations for operation_time = 0
#######
#
#
#
####### (p): Write output to files 
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output,melter_probability_density_function_output,melter_unreliability_function_output=des_f.write_output(operation_time,failure_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,melter_probability_density_function_evaluate,melter_probability_density_function_failure_evaluate,melter_unreliability_function_evaluate,melter_unreliability_function_failure_evaluate,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output,melter_probability_density_function_output,melter_unreliability_function_output)
### (v): False alarm write
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
### (v): False alarm write
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,failure_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### (d): Storage buffer preparation
    operation_time,true_weight,expected_weight,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory=des_f.storage_transfer(operation_time,batch,process_time[0],true_weight,expected_weight,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory)
#######
#
#
#
### data output routines
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### edge transition
# Storage Buffer to KMP0
    operation_time=des_f.edge_transition(operation_time,edge_time[0])
#######
#
#
#
####### KMP measurement if active (0)
    operation_time,measured_weight,measured_storage_inventory,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,measured_system_inventory=des_f.kmp_measurement(operation_time,kmp_measurement_uncertainty[0],kmp_time[0],kmp_measurement_threshold[0],true_weight,expected_weight,measured_storage_inventory,measured_system_inventory,0)
### data output routines
    true_kmp0,expected_kmp0,measured_kmp0=des_f.kmp_write(operation_time,true_weight,expected_weight,measured_weight,true_kmp0,expected_kmp0,measured_kmp0)
#
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### edge transition
# Storage KMP0 to Melter
    operation_time=des_f.edge_transition(operation_time,edge_time[1])
#######
#
#
#
####### Melter
    operation_time,true_weight,expected_weight,accumulated_true_crucible,accumulated_expected_crucible,melter_failure_event,melter_failure_counter,melter_process_counter=des_f.melter(operation_time,true_weight,expected_weight,melter_failure_number,melter_failure_type,melter_failure_probability,process_time[1],crucible_fraction,accumulated_true_crucible,accumulated_expected_crucible,melter_failure_event,melter_failure_counter,melter_process_counter)
### data output routines
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
#######
# need to fix the frequency analysis for the failure
# if there is a failure, there needs to be an associated time lapse to transfer to KMP3 for batch and then heel.
# change failure to every 30 days
#######
#
#
#
########################################################################
### Maintenance loop
# If there is a failure, operation stops, material moves to recycle
#    while(melter_failure_event==True):
#        print 'Entering maintenance loop','\n\n'
### 
#
### KMP measurement if active (3)
#        operation_time,measured_weight,measured_storage_inventory=des_f.kmp_measurement(operation_time,measurement_uncertainty[3],kmp_delay_time[3],measurement_threshold_system[3],true_weight,expected_weight,measured_storage_inventory,measured_system_inventory,3)
###
#
### data output routines
#        true_kmp3,expected_kmp3,measured_kmp3=des_f.kmp_write(operation_time,true_weight,expected_weight,measured_weight,true_kmp3,expected_kmp3,measured_kmp3)
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Recycle storage
#        operation_time=des_f.recycle_storage(operation_time,process_time[3])
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Failure inspection
#        operation_time,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc=des_f.mass_balance(operation_time,inspection_time,storage_inventory_start,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_muf,expected_muf,measured_muf,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,melter_failure_event,true_system_inventory,expected_system_inventory,measured_system_inventory)
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Test for false alarm
#        system_false_alarm_counter,system_false_alarm,system_alarm_test=des_f.false_alarm_test(system_false_alarm_limit,system_false_alarm_counter,expected_muf,measured_muf)
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Conduct cleaning process
# Heel is removed from the melter
#        operation_time=des_f.melter_cleaning(operation_time,melter_cleaning_time)
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Measure heel at KMP (3) 
#        operation_time,accumulated_measured_crucible,measured_storage_inventory=des_f.kmp_measurement(operation_time,measurement_uncertainty[3],kmp_delay_time[3],measurement_threshold_system[3],accumulated_true_crucible,accumulated_expected_crucible,measured_storage_inventory,measured_system_inventory,3)
###
#
### data output routines
#        true_heel,expected_heel,measured_heel=des_f.kmp_write(operation_time,accumulated_true_crucible,accumulated_expected_crucible,accumulated_measured_crucible,true_heel,expected_heel,measured_heel)
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Recycle storage
#        operation_time=des_f.recycle_storage(operation_time,process_time[3])
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Perform maintenance
#        operation_time,true_weight,expected_weight,measured_weight,accumulated_true_crucible,accumulated_expected_crucible,accumulated_measured_crucible,true_initial_inventory,expected_initial_inventory,measured_initial_inventory=des_f.maintenance_melter(operation_time,failure_delay_time[0],true_weight,expected_weight,measured_weight,accumulated_true_crucible,accumulated_expected_crucible,accumulated_measured_crucible,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,true_muf,expected_muf,measured_muf)
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Restart inspection
#        operation_time,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc=des_f.mass_balance(operation_time,inspection_time,storage_inventory_start,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_muf,expected_muf,measured_muf,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,melter_failure_event,true_system_inventory,expected_system_inventory,measured_system_inventory)
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Test for false alarm
#        system_false_alarm_counter,system_false_alarm,system_alarm_test=des_f.false_alarm_test(system_false_alarm_limit,system_false_alarm_counter,expected_muf,measured_muf)
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### back through to melter via KMP (-3)
#        operation_time,measured_weight,measured_storage_inventory=des_f.kmp_measurement(operation_time,measurement_uncertainty[3],kmp_delay_time[3],measurement_threshold_system[3],true_weight,expected_weight,measured_storage_inventory,measured_system_inventory,-3)
###
#
### data output routines
#        true_kmp4,expected_kmp4,measured_kmp4=des_f.kmp_write(operation_time,true_weight,expected_weight,measured_weight,true_kmp4,expected_kmp4,measured_kmp4)
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Melter
#        operation_time,true_weight,expected_weight,accumulated_true_crucible,accumulated_expected_crucible,melter_failure_event,total_melter_failure=des_f.melter(operation_time,true_weight,expected_weight,failure_probability[0],process_time[1],crucible_fraction_limit,accumulated_true_crucible,accumulated_expected_crucible,melter_failure_event,total_melter_failure)
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
# need to fix the frequency analysis for the failure
###
#
###
#        print 'Maintenance complete','\n','Resume processing','\n\n'
### end maintenance loop
########################################################################
#
#
#
####### return to main process loop
#
#
#
####### edge transition
# Melter to KMP1
    operation_time=des_f.edge_transition(operation_time,edge_time[2])
#######
#
#
#
####### KMP measurement if active (1)
    operation_time,measured_weight,measured_storage_inventory=des_f.kmp_measurement(operation_time,kmp_measurement_uncertainty[1],kmp_time[1],kmp_measurement_threshold[1],true_weight,expected_weight,measured_storage_inventory,measured_system_inventory,1)
### data output routines
    true_kmp1,expected_kmp1,measured_kmp1=des_f.kmp_write(operation_time,true_weight,expected_weight,measured_weight,true_kmp1,expected_kmp1,measured_kmp1)
#
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### edge transition
# KMP1 to Trimmer
    operation_time=des_f.edge_transition(operation_time,edge_time[3])
#######
#
#
#
####### Trimmer
# material changes due to fines (trimming leftovers) currently neglected
    operation_time,true_weight,expected_weight,trimmer_process_counter=des_f.trimmer(operation_time,process_time[2],true_weight,expected_weight,trimmer_process_counter)
### data output routines
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### edge transition
# Trimmer to KMP2
    operation_time=des_f.edge_transition(operation_time,edge_time[4])
#######
#
#
#
####### KMP measurement if active (2)
    operation_time,measured_weight,measured_processed_inventory=des_f.kmp_measurement(operation_time,kmp_measurement_uncertainty[2],kmp_time[2],kmp_measurement_threshold[2],true_weight,expected_weight,measured_processed_inventory,measured_system_inventory,2)
### data output routines
    true_kmp2,expected_kmp2,measured_kmp2=des_f.kmp_write(operation_time,true_weight,expected_weight,measured_weight,true_kmp2,expected_kmp2,measured_kmp2)
#
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### edge transition
# KMP2 to Product Storage
    operation_time=des_f.edge_transition(operation_time,edge_time[5])
#######
#
#
#
####### Product storage and final processing
    operation_time,true_processed_inventory,expected_processed_inventory=des_f.product_processing(operation_time,process_time[4],true_weight,expected_weight,true_processed_inventory,expected_processed_inventory)
### data output routines
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
###### End of campaign inspection
    operation_time,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc=des_f.mass_balance(operation_time,campaign_inspection_time,storage_inventory_start,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_muf,expected_muf,measured_muf,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,melter_failure_event,true_system_inventory,expected_system_inventory,measured_system_inventory)
### Test for false alarm
#    system_false_alarm_counter,system_false_alarm,system_alarm_test=des_f.false_alarm_test(system_false_alarm_limit,system_false_alarm_counter,expected_muf,measured_muf)
### data output routines
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### Loop back to start next campaign
# reset campaign based variables and advance campaign counter
    total_campaign,total_batch=des_f.end_of_campaign(total_campaign,total_batch)
    true_weight,expected_weight,measured_weight=des_f.reset_weight()
#######
#
#
#
####### end facility operation loop
########################################################################
#
#
#    
####### close output files
time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,end_of_campaign_false_alarm_counter_output,melter_failure_false_alarm_counter_output,true_kmp0,true_kmp1,true_kmp2,true_kmp3,true_kmp4,expected_kmp0,expected_kmp1,expected_kmp2,expected_kmp3,expected_kmp4,measured_kmp0,measured_kmp1,measured_kmp2,measured_kmp3,measured_kmp4,true_heel,expected_heel,measured_heel,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.close_files(time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,end_of_campaign_false_alarm_counter_output,melter_failure_false_alarm_counter_output,true_kmp0,true_kmp1,true_kmp2,true_kmp3,true_kmp4,expected_kmp0,expected_kmp1,expected_kmp2,expected_kmp3,expected_kmp4,measured_kmp0,measured_kmp1,measured_kmp2,measured_kmp3,measured_kmp4,true_heel,expected_heel,measured_heel,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
####### 
#
#
#
#######################################################################
#
# end main fuel fabrication model
#
#######################################################################
#
#
#
########################################################################
####### postprocessing
#
#
#
### system false alarm probability
#des_postproc.false_alarm_probability('system',home_dir,output_data_dir)
###
#
### plots
#des_postproc.make_plots(operation_time,total_campaign,storage_inventory_start,total_melter_failure,system_false_alarm_counter,home_dir,output_data_dir,output_figure_dir)
###
#
#
#
####### end postprocessing
#######################################################################
#
#
#
########################################################################
#      EOF
########################################################################
