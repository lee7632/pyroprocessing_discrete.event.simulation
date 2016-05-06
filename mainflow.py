########################################################################
# Malachi Tolman
# @tolman42
# rev.4.April.2016
########################################################################
#
# This program will simulate the fuel fabrication process.
#
# True to the system diagram, U and TRU will get fed into the fuel
# fabricator.  It then processes the SNM (special nuclear material)
# into metal slugs that are stored in product storage.  One batch that moves
# from the storage buffer through the system to product storage counts
# as a single campaign.  Once that occurs, a brief end of campaign
# inspection is held.
#
# Variables for the most part are stored in the facility component moduble in
# charge of operations pertaining to that state variable, altough
# some variables important to the whole facility are stored in
# the facility_command module that is passed from component to component.
#
########################################################################
#
# EDITOR'S NOTES:
#
# If you are viewing this code for one of the first times, I'd recommend
# following the logic file by file.  Start with the facility command
# module, follow the initializing routine and process batch, then view
# the called module as it comes up.
#
# This code tries to be as straightforward as possible while maintaining
# modularity and component hierarchy.  The only process that is a bit
# of a black box is the edge transition. But all it really does is take
# the expected batch weight of object 1, pass it to object 2, then
# resets the expected batch weight of object 1.
#
# Again, aside from that, although the code is bloated, it tends to be
# straightforward in describing itself.
#
# Most of the notes are found in the class and method descriptions. This
# was done so that the readme of each object could be called from the
# command line.
#
########################################################################
#
# Imports
#
########################################################################
import numpy as np
import global_vars
import sys

sys.path.insert(0, global_vars.root_dir+'/src/oo.fuel.fabrication')
from facility_command_module import facility_command_class

np.random.seed(0)

######## 
# initialize facility
######## 
facility = facility_command_class(global_vars.root_dir,'fuel.fabrication')

######
# Process the materials  
######
facility.write_to_log('Start facility operation\n')
while facility.operation_time <= facility.total_operation_time:
    facility.write_to_log('Starting campaign: %i at time:  %.4f  days \n\n' \
            %(facility.total_campaign, facility.operation_time))
    
    facility.process_batch()
    facility.end_of_campaign()
    
facility.close_files()
