########################################################################
# Malachi Tolman
# @tolman42
# 18.February.2016
#
########################################################################
#
# This program will serve as the unit test while the fuel.fabrication
# module undergoes heavy revisions to become object oriented instead
# of being procedural.
#
# Currently the log file in the unit test only has an "operation time"
# of 10.  If you run the program differently, it will throw an error.
# Perhaps later I will fix it so that this program will run 
# command and control like file input writing, but this works for now.  
#
# As of now, this only checks a few lines, since the whole file can't be
# compared due to the random distribution.  I could go in an fix the 
# seed, but I'm going with this solution for now.
########################################################################
#
# Imports
#
import numpy
from mainflow_fuel_fabrication import root_dir
#
########################################################################
#
new_log_file = open(root_dir+'/log.txt','r')
#unit_log_file = open('Unit_Test_Docs/unit_test_log.txt','r')

n = 1
did_fail = False
line_test_array = [1,3,5,7,9,11,13,15,16,23,24,28,29,83,84,185,187,188,716,717,755,757]

with open(root_dir+'/src/fuel.fabrication/Unit_Test_Docs/unit_test_log.txt') as unit_log_file:
    for unit_line in unit_log_file:
        log_file_line = new_log_file.readline()
        if log_file_line != unit_line and n in line_test_array:
            print 'difference in ouput files in line %i\n'%(n)
            print 'Unit test log file reads\n%s\n'%(unit_line)
            print 'Your log file reads\n%s\n'%(log_file_line)
            did_fail = True
        n = n+1

if did_fail == False:
    print 'No detected discrepancies in the log file with the unit test.'

            
    
