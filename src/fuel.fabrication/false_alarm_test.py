########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.03.Decemeber.2015
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
# Currently, any false alarm is resolved.
# No time lapse for false alarm test.
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
# (1): false alarm test
#
########################################################################
#
#
#
########################################################################
#
# (1): false alarm test
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
# EOF
#
########################################################################
