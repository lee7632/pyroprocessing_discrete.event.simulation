########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.23.October.2015
########################################################################
# 
# Melter vertex 
# 
########################################################################
#
# Metal alloy rods are fabricated by injection casting. 
# U, TRU-REFP, and Zr are loaded into the equipment.
# Heat is induced, and the metals melt in a graphite crucible.
# Quartz molds are inserted into the liquid alloy.
# Induced vaccuum causes alloy to be injected in the molds.
# Filled molds are removed and sent to Trimmer.
#
########################################################################
#
# Many failures could occur during this process.
# Currenly, a single, general failure is assumed. 
#
########################################################################
#
# imports
#
import numpy 
from facility_component_module import facility_component_class
from facility_vars_module import facility_vars_class as facility_vars
# import failure_testing_weibull_distribution as failure_analysis
#
########################################################################
#
# function list
#
# (1): injection casting
#
########################################################################
#
#
#
########################################################################
#
# (1): injection casting
# 
#######

class melter_class(facility_component_class):

    def injection_casting(self,facility_vars,delay_time,true_quantity,expected_quantity,equipment_loss_fraction,accumulated_true_equipment_loss,accumulated_expected_equipment_loss,equipment_failure_event,equipment_counter):
    #######
    #print 'Alloy melting'
        self.write_to_log(facility_vars,'Alloy melting\n')
        #operation_time=operation_time+0.5*delay_time
        self.increment_operation_time(facility_vars,0.5*delay_time)
        equipment_counter=equipment_counter+1
        #
        true_equipment_loss=(equipment_loss_fraction[1]-equipment_loss_fraction[2])*numpy.random.random_sample()+equipment_loss_fraction[2] 
        expected_equipment_loss=equipment_loss_fraction[0]
    #
        true_quantity=true_quantity-true_equipment_loss
        expected_quantity=expected_quantity-expected_equipment_loss
    #
        accumulated_true_equipment_loss=accumulated_true_equipment_loss+true_equipment_loss
        accumulated_expected_equipment_loss=accumulated_expected_equipment_loss+expected_equipment_loss    
    ###
    #
    # failure testing at 0.5 delay time
    # if no failure rest of delay time is added
    # if failure then failure times occur
    #
    ###
    #    melter_failure_event,melter_failure_counter=failure_analysis(operation_time,melter_failure_number,melter_failure_type,melter_failure_probability,melter_failure_event,melter_failure_counter,melter_process_counter)
    ###
        if(equipment_failure_event==False):
            #operation_time=operation_time+0.5*delay_time
            self.increment_operation_time(facility_vars,0.5*delay_time)
        #print 'Failure status: ',equipment_failure_event,'\n\n'
        #log_file.write('Failure status: %s\n\n'%(equipment_failure_event))
        self.write_to_log(facility_vars,'Failure status: %s\n\n'%(equipment_failure_event))
            
    ###
        return(facility_vars.operation_time,true_quantity,expected_quantity,accumulated_true_equipment_loss,accumulated_expected_equipment_loss,equipment_failure_event,equipment_counter)
########################################################################
#
# EOF
#
########################################################################
