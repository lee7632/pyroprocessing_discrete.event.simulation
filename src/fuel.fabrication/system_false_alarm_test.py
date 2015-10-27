########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.16.July.2015
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
# (3): initialize parameters
#
#######
def initialize_parameters():
#######
#
    end_of_campaign_false_alarm_counter=0 #total false alarms due to end of campaign inspection
    melter_failure_false_alarm_counter=0 #total false alarms due to melter failures
    end_of_campaign_false_alarm=False #end of campaign false alarm flag
    melter_failure_false_alarm=False #melter failure false alarm flag
    end_of_campaign_false_alarm_test=0 #difference in selected material quantities compared to threshold to trigger false alarm for end of campaign inspection
    melter_failure_false_alarm_test=0 #difference in selected material quantities compared to threshold to trigger false alarm for melter failure inspection
###
    print 'False alarm initialization complete.'
###
    return(end_of_campaign_false_alarm_counter,melter_failure_false_alarm_counter,end_of_campaign_false_alarm,melter_failure_false_alarm,end_of_campaign_false_alarm_test,melter_failure_false_alarm_test)
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
def close_files(end_of_campaign_false_alarm_counter_output,melter_failure_false_alarm_counter_output):
#######
#
    end_of_campaign_false_alarm_counter_output.close()
    melter_failure_false_alarm_counter_output.close()
###
    return(end_of_campaign_false_alarm_counter_output,melter_failure_false_alarm_counter_output)
#
########################################################################
#
# EOF
#
########################################################################
