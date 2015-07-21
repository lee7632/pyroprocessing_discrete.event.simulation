########################################################################
# R.A.Borrelli
# @TheDoctorRAB 
# rev.20.July.2015
########################################################################
#
# The Weibull distribution is used for a lot of failure analysis.
# It is very flexible for a wide variety of failure scenarios. 
#
########################################################################
#
#
#
########################################################################
#
# The two-parameter Weibull distribution is used for failure analysis in pyroprocessing equipment.
# The main system file control to what equipment Weibull is applied.
#
########################################################################
#
#
#
########################################################################
#
# probability density function
# f(t)=(beta/eta)*((time/eta)**(beta-1))*exp(-(time/eta)**(beta))
#
# cumulative density function
# F(t)=1-exp(-(time/eta)**(beta))
#
# F(T) gives the probability of a failure occuring within time <= T. 
# This is also called the unreliability function, Q(t).
#
# Typically, failure data is fit to the distribution to determine beta and eta.
#
########################################################################
#
#
#
########################################################################
#
# Assumption
#
# beta = 1 for random failures.
# Then, MTTF = eta for this case and the failure rate = 1/eta.
# With increasing time, failure is more likely due to wearing out of the equipment.
# The parameters are read in through the main system file.
#
########################################################################
#
#
#
########################################################################
#
# imports
#
import numpy
#
########################################################################
#
#
#
########################################################################
#
#
#
########################################################################
#
# function list
#
# (1): probability density function
# (2): unreliability function
#
########################################################################
#
#
#
########################################################################
#
# (1): probability density function
#
# Computes weibull probability density function
#
###
def probability_density_function(time_domain,weibull_beta,weibull_eta):
###
    function_evaluate=(weibull_beta/weibull_eta)*((time_domain/weibull_eta)**(weibull_beta-1))*numpy.exp(-(time_domain/weibull_eta)**(weibull_beta))
###
    return(function_evaluate)
########################################################################
#
# (2): unreliability function
#
# Computes weibull unreliability function

###
def unreliability_function(time_domain,weibull_beta,weibull_eta):
###
    function_evaluate=1-numpy.exp(-(time_domain/weibull_eta)**(weibull_beta)) 
###
    return(function_evaluate)
########################################################################
#
# EOF
#
########################################################################
