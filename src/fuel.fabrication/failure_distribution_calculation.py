########################################################################
# R.A.Borrelli
# @TheDoctorRAB 
# rev.20.October.2015
# v1.0
########################################################################
#
# Calculations for the statistical distribution functions related to equipment 
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
def failure_distribution_calculation(operation_time,equipment_failure_time,weibull_beta,weibull_eta):
#######
    probability_density_function_evaluate=failure_weibull.probability_density_function(operation_time,weibull_beta,weibull_eta)
    unreliability_function_evaluate=failure_weibull.unreliability_function(operation_time,weibull_beta,weibull_eta)
    probability_density_function_failure_evaluate=failure_weibull.probability_density_function(equipment_failure_time,weibull_beta,weibull_eta)
    unreliability_function_failure_evaluate=failure_weibull.unreliability_function(equipment_failure_time,weibull_beta,weibull_eta)
###
    return(probability_density_function_evaluate,unreliability_function_evaluate,probability_density_function_failure_evaluate,unreliability_function_failure_evaluate)
########################################################################
#
# EOF
#
########################################################################
