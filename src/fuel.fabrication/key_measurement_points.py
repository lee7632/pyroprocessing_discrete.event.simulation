########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.24.February.2015
########################################################################
# 
# Key measurement points (KMPs) are located based on the system diagram.
# 
########################################################################
#
# Assumptions
#
# No false alarms at KMPs.
# No state variable changes at KMPs.
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
# (1): read in input data
# (2): open output files
# (3): kmp measurement
# (4): write kmp measurement data
# (5): close output files
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
    kmp_data=numpy.loadtext('kmps\\key.measurement.points.inp',usecols=[0]) #reads in the KMP lables to determine the total number of KMPs in the facility
    kmp_measurement_time=numpy.loadtxt('kmps\\key.measurement.points.inp',usecols=[1]) #measurement time at each KMP
    kmp_measurement_uncertainty=numpy.loadtxt('kmps\\key.measurement.points.inp',usecols=[2]) #measurement uncertainty at each KMP
    kmp_measurement_threshold=numpy.loadtxt('kmps\\key.measurement.points.inp',usecols=[3]) #measurement threshold to trigger false alarms at each KMP
###
#
### determine maximum KMPs
    maximum_kmp=len(kmp_data) #total number of KMPs
###
#
### go back to home directory
    os.chdir(home_dir)
###
    print 'Key measurment point information read.','Total KMPs:',maximum_kmp,'\n'
###
    return(kmp_measurement_time,kmp_measurement_uncertainty,kmp_measurement_threshold)
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
    true_kmp=open('true.kmp.out','w+')
    expected_kmp=open('expected.kmp.out','w+')
    measured_kmp=open('measured.kmp.out','w+')
###
#
### return to home directory
    os.chdir(home_dir)
###
    return(true_kmp,expected_kmp,measured_kmp)
#
########################################################################
#
#
#
#########################################################################
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
########################################################################
#
# (N): close output files
#
#######
def close_files(time_output,campaign_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_kmp0,true_kmp1,true_kmp2,true_kmp3,true_kmp4,expected_kmp0,expected_kmp1,expected_kmp2,expected_kmp3,expected_kmp4,measured_kmp0,measured_kmp1,measured_kmp2,measured_kmp3,measured_kmp4,true_heel,expected_heel,measured_heel,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output):
#######
#
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
####### (y): Weibull probability density function evaluation
# Compute the probability density function [f(t)] for the weibull distribution
###
#
def weibull_probability_density_function(time_domain,weibull_beta,weibull_eta):
###
    function_evaluate=(weibull_beta/weibull_eta)*((time_domain/weibull_eta)**(weibull_beta-1))*numpy.exp(-(time_domain/weibull_eta)**(weibull_beta))
###
    return(function_evaluate)
########################################################################
#
#
#
####### (z): Weibull unreliability function evaluation
# Compute the unreliability function [Q(t)]for the weibull distribution
# This is also the cumulative density function [F(t)]
###
#
def weibull_unreliability_function(time_domain,weibull_beta,weibull_eta):
###
    function_evaluate=1-numpy.exp(-(time_domain/weibull_eta)**(weibull_beta)) 
###
    return(function_evaluate)
########################################################################
#
#
#
########################################################################
#
#      EOF
#
########################################################################
