########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.23.October.2015
########################################################################
# 
# Product storage and final processing 
# 
########################################################################
#
# After metal slugs are obtained from trimming, they would most likely be stored before further fuel rod assembly. 
# Not much happens here. 
# This could be used for non destructive assay; i.e., weight, neutron count, straightness, etc.
# There should be no material losses here.
#
########################################################################
#
# If there is NDA, specific failures would be attributed to the mechanisms; i.e., scale, or detector, which should be its own module.
# No failures here then.
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
# (1): product storage and final processing
#
########################################################################
#
#
#
########################################################################
#
# (1): product storage and final processing
# 
#######
def product_storage(operation_time,equipment_failure_time_0,equipment_failure_time_1,time_delay,true_quantity,expected_quantity,measured_quantity,true_inventory,expected_inventory,measured_inventory):
#######
    print 'Processing the final product','\n\n'
    operation_time=operation_time+time_delay
    equipment_failure_time_0=equipment_failure_time_0+time_delay
    equipment_failure_time_1=equipment_failure_time_1+time_delay
    true_inventory=true_inventory+true_quantity
    expected_inventory=expected_inventory+expected_quantity
    measured_inventory=measured_inventory+measured_quantity
    
###
    return(operation_time,equipment_failure_time_0,equipment_failure_time_1,true_inventory,expected_inventory,measured_inventory)
###########################################################################
#
# EOF
#
########################################################################
