########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.06.December.2014
########################################################################
# These functions will be used to support DES modeling.
########################################################################
#
########################################################################
# i,j,k,l,n are used for loop indices
########################################################################
#
#
#
####### imports
import numpy
import scipy
import os
from scipy import stats
########################################################################
#
#
#
########################################################################
#
####### (a): Read input data
####### (b): Set facility configuration
####### (d): Storage transfer
####### (e): KMP measurement
####### (f): melter
####### (g): trimmer
####### (h): product processing
####### (i): mass balance
####### (j): false alarm test
####### (k): recycle storage
####### (m): Failure test
####### (n): End of campaign reset
####### (n): End of campaign reset
####### (o): Open output files
####### (p): Write to output files
####### (q): Close output files
####### (r): Initialize parameters
####### (s): Melter cleaning procedure
####### (t): Maintenance
####### (u): KMP measurement recording write to file
####### (v): False alarm write
####### (w): Get working directories
#
########################################################################
#
#
#
####### (a): Read input data
# Read in or calculate all the user set input data for the DES model
# Some of these are hypothethical values for now
# When real data is obtained, this can be changed
# The variable list is in the main program
### 
#
###            
def input_parameters(home_dir,input_dir,output_data_dir):
###
#
#
### go to input file directory
    os.chdir(input_dir)
###
#
### open data files
    facility_configuration=numpy.loadtxt('facility.configuration.inp',dtype=int)
    maximum_kmp=numpy.loadtxt('kmp.inp',dtype=int)
    storage_inventory_start=numpy.loadtxt('storage.inventory.inp')
    failure_number=numpy.loadtxt('failure.number.inp')
    process_failure_probability=numpy.loadtxt('failure.probability.inp')
    process_failure_delay_time=numpy.loadtxt('failure.delay.time.inp')
    batch=numpy.loadtxt('batch.inp')
    facility_operation=numpy.loadtxt('facility.operation.inp')
    inspection_time_limit=numpy.loadtxt('inspection.time.inp')
    measurement_uncertainty_limit=numpy.loadtxt('measurement.uncertainty.inp')
    crucible_fraction_limit=numpy.loadtxt('crucible.inp')
    kmp_delay_time_limit=numpy.loadtxt('kmp.delay.time.inp')
    process_time=numpy.loadtxt('process.time.inp',usecols=[1])
    measurement_threshold=numpy.loadtxt('measurement.threshold.inp')
    system_false_alarm_threshold=numpy.loadtxt('system.false.alarm.inp')
    melter_cleaning_time_limit=numpy.loadtxt('melter.cleaning.delay.time.inp')
    readme_input=open('readme.md').readlines()
###
# only the melter will fail
# there hypothetical failures with associated delay times
    failure_probability=numpy.zeros((failure_number))
    failure_delay_time=numpy.zeros((failure_number))
#    
    for i in range(0,failure_number):
        failure_probability[i]=process_failure_probability*numpy.random.random_sample()
        failure_delay_time[i]=process_failure_delay_time[i]
# end i
### 
    inspection_time=inspection_time_limit
    melter_cleaning_time=melter_cleaning_time_limit
### 
# each KMP will have a measurement uncertainty and a time delay
    measurement_uncertainty=numpy.zeros((maximum_kmp))
    kmp_delay_time=numpy.zeros((maximum_kmp))
    measurement_threshold_system=numpy.zeros((maximum_kmp))
    for j in range(0,maximum_kmp):
        measurement_uncertainty[j]=measurement_uncertainty_limit[j]
        kmp_delay_time[j]=kmp_delay_time_limit[j]
        measurement_threshold_system[j]=measurement_threshold[j]
# end j
###
    system_false_alarm_limit=system_false_alarm_threshold
###
#
### output
    process_failures_output=numpy.zeros((failure_number,2))
    inspection_time_output=numpy.zeros((1))
    measurement_kmp_output=numpy.zeros((maximum_kmp,4))
    system_false_alarm_output=numpy.zeros((1))
    melter_cleaning_time_output=numpy.zeros((1))
    batch_output=numpy.zeros((1))
    facility_operation_output=numpy.zeros((1))
#
    for k in range(0,failure_number):
        process_failures_output[k,0]=failure_probability[k]
        process_failures_output[k,1]=(24*failure_delay_time[k])
# end k
#
    inspection_time_output[0]=24*inspection_time
    system_false_alarm_output[0]=system_false_alarm_limit
    melter_cleaning_time_output[0]=24*melter_cleaning_time
    batch_output[0]=batch
    facility_operation_output[0]=facility_operation
#
    for l in range(0,maximum_kmp):
        measurement_kmp_output[l,0]=l
        measurement_kmp_output[l,1]=measurement_uncertainty[l]
        measurement_kmp_output[l,2]=24*kmp_delay_time[l]
        measurement_kmp_output[l,3]==measurement_threshold[l]        
###
#
### save files
# move to output directory
    os.chdir(home_dir)
    os.chdir(output_data_dir)
#
    numpy.savetxt('process.failures.out',process_failures_output,fmt=['%.4f','%.2f'],header='Failure probability\tMaintenance time (h)',comments='',delimiter='\t\t\t')
    numpy.savetxt('inspection.time.out',inspection_time_output,fmt=['%.2f'],header='Inspection time (h)',comments='')
    numpy.savetxt('measurement.kmp.out',measurement_kmp_output,fmt=['%.0f','%.4f','%.2f','%.4f'],header='KMP\tMeasurement uncertainty\tMeasurement delay time (h)\tMeasurement threshold',comments='',delimiter='\t\t\t')
    numpy.savetxt('system.false.alarm.out',system_false_alarm_output,fmt=['%.4f'],header='Fraction of MUF to trigger alarm for system inspection',comments='')
    numpy.savetxt('melter.cleaning.time.out',melter_cleaning_time_output,fmt=['%.4f'],header='Time to clean the melter additional to maintenance activity (h)',comments='')
    numpy.savetxt('facility.operation.out',facility_operation_output,fmt=['%.1f'],header='Facility operational period (d)',comments='')
    numpy.savetxt('batch.out',batch_output,fmt=['%.1f'],header='Batch per campaign (kg)',comments='')
#
    readme_output=open('readme.md','w+')
    readme_output.write(readme_input[0])
    readme_output.close()
###
#
### go back to home directory
    os.chdir(home_dir)
###
    return (facility_configuration,maximum_kmp,storage_inventory_start,failure_probability,failure_delay_time,inspection_time,measurement_uncertainty,kmp_delay_time,crucible_fraction_limit,batch,facility_operation,process_time,measurement_threshold_system,system_false_alarm_limit,melter_cleaning_time)
########################################################################
#
#    
#
####### (b): Set facility configuration
# Sets facility configuration by turning 'off' relevant KMPs
###
#
###
#def
###
#
#
###
#   return
########################################################################
#
#
#
####### (d): Storage transfer
# Material leaves the storage buffer
###
#
###
def storage_transfer(operation_time,batch,delay,true_quantity,expected_quantity,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory):
###
    print 'Storage transfer: One batch is transferred.',batch,'kg','\n\n'    
    operation_time=operation_time+delay
#
    true_quantity=batch
    expected_quantity=batch
#
    true_storage_inventory=true_storage_inventory-true_quantity
    expected_storage_inventory=expected_storage_inventory-expected_quantity
#
    true_system_inventory=true_system_inventory+true_quantity
    expected_system_inventory=expected_system_inventory+expected_quantity
###
    return(operation_time,true_quantity,expected_quantity,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory)
########################################################################
#
#
#
####### (e): KMP measurement
# Conducts measurement at a KMP
# The kmp_counter identifies which KMP parameters
# These are delay time, threshold, measurement uncertainty
# If there is a discrepancy with the measured weight and expected weight
# Then the alarm is triggered
# The measured quantities will change because each KMP has uncertainty
###
#
###
def kmp_measurement(operation_time,uncertainty,delay,threshold,true_quantity,expected_quantity,measured_inventory,measured_system_inventory,kmp_identifier):
###
    print 'Measurement event at KMP:',kmp_identifier
    operation_time=operation_time+delay
    measured_quantity=0
###
    if (kmp_identifier==0): #storage transfer
        measured_quantity=true_quantity+uncertainty*numpy.random.randn()
        measured_inventory=measured_inventory-measured_quantity
        measured_system_inventory=measured_system_inventory+measured_quantity
#
        true_initial_inventory=true_quantity
        expected_initial_inventory=expected_quantity
        measured_initial_inventory=measured_quantity
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
# end if
###
    print 'Operation time','%.4f'%operation_time,'(d)','\n','True quantity','%.4f'%true_quantity,'(kg)','\n','Expected quantity','%.4f'%expected_quantity,'(kg)','\n','Measured quantity','%.4f'%measured_quantity,'(kg)','\n\n'
###
    if (kmp_identifier==0):
        return(operation_time,measured_quantity,measured_inventory,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,measured_system_inventory)
    else:
        return(operation_time,measured_quantity,measured_inventory)
########################################################################
#
#
#
####### (f): melter
# Alloy is melted and injected into quartz molds
# There is a probability of failure
# Each failure has an associated failure time
# Some fraction of material is held up in the crucible (heel)
# The heel occurs when material leaves
###
#
###
def melter(operation_time,true_weight,expected_weight,equipment_failure_probability,delay,crucible_fraction_limit,accumulated_true_crucible,accumulated_expected_crucible,melter_failure_event,total_melter_failure):
###
    print 'Alloy melting','\n\n'
    operation_time=operation_time+delay
#
    true_crucible=crucible_fraction_limit[0]*numpy.random.random_sample()
    expected_crucible=crucible_fraction_limit[1]
#
    true_weight=true_weight-true_crucible
    expected_weight=expected_weight-expected_crucible  
#
    accumulated_true_crucible=accumulated_true_crucible+true_crucible
    accumulated_expected_crucible=accumulated_expected_crucible+expected_crucible    
#
    melter_failure_event,total_melter_failure=failure_test(equipment_failure_probability,melter_failure_event,total_melter_failure)
###
    return(operation_time,true_weight,expected_weight,accumulated_true_crucible,accumulated_expected_crucible,melter_failure_event,total_melter_failure)
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
def trimmer(operation_time,delay,true_quantity,expected_quantity):
###
    print 'Slug trimming','\n\n'
    operation_time=operation_time+delay
###
    return(operation_time,true_quantity,expected_quantity)
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
def product_processing(operation_time,delay,true_quantity,expected_quantity,measured_quantity,true_processed_inventory,expected_processed_inventory,measured_processed_inventory):
###
    print 'Processing the final product','\n\n'
    operation_time=operation_time+delay
#
    true_processed_inventory=true_processed_inventory+true_quantity
    expected_processed_inventory=expected_processed_inventory+expected_quantity
    
###
    return(operation_time,true_processed_inventory,expected_processed_inventory,measured_processed_inventory)
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
####### (j): false alarm test
# Tests for false alarm at inspection and KMP measurements
###
#
###
def false_alarm_test(threshold,false_alarm_counter,expected_quantity,measured_quantity):
###
    false_alarm=False
    alarm_test=0
    alarm_test=abs(measured_quantity-expected_quantity)
    if (alarm_test>threshold):
        false_alarm=True
        false_alarm_counter=false_alarm_counter+1
        print 'False alarm triggered','\n','Threshold','%.4f'%threshold,'Test','%.4f'%alarm_test,'Alarm count',false_alarm_counter,'\n\n'
    elif (measured_quantity==expected_quantity):
        print 'No false alarm','\n','Threshold','%.4f'%threshold,'Test','%.4f'%0,'Alarm count',false_alarm_counter,'\n\n'
        
    else:
        print 'No false alarm','\n','Threshold','%.4f'%threshold,'Test','%.4f'%alarm_test,'Alarm count',false_alarm_counter,'\n\n'
# end if
###
    return(false_alarm_counter,false_alarm,alarm_test)
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
# Tests for a failure in whatever equipment
###
#
###
def failure_test(equipment_failure_probability,failure_event,total_failure):
###
    failure_test=0
    lower_failure_test=0
    upper_failure_test=0
    lower_failure_pdf=0
    upper_failure_pdf=0
#
    failure_test=numpy.random.randn()    
    lower_failure_test=failure_test-1
    upper_failure_test=failure_test+1
    lower_failure_pdf=scipy.stats.norm.pdf(lower_failure_test)
    upper_failure_pdf=scipy.stats.norm.pdf(upper_failure_test)
    print 'Failure test'
    print 'Failure probability','%.4f'%equipment_failure_probability
    print 'Test range','%.4f'%lower_failure_test,'%.4f'%upper_failure_test
    print 'Probability range','%.4f'%lower_failure_pdf,'%.4f'%equipment_failure_probability,'%.4f'%upper_failure_pdf
    if (lower_failure_pdf<=equipment_failure_probability<=upper_failure_pdf):     
        print 'Failure'
        failure_event=True
        total_failure=total_failure+1
        print 'Failure #:',total_failure,'\n\n'
    elif (upper_failure_pdf<=equipment_failure_probability<=lower_failure_pdf):
        print 'Failure'
        failure_event=True
        total_failure=total_failure+1
        print 'Failure #:',total_failure,'\n\n'    
    else:
        print 'No failure','\n\n'
        failure_event=False
###
    return(failure_event,total_failure)
########################################################################
#
#
#
####### (n): End of campaign reset
# This advances the counters
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
####### (n): End of campaign reset
# This zeros out the weights
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
####### (o): Open output files
# Opens output files
###
#
###
def open_files(home_dir,output_data_dir):
###
#
### change directory
    os.chdir(output_data_dir)
###
#
###
    time_output=open('facility.operation.time.out','w+')
    campaign_output=open('facility.campaign.out','w+')
    true_storage_inventory_output=open('true.storage.inventory.out','w+')
    expected_storage_inventory_output=open('expected.storage.inventory.out','w+')
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
    total_melter_failure_output=open('total.melter.failures.out','w+')
    system_false_alarm_counter_output=open('system.false.alarm.counter.out','w+')
    true_kmp0=open('true.kmp0.out','w+')
    true_kmp1=open('true.kmp1.out','w+')
    true_kmp2=open('true.kmp2.out','w+')
    true_kmp3=open('true.kmp3.out','w+')
    true_kmp4=open('true.kmp4.out','w+')
    expected_kmp0=open('expected.kmp0.out','w+')
    expected_kmp1=open('expected.kmp1.out','w+')
    expected_kmp2=open('expected.kmp2.out','w+')
    expected_kmp3=open('expected.kmp3.out','w+')
    expected_kmp4=open('expected.kmp4.out','w+')
    measured_kmp0=open('measured.kmp0.out','w+')
    measured_kmp1=open('measured.kmp1.out','w+')
    measured_kmp2=open('measured.kmp2.out','w+')
    measured_kmp3=open('measured.kmp3.out','w+')
    measured_kmp4=open('measured.kmp4.out','w+')
    true_heel=open('true.heel.out','w+')
    expected_heel=open('expected.heel.out','w+')
    measured_heel=open('measured.heel.out','w+')
    true_system_inventory_output=open('true.system.inventory.out','w+')
    expected_system_inventory_output=open('expected.system.inventory.out','w+')
    measured_system_inventory_output=open('measured.system.inventory.out','w+')
###
#
### return to home directory
    os.chdir(home_dir)
###
    return(time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,system_false_alarm_counter_output,true_kmp0,true_kmp1,true_kmp2,true_kmp3,true_kmp4,expected_kmp0,expected_kmp1,expected_kmp2,expected_kmp3,expected_kmp4,measured_kmp0,measured_kmp1,measured_kmp2,measured_kmp3,measured_kmp4,true_heel,expected_heel,measured_heel,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output)
########################################################################
#
#
#
####### (p): Write to output files
# Writes data to output files
###
#
###
def write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,total_melter_failure,true_system_inventory,expected_system_inventory,measured_system_inventory,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output):
###
    time_output.write(str.format('%.4f'%operation_time)+'\n')
    campaign_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%i'%total_campaign)+'\n')
    true_storage_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_storage_inventory)+'\n')
    expected_storage_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_storage_inventory)+'\n')
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
    true_system_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_system_inventory)+'\n')
    expected_system_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_system_inventory)+'\n')
    measured_system_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_system_inventory)+'\n')
###
    return(time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output)
########################################################################
#
#
#
####### (q): Close output files
# Writes data to output files
###
#
###
def close_files(time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,system_false_alarm_counter_output,true_kmp0,true_kmp1,true_kmp2,true_kmp3,true_kmp4,expected_kmp0,expected_kmp1,expected_kmp2,expected_kmp3,expected_kmp4,measured_kmp0,measured_kmp1,measured_kmp2,measured_kmp3,measured_kmp4,true_heel,expected_heel,measured_heel,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output):
###
    time_output.close()
    campaign_output.close()
    true_storage_inventory_output.close()
    expected_storage_inventory_output.close()
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
    system_false_alarm_counter_output.close()
    true_kmp0.close()
    true_kmp1.close()
    true_kmp2.close()
    true_kmp3.close()
    true_kmp4.close()
    expected_kmp0.close()
    expected_kmp1.close()
    expected_kmp2.close()
    expected_kmp3.close()
    expected_kmp4.close()
    measured_kmp0.close()
    measured_kmp1.close()
    measured_kmp2.close()
    measured_kmp3.close()
    measured_kmp4.close()
    true_heel.close()
    expected_heel.close()
    measured_heel.close()
    true_system_inventory_output.close()
    expected_system_inventory_output.close()
    measured_system_inventory_output.close()
###
    return(time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,system_false_alarm_counter_output,true_kmp0,true_kmp1,true_kmp2,true_kmp3,true_kmp4,expected_kmp0,expected_kmp1,expected_kmp2,expected_kmp3,expected_kmp4,measured_kmp0,measured_kmp1,measured_kmp2,measured_kmp3,measured_kmp4,true_heel,expected_heel,measured_heel,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output)
########################################################################
#
#
#
####### (r): Initialize parameters
# Sets the storage buffer and initializes parameters
# true_,expected_,measured_inventory is set up for when fuel fabrication is combined with electrowinning
# There will be a KMP prior to loading into the storage buffer
# So inventory is true inventory for now 
###
#
###
def initialize_parameters(storage_inventory_start):
###
    operation_time=0
    true_processed_inventory=0
    expected_processed_inventory=0
    measured_processed_inventory=0
    total_campaign=1
    total_batch=1
    total_melter_failure=0
    true_weight=0
    expected_weight=0
    measured_weight=0
    true_crucible=0
    expected_crucible=0
    measured_crucible=0
    accumulated_true_crucible=0
    accumulated_expected_crucible=0
    accumulated_measured_crucible=0
    true_muf=0
    expected_muf=0
    measured_muf=0
    true_mufc=0
    expected_mufc=0
    measured_mufc=0
    system_false_alarm_counter=0
    system_false_alarm=False
    melter_failure_event=False
    true_storage_inventory=storage_inventory_start
    expected_storage_inventory=storage_inventory_start
    measured_storage_inventory=storage_inventory_start
    true_system_inventory=0
    expected_system_inventory=0
    measured_system_inventory=0
    system_alarm_test=0
###
    return(operation_time,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,total_campaign,total_batch,total_melter_failure,true_weight,expected_weight,measured_weight,true_crucible,expected_crucible,measured_crucible,accumulated_true_crucible,accumulated_expected_crucible,accumulated_measured_crucible,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,system_false_alarm_counter,system_false_alarm,melter_failure_event,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,system_alarm_test)
#########################################################################
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
#
#
####### (u): KMP measurement recording write to file
# Maintenance is performed on the equipment
# Currently this is only for the melter
###
def kmp_write(operation_time,true_quantity,expected_quantity,measured_quantity,true_kmp,expected_kmp,measured_kmp):
###
    true_kmp.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_quantity)+'\n')
    expected_kmp.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_quantity)+'\n')
    measured_kmp.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_quantity)+'\n')#
###
    return(true_kmp,expected_kmp,measured_kmp)
########################################################################
#
#
#
####### (v): False alarm write
# Writes data to output files for false alarms
###
#
###
def false_alarm_write(operation_time,total_campaign,false_alarm_counter,threshold,false_alarm_counter_output,alarm_test):
###
    false_alarm_counter_output.write(str.format('%i'%total_campaign)+'\t'+str.format('%i'%false_alarm_counter)+'\t'+str.format('%.4f'%threshold)+'\t'+str.format('%.4f'%alarm_test)+'\t'+str.format('%.4f'%operation_time)+'\n')
###
    return(false_alarm_counter_output)
########################################################################
#
#
#
####### (w): Get working directories
# Input and output files are in different directories than the system files.
# Command and control file creates the directories and copies the input files into them from the default directory.
# A system locator file is also created containing the relative (to the system files) paths. 
###
def get_working_directory():
###
#
### get home directory
# Home directory is where the system files are located.
    home_dir=os.getcwd()
###
#
### open path file
# The path file contains the three directory locations split by commas, so it is all one string.
# Writing the file with the '\n' made it 'stuck' so using os.chdir could not be done because the '\n' could not be removed.
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
    return(home_dir,input_dir,output_data_dir,output_figure_dir)
########################################################################
#
#
#
########################################################################
#      EOF
########################################################################
