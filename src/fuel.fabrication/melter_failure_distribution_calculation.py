########################################################################
# R.A.Borrelli
# @TheDoctorRAB 
# rev.14.October.2015
# v1.0
########################################################################
#
# Calculations for the statistical distribution functions related to melter failure
# This would be the only call in the mainflow for the melter failure
# Specific distribution functions then only have to be imported here
# Calculations are made in real time for future manual equipment removal
# For example, on facility immobilization, check on failure probability, decide on removal
# Rather than just equipment removal automated only on failure event
#
########################################################################
#
# imports
#
import numpy
import failure_analysis_weibull_functions as failure_weibull
#
########################################################################
#
# function list
#
# (1): failure distribution calculation
#
########################################################################
#
#
#
########################################################################
#
# (1): failure distribution calculation 
#
#######
def failure_distribution_calculation(operation_time,melter_failure_time,weibull_beta_melter,weibull_eta_melter):
#######
    melter_probability_density_function_evaluate=failure_weibull.probability_density_function(operation_time,weibull_beta_melter,weibull_eta_melter)
    melter_unreliability_function_evaluate=failure_weibull.unreliability_function(operation_time,weibull_beta_melter,weibull_eta_melter)
    melter_probability_density_function_failure_evaluate=failure_weibull.probability_density_function(melter_failure_time,weibull_beta_melter,weibull_eta_melter)
    melter_unreliability_function_failure_evaluate=failure_weibull.unreliability_function(melter_failure_time,weibull_beta_melter,weibull_eta_melter)
###
    return(melter_probability_density_function_evaluate,melter_unreliability_function_evaluate,melter_probability_density_function_failure_evaluate,melter_unreliability_function_failure_evaluate)
########################################################################
#
# EOF
#
########################################################################
