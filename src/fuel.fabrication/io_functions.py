########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.20.July.2015
########################################################################
# 
# Functions for in-simulation data processing
# 
########################################################################
#
# imports
#
import os
import numpy
import shutil
#
########################################################################
#
# function list
#
# (1): get simulation directories
#
# input regime
# (2a): read system operation input data
# (2b): read storage buffer input data
# (2c): read melter input data
# (2d): read system false alarm input data
# (2e): read edge transition input data
# (2f): read kmp input data
#
# output regime
# (3a): open system output files
# (3b): open material flow output files
# (3c): open inventory output files
# (3d): open system false alarm output files
# (3e): open kmp output files
# (3f): open melter failure output files
# (3g): open muf output files
#
# initialization regime
# (4a): initialize system parameters
# (4b): initialize material flow parameters
# (4c): initialize inventory parameters
# (4d): initialize system false alarm parameters
# (4e): initialize melter failure parameters
# (4f): initialize muf parameters
#
# data writing regime
# (5a): write system operation 
# (5b): write material flow 
# (5c): write inventory 
#
########################################################################
#
#
#
########################################################################
#
# (1): get simulation directories
#
# directories are created and input files are copied into them from the default directory by pyroprocessing_command.py
# system locator file is created containing the directory paths in each subsystem folder
#
#######
def get_simulation_dir(subsystem):
#######
#
### get home directory
    os.chdir('C:\\root\\pyroDES')
    home_dir=open('home.dir.inp').read()
#
### get simulation directory paths 
    simulation_dir=home_dir+'\\input\\'+subsystem
    os.chdir(home_dir+'\\input\\'+subsystem)
    directory_path_file=open('simulation.dir.inp').readlines()
#
### split the string
    directory_paths=directory_path_file[0].split(',')
#
### set directories
    input_dir=directory_paths[0]
    output_dir=directory_paths[1]
#
    edge_transition_dir=directory_paths[2]
    failure_distribution_dir=directory_paths[3]
    failure_equipment_dir=directory_paths[4]
    kmps_dir=directory_paths[5]
    process_states_dir=directory_paths[6]
    system_false_alarm_dir=directory_paths[7]
#    
    data_dir=directory_paths[8]
    figures_dir=directory_paths[9]
#    
    system_odir=directory_paths[10]
    material_flow_odir=directory_paths[11]
    inventory_odir=directory_paths[12]
    false_alarm_odir=directory_paths[13]
    kmps_odir=directory_paths[14]
    muf_odir=directory_paths[15]
    melter_failure_odir=directory_paths[16]
#
    system_gdir=directory_paths[17]
    material_flow_gdir=directory_paths[18]
    inventory_gdir=directory_paths[19]
    false_alarm_gdir=directory_paths[20]
    kmps_gdir=directory_paths[21]
    muf_gdir=directory_paths[22]
    melter_failure_gdir=directory_paths[23]
#
#   os.remove('simulation.dir.inp') 
###
    return(input_dir,output_dir,edge_transition_dir,failure_distribution_dir,failure_equipment_dir,kmps_dir,process_states_dir,system_false_alarm_dir,data_dir,figures_dir,system_odir,material_flow_odir,inventory_odir,false_alarm_odir,kmps_odir,muf_odir,melter_failure_odir,system_gdir,material_flow_gdir,inventory_gdir,false_alarm_gdir,kmps_gdir,muf_gdir,melter_failure_gdir)
########################################################################
#
# (2a): read system operation input data
#
#######
def input_system_operation(input_dir,process_states_dir,output_dir):
#######
#
### 
    os.chdir(process_states_dir) #change dir
#
    facility_operation=numpy.loadtxt('facility.operation.inp') #total time of facility operation; i.e., simulation time 
    process_time=numpy.loadtxt('process.operation.time.inp',usecols=[1]) #time for each vertex to process material
#
### copy readme to output dir 
    os.chdir(input_dir) #change dir
    shutil.copy('readme.md',output_dir) #copy file
###
    return(facility_operation,process_time)
########################################################################
#
# (2b): read storage buffer input data
#
#######
def input_storage_buffer(process_states_dir):
#######
#
### 
    os.chdir(process_states_dir) #change dir
#
    batch=numpy.loadtxt('batch.inp') #batch size
    unprocessed_storage_inventory=numpy.loadtxt('unprocessed.storage.inventory.inp') #total quantity of naterial in storage buffer at TIME=0
###
    return(batch,unprocessed_storage_inventory)
########################################################################
#
# (2c): read melter input data
#
#######
def input_melter(process_states_dir,failure_equipment_dir,failure_distribution_dir):
#######
#
### 
    os.chdir(process_states_dir) #change dir
#
    crucible_fraction=numpy.loadtxt('melter.crucible.fraction.inp',usecols=[1]) #fraction of material left in the crucible during melting; 1st element is the expected quantity, 2nd and 3rd are the range for the true quantity
#
    os.chdir(failure_equipment_dir) #change dir
#
    melter_failure_type=numpy.loadtxt('melter.failure.data.inp',usecols=[0],dtype=str) #type of melter failure
    melter_failure_rate=numpy.loadtxt('melter.failure.data.inp',usecols=[1]) #corresponding melter failure rate
    melter_failure_maintenance_time=numpy.loadtxt('melter.failure.data.inp',usecols=[2]) #time to repair each failure
    melter_cleaning_time=numpy.loadtxt('melter.failure.data.inp',usecols=[3]) #time to clean the melter prior to equipment removal
#
    os.chdir(failure_distribution_dir) #change dir
#
    weibull_beta_melter=numpy.loadtxt('weibull.beta.inp',usecols=[1]) #weibull distribution beta parameter for the melter
#
### calculations
    weibull_eta_melter=(1)/melter_failure_rate #eta for weibull distribution is reciprocal of failure rate if beta = 1; assumes random failure
#    melter_failure_number=len(melter_failure_type) #total number of possible failures if > 1
###
    return(crucible_fraction,melter_failure_type,melter_failure_rate,melter_failure_maintenance_time,melter_cleaning_time,weibull_beta_melter,weibull_eta_melter) 
########################################################################
#
# (2d): read system false alarm input data
#
#######
def input_system_false_alarm(system_false_alarm_dir):
#######
#
### 
    os.chdir(system_false_alarm_dir) #change dir
#
    false_alarm_threshold=numpy.loadtxt('false.alarm.threshold.inp',usecols=[1]) #false alarm thresholds
    inspection_time=numpy.loadtxt('inspection.time.inp',usecols=[1]) #time elapsed for each inspection
#
### sort false alarms
    melter_failure_inspection_time=inspection_time[0]
    end_of_campaign_inspection_time=inspection_time[1]
#
    melter_failure_false_alarm_threshold=false_alarm_threshold[0]
    end_of_campaign_false_alarm_threshold=false_alarm_threshold[1]
###
    return(melter_failure_false_alarm_threshold,end_of_campaign_false_alarm_threshold,melter_failure_inspection_time,end_of_campaign_inspection_time) 
########################################################################
#
# (2e): read edge transition input data
#
#######
def input_edge_transition(edge_transition_dir):
#######
#
### 
    os.chdir(edge_transition_dir) #change dir
#
    edge_transition=numpy.loadtxt('edge.transition.inp',usecols=[1]) #time elapsed on each edge transition
###
    return(edge_transition) 
########################################################################
#
# (2f): read kmp input data
#
#######
def input_kmps(kmps_dir):
#######
#
### 
    os.chdir(kmps_dir) #change dir
#
    kmp_id=numpy.loadtxt('key.measurement.points.inp',usecols=[0]) #kmp identification numbers
    kmp_time=numpy.loadtxt('key.measurement.points.inp',usecols=[1]) #measurement time at each kmp
    kmp_uncertainty=numpy.loadtxt('key.measurement.points.inp',usecols=[2]) #measurement uncertainty at each kmp
    kmp_threshold=numpy.loadtxt('key.measurement.points.inp',usecols=[3]) #measurement threshold to trigger false alarms at each kmp
#
### determine maximum number of kmps
    maximum_kmp=len(kmp_id)
###
    return(kmp_id,kmp_time,kmp_uncertainty,kmp_threshold,maximum_kmp) 
########################################################################
#
# (3a): open system output files
#
#######
def output_system_operation(system_odir):
#######
#
###
    os.chdir(system_odir) #change dir
#
    time_output=open('facility.operation.time.out','w+')
    campaign_output=open('facility.campaign.out','w+')
#
    melter_process_counter_output=open('melter.process.counter.out','w+')
    trimmer_process_counter_output=open('trimmer.process.counter.out','w+')
###
    return(time_output,campaign_output,melter_process_counter_output,trimmer_process_counter_output)
########################################################################
#
# (3b): open material flow output files
#
#######
def output_material_flow(material_flow_odir):
#######
#
### 
    os.chdir(material_flow_odir) #change dir
#
    batch_output=open('batch.out','w+')
    true_weight_output=open('true.weight.out','w+')
    expected_weight_output=open('expected.weight.out','w+')
    measured_weight_output=open('measured.weight.out','w+')
#
    true_heel_output=open('true.heel.out','w+')
    expected_heel_output=open('expected.heel.out','w+')
    measured_heel_output=open('measured.heel.out','w+')
###
    return(batch_output,true_weight_output,expected_weight_output,measured_weight_output,true_heel_output,expected_heel_output,measured_heel_output)
########################################################################
#
# (3c): open inventory output files
#
#######
def output_inventory(inventory_odir):
#######
#
###
    os.chdir(inventory_odir) #change dir
#
    true_storage_inventory_output=open('true.storage.inventory.out','w+')
    expected_storage_inventory_output=open('expected.storage.inventory.out','w+')
    measured_storage_inventory_output=open('measured.storage.inventory.out','w+')
#
    true_processed_inventory_output=open('true.processed.inventory.out','w+')
    expected_processed_inventory_output=open('expected.processed.inventory.out','w+')
    measured_processed_inventory_output=open('measured.processed.inventory.out','w+')
#
    true_system_inventory_output=open('true_system.inventory.out','w+')
    expected_system_inventory_output=open('expected.system.inventory.out','w+')
    measured_system_inventory_output=open('measured.system.inventory.out','w+')
###
    return(true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output)  
########################################################################
#
# (3d): open system false alarm output files
#
#######
def output_false_alarm(false_alarm_odir):
#######
#
### 
    os.chdir(false_alarm_odir) #change dir
#
    melter_failure_false_alarm_counter_output=open('melter.failure.false.alarm.counter.out','w+')
    end_of_campaign_false_alarm_counter_output=open('end.of.campaign.false.alarm.counter.out','w+')
###
    return(melter_failure_false_alarm_counter_output,end_of_campaign_false_alarm_counter_output)  
########################################################################
#
# (3e): open kmp output files
#
#######
def output_kmps(kmps_odir):
#######
#
### 
    os.chdir(kmps_odir) #change dir
#
    true_kmp_output=open('true.kmp.out','w+')
    expected_kmp_output=open('expected.kmp.out','w+')
    measured_kmp_output=open('measured.kmp.out','w+')
###
    return(true_kmp_output,expected_kmp_output,measured_kmp_output)  
########################################################################
#
# (3f): open melter failure output files
#
#######
def output_melter_failure(melter_failure_odir):
#######
#
### 
    os.chdir(melter_failure_odir) #change dir
#
    melter_failure_campaign_counter_output=open('melter.failure.campaign.counter.out','w+')
    melter_failure_total_counter_output=open('melter.failure.total.counter.out','w+')
#
    melter_probability_density_function_output=open('melter.probability.density.function.out','w+')
    melter_unreliability_function_output=open('melter.unreliability.function.out','w+')
###
    return(melter_failure_campaign_counter_output,melter_failure_total_counter_output,melter_probability_density_function_output,melter_unreliability_function_output)  
########################################################################
#
# (3g): open muf output files
#
#######
def output_muf(muf_odir):
#######
#
### 
    os.chdir(muf_odir) #change dir
#
    true_muf_output=open('true.muf.out','w+')
    expected_muf_output=open('expected.muf.out','w+')
    measured_muf_output=open('measured.muf.out','w+')
#
    true_mufc_output=open('true.mufc.out','w+')
    expected_mufc_output=open('expected.mufc.out','w+')
    measured_mufc_output=open('measured.mufc.out','w+')
###
    return(true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output)  
########################################################################
#
# (4a): initialize system parameters
#
#######
def initialize_system():
#######
#
###
    operation_time=0 #simulation time
    failure_time=0 #time elapsed for failure modeling
    total_campaign=1 #total campaigns processed over facility operation
    melter_process_counter=0 #total times the melter process was initiatedd over facility operation
    trimmer_process_counter=0 #total times the trimmer process was initiated over facility operation
###
    return(operation_time,failure_time,total_campaign,melter_process_counter,trimmer_process_counter)
########################################################################
#
# (4b): initialize material flow parameters
#
#######
def initialize_material_flow():
#######
#
###
    total_batch=1 #total batches processed over facility operation
#
    true_weight=0 #true quantity processed per campaign
    expected_weight=0 #expected quantity processed per campaign
    measured_weight=0 #measured quantity processed per campaign
#
    true_heel=0 #true quantity of heel per campaign
    expected_heel=0 #expected quantity of heel per campaign
    measured_heel=0 #measured quantity of heel per campaign
#
    accumulated_true_heel=0 #accumulated quantity of heel prior to failure; zeroed out on cleaning 
    accumulated_expected_heel=0 #expected quantity of heel prior to failure; zeroed out on cleaning
    accumulated_measured_heel=0 #measured quantity of heel prior to failure; zeroed out on cleaning 
###
    return(total_batch,true_weight,expected_weight,measured_weight,true_heel,expected_heel,measured_heel,accumulated_true_heel,accumulated_expected_heel,accumulated_measured_heel)
########################################################################
#
# (4c): initialize inventory parameters
#
#######
def initialize_inventory(unprocessed_storage_inventory):
#######
#
###
    true_storage_inventory=unprocessed_storage_inventory #true quantity of unprocessed material over facility operation
    expected_storage_inventory=unprocessed_storage_inventory #expected quantity of unprocessed material over facility operation
    measured_storage_inventory=unprocessed_storage_inventory #measured quantity of unprocessed material over facility operation
#
    true_processed_inventory=0 #true quantity of processed material over facility operation
    expected_processed_inventory=0 #expected quantity of processed material over facility operation
    measured_processed_inventory=0 #measured quantity of processed material over facility operation
#
    true_system_inventory=0 #true quantity of material transferred out of storage buffer over facility operation
    expected_system_inventory=0 #expected quantity of material transferred out of storage buffer over facility operation
    measured_system_inventory=0 #measured quantity of material transferred out of storage buffer over facility operation
# 
    true_initial_inventory=0 #true inventory used for MUFc calculation
    expected_initial_inventory=0 #expected inventory used for MUFc calculation
    measured_initial_inventory=0 #measured inventory used for MUFc calculation
###
    return(true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,true_initial_inventory,expected_initial_inventory,measured_initial_inventory)
########################################################################
#
# (4d): initialize system false alarm parameters
#
#######
def initialize_false_alarm():
#######
#
###
    end_of_campaign_false_alarm_counter=0 #total false alarms due to end of campaign inspection
    melter_failure_false_alarm_counter=0 #total false alarms due to melter failures
    end_of_campaign_false_alarm=False #end of campaign false alarm flag
#
    melter_failure_false_alarm=False #melter failure false alarm flag
    end_of_campaign_false_alarm_test=0 #difference in selected material quantities compared to threshold to trigger false alarm for end of campaign inspection
    melter_failure_false_alarm_test=0 #difference in selected material quantities compared to threshold to trigger false alarm for melter failure inspection
###
    return(end_of_campaign_false_alarm_counter,melter_failure_false_alarm_counter,end_of_campaign_false_alarm,melter_failure_false_alarm,end_of_campaign_false_alarm_test,melter_failure_false_alarm_test)
########################################################################
#
# (4e): initialize melter failure parameters
#
#######
def initialize_melter_failure():
#######
#
###
    melter_failure_time=0 #time used to determine melter failures
    melter_failure_counter=0 #total times the melter failed over facility operation
    melter_failure_event=False #melter failure flag for an equipment failure
#
    melter_process_counter=0 #total times the melter process was initiated over facility operation
    melter_probability_density_function_evaluate=0 #pdf for melter failure distribution at operation_time
    melter_probability_density_function_failure_evaluate=0 #pdf for melter failure distribution at melter_failure_time
#
    melter_unreliability_function_evaluate=0 #cdf for melter failure distribution at operation_time
    melter_unreliability_function_failure_evaluate=0 #cdf for melter failure distribution at failure_time
###
    return(melter_failure_time,melter_failure_counter,melter_failure_event,melter_process_counter,melter_probability_density_function_evaluate,melter_probability_density_function_failure_evaluate,melter_unreliability_function_evaluate,melter_unreliability_function_failure_evaluate)
########################################################################
#
# (4f): initialize muf parameters
#
#######
def initialize_muf():
#######
#
###
    melter_true_muf=0 #true quantity of muf over facility operation; zeroed out on cleaning; zeroed out on cleaning
    melter_expected_muf=0 #expected quantity of muf over facility operation; zeroed out on cleaning
    melter_measured_muf=0 #measured quantity of muf over facility operation; zeroed out on cleaning
#
    melter_true_mufc=0 #true quantity of muf per campaign; zeroed out on cleaning
    melter_expected_mufc=0 #expected quantity of muf per campaign; zeroed out on cleaning
    melter_measured_mufc=0 #measured quantity of muf per campaign; zeroed out on cleaning
###
    return(melter_true_muf,melter_expected_muf,melter_measured_muf,melter_true_mufc,melter_expected_mufc,melter_measured_mufc)
#########################################################################
#
# (5a): write system operation 
#
#######
def write_system_operation(operation_time,melter_failure_time,total_campaign,melter_process_counter,trimmer_process_counter,time_output,campaign_output,melter_process_counter_output,trimmer_process_counter_output):
#######
    time_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%melter_failure_time)+'\n') #time data is written whenever operation time changes
    campaign_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%i'%total_campaign)+'\n')
    melter_process_counter_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%i'%melter_process_counter)+'\n')
    trimmer_process_counter_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%i'%trimmer_process_counter)+'\n')
###
    return(time_output,campaign_output,melter_process_counter_output,trimmer_process_counter_output)
########################################################################
#
# (5b): write material flow
#
#######
def write_material_flow(operation_time,total_batch,true_weight,expected_weight,measured_weight,true_heel,expected_heel,measured_heel,batch_output,true_weight_output,expected_weight_output,measured_weight_output,true_heel_output,expected_heel_output,measured_heel_output):
#######
#
###
    batch_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%i'%total_batch)+'\n') 
    true_weight_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_weight)+'\n')
    expected_weight_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_weight)+'\n')
    measured_weight_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_weight)+'\n')
    true_heel_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_heel)+'\n')
    expected_heel_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_heel)+'\n')
    measured_heel_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_heel)+'\n')
###
    return(batch_output,true_weight_output,expected_weight_output,measured_weight_output,true_heel_output,expected_heel_output,measured_heel_output)
########################################################################
#
# (5c): write inventory 
#
#######
def write_inventory(operation_time,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,true_initial_inventory_output,expected_initial_inventory_output,measured_initial_inventory_output):
#######
#
###
    _output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%)+'\n') 
    _output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%)+'\n')
    _output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%)+'\n')
    _output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%)+'\n')
    _output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%)+'\n')
    _output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%)+'\n')
    _output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%)+'\n')
###
    return(true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,true_initial_inventory_output,expected_initial_inventory_output,measured_initial_inventory_output)
########################################################################
#
#
#    measured_storage_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_storage_inventory)+'\n')
#
    #true_muf_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_muf)+'\n')
    #expected_muf_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_muf)+'\n')
    #measured_muf_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_muf)+'\n')    
    #true_mufc_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_mufc)+'\n')
    #expected_mufc_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_mufc)+'\n')
    #measured_mufc_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_mufc)+'\n')    
    #true_processed_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_processed_inventory)+'\n')
    #expected_processed_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_processed_inventory)+'\n')
    #measured_processed_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_processed_inventory)+'\n')
    #measured_system_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_system_inventory)+'\n')
#
#
########################################################################
#
#
#
####### (g): trimmer
# Metal alloy is trimmed into fuel slugs
# Currently there are no failures or held up material
###
#
###
def trimmer(operation_time,delay,true_quantity,expected_quantity,trimmer_process_counter):
###
    print 'Slug trimming','\n\n'
    operation_time=operation_time+delay
    trimmer_process_counter=trimmer_process_counter+1
###
    return(operation_time,true_quantity,expected_quantity,trimmer_process_counter)
########################################################################
#
#
#
####### (h): product processing
# The final product is 'processed' with an associated delay time
# This is the final stage before the end of the campaign
###
#
###    
def product_processing(operation_time,delay,true_quantity,expected_quantity,true_processed_inventory,expected_processed_inventory):
###
    print 'Processing the final product','\n\n'
    operation_time=operation_time+delay
#
    true_processed_inventory=true_processed_inventory+true_quantity
    expected_processed_inventory=expected_processed_inventory+expected_quantity
    
###
    return(operation_time,true_processed_inventory,expected_processed_inventory)
###########################################################################
#
#
#
####### (i): mass balance
# Conducts mass balance
# This is needed after a campaign, alarm, inspection
# MUF is calculated and compared to true weight
# True weight is realistically never known
# Later on something more sophisticated will be built
###
#
###
def mass_balance(operation_time,delay,storage_inventory_start,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_quantity,expected_quantity,measured_quantity,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_muf,expected_muf,measured_muf,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,melter_failure_event,true_system_inventory,expected_system_inventory,measured_system_inventory):
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
