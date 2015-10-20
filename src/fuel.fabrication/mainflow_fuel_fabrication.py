########################################################################
# R.A.Borrelli
# @TheDoctorRAB 
# rev.20.October.2015
# v1.2
########################################################################
#
# v1.0: Basic structure to compute inventory and make material flow work
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
# imports
#
import numpy
import io_functions as io
import system_false_alarm 
import vertex_storage_buffer as storage_buffer
import edge_transition as edge_trans
import key_measurement_points as kmp
import vertex_melter as melter
import failure_distribution_calculation as failure_calculation
import sys
#
########################################################################
#
# diagnostics 
# 
sys.stdout=open('log.txt','w+') #all the print statements will write to file 
#
########################################################################
#
#
#
#   PREPROCESSING
#
#
#
########################################################################
#
print 'Fuel fabrication','\n\n','PREPROCESSING'
#
root_dir='/home/usr/borrelli/pyroprocessing_discrete.event.simulation'
#
####### get directory paths  
input_dir,output_dir,edge_transition_dir,failure_distribution_dir,failure_equipment_dir,kmps_dir,process_states_dir,system_false_alarm_dir,data_dir,figures_dir,system_odir,material_flow_odir,inventory_odir,false_alarm_odir,kmps_odir,muf_odir,equipment_failure_odir,system_gdir,material_flow_gdir,inventory_gdir,false_alarm_gdir,kmps_gdir,muf_gdir,equipment_failure_gdir=io.get_dir_path(root_dir,'fuel.fabrication')
#######
#
####### read input data
facility_operation,storage_buffer_process_time,injection_casting_process_time,trimming_process_time,product_process_time=io.input_system_operation(process_states_dir) #system
#
batch,unprocessed_storage_inventory=io.input_storage_buffer(process_states_dir) #material flow
#
crucible_fraction,melter_failure_type,melter_failure_rate,melter_failure_maintenance_time,melter_cleaning_time,weibull_beta_melter,weibull_eta_melter,melter_failure_number=io.input_equipment(process_states_dir,failure_equipment_dir,failure_distribution_dir,'melter') #vertex melter
fines_fraction,trimmer_failure_type,trimmer_failure_rate,trimmer_failure_maintenance_time,trimmer_cleaning_time,weibull_beta_trimmer,weibull_eta_trimmer,trimmer_failure_number=io.input_equipment(process_states_dir,failure_equipment_dir,failure_distribution_dir,'trimmer') #vertex trimmer
#
end_of_campaign_false_alarm_inspection_time,end_of_campaign_false_alarm_threshold=io.input_system_false_alarm(system_false_alarm_dir,'system') #false alarm system
melter_failure_false_alarm_inspection_time,melter_failure_false_alarm_threshold=io.input_system_false_alarm(system_false_alarm_dir,'melter') #false alarm melter
trimmer_failure_false_alarm_inspection_time,trimmer_failure_false_alarm_threshold=io.input_system_false_alarm(system_false_alarm_dir,'trimmer') #false alarm trimmer
#
edge_transition=io.input_edge_transition(edge_transition_dir) #edge transition
#
kmp_id,kmp_time,kmp_uncertainty,kmp_threshold,maximum_kmp=io.input_kmps(kmps_dir) #key measurement points
#######
#
####### open output files 
system_time_output,campaign_output=io.output_system_operation(system_odir) #system
melter_failure_time_output,melter_process_counter_output=io.output_process_operation(system_odir,'melter') #melter
trimmer_failure_time_output,trimmer_process_counter_output=io.output_process_operation(system_odir,'trimmer') #trimmer 
#
batch_output,true_weight_output,expected_weight_output,measured_weight_output=io.output_material_flow(material_flow_odir) #material flow
true_heel_output,expected_heel_output,measured_heel_output=io.output_process_loss(material_flow_odir,'melter') #melter
true_fines_output,expected_fines_output,measured_fines_output=io.output_process_loss(material_flow_odir,'trimmer') #trimmer
#
true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output=io.output_inventory(inventory_odir) #inventory 
#
end_of_campaign_false_alarm_counter_output=io.output_false_alarm(false_alarm_odir,'end.of.campaign') #false alarm system
melter_failure_false_alarm_counter_output=io.output_false_alarm(false_alarm_odir,'melter.failure') #false alarm melter
trimmer_failure_false_alarm_counter_output=io.output_false_alarm(false_alarm_odir,'trimmer') #false alarm trimmer
#
true_kmp_output,expected_kmp_output,measured_kmp_output=io.output_kmps(kmps_odir) #key measurement points
#
melter_failure_total_counter_output,melter_probability_density_function_output,melter_unreliability_function_output=io.output_equipment_failure(equipment_failure_odir,'melter') #failure melter
trimmer_failure_total_counter_output,trimmer_probability_density_function_output,trimmer_unreliability_function_output=io.output_equipment_failure(equipment_failure_odir,'trimmer') #failure trimmer
#
melter_true_muf_output,melter_expected_muf_output,melter_measured_muf_output,melter_true_mufc_output,melter_expected_mufc_output,melter_measured_mufc_output=io.output_muf(muf_odir,'melter') #muf melter
trimmer_true_muf_output,trimmer_expected_muf_output,trimmer_measured_muf_output,trimmer_true_mufc_output,trimmer_expected_mufc_output,trimmer_measured_mufc_output=io.output_muf(muf_odir,'trimmer') #muf trimmer
#######
#
####### initialize parameters
operation_time,total_campaign=io.initialize_system() #system
#
total_batch,true_weight,expected_weight,measured_weight=io.initialize_material_flow() #material flow 
true_heel,expected_heel,measured_heel,accumulated_true_heel,accumulated_expected_heel,accumulated_measured_heel=io.initialize_equipment_process_loss() #process loss melter
true_fines,expected_fines,measured_fines,accumulated_true_fines,accumulated_expected_fines,accumulated_measured_fines=io.initialize_equipment_process_loss() #process loss trimmer 
#
true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,true_initial_inventory,expected_initial_inventory,measured_initial_inventory=io.initialize_inventory(unprocessed_storage_inventory) #inventory 
#
end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm,end_of_campaign_false_alarm_test=io.initialize_false_alarm() #false alarm system
melter_failure_false_alarm_counter,melter_failure_false_alarm,melter_failure_false_alarm_test=io.initialize_false_alarm() #false alarm melter
trimmer_failure_false_alarm_counter,trimmer_failure_false_alarm,trimmer_failure_false_alarm_test=io.initialize_false_alarm() #false alarm trimmer
#
melter_failure_time,melter_failure_counter,melter_failure_event,melter_process_counter,melter_probability_density_function_evaluate,melter_probability_density_function_failure_evaluate,melter_unreliability_function_evaluate,melter_unreliability_function_failure_evaluate,melter_process_counter=io.initialize_equipment() #failure melter
trimmer_failure_time,trimmer_failure_counter,trimmer_failure_event,trimmer_process_counter,trimmer_probability_density_function_evaluate,trimmer_probability_density_function_failure_evaluate,trimmer_unreliability_function_evaluate,trimmer_unreliability_function_failure_evaluate,trimmer_process_counter=io.initialize_equipment() #failure trimmer
#
melter_true_muf,melter_expected_muf,melter_measured_muf,melter_true_mufc,melter_expected_mufc,melter_measured_mufc=io.initialize_muf() #muf melter
trimmer_true_muf,trimmer_expected_muf,trimmer_measured_muf,trimmer_true_mufc,trimmer_expected_mufc,trimmer_measured_mufc=io.initialize_muf() #muf trimmer
#######
#
####### failure distribution calculations
melter_probability_density_function_evaluate,melter_unreliability_function_evaluate,melter_probability_density_function_failure_evaluate,melter_unreliability_function_failure_evaluate=failure_calculation.failure_distribution_calculation(operation_time,melter_failure_time,weibull_beta_melter,weibull_eta_melter) #failure melter
trimmer_probability_density_function_evaluate,trimmer_unreliability_function_evaluate,trimmer_probability_density_function_failure_evaluate,trimmer_unreliability_function_failure_evaluate=failure_calculation.failure_distribution_calculation(operation_time,trimmer_failure_time,weibull_beta_trimmer,weibull_eta_trimmer) #failure trimmer
#######
#
####### data writing for TIME=0
system_time_output=io.write_system_time(operation_time,system_time_output) #time system 
melter_failure_time_output=io.write_system_time(melter_failure_time,melter_failure_time_output) #time melter 
trimmer_failure_time_output=io.write_system_time(trimmer_failure_time,trimmer_failure_time_output) #time trimmer 
#
campaign_output=io.write_campaign(operation_time,total_campaign,campaign_output) #campaign
#
melter_process_counter_output=io.write_process_counter(operation_time,melter_process_counter,melter_process_counter_output) #process counter melter
trimmer_process_counter_output=io.write_process_counter(operation_time,trimmer_process_counter,trimmer_process_counter_output) #process counter trimmer
#
batch_output,true_weight_output,expected_weight_output,measured_weight_output=io.write_material_flow(operation_time,total_batch,true_weight,expected_weight,measured_weight,batch_output,true_weight_output,expected_weight_output,measured_weight_output) #material flow
#
true_heel_output,expected_heel_output,measured_heel_output=io.write_process_loss(operation_time,true_heel,expected_heel,measured_heel,true_heel_output,expected_heel_output,measured_heel_output) #process loss melter
true_fines_output,expected_fines_output,measured_fines_output=io.write_process_loss(operation_time,true_fines,expected_fines,measured_fines,true_fines_output,expected_fines_output,measured_fines_output) #process loss trimmer
#
true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output=io.write_inventory(operation_time,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output) #inventory 
#
melter_true_muf_output,melter_expected_muf_output,melter_measured_muf_output,melter_true_mufc_output,melter_expected_mufc_output,melter_measured_mufc_output=io.write_muf(operation_time,melter_true_muf,melter_expected_muf,melter_measured_muf,melter_true_mufc,melter_expected_mufc,melter_measured_mufc,melter_true_muf_output,melter_expected_muf_output,melter_measured_muf_output,melter_true_mufc_output,melter_expected_mufc_output,melter_measured_mufc_output) #muf melter
trimmer_true_muf_output,trimmer_expected_muf_output,trimmer_measured_muf_output,trimmer_true_mufc_output,trimmer_expected_mufc_output,trimmer_measured_mufc_output=io.write_muf(operation_time,trimmer_true_muf,trimmer_expected_muf,trimmer_measured_muf,trimmer_true_mufc,trimmer_expected_mufc,trimmer_measured_mufc,trimmer_true_muf_output,trimmer_expected_muf_output,trimmer_measured_muf_output,trimmer_true_mufc_output,trimmer_expected_mufc_output,melter_measured_mufc_output) #muf trimmer
#
end_of_campaign_false_alarm_counter_output=io.write_end_of_campaign_false_alarm(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_test,end_of_campaign_false_alarm_counter_output) #false alarm system
melter_failure_false_alarm_counter_output=io.write_equipment_failure_false_alarm(operation_time,melter_failure_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_test,melter_failure_false_alarm_counter_output) #false alarm melter
trimmer_failure_false_alarm_counter_output=io.write_equipment_failure_false_alarm(operation_time,trimmer_failure_time,total_campaign,trimmer_failure_false_alarm_counter,trimmer_failure_false_alarm_threshold,trimmer_failure_false_alarm_test,trimmer_failure_false_alarm_counter_output) #false alarm trimmer
#
melter_failure_total_counter_output,melter_probability_density_function_output,melter_unreliability_function_output=io.write_equipment_failure(operation_time,melter_failure_time,total_campaign,melter_failure_counter,melter_process_counter,melter_probability_density_function_evaluate,melter_probability_density_function_failure_evaluate,melter_unreliability_function_evaluate,melter_unreliability_function_failure_evaluate,melter_failure_total_counter_output,melter_probability_density_function_output,melter_unreliability_function_output) #failure melter
trimmer_failure_total_counter_output,trimmer_probability_density_function_output,trimmer_unreliability_function_output=io.write_equipment_failure(operation_time,trimmer_failure_time,total_campaign,trimmer_failure_counter,trimmer_process_counter,trimmer_probability_density_function_evaluate,trimmer_probability_density_function_failure_evaluate,trimmer_unreliability_function_evaluate,trimmer_unreliability_function_failure_evaluate,trimmer_failure_total_counter_output,trimmer_probability_density_function_output,trimmer_unreliability_function_output) #failure trimmer
#
print 'END PREPROCESSING','\n\n'
#
########################################################################
#
#
#
# main process loop start
print 'Start facility operation'
#
#
#
########################################################################
#
# process loop
#
while(operation_time<=facility_operation):
    print 'Starting campaign:',total_campaign,'at time: ',operation_time,' days','\n'
#
########################################################################
#
#
#
#######
#
# storage buffer batch preparation process
#
    operation_time,melter_failure_time,trimmer_failure_time,true_weight,expected_weight,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory,true_initial_inventory,expected_initial_inventory=storage_buffer.batch_preparation(operation_time,melter_failure_time,trimmer_failure_time,storage_buffer_process_time,batch,true_weight,expected_weight,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory,true_initial_inventory,expected_initial_inventory)
#
# data writing
#
    system_time_output=io.write_system_time(operation_time,system_time_output) #system time 
    melter_failure_time_output=io.write_system_time(melter_failure_time,melter_failure_time_output) #melter 
    trimmer_failure_time_output=io.write_system_time(trimmer_failure_time,trimmer_failure_time_output) #trimmer
#
    campaign_output=io.write_campaign(operation_time,total_campaign,campaign_output) #campaign
#
    melter_process_counter_output=io.write_process_counter(operation_time,melter_process_counter,melter_process_counter_output) #process counter 
    trimmer_process_counter_output=io.write_process_counter(operation_time,trimmer_process_counter,trimmer_process_counter_output) #process counter 
#
    batch_output,true_weight_output,expected_weight_output,measured_weight_output=io.write_material_flow(operation_time,total_batch,true_weight,expected_weight,measured_weight,batch_output,true_weight_output,expected_weight_output,measured_weight_output) #material flow
#
    true_heel_output,expected_heel_output,measured_heel_output=io.write_heel(operation_time,true_heel,expected_heel,measured_heel,true_heel_output,expected_heel_output,measured_heel_output) #heel
#
    true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output=io.write_inventory(operation_time,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output) #inventory 
#
    melter_true_muf_output,melter_expected_muf_output,melter_measured_muf_output,melter_true_mufc_output,melter_expected_mufc_output,melter_measured_mufc_output=io.write_muf(operation_time,melter_true_muf,melter_expected_muf,melter_measured_muf,melter_true_mufc,melter_expected_mufc,melter_measured_mufc,melter_true_muf_output,melter_expected_muf_output,melter_measured_muf_output,melter_true_mufc_output,melter_expected_mufc_output,melter_measured_mufc_output) #muf 
#
    end_of_campaign_false_alarm_counter_output=io.write_end_of_campaign_false_alarm(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_test,end_of_campaign_false_alarm_counter_output) #end of campaign false alarm
#
    melter_failure_false_alarm_counter_output=io.write_equipment_failure_false_alarm(operation_time,melter_failure_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_test,melter_failure_false_alarm_counter_output) #melter failure false alarm
#
    melter_failure_total_counter_output,melter_probability_density_function_output,melter_unreliability_function_output=io.write_equipment_failure(operation_time,melter_failure_time,total_campaign,melter_failure_counter,melter_process_counter,melter_probability_density_function_evaluate,melter_probability_density_function_failure_evaluate,melter_unreliability_function_evaluate,melter_unreliability_function_failure_evaluate,melter_failure_total_counter_output,melter_probability_density_function_output,melter_unreliability_function_output) #melter failure
#
#######
#
# edge transition: storage buffer to KMP0
#
    operation_time=edge_trans.edge_transition(operation_time,edge_transition[0])
#
# data writing
#
    system_time_output=io.write_system_time(operation_time,system_time_output) #system time 
    melter_failure_time_output=io.write_system_time(melter_failure_time,melter_failure_time_output) #melter 
    trimmer_failure_time_output=io.write_system_time(trimmer_failure_time,trimmer_failure_time_output) #trimmer
#
#######
#
# KMP measurement (0)
#
    operation_time,measured_weight,measured_storage_inventory,measured_initial_inventory,measured_system_inventory=kmp.kmp_measurement(operation_time,kmp_time[0],kmp_uncertainty[0],kmp_threshold[0],true_weight,expected_weight,measured_storage_inventory,measured_system_inventory,0)
#
# data writing
#
    true_kmp_output,expected_kmp_output,measured_kmp_output=io.kmp_write(operation_time,true_weight,expected_weight,measured_weight,true_kmp_output,expected_kmp_output,measured_kmp_output,0) #kmp measurement data
#
    system_time_output=io.write_system_time(operation_time,system_time_output) #system time 
    melter_failure_time_output=io.write_system_time(melter_failure_time,melter_failure_time_output) #melter 
    trimmer_failure_time_output=io.write_system_time(trimmer_failure_time,trimmer_failure_time_output) #trimmer
#
    campaign_output=io.write_campaign(operation_time,total_campaign,campaign_output) #campaign
#
    melter_process_counter_output=io.write_process_counter(operation_time,melter_process_counter,melter_process_counter_output) #process counter 
    trimmer_process_counter_output=io.write_process_counter(operation_time,trimmer_process_counter,trimmer_process_counter_output) #process counter 
#
    batch_output,true_weight_output,expected_weight_output,measured_weight_output=io.write_material_flow(operation_time,total_batch,true_weight,expected_weight,measured_weight,batch_output,true_weight_output,expected_weight_output,measured_weight_output) #material flow
#
    true_heel_output,expected_heel_output,measured_heel_output=io.write_heel(operation_time,true_heel,expected_heel,measured_heel,true_heel_output,expected_heel_output,measured_heel_output) #heel
#
    true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output=io.write_inventory(operation_time,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output) #inventory 
#
    melter_true_muf_output,melter_expected_muf_output,melter_measured_muf_output,melter_true_mufc_output,melter_expected_mufc_output,melter_measured_mufc_output=io.write_muf(operation_time,melter_true_muf,melter_expected_muf,melter_measured_muf,melter_true_mufc,melter_expected_mufc,melter_measured_mufc,melter_true_muf_output,melter_expected_muf_output,melter_measured_muf_output,melter_true_mufc_output,melter_expected_mufc_output,melter_measured_mufc_output) #muf 
#
    end_of_campaign_false_alarm_counter_output=io.write_end_of_campaign_false_alarm(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_test,end_of_campaign_false_alarm_counter_output) #end of campaign false alarm
#
    melter_failure_false_alarm_counter_output=io.write_equipment_failure_false_alarm(operation_time,melter_failure_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_test,melter_failure_false_alarm_counter_output) #melter failure false alarm
#
    melter_failure_total_counter_output,melter_probability_density_function_output,melter_unreliability_function_output=io.write_equipment_failure(operation_time,melter_failure_time,total_campaign,melter_failure_counter,melter_process_counter,melter_probability_density_function_evaluate,melter_probability_density_function_failure_evaluate,melter_unreliability_function_evaluate,melter_unreliability_function_failure_evaluate,melter_failure_total_counter_output,melter_probability_density_function_output,melter_unreliability_function_output) #melter failure
#
#######
#
# edge transition: KMP0 to melter
# 
    operation_time=edge_trans.edge_transition(operation_time,edge_transition[1])
#
# data writing
#
#
    system_time_output=io.write_system_time(operation_time,system_time_output) #system time 
    melter_failure_time_output=io.write_system_time(melter_failure_time,melter_failure_time_output) #melter 
    trimmer_failure_time_output=io.write_system_time(trimmer_failure_time,trimmer_failure_time_output) #trimmer 
#
#######
#
# melter
#
    operation_time,melter_failure_time,true_weight,expected_weight,accumulated_true_heel,accumulated_expected_heel,melter_failure_event,melter_failure_counter,melter_process_counter=melter.injection_casting(operation_time,melter_failure_time,true_weight,expected_weight,melter_failure_number,melter_failure_type,melter_failure_rate,injection_casting_process_time,crucible_fraction,accumulated_true_heel,accumulated_expected_heel,melter_failure_event,melter_failure_counter,melter_process_counter)
#
# data writing
#
    system_time_output=io.write_system_time(operation_time,system_time_output) #system time 
    melter_failure_time_output=io.write_system_time(melter_failure_time,melter_failure_time_output) #melter 
    trimmer_failure_time_output=io.write_system_time(trimmer_failure_time,trimmer_failure_time_output) #trimmer 
#
    campaign_output=io.write_campaign(operation_time,total_campaign,campaign_output) #campaign
#
    melter_process_counter_output=io.write_process_counter(operation_time,melter_process_counter,melter_process_counter_output) #process counter 
    trimmer_process_counter_output=io.write_process_counter(operation_time,trimmer_process_counter,trimmer_process_counter_output) #process counter 
#
    batch_output,true_weight_output,expected_weight_output,measured_weight_output=io.write_material_flow(operation_time,total_batch,true_weight,expected_weight,measured_weight,batch_output,true_weight_output,expected_weight_output,measured_weight_output) #material flow
#
    true_heel_output,expected_heel_output,measured_heel_output=io.write_heel(operation_time,true_heel,expected_heel,measured_heel,true_heel_output,expected_heel_output,measured_heel_output) #heel
#
    true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output=io.write_inventory(operation_time,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output) #inventory 
#
    melter_true_muf_output,melter_expected_muf_output,melter_measured_muf_output,melter_true_mufc_output,melter_expected_mufc_output,melter_measured_mufc_output=io.write_muf(operation_time,melter_true_muf,melter_expected_muf,melter_measured_muf,melter_true_mufc,melter_expected_mufc,melter_measured_mufc,melter_true_muf_output,melter_expected_muf_output,melter_measured_muf_output,melter_true_mufc_output,melter_expected_mufc_output,melter_measured_mufc_output) #muf 
#
    end_of_campaign_false_alarm_counter_output=io.write_end_of_campaign_false_alarm(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_test,end_of_campaign_false_alarm_counter_output) #end of campaign false alarm
#
    melter_failure_false_alarm_counter_output=io.write_equipment_failure_false_alarm(operation_time,melter_failure_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_test,melter_failure_false_alarm_counter_output) #melter failure false alarm
#
    melter_failure_total_counter_output,melter_probability_density_function_output,melter_unreliability_function_output=io.write_equipment_failure(operation_time,melter_failure_time,total_campaign,melter_failure_counter,melter_process_counter,melter_probability_density_function_evaluate,melter_probability_density_function_failure_evaluate,melter_unreliability_function_evaluate,melter_unreliability_function_failure_evaluate,melter_failure_total_counter_output,melter_probability_density_function_output,melter_unreliability_function_output) #melter failure
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
#
#
# maintenance loop start 
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
########################################################################
#
#
# maintenance loop end
#
#
########################################################################
#
#
# return to main process loop
#
#
########################################################################
#
#
#
#######
#
# edge transition: melter to KMP1 
#
    operation_time=edge_trans.edge_transition(operation_time,edge_transition[2])
#
# data writing
#
    system_time_output=io.write_system_time(operation_time,system_time_output) #system time 
    melter_failure_time_output=io.write_system_time(melter_failure_time,melter_failure_time_output) #melter 
    trimmer_failure_time_output=io.write_system_time(trimmer_failure_time,trimmer_failure_time_output) #trimmer
#
#######
#
# KMP measurement (1)
#
    operation_time,measured_weight,measured_storage_inventory=kmp.kmp_measurement(operation_time,kmp_time[1],kmp_uncertainty[1],kmp_threshold[1],true_weight,expected_weight,measured_storage_inventory,measured_system_inventory,1)
#
# data writing
#
    true_kmp_output,expected_kmp_output,measured_kmp_output=io.kmp_write(operation_time,true_weight,expected_weight,measured_weight,true_kmp_output,expected_kmp_output,measured_kmp_output,1) #kmp measurement data
#
    system_time_output=io.write_system_time(operation_time,system_time_output) #system time 
    melter_failure_time_output=io.write_system_time(melter_failure_time,melter_failure_time_output) #melter 
    trimmer_failure_time_output=io.write_system_time(trimmer_failure_time,trimmer_failure_time_output) #trimmer
#
    campaign_output=io.write_campaign(operation_time,total_campaign,campaign_output) #campaign
#
    melter_process_counter_output=io.write_process_counter(operation_time,melter_process_counter,melter_process_counter_output) #process counter 
    trimmer_process_counter_output=io.write_process_counter(operation_time,trimmer_process_counter,trimmer_process_counter_output) #process counter 
#
    batch_output,true_weight_output,expected_weight_output,measured_weight_output=io.write_material_flow(operation_time,total_batch,true_weight,expected_weight,measured_weight,batch_output,true_weight_output,expected_weight_output,measured_weight_output) #material flow
#
    true_heel_output,expected_heel_output,measured_heel_output=io.write_heel(operation_time,true_heel,expected_heel,measured_heel,true_heel_output,expected_heel_output,measured_heel_output) #heel
#
    true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output=io.write_inventory(operation_time,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output) #inventory 
#
    melter_true_muf_output,melter_expected_muf_output,melter_measured_muf_output,melter_true_mufc_output,melter_expected_mufc_output,melter_measured_mufc_output=io.write_muf(operation_time,melter_true_muf,melter_expected_muf,melter_measured_muf,melter_true_mufc,melter_expected_mufc,melter_measured_mufc,melter_true_muf_output,melter_expected_muf_output,melter_measured_muf_output,melter_true_mufc_output,melter_expected_mufc_output,melter_measured_mufc_output) #muf 
#
    end_of_campaign_false_alarm_counter_output=io.write_end_of_campaign_false_alarm(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_test,end_of_campaign_false_alarm_counter_output) #end of campaign false alarm
#
    melter_failure_false_alarm_counter_output=io.write_equipment_failure_false_alarm(operation_time,melter_failure_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_test,melter_failure_false_alarm_counter_output) #melter failure false alarm
#
    melter_failure_total_counter_output,melter_probability_density_function_output,melter_unreliability_function_output=io.write_equipment_failure(operation_time,melter_failure_time,total_campaign,melter_failure_counter,melter_process_counter,melter_probability_density_function_evaluate,melter_probability_density_function_failure_evaluate,melter_unreliability_function_evaluate,melter_unreliability_function_failure_evaluate,melter_failure_total_counter_output,melter_probability_density_function_output,melter_unreliability_function_output) #melter failure
#
#######
#
# edge transition: KMP1 to trimmer
#
    operation_time=edge_trans.edge_transition(operation_time,edge_transition[3])
#
# data writing
#
    system_time_output=io.write_system_time(operation_time,system_time_output) #system time 
    melter_failure_time_output=io.write_system_time(melter_failure_time,melter_failure_time_output) #melter 
    trimmer_failure_time_output=io.write_system_time(trimmer_failure_time,trimmer_failure_time_output) #trimmer
#
#######
#
#
#
#
#
#
####### Trimmer
# material changes due to fines (trimming leftovers) currently neglected
#    operation_time,true_weight,expected_weight,trimmer_process_counter=des_f.trimmer(operation_time,process_time[2],true_weight,expected_weight,trimmer_process_counter)
### data output routines
#    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#######
#
# trimmer 
#
    operation_time,melter_failure_time,true_weight,expected_weight,accumulated_true_heel,accumulated_expected_heel,melter_failure_event,melter_failure_counter,melter_process_counter=melter.injection_casting(operation_time,melter_failure_time,true_weight,expected_weight,melter_failure_number,melter_failure_type,melter_failure_rate,injection_casting_process_time,crucible_fraction,accumulated_true_heel,accumulated_expected_heel,melter_failure_event,melter_failure_counter,melter_process_counter)
#
# data writing
#
    system_time_output=io.write_system_time(operation_time,system_time_output) #system time 
    melter_failure_time_output=io.write_system_time(melter_failure_time,melter_failure_time_output) #melter 
    trimmer_failure_time_output=io.write_system_time(trimmer_failure_time,trimmer_failure_time_output) #trimmer 
#
    campaign_output=io.write_campaign(operation_time,total_campaign,campaign_output) #campaign
#
    melter_process_counter_output=io.write_process_counter(operation_time,melter_process_counter,melter_process_counter_output) #process counter 
    trimmer_process_counter_output=io.write_process_counter(operation_time,trimmer_process_counter,trimmer_process_counter_output) #process counter 
#
    batch_output,true_weight_output,expected_weight_output,measured_weight_output=io.write_material_flow(operation_time,total_batch,true_weight,expected_weight,measured_weight,batch_output,true_weight_output,expected_weight_output,measured_weight_output) #material flow
#
    true_heel_output,expected_heel_output,measured_heel_output=io.write_heel(operation_time,true_heel,expected_heel,measured_heel,true_heel_output,expected_heel_output,measured_heel_output) #heel
#
    true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output=io.write_inventory(operation_time,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output) #inventory 
#
    melter_true_muf_output,melter_expected_muf_output,melter_measured_muf_output,melter_true_mufc_output,melter_expected_mufc_output,melter_measured_mufc_output=io.write_muf(operation_time,melter_true_muf,melter_expected_muf,melter_measured_muf,melter_true_mufc,melter_expected_mufc,melter_measured_mufc,melter_true_muf_output,melter_expected_muf_output,melter_measured_muf_output,melter_true_mufc_output,melter_expected_mufc_output,melter_measured_mufc_output) #muf 
#
    end_of_campaign_false_alarm_counter_output=io.write_end_of_campaign_false_alarm(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_test,end_of_campaign_false_alarm_counter_output) #end of campaign false alarm
#
    melter_failure_false_alarm_counter_output=io.write_equipment_failure_false_alarm(operation_time,melter_failure_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_test,melter_failure_false_alarm_counter_output) #melter failure false alarm
#
    melter_failure_total_counter_output,melter_probability_density_function_output,melter_unreliability_function_output=io.write_equipment_failure(operation_time,melter_failure_time,total_campaign,melter_failure_counter,melter_process_counter,melter_probability_density_function_evaluate,melter_probability_density_function_failure_evaluate,melter_unreliability_function_evaluate,melter_unreliability_function_failure_evaluate,melter_failure_total_counter_output,melter_probability_density_function_output,melter_unreliability_function_output) #melter failure
#
#######
#
#
#
####### edge transition
# Trimmer to KMP2
#    operation_time=des_f.edge_transition(operation_time,edge_time[4])
#######
#
#
#
####### KMP measurement if active (2)
#    operation_time,measured_weight,measured_processed_inventory=des_f.kmp_measurement(operation_time,kmp_measurement_uncertainty[2],kmp_time[2],kmp_measurement_threshold[2],true_weight,expected_weight,measured_processed_inventory,measured_system_inventory,2)
### data output routines
#    true_kmp2,expected_kmp2,measured_kmp2=des_f.kmp_write(operation_time,true_weight,expected_weight,measured_weight,true_kmp2,expected_kmp2,measured_kmp2)
#
#    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### edge transition
# KMP2 to Product Storage
#    operation_time=des_f.edge_transition(operation_time,edge_time[5])
#######
#
#
#
####### Product storage and final processing
#    operation_time,true_processed_inventory,expected_processed_inventory=des_f.product_processing(operation_time,process_time[4],true_weight,expected_weight,true_processed_inventory,expected_processed_inventory)
### data output routines
#    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
###### End of campaign inspection
#    operation_time,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc=des_f.mass_balance(operation_time,campaign_inspection_time,storage_inventory_start,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_muf,expected_muf,measured_muf,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,melter_failure_event,true_system_inventory,expected_system_inventory,measured_system_inventory)
### Test for false alarm
#    system_false_alarm_counter,system_false_alarm,system_alarm_test=des_f.false_alarm_test(system_false_alarm_limit,system_false_alarm_counter,expected_muf,measured_muf)
### data output routines
#    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### loop back to start next campaign
#
# reset campaign based variables and advance campaign counter
    total_campaign,total_batch=io.end_of_campaign(total_campaign,total_batch)
    true_weight,expected_weight,measured_weight=io.reset_batch_weight()
#
#######
#
# end facility operation loop
#
########################################################################
#
# close output files
#
####################################################################### 
#
# end main fuel fabrication model
#
print 'End facility operation'
#
#######################################################################
#
#
#
########################################################################
#
# postprocessing
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
#
#######################################################################
#
#
#
########################################################################
#      EOF
########################################################################
