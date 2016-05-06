########################################################################
# Malachi Tolman
# @tolman42
# rev.4.April.2016
#
########################################################################
#
# This program simply compares the latest log.txt printed to the 
# primary directory indicated by command and control to a stock
# "unit_test_log" that can be saved as anything.  I normally update
# the unit_test_log after I've made a significant change and have
# confirmed that everything still runs correctly.
#
# I've also set the program to break after one discrepancy is found,
# because more often than not, a discrepancy at one place results
# in the rest of the file being off.  So make sure to run the test
# again after you fixed one problem, because it only detects one problem
# at a time.
#
# Notice that for now, this is based off of setting the pseudo-random
# seed to "0" in mainflow.
########################################################################
#
# Imports
#
import numpy
import global_vars
#
########################################################################
#
# Test log file
#
########################################################################
#new_log_file = open(global_vars.root_dir+'/log.txt','r')
unit_log_file = open(global_vars.root_dir+'/src/oo.fuel.fabrication/Unit_Test_Docs/unit_test_log.txt','r')

n = 1
did_fail = False
#line_test_array = [1,3,4,7,10,13,16,17,18,19,23,26,27,30,33,34,36,40,43,44,47,50,51,53,64,66,67,71,75,79,83, \
        #86,89,229,241,245,294,296,874,876,877,881,884,855,889,893]

with open(global_vars.root_dir+'/log.txt') as new_log_file:
    for test_line in new_log_file:
        unit_line = unit_log_file.readline()
        if test_line != unit_line:
            print 'difference in log files in line %i'%(n)
            print 'Unit test log file reads\n%s'%(unit_line)
            print 'Your log file reads\n%s\n'%(test_line)
            did_fail = True
            break
        n = n+1

if did_fail == False:
    print 'No detected discrepancies in the log file with the unit test.\n\n'

########################################################################
#
# Test operation time output
#
########################################################################
#
# Note that this test breaks if it finds a single discrepancy.  That's because there really is no point
# pointing out the inevitability that every single other number will be wrong in this list if even one is off.
#
########################################################################
'''
n = 1 

new_operation_output = open(global_vars.simulation_dir+'/fuel.fabrication/output/data/system/facility.operation.time.out','r')

with open(global_vars.root_dir+'/src/fuel.fabrication/Unit_Test_Docs/fuel.fabrication/output/data/system/facility.operation.time.out') as unit_operation_output:
    for unit_line in unit_operation_output:
        new_operation_output_line = new_operation_output.readline()
        if unit_line != new_operation_output_line:
            print 'difference in operation ouput files in line %i'%(n)
            print 'Unit test operation time file reads\n%s'%(unit_line)
            print 'Your operation time file reads\n%s\n'%(new_operation_output_line)
            break
        n = n+1

    else:
        print 'No detected discrepancies in the operation time file with the unit test.'
'''
