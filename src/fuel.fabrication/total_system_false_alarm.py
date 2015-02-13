########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.06.February.2015
########################################################################
# 
# System false alarm module 
# 
########################################################################
#
# False alarm test is initiated after:
# 
# (1): Equipment failure
# (2): End of campaign
#
# Coming soon: 
#
# (3): After KMP measurement
#
########################################################################
#
# False alarm is triggered if the difference between the measured quantity and expected quantity exceeds a prescribed threshold.
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
# (1): read input data
# (2): open output files
# (3): initialize parameters
# (4): write false alarm data
# (5): false alarm test
# (6): close output files
#
########################################################################
#
#
#
########################################################################
#
# (1): read input data
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
    false_alarm_threshold=numpy.loadtxt('\\system_false_alarm\\false.alarm.threshold.inp',usecols=[1]) #false alarm thresholds
    inspection_time=numpy.loadtxt('\\system_false_alarm\\inspection.time.inp',usecols=[1]) #time elapsed for each inspection
#
    melter_failure_inspection_time=inspection_time[0]
    campaign_inspection_time=inspection_time[1]
    melter_failure_false_alarm_threshold=false_alarm_threshold[0]
    campaign_false_alarm_threshold=false_alarm_threshold[1]
###
#
###  prepare output files
    melter_failure_inspection_time_output=numpy.zeros((1))
    campaign_inspection_time_output=numpy.zeros((1))
    campaign_false_alarm_output=numpy.zeros(1)
    melter_failure_false_alarm_output=numpy.zeros(1)
#
    melter_failure_inspection_time_output[0]=24*melter_failure_inspection_time
    campaign_inspection_time_output[0]=24*campaign_inspection_time    
    campaign_false_alarm_output[0]=end_of_campaign_false_alarm_threshold
    melter_failure_false_alarm_output[0]=melter_failure_false_alarm_threshold    
###
#
### move to output directory
    os.chdir(home_dir)
    os.chdir(output_data_dir)
###
#
### save files
    numpy.savetxt('\\system_false_alarm\\melter.failure.inspection.time.out',melter_failure_inspection_time_output,fmt=['%.2f'],header='Melter failure inspection time (h)',comments='')
    numpy.savetxt('\\system_false_alarm\\campaign.inspection.time.out',campaign_inspection_time_output,fmt=['%.2f'],header='End of campaign inspection time (h)',comments='')
    numpy.savetxt('\\system_false_alarm\\campaign.false.alarm.out',end_of_campaign_false_alarm_output,fmt=['%.4f'],header='Fraction of MUF to trigger alarm for system inspection',comments='')
    numpy.savetxt('\\system_false_alarm\\melter.failure.false.alarm.out',melter_failure_false_alarm_output,fmt=['%.4f'],header='Fraction of MUF to trigger alarm for system inspection due to failure',comments='')
###
#
### go back to home directory
    os.chdir(home_dir)
###
#
###
    print 'False alarm parameters loaded.','\n'
###
    return (melter_failure_false_alarm_threshold,campaign_false_alarm_threshold,melter_failure_inspection_time,campaign_inspection_time)
#
########################################################################
#
#
#
########################################################################
#
# (2): open output files
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
    melter_failure_false_alarm_counter_output=open('\\system_false_alarm\\melter.failure.false.alarm.counter.out','w+')
    campaign_false_alarm_counter_output=open('\\system_false_alarm\\campaign.false.alarm.counter.out','w+')
###
#
### return to home directory
    os.chdir(home_dir)
###
    return(melter_failure_false_alarm_counter_output,campaign_false_alarm_counter_output)
#
########################################################################
#
#
#
########################################################################
#
# (3): initialize parameters
#
#######
def initialize_parameters():
#######
#
    campaign_false_alarm_counter=0 #total false alarms due to end of campaign inspection
    melter_failure_false_alarm_counter=0 #total false alarms due to melter failures
    campaign_false_alarm=False #end of campaign false alarm flag
    melter_failure_false_alarm=False #melter failure false alarm flag
    campaign_false_alarm_test=0 #difference in selected material quantities compared to threshold to trigger false alarm for end of campaign inspection
    melter_failure_false_alarm_test=0 #difference in selected material quantities compared to threshold to trigger false alarm for melter failure inspection
###
    print 'False alarm initialization complete.'
###
    return(campaign_false_alarm_counter,melter_failure_false_alarm_counter,campaign_false_alarm,melter_failure_false_alarm,campaign_false_alarm_test,melter_failure_false_alarm_test)
#
#########################################################################
#
#
#
#########################################################################
#
# (4): write false alarm data
#
#######
def false_alarm_write(operation_time,total_campaign,false_alarm_counter,threshold,false_alarm_counter_output,alarm_test):
#######
#    
    false_alarm_counter_output.write(str.format('%i'%total_campaign)+'\t'+str.format('%i'%false_alarm_counter)+'\t'+str.format('%.4f'%threshold)+'\t'+str.format('%.4f'%alarm_test)+'\t'+str.format('%.4f'%operation_time)+'\n')
###
    return(false_alarm_counter_output)
#
########################################################################
#
#
#
########################################################################
#
# (5): false alarm test
#
#######
def false_alarm_test(threshold,false_alarm_counter,expected_quantity,measured_quantity):
#######
#
    false_alarm=False
    alarm_test=0
#
    alarm_test=abs(measured_quantity-expected_quantity)
#
    if (alarm_test>threshold):
        false_alarm=True
        false_alarm_counter=false_alarm_counter+1
        print 'False alarm triggered','\n','Threshold','%.4f'%threshold,'Test','%.4f'%alarm_test,'Alarm count',false_alarm_counter,'\n\n'
    elif (measured_quantity==expected_quantity):
        print 'No false alarm','\n','Threshold','%.4f'%threshold,'Test','%.4f'%0,'Alarm count',false_alarm_counter,'\n\n'
        
    else:
        print 'No false alarm','\n','Threshold','%.4f'%threshold,'Test','%.4f'%alarm_test,'Alarm count',false_alarm_counter,'\n\n'
# end
###
    return(false_alarm_counter,false_alarm,alarm_test)
#
########################################################################
#
#
#
########################################################################
#
# (6): close output files
#
#######
def close_files(campaign_false_alarm_counter_output,melter_failure_false_alarm_counter_output):
#######
#
    campaign_false_alarm_counter_output.close()
    melter_failure_false_alarm_counter_output.close()
###
    return(campaign_false_alarm_counter_output,melter_failure_false_alarm_counter_output)
#
########################################################################
#
#
#
########################################################################
#
# EOF
#
########################################################################
