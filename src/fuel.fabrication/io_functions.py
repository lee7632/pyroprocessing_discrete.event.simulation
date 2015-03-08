########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.26.February.2015
########################################################################
# 
# Functions for in-simulation data processing
# 
########################################################################
#
# imports
#
import os
#
########################################################################
#
# function list
#
# (1): get simulation directories 
# (2): read in input data and prepare output data tables
# (3): open output files
# (4): initialize parameters
# (5): write operation time data
# (6): write system and material flow data
#
########################################################################
####### (b): Set facility configuration
####### (f): melter
####### (g): trimmer
####### (h): product processing
####### (i): mass balance
####### (k): recycle storage
####### (m): Failure test
####### (n): End of campaign reset
####### (n): End of campaign reset weight
####### (o): Open output files
####### (q): Close output files
####### (s): Melter cleaning procedure
####### (t): Maintenance
####### (u): KMP measurement recording write to file
####### (y): Weibull probability density function evaluation
####### (z): Weibull unreliability function evaluation
#
########################################################################
#
#
#
########################################################################
#
# (1): get simulation directories
#
# Input and output files are in different directories than the system files.
# Directories are created and input files are copied into them from the default directory by pyroprocessing_command.py.
# A system locator file is also created containing the relative (to the system files) directory paths. 
#
#######
def get_simulation_dir():
#######
#
### get home directory
    home_dir=os.getcwd() #home directory is where the system files are located
###
#
### open path file containing directory locations
    directory_path_file=open('..\\..\\input\\fuel.fabrication\\simulation.dir.inp').readlines()
###
#
### split the string
    directory_paths=directory_path_file[0].split(',')
###
#
### set directories
    input_dir=directory_paths[0]
    output_data_dir=directory_paths[1]
    output_figure_dir=directory_paths[2]
###
    print 'Working directories processed.'
    print 'Home directory:',home_dir
    print 'Input directory:',input_dir
    print 'Output data directory:',output_data_dir
    print 'Output figure directory:',output_figure_dir
###
    return(home_dir,input_dir,output_data_dir,output_figure_dir)
#
########################################################################
#
# (2): read input data and prepare output data tables
#
#######
def input_parameters(home_dir,input_dir,output_data_dir):
#######
#
### go to input file directory
    os.chdir(input_dir)
###
#
### open data files
    batch=numpy.loadtxt('batch.inp') #batch size
    crucible_fraction=numpy.loadtxt('crucible.fraction.inp') #fraction of material left in the crucible during melting; 1st element is the expected quantity, 2nd and 3rd are the range for the true quantity
    edge_transition=numpy.loadtxt('edge_transition\\edge.transition.inp') #time elapsed on each edge transition
    facility_operation=numpy.loadtxt('facility.operation.inp') #total time of facility operation; i.e., simulation time 
    false_alarm_threshold=numpy.loadtxt('false.alarm.threshold.inp',usecols=[1]) #false alarm thresholds
    inspection_time=numpy.loadtxt('inspection.time.inp',usecols=[1]) #time elapsed for each inspection
    kmp_data=numpy.loadtxt('kmps\\kmp.measurement.points.inp') #KMP data
    melter_failure_number=numpy.loadtxt('melter.failure.number.inp',dtype=int) #total number of possible melter failures
    melter_failure_type=numpy.loadtxt('melter.failure.data.inp',usecols=[0],dtype=str) #type of melter failure
    melter_failure_rate=numpy.loadtxt('melter.failure.data.inp',usecols=[1]) #corresponding melter failure rate
    melter_failure_maintenance_time=numpy.loadtxt('melter.failure.data.inp',usecols=[2]) #time to repair each failure
    melter_cleaning_time=numpy.loadtxt('melter.cleaning.time.inp') #time to clean the melter prior to equipment removal
    process_time=numpy.loadtxt('process.time.inp',usecols=[1]) #time for each vertex to process material
    weibull_beta_melter=numpy.loadtxt('weibull.beta.inp') #weibull distribution beta parameter for the melter
###
    readme_input=open('readme.md').readlines()
###
#
### 
    melter_failure_inspection_time=inspection_time[0]
    end_of_campaign_inspection_time=inspection_time[1]
    melter_failure_false_alarm_threshold=false_alarm_threshold[0]
    end_of_campaign_false_alarm_threshold=false_alarm_threshold[1]
    weibull_eta_melter=(1)/(melter_failure_rate) # the eta parameter for the weibull distribution is equal to the reciprocal of the failure rate if beta = 1; i.e., this assumes random failures
###
#
### output
    crucible_fraction_output=numpy.zeros((3))    
    edge_time_output=numpy.zeros((2*maximum_kmp))    
    kmp_output=numpy.zeros((maximum_kmp,4))
    process_failures_output=numpy.zeros((melter_failure_number,2))
    melter_failure_inspection_time_output=numpy.zeros((1))
    end_of_campaign_inspection_time_output=numpy.zeros((1))
    end_of_campaign_false_alarm_output=numpy.zeros(1)
    melter_failure_false_alarm_output=numpy.zeros(1)
    melter_cleaning_time_output=numpy.zeros((1))
    batch_output=numpy.zeros((1))
    facility_operation_output=numpy.zeros((1))
#
    for i in range(0,melter_failure_number):
        process_failures_output[i,0]=melter_failure_rate[i]
        process_failures_output[i,1]=24*melter_failure_maintenance_time[i]
# end
#
    melter_failure_inspection_time_output[0]=24*melter_failure_inspection_time
    end_of_campaign_inspection_time_output[0]=24*end_of_campaign_inspection_time    
    end_of_campaign_false_alarm_output[0]=end_of_campaign_false_alarm_threshold
    melter_failure_false_alarm_output[0]=melter_failure_false_alarm_threshold    
    melter_cleaning_time_output[0]=24*melter_cleaning_time
    batch_output[0]=batch
    facility_operation_output[0]=facility_operation
#
    for j in range(0,maximum_kmp):
        kmp_output[j,0]=j
        kmp_output[j,1]=kmp_measurement_uncertainty[j]
        kmp_output[j,2]=24*kmp_time[j]
        kmp_output[j,3]=kmp_measurement_threshold[j]        
# end
###
#
###
    for k in range(0,2*maximum_kmp):
        edge_time_output[k]=24*edge_time[k]
# end
###
#
###
    for l in range(0,2):
        crucible_fraction_output[l]=crucible_fraction[l]
# end
###
#
### save files
# move to output directory
    os.chdir(home_dir)
    os.chdir(output_data_dir)
#
    numpy.savetxt('process.failures.out',process_failures_output,fmt=['%.4f','%.2f'],header='Failure probability\tMaintenance time (h)',comments='',delimiter='\t\t\t')
    numpy.savetxt('melter.failure.inspection.time.out',melter_failure_inspection_time_output,fmt=['%.2f'],header='Melter failure inspection time (h)',comments='')
    numpy.savetxt('campaign.inspection.time.out',end_of_campaign_inspection_time_output,fmt=['%.2f'],header='End of campaign inspection time (h)',comments='')
    numpy.savetxt('kmp.out',kmp_output,fmt=['%.0f','%.4f','%.2f','%.4f'],header='KMP\tMeasurement uncertainty\tMeasurement delay time (h)\tMeasurement threshold',comments='',delimiter='\t\t\t')
    numpy.savetxt('end.of.campaign.false.alarm.out',end_of_campaign_false_alarm_output,fmt=['%.4f'],header='Fraction of MUF to trigger alarm for system inspection',comments='')
    numpy.savetxt('melter.failure.false.alarm.out',melter_failure_false_alarm_output,fmt=['%.4f'],header='Fraction of MUF to trigger alarm for system inspection due to failure',comments='')
    numpy.savetxt('melter.cleaning.time.out',melter_cleaning_time_output,fmt=['%.4f'],header='Time to clean the melter additional to maintenance activity (h)',comments='')
    numpy.savetxt('facility.operation.out',facility_operation_output,fmt=['%.1f'],header='Facility operational period (d)',comments='')
    numpy.savetxt('batch.out',batch_output,fmt=['%.1f'],header='Batch per campaign (kg)',comments='')
    numpy.savetxt('edge.time.out',edge_time_output,fmt=['%.2f'],header='Transition time along edges (h); see system diagram',comments='')
    numpy.savetxt('crucible.fraction.out',crucible_fraction_output,fmt=['%.4f'],header='Crucible fraction (kg)',comments='')
#
    readme_output=open('readme.md','w+')
    readme_output.write(readme_input[0])
    readme_output.close()
###
#
### go back to home directory
    os.chdir(home_dir)
###
    print 'System write complete.','\n'
###
    return(facility_operation,process_time)
#
########################################################################
#
#
#
########################################################################
#
# (3): open output files
#
#######
def open_output_files(home_dir,output_data_dir):
#######
#
### change directory
    os.chdir(output_data_dir)
###
#
### open files: the functions for writing data to the files explain what is in each of them since the variables are listed
    time_output=open('facility.operation.time.out','w+')
    campaign_output=open('facility.campaign.out','w+')
    measured_storage_inventory_output=open('measured.storage.inventory.out','w+')
    true_weight_output=open('true.weight.out','w+')
    expected_weight_output=open('expected.weight.out','w+')
    measured_weight_output=open('measured.weight.out','w+')
    true_muf_output=open('true.muf.out','w+')
    expected_muf_output=open('expected.muf.out','w+')
    measured_muf_output=open('measured.muf.out','w+')
    true_mufc_output=open('true.mufc.out','w+')
    expected_mufc_output=open('expected.mufc.out','w+')
    measured_mufc_output=open('measured.mufc.out','w+')
    true_processed_inventory_output=open('true.processed.inventory.out','w+')
    expected_processed_inventory_output=open('expected.processed.inventory.out','w+')
    measured_processed_inventory_output=open('measured.processed.inventory.out','w+')
    measured_system_inventory_output=open('measured.system.inventory.out','w+')
    trimmer_process_counter_output=open('trimmer.process.counter.out','w+')
###
#
### return to home directory
    os.chdir(home_dir)
###
    return(time_output,campaign_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,measured_system_inventory_output,trimmer_process_counter_output)
#
########################################################################
#
#
#
########################################################################
#
# (4): initialize parameters
#
#######
def initialize_parameters(unprocessed_storage_inventory):
#######
#
    operation_time=0 #simulation time
    true_processed_inventory=0 #true quantity of processed material over facility operation
    expected_processed_inventory=0 #expected quantity of processed material over facility operation
    measured_processed_inventory=0 #measured quantity of processed material over facility operation
    total_campaign=1 #total campaigns processed over facility operation
    true_weight=0 #true quantity processed per campaign
    expected_weight=0 #expected quantity processed per campaign
    measured_weight=0 #measured quantity processed per campaign
    melter_true_muf=0 #true quantity of muf over facility operation; zeroed out on cleaning; zeroed out on cleaning
    melter_expected_muf=0 #expected quantity of muf over facility operation; zeroed out on cleaning
    melter_measured_muf=0 #measured quantity of muf over facility operation; zeroed out on cleaning
    melter_true_mufc=0 #true quantity of muf per campaign; zeroed out on cleaning
    melter_expected_mufc=0 #expected quantity of muf per campaign; zeroed out on cleaning
    melter_measured_mufc=0 #measured quantity of muf per campaign; zeroed out on cleaning
    measured_storage_inventory=unprocessed_storage_inventory #measured quantity of unprocessed material over facility operation
    measured_system_inventory=0 #measured quantity of material transferred out of storage buffer over facility operation
    trimmer_process_counter=0 #total times the trimmer process was initiated over facility operation
###
    print 'System initialization complete.'
###
    return(operation_time,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,total_campaign,true_weight,expected_weight,measured_weight,melter_true_muf,melter_expected_muf,melter_measured_muf,melter_true_mufc,melter_expected_mufc,melter_measured_mufc,measured_storage_inventory,measured_system_inventory,trimmer_process_counter)
#
#########################################################################
#
#
#
#########################################################################
#
# (5): write operation time data
#
#######
def write_time_output(operation_time,failure_time,time_output):
#######
    time_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%failure_time)+'\n') #time data is written whenever operation time changes
###
    return(time_output)
#
########################################################################
#
#
#
########################################################################
#
# (6): write system and material flow data
#
#######
def write_system_output(operation_time,total_campaign,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,total_melter_failure,measured_system_inventory,melter_process_counter,trimmer_process_counter,melter_probability_density_function_evaluate,melter_probability_density_function_failure_evaluate,melter_unreliability_function_evaluate,melter_unreliability_function_failure_evaluate,campaign_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output,melter_probability_density_function_output,melter_unreliability_function_output):
#######
    campaign_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%i'%total_campaign)+'\n')
    measured_storage_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_storage_inventory)+'\n')
    true_weight_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_weight)+'\n')
    expected_weight_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_weight)+'\n')
    measured_weight_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_weight)+'\n')
    true_muf_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_muf)+'\n')
    expected_muf_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_muf)+'\n')
    measured_muf_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_muf)+'\n')    
    true_mufc_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_mufc)+'\n')
    expected_mufc_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_mufc)+'\n')
    measured_mufc_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_mufc)+'\n')    
    true_processed_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_processed_inventory)+'\n')
    expected_processed_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_processed_inventory)+'\n')
    measured_processed_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_processed_inventory)+'\n')
    total_melter_failure_output.write(str.format('%i'%total_campaign)+'\t'+str.format('%i'%total_melter_failure)+'\n')
    measured_system_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_system_inventory)+'\n')
    melter_process_counter_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%i'%melter_process_counter)+'\n')
    trimmer_process_counter_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%i'%trimmer_process_counter)+'\n')
    melter_probability_density_function_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%melter_probability_density_function_evaluate)+'\t'+str.format('%.4f'%failure_time)+'\t'+str.format('%.4f'%melter_probability_density_function_failure_evaluate)+'\n')
    melter_unreliability_function_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%melter_unreliability_function_evaluate)+'\t'+str.format('%.4f'%failure_time)+'\t'+str.format('%.4f'%melter_unreliability_function_failure_evaluate)+'\n')
###
    return(campaign_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output,melter_probability_density_function_output,melter_unreliability_function_output)
#
########################################################################
#
#
#
#
#
####### (f): melter
# Alloy is melted and injected into quartz molds
# There is a probability of failure(s)
# Each failure has an associated failure time
# Some fraction of material is held up in the crucible (heel)
# The heel remains when material leaves
###
#
###
def melter(operation_time,true_weight,expected_weight,melter_failure_number,melter_failure_type,melter_failure_probability,delay,crucible_fraction,accumulated_true_crucible,accumulated_expected_crucible,melter_failure_event,melter_failure_counter,melter_process_counter):
###
    print 'Alloy melting'
    operation_time=operation_time+0.5*delay
    melter_process_counter=melter_process_counter+1
###
    true_crucible=(crucible_fraction[1]-crucible_fraction[2])*numpy.random.random_sample()+crucible_fraction[2] 
    expected_crucible=crucible_fraction[0]
#
    true_weight=true_weight-true_crucible
    expected_weight=expected_weight-expected_crucible  
#
    accumulated_true_crucible=accumulated_true_crucible+true_crucible
    accumulated_expected_crucible=accumulated_expected_crucible+expected_crucible    
###
#
###
# failure testing
# a failure will occur at 0.5 delay time
    melter_failure_event,melter_failure_counter=failure_test(operation_time,melter_failure_number,melter_failure_type,melter_failure_probability,melter_failure_event,melter_failure_counter,melter_process_counter)
###
    if(melter_failure_event==False):
        operation_time=operation_time+0.5*delay
### end if
    return(operation_time,true_weight,expected_weight,accumulated_true_crucible,accumulated_expected_crucible,melter_failure_event,melter_failure_counter,melter_process_counter)
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
