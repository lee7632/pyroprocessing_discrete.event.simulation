########################################################################
# Malachi Tolman
# @tolman42
# 18.February.2016
########################################################################
#
# This class will contain state variables shared by all the components
# of the facility and will be inherited by each one.
#
########################################################################
#
# Imports
#
import numpy
import global_vars

class Facility_Class:
    'This class should be declared first when running fuel fabrication then get inherited by each component to follow.  It has several state variables that each component object will need.'

    operation_time = 0
    log_file = open(global_vars.root_dir + '/log.txt','w')

    #def __init__(self):
        #self.log_file = log_file
        #self.operation_time = operation_time


    def write_to_log(self,message):
        self.log_file.write(message)

    def increment_operation_time(self,time_added):
        self.operation_time = self.operation_time + time_added
    
        
