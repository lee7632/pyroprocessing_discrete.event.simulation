########################################################################
# Malachi Tolman
# @tolman42
# 18.February.2016
########################################################################
#
# This class will contain the variables associated with the entire
# facility.  It will get declared first, and then will simply get passed
# into each method that needs to act on any given variable.  It will act
# as a package that gets passed around with the "batch" to help keep track
# of a given number of state variables.
#
########################################################################
#
# Imports
#
import numpy

class facility_vars_class:
    'This class contains all of the state variables associated with the facility.  It should be passed to most every method'

    def __init__(self,root_dir):
        self.operation_time = 0
        self.log_file = open(root_dir + '/log.txt','w')
