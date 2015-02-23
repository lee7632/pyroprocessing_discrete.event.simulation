########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.23.February.2015
########################################################################
# 
# Edge transitions occur between each vertex.
# State variables do not change on the edges.
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
# (2): edge transition
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
    edge_transition=numpy.loadtxt('edge_transition\\edge.transition.inp',usecols=[1]) #time elapsed on each edge transition
###
#
### go back to home directory
    os.chdir(home_dir)
###
    print 'Edge transition paramters loaded.','\n'
###
    return(edge_transition)
#
########################################################################
#
# (2): edge transition
#
#######
def edge_transition(operation_time,delay):
#######
    print 'Edge transition','\n\n'
    operation_time=operation_time+delay
###
    return(operation_time)
########################################################################
#
# EOF
#
########################################################################
