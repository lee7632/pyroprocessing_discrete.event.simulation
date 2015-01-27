########################################################################
# R.A.Borrelli
# @TheDoctorRAB 
# rev.26.January.2015
# v1.2
########################################################################
#
# v1.0: Basic structure to compute inventory; make material flow work
# v1.1: Add edge travel time; clean up variables and dummys
# v1.2: Weibull distrubution applied to melter failure
#
########################################################################
### Introduction
#
# This is a discrete event simulation code (DES) for the fuel fabrication system in pyroprocessing.
# U,TRU,Zr arrive into the system into a storage buffer.
# Materials are melted by injection casting to form metal rods.
# The metal rods are trimmed to make fuel slugs.
# The fuel slugs are 'processed' into a final storage bufer.
#
# There is an alphabetical list of variables in the last comment section: System variables
#
# Although a fairly simple process, it quickly becomes complicated, due to measurement events (KMPx), equipment failures, subsequent maintenance, false alarms.
# The code then tracks inventory processed, batch weight per campaign, materials unaccounted for (MUF), along with all the above.
#
# The main objective of the code is to track the material in the system during a processing campaign, subject to failure, maintenance, and inspection events. 
# The running processed inventory is recorded for materials unaccounted for (MUF) calculations.
# 
# Operationally, the goal is to process as many campaigns within the operation time.
# Equipment failures would affect operational goals due to maintenance delays.
# Safeguardability comes in because plutonium is being processed.
# The MUF cannot be so large as to indicate there was a diversion. 
# So, optimization is needed between processing as much material as possible, but minimizing MUF and potential false alarms. 
# 
# It is largely a matter of materials accounting and tracking operation time.
# Accurate materials accounting is essential to safeguardability. 
#
# It is intended that this initial code is a test run for pyroprocessing and DES.
# Later, this will become its own class and integrate with the other pyroprocessing systems to form the safeguardability assessment model.
#
########################################################################
#
#
########################################################################
### File tree
#
# des_fuel fabrication: main system file
# des_functions: functions to support the main system file
# des_postprocessing: plotting and data processing, including false alarm probability  
#
########################################################################
### Discrete event simulation description
#
# Each 'event' is a 'vertex'.
# There are state changes and/or parameters associated with a vertex.
# State changes are assigning values to a variable or an equation.
# Parameters are variables needed to make the state change.
# So, DES steps discretely in time through each vertex via an 'edge.'
# At each vertex, the equations are run and the state variables change.
# The edges are dynamic and logical relationships between events. 
#
########################################################################
#
#
########################################################################
### Simulation notes
#
# One campaign = the processing of one batch.
# 1 time unit = 1 DAY.
# Mass is based on kg.
# Results are the number of batches processed per operational period.
# False alarm probability is functionally dependent on equipment falure rate.
#
########################################################################
#
#
########################################################################
### Vertices 
#
# 0. storage
# 1. melter/injection casting 
# 2. trimmer
# 3. recycle
# 4. product
# x. maintenance
#
# State changes only occur at these vericies. 
# Realistically, the true weight is unknown until it is measured at the edges (KMPs for here). 
# Maintence is outside of the main process loop because it is triggered on an equipment failure. 
#
# The index for each vertex is its label in the code; i.e., process_time[1] is the time elapsed for melting.  
# 
########################################################################
#
#
########################################################################
### System diagram
#
# See fuel.fabrication.md on github.
#
# KMP(0): storage transfer to melter
# KMP(1): melter to trimmer
# KMP(2): trimmer to final processing
# KMP(3): melter to recycle
# KMP(-3): recycle back to melter (KMP4 in output)
#
# The KMPs will eventually be able to be turned 'on' or 'off' for different facility configurations.
# Then, the model is run to quantify the safeguardability of each design proposal. 
#
########################################################################
#
#
########################################################################
### Process model (also includes code operations) 
# see also variable list
#
# There is a set time for each vertex and edge.
# These are set ahead of time as part of the input parameters.
#
### preprocessing
#
# 0.    input parameters are read in, open data files  
# 1.    storage_inventory is loaded into storage buffer at TIME=0
#
###
#
### start operation loop
#
# 2.    batch transfer from storage buffer...time lapse
# 3.    batch weight measurement at KMP0 and comparison to expected weight...time lapse
#
# 4.    batch transfer to melter...time lapse
#	. failure test
#
### if failure start maintenance loop
#
# 5.   batch weight measurement at KMP3 and comparision to expected weight...time lapse
# 6.   batch transfer to recycle storage...time lapse
#
# 7.   conduct inspection...time lapse
#	. calculate MUFc, MUF
#	. MUF>0, unprocessed material is in the melter, and the melter needs to be cleaned
# 	. even if this is the first failure, there will be material left over in the equipment upon transfer to recycle
#	. false alarm test
#	. currently no action on false alarm
#
# 8.   conduct cleaning procedure to extract heel...time lapse
#
# 9.   heel weight measurement at KMP3 and comparision to expected weight...time lapse
# 10.  heel transfer to recycle storage...time lapse
#
# 11.  perform maintenance...time lapse
#
# 12.  conduct inspection...time lapse (inspection is needed to restart operation) 
#	. calculate MUFc, MUF
#	. MUFc,MUF=0 because all unprocessed material is located in recycle storage
#	. false alarm test
#	. currently no action on false alarm
#
# 13.  total weight measurement (batch+heel) at KMP3 and comparision to expected weight...time lapse
# 14.  total material transfer to melter...time lapse
#	. failure test
#
### if failure repeat loop, else continue on in the system 
#
# 15.  batch weight measurement at KMP1 and comparison to expected weight...time lapse
# 16.  batch transfer to trimmer...time lapse
#
# 17.  batch weight measurement at KMP2 and comparison to expected weight...time lapse
# 18.  batch transfer to product buffer storage (inventory updated)...time lapse
#
# 19.  conduct inspection...time lapse
#	. calculate MUFc, MUF
#	. MUF>0 due to heel in the melter, no action taken 
#	. false alarm test
#	. currently no action on false alarm
#
# 20.  perform record keeping for batches, campaigns processed, reset campaign-based variables, close data files
#
### if facility operation still active go to 2
#
### postprocessing
#
# 21.  compute false alarm probability
# 22.  make plots
#
###
#
# Data is written continutally with the write_output function as the code steps through the processes, but it is not indicated here because it would clutter up the process description.
# System false alarm data is written continually in the false_alarm_write function.
# KMP data is only recorded at a KMP event with the kmp_write function.
# 
######################################################################## 
#
#
########################################################################
### Assumptions
#
# The code is 'bare bones' and essentially a proof of principle for higher level modeling.
# Several assumptions are made (in no particular order) to get the code to work, get some results (get published).
#
#   . system starts with a fixed quantity of material in the storage buffer
#   . no MUF in the trimmer
#   . no failure of the trimmer
#   . no diversion events
#   . all false alarms are resolved
#   . melter failure is sampled from a standard normal distribution and compared to a prescibed failure probability
#
########################################################################
#
#
########################################################################
### MUF (system) and MUFc (campaign)
# MUF is calculated by Avenhaus
#
# MUF calculations are essential to safeguardability.
#
# MUF is calculated:
#   . end of campaign
#   . on failure after moving bulk material to recycle storage
#   . after maintenance to verify all material is accounted for  
#
# At the end of the campaign, MUF is calculated, but no further action is taken because it is 'known' that MUF is in the melter.
# 
# This will not be the case once diversion is introdced into the model, since it would not be known if the MUF was in the melter or diverted. 
#
# MUF is calculated based on initial and final inventories:
#   . the inventories are determined by the state variables and location of material in the system
#
# MUF and MUFc are independently calculated in order to verify both.
#
# Once through campaign (no failure): 
#   . MUFc = KMP0 - KMP2
#   . KMP0 records inventory transferred from storage buffer
#   . KMP2 records product processed
#
#   . MUF = system inventory - processed inventory
#   . system inventory is running total transferred out of the storage buffer from KMP0
#   . processed inventory is running total from KMP2
#
# Failure inspection: If there is a failure, production stops, equpiment cleaned, and inventory verified
#   . MUFc = KMP3 - KMP0
#   . KMP3 records material transferred out of melter to recycle storage
#
#   . MUF = system inventory - (processed inventory + KMP3)
#   . processed inventory is from prior campaign if the failure occurs
#   
# After the failure inspection, the melter is cleaned, the 'heel' is removed, also measured at KMP3, and transferred to recycle storage.
# Note that KMP3 is needed twice: (1) measures batch from meleter and (2) measures heel from melter; i.e., equipment cleaning.
# Therefore, all intracampaign material is in recycle storage at this point.
# 
# The heel is the amount of material that accumulates in the melter (crucible), randomly during each melting event.
#
# Maintenance is conducted. This is essentially hypothetical and just is associated with a time delay.
# 
# Restart inspection is needed upon completion of maintenance: Confirm all the material is in the recycle storage and MUF =0
#   . MUFc = (KMP3(batch)+MUF)-(KMP3(batch)+KMP3(heel))
#   . verifies that previous system MUF is equal to heel
#   . use of KMP0 would not be correct here because KMP0 will always measure the the batch input quantity per campaign
#   . if failure occurs for campaign > 1, MUF in the melter is left from prior campaigns
#   . system MUF is then needed in MUFc calculation here for material from the prior campaignand based on overall material throughput
#   . (KMP3(batch)+KMP3(heel)) is total unprocessed material for the current campaign
#   . MUFc = 0 because all intracampaign material is accounted for and located in recycle storage
#
#   . MUF = system inventory-(processed inventory+(KMP3(batch)+KMP3(heel))
#   . system MUF = 0 
#   . processed and intracampaign material equals material input into the system over current facility time
###
#
### MUF uncertainty is not currently calculated
#
########################################################################
#
#
########################################################################
### Loop convention
#
# I use e,i,j,k,n for loop indices.
# Otherwise the loop index would be 'spelled out'
#
########################################################################
#
#
########################################################################
### System variables 
#
# Variables are listed in alphabetical order because there are so many.
# Any 'dummy" variable means ones that are called in the function; i.e., multi-use.
# Variable list is for main system and function files for the fuel fabrication model.
#
# true=actual material flow...unknown realistically
# expected=material flow...based on prior data cohorts realistically...set in preprocessing 
# measured=material flow...recorded at each KMP
#
###
#
### Postprocessing variable notes
#
# Variables in postprocessing are largely for making plots and not listed here.
# They are: xmin,ymin,title, etc., and should be self-explanatory.
# Most first appear in the make_plots function.
# There are a few dummy variables because the plot functions are resused several times.
# This all should be straighforward to a knowledgable coder.
#
###
#
### A
#
# accumulated_true_crucible=true material accumulated in crucible
# accumulated_expected_crucible=expected material accumulated in crucible
# accumulated_measured_crucible=measured material accumulated in crucible
# alarm_test=dummy for false alarm testing
#
### B
#
# batch=batch size to be processed...set in preprocessing
#
### C
#
# campaign_inspection_time=end of campaign inspection time
# crucible_fraction=expected_crucible,limits to true_crucible...set in preprocessing
#
### D
#
# delay=dummy variable used in the functions for the time delays...all set in preprocessing
#
### E
#
# edge_time=transfer times along each edge...see system...diagram...set in preprocessing
#
# equipment_failure_probability=dummy variable for equipment failures...set in preprocessing
# equipment_failure_delay_time=dummy variable for equipment failures delay time...set in preprocessing
# equipment_failure_number=dummy for number of failures for specific equipment
# equipment_failure_type=dummy for specific failure
# equipment_failure_counter=number of total failures for specific equipment over operation time
#
# expected_initial/final_inventory=dummy variable used for MUFc calculation 
# expected_quantity=dummy variable for KMP measurement, false alarm test
# expected_kmpX=data file stores measured quantities at each KMP
# expected_system_inventory=running total of mass transfer from storage
# expected_storage_inventory=total expected mass in storage buffer
# expected_crucible=expected material left in the crucible
# expected_weight=expected weight processed per campaign
# expected_crucible_fraction=expected fraction of material left in the crucible...set in preprocessing  
# expected_processed_inventory=total expected mass processed
# expected_muf=total expected facility material unaccounted for
# expected_mufc=expected muf per campagn
#
### F
#
# facility_operation=total number of days per year of facility operation...set in preprocessing 
#
# failure_event=dummy variable boolean to indicate a failure occurred
#
### v1.0 
# failure_test=random variable to compare to failure probability to determine if a failure occurs 
# failure_pdf=probability of random number to test for a failure...based on standard normal distribution 
### 
#
# failure_inspection_time=time to inspect due to failure
#
# _false_alarm_threshold=threshold to trigger false alarm...compared to alarm_test...set in preprocessing 
# _false_alarm_counter=counts false alarms 
# _false_alarm_threshold=threshold to trigger false alarms..not at KMPs...set in preprocessing
# _false_alarm=boolean to activate alarm
# _false_alarm_counter=counts total false alarms over facility_operation
# _false_alarm_attempt=number of total false alarm attempts
# _false_alarm_trigger=actual false alarm
# _false_alarm_error_probability=Type I error=false alarm probability
# false_alarm_identifier=dummy to indicate whether to use system false alarm or kmp false alarm
# _false_alarm_filename=name of file to output
# _false_alarm_test=difference in selected material quantities...compared to threshold to trigger false alarm
# file_=part of the file names for saving, opening, writing, etc.; i.e., file_tree is directory structure
# filename=same thing
#
# failure_time=time record to determine melter failure; if there is a failure, failure_time resets to 0; i.e., there is a new probability distribution
# 
### G
#
# _graph=data files needed for plots
#
### H
#
# home_dir=home directory for the system files
#
### I
#
# inspection_time=dummy variable for time to inspect for end of campaign or failure...set in preprocessing
# inspection_time=contains all the inspection times...set in preprocessing
# input_dir=location of input files
#     
### J
### K
#
# kmp_time=dummy variable for time at each kmp to conduct a measurement...set in preprocessing
# kmp_identifier=dummy variable for identifying the KMP location
# kmp_measurement_threshold=threshold at each KMP determining false alarm...set in preprocessing
# kmp_measurement_uncertainty=uncertainty at KMP...set in preprocessing...used as...true_quantity +/- N(0,measurement_uncertainty)
#
### L
#
### v1.0
# lower_failure_test=random number=failure_test-1s for determining equipment failure
# lower_failure_pdf=associated probability of lower failure test...based on standard normal distribution
###
#
### M
#
# maximum_kmp=maximum number of KMPs based on total processes
# material_quantity=dummy variable for writing data at a KMP
#
# measured_initial/final_inventory=dummy variable used for mufc 
# measured_quantity=dummy variable for KMP measurement, false alarm test
# measured_kmpX=stores quantities at each KMP
# measured_weight=measured weight of material at KMPx
# measured_crucible=measured material left in the crucible
# measured_storage_inventory=total measured mass in storage buffer...at KMP0 
# measured_system_inventory=running total of mass transfer from storage
# measured_processed_inventory=total measured mass processed
# measured_muf=total measured facility material unaccounted for
# measured_mufc=muf for specific campaign
#
# melter_failure_counter=total number of melter failures over operation time
# melter_failure_event=boolean to indicate a melter failure occurred
# melter_failure_number=number of failures that could occur in the melter
# melter_cleaning_time=time delay for the melter to be cleaned...set in preprocessing
# melter_failure_probability=associated probability for each melter failure...set in preprocessing
# melter_failure_maintenance_time=time for maintenance for each failure...set in preprocessing
# melter_failure_false_alarm_threshold=threshold to trigger false alarm due to melter failure...compared to alarm test...set in preprocessing 
# melter_failure_inspection_time=melter failure inspection time
# melter_failure_type=type of melter failure...set in preprocessing
#
# melter_process_counter=counts the number of times the melting process is initiated
#
### N
### O
#
# _output is for output data files...there are a lot of them
# operation_time=operation time of the facility 0<T<facility_operation...set in preprocessing
# output_dir=location of output files (data and figures)
#
### P
#
# plot=data files needed to make plots
# process_time=time elapsed at each process/vertex (not maintenance)...set in preprocessing
#
### Q
### R
### S
#
#
# storage_inventory_start=total amount of material in the storage buffer...currently fixed amount...to be material arrival vertex
# storage_inventory=current inventory in the storage buffer at time=T...eventually this will change with time with arrival of material
#
### T
#
# threshold=dummy variable for measurement threshold (for alarms)
# total_failure=dummy variable for counting failures
# total_campaign=total campaigns processed over facility_operation
# total_batch=total batches processed facility_operation
#
# true_quantity=dummy variable for KMP measurement, false alarm test
# true_kmpX=stores quantities at each KMP
# true_storage_inventory=total mass in storage buffer
# true_crucible=true material left in the crucible per campaign
# true_weight=true weight of material transferred through the system
# total_melter_failure=total failures per campaign for melter
# true_crucible_fraction=quantity of material left in the crucible...randomized per melting process 
# true_system_inventory=running total of mass transfer from storage
# true_processed_inventory=total mass processed 
# true_muf=total material unaccounted for
# true_mufc=muf for specific campaign
# true_initial/final_inventory=dummy variable used for mufc 
#
# trimmer_process_counter=counts the number of times the trimmer process is initiated
#
### U
#
# uncertainty=dummy variable for measurement uncertainty
#
### v1.0
# upper_failure_test=failure_test+1s for determining equipment failure 
# upper_failure_pdf=associated probability of upper failure test...based on standard normal distribution
###
#
### V
### W
#
# weibull_beta=beta parameter for the weibull distribution for failure testing; beta=1.0 assumes failures are random
# weibull_eta=eta parameter for the weibull distribution for failure testing; beta=1.0 means eta=1/failure_rate
#
### X
### Y
### Z
########################################################################
# 
#
#
########################################################################
#
# start main fuel fabrication model
#
########################################################################
#
# 
#
####### imports
import numpy
import des_functions as des_f
import des_postprocessing as des_postproc
########################################################################
#
#
#
####### get working directories
home_dir,input_dir,output_data_dir,output_figure_dir=des_f.get_working_directory()
#######
#
####### read in the input data
batch,crucible_fraction,edge_time,facility_operation,melter_failure_false_alarm_threshold,end_of_campaign_false_alarm_threshold,melter_failure_inspection_time,campaign_inspection_time,kmp_measurement_uncertainty,kmp_time,kmp_measurement_threshold,maximum_kmp,melter_failure_number,melter_failure_type,melter_failure_probability,melter_failure_maintenance_time,melter_cleaning_time,process_time,storage_inventory_start,weibull_beta,weibull_eta=des_f.input_parameters(home_dir,input_dir,output_data_dir)
#######
#
#
#
####### open the output files for data export
time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,end_of_campaign_false_alarm_counter_output,melter_failure_false_alarm_counter_output,true_kmp0,true_kmp1,true_kmp2,true_kmp3,true_kmp4,expected_kmp0,expected_kmp1,expected_kmp2,expected_kmp3,expected_kmp4,measured_kmp0,measured_kmp1,measured_kmp2,measured_kmp3,measured_kmp4,true_heel,expected_heel,measured_heel,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output,probability_density_function_output,unreliability_function_output=des_f.open_files(home_dir,output_data_dir)
#######
#
#
#
####### set facility configurations
# function (b)
# currently inactive
#######
#
#
#
####### main loop for facility operation
#
# 
#
### set the storage buffer and initialize time and KMPs
operation_time,failure_time,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,total_campaign,total_batch,melter_failure_counter,true_weight,expected_weight,measured_weight,true_crucible,expected_crucible,measured_crucible,accumulated_true_crucible,accumulated_expected_crucible,accumulated_measured_crucible,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,end_of_campaign_false_alarm_counter,melter_failure_false_alarm_counter,end_of_campaign_false_alarm,melter_failure_false_alarm,melter_failure_event,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,end_of_campaign_false_alarm_test,melter_failure_false_alarm_test,melter_process_counter,trimmer_process_counter,weibull_probability_density_function_evaluate,weibull_probability_density_function_failure_evaluate,weibull_unreliability_function_evaluate,weibull_unreliability_function_failure_evaluate=des_f.initialize_parameters(storage_inventory_start)
###
#
#
#
########################################################################
####### main process loop
print 'Start facility operation.'
#
while(operation_time<=facility_operation):
    print 'Starting campaign:',total_campaign,'\n'
###
#
####### initial data output routines
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### Storage Buffer preparation
    operation_time,true_weight,expected_weight,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory=des_f.storage_transfer(operation_time,batch,process_time[0],true_weight,expected_weight,true_storage_inventory,expected_storage_inventory,true_system_inventory,expected_system_inventory)
### data output routines
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### edge transition
# Storage Buffer to KMP0
    operation_time=des_f.edge_transition(operation_time,edge_time[0])
#######
#
#
#
####### KMP measurement if active (0)
    operation_time,measured_weight,measured_storage_inventory,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,measured_system_inventory=des_f.kmp_measurement(operation_time,kmp_measurement_uncertainty[0],kmp_time[0],kmp_measurement_threshold[0],true_weight,expected_weight,measured_storage_inventory,measured_system_inventory,0)
### data output routines
    true_kmp0,expected_kmp0,measured_kmp0=des_f.kmp_write(operation_time,true_weight,expected_weight,measured_weight,true_kmp0,expected_kmp0,measured_kmp0)
#
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### edge transition
# Storage KMP0 to Melter
    operation_time=des_f.edge_transition(operation_time,edge_time[1])
#######
#
#
#
####### Melter
    operation_time,true_weight,expected_weight,accumulated_true_crucible,accumulated_expected_crucible,melter_failure_event,melter_failure_counter,melter_process_counter=des_f.melter(operation_time,true_weight,expected_weight,melter_failure_number,melter_failure_type,melter_failure_probability,process_time[1],crucible_fraction,accumulated_true_crucible,accumulated_expected_crucible,melter_failure_event,melter_failure_counter,melter_process_counter)
### data output routines
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
#######
# need to fix the frequency analysis for the failure
# if there is a failure, there needs to be an associated time lapse to transfer to KMP3 for batch and then heel.
# change failure to every 30 days
#######
#
#
#
########################################################################
### Maintenance loop
# If there is a failure, operation stops, material moves to recycle
#    while(melter_failure_event==True):
#        print 'Entering maintenance loop','\n\n'
### 
#
### KMP measurement if active (3)
#        operation_time,measured_weight,measured_storage_inventory=des_f.kmp_measurement(operation_time,measurement_uncertainty[3],kmp_delay_time[3],measurement_threshold_system[3],true_weight,expected_weight,measured_storage_inventory,measured_system_inventory,3)
###
#
### data output routines
#        true_kmp3,expected_kmp3,measured_kmp3=des_f.kmp_write(operation_time,true_weight,expected_weight,measured_weight,true_kmp3,expected_kmp3,measured_kmp3)
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Recycle storage
#        operation_time=des_f.recycle_storage(operation_time,process_time[3])
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Failure inspection
#        operation_time,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc=des_f.mass_balance(operation_time,inspection_time,storage_inventory_start,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_muf,expected_muf,measured_muf,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,melter_failure_event,true_system_inventory,expected_system_inventory,measured_system_inventory)
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Test for false alarm
#        system_false_alarm_counter,system_false_alarm,system_alarm_test=des_f.false_alarm_test(system_false_alarm_limit,system_false_alarm_counter,expected_muf,measured_muf)
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Conduct cleaning process
# Heel is removed from the melter
#        operation_time=des_f.melter_cleaning(operation_time,melter_cleaning_time)
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Measure heel at KMP (3) 
#        operation_time,accumulated_measured_crucible,measured_storage_inventory=des_f.kmp_measurement(operation_time,measurement_uncertainty[3],kmp_delay_time[3],measurement_threshold_system[3],accumulated_true_crucible,accumulated_expected_crucible,measured_storage_inventory,measured_system_inventory,3)
###
#
### data output routines
#        true_heel,expected_heel,measured_heel=des_f.kmp_write(operation_time,accumulated_true_crucible,accumulated_expected_crucible,accumulated_measured_crucible,true_heel,expected_heel,measured_heel)
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Recycle storage
#        operation_time=des_f.recycle_storage(operation_time,process_time[3])
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Perform maintenance
#        operation_time,true_weight,expected_weight,measured_weight,accumulated_true_crucible,accumulated_expected_crucible,accumulated_measured_crucible,true_initial_inventory,expected_initial_inventory,measured_initial_inventory=des_f.maintenance_melter(operation_time,failure_delay_time[0],true_weight,expected_weight,measured_weight,accumulated_true_crucible,accumulated_expected_crucible,accumulated_measured_crucible,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,true_muf,expected_muf,measured_muf)
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Restart inspection
#        operation_time,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc=des_f.mass_balance(operation_time,inspection_time,storage_inventory_start,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_muf,expected_muf,measured_muf,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,melter_failure_event,true_system_inventory,expected_system_inventory,measured_system_inventory)
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Test for false alarm
#        system_false_alarm_counter,system_false_alarm,system_alarm_test=des_f.false_alarm_test(system_false_alarm_limit,system_false_alarm_counter,expected_muf,measured_muf)
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### back through to melter via KMP (-3)
#        operation_time,measured_weight,measured_storage_inventory=des_f.kmp_measurement(operation_time,measurement_uncertainty[3],kmp_delay_time[3],measurement_threshold_system[3],true_weight,expected_weight,measured_storage_inventory,measured_system_inventory,-3)
###
#
### data output routines
#        true_kmp4,expected_kmp4,measured_kmp4=des_f.kmp_write(operation_time,true_weight,expected_weight,measured_weight,true_kmp4,expected_kmp4,measured_kmp4)
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
###
#
### Melter
#        operation_time,true_weight,expected_weight,accumulated_true_crucible,accumulated_expected_crucible,melter_failure_event,total_melter_failure=des_f.melter(operation_time,true_weight,expected_weight,failure_probability[0],process_time[1],crucible_fraction_limit,accumulated_true_crucible,accumulated_expected_crucible,melter_failure_event,total_melter_failure)
###
#
### data output routines
#        time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#        end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
#        melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
# need to fix the frequency analysis for the failure
###
#
###
#        print 'Maintenance complete','\n','Resume processing','\n\n'
### end maintenance loop
########################################################################
#
#
#
####### return to main process loop
#
#
#
####### edge transition
# Melter to KMP1
    operation_time=des_f.edge_transition(operation_time,edge_time[2])
#######
#
#
#
####### KMP measurement if active (1)
    operation_time,measured_weight,measured_storage_inventory=des_f.kmp_measurement(operation_time,kmp_measurement_uncertainty[1],kmp_time[1],kmp_measurement_threshold[1],true_weight,expected_weight,measured_storage_inventory,measured_system_inventory,1)
### data output routines
    true_kmp1,expected_kmp1,measured_kmp1=des_f.kmp_write(operation_time,true_weight,expected_weight,measured_weight,true_kmp1,expected_kmp1,measured_kmp1)
#
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### edge transition
# KMP1 to Trimmer
    operation_time=des_f.edge_transition(operation_time,edge_time[3])
#######
#
#
#
####### Trimmer
# material changes due to fines (trimming leftovers) currently neglected
    operation_time,true_weight,expected_weight,trimmer_process_counter=des_f.trimmer(operation_time,process_time[2],true_weight,expected_weight,trimmer_process_counter)
### data output routines
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### edge transition
# Trimmer to KMP2
    operation_time=des_f.edge_transition(operation_time,edge_time[4])
#######
#
#
#
####### KMP measurement if active (2)
    operation_time,measured_weight,measured_processed_inventory=des_f.kmp_measurement(operation_time,kmp_measurement_uncertainty[2],kmp_time[2],kmp_measurement_threshold[2],true_weight,expected_weight,measured_processed_inventory,measured_system_inventory,2)
### data output routines
    true_kmp2,expected_kmp2,measured_kmp2=des_f.kmp_write(operation_time,true_weight,expected_weight,measured_weight,true_kmp2,expected_kmp2,measured_kmp2)
#
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### edge transition
# KMP2 to Product Storage
    operation_time=des_f.edge_transition(operation_time,edge_time[5])
#######
#
#
#
####### Product storage and final processing
    operation_time,true_processed_inventory,expected_processed_inventory=des_f.product_processing(operation_time,process_time[4],true_weight,expected_weight,true_processed_inventory,expected_processed_inventory)
### data output routines
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
###### End of campaign inspection
    operation_time,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc=des_f.mass_balance(operation_time,campaign_inspection_time,storage_inventory_start,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_muf,expected_muf,measured_muf,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,melter_failure_event,true_system_inventory,expected_system_inventory,measured_system_inventory)
### Test for false alarm
#    system_false_alarm_counter,system_false_alarm,system_alarm_test=des_f.false_alarm_test(system_false_alarm_limit,system_false_alarm_counter,expected_muf,measured_muf)
### data output routines
    time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.write_output(operation_time,total_campaign,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_weight,expected_weight,measured_weight,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,melter_failure_counter,true_system_inventory,expected_system_inventory,measured_system_inventory,melter_process_counter,trimmer_process_counter,time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
    end_of_campaign_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_counter_output,end_of_campaign_false_alarm_test)
    melter_failure_false_alarm_counter_output=des_f.false_alarm_write(operation_time,total_campaign,melter_failure_false_alarm_counter,melter_failure_false_alarm_threshold,melter_failure_false_alarm_counter_output,melter_failure_false_alarm_test)
#######
#
#
#
####### Loop back to start next campaign
# reset campaign based variables and advance campaign counter
    total_campaign,total_batch=des_f.end_of_campaign(total_campaign,total_batch)
    true_weight,expected_weight,measured_weight=des_f.reset_weight()
#######
#
#
#
####### end facility operation loop
########################################################################
#
#
#    
####### close output files
time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,end_of_campaign_false_alarm_counter_output,melter_failure_false_alarm_counter_output,true_kmp0,true_kmp1,true_kmp2,true_kmp3,true_kmp4,expected_kmp0,expected_kmp1,expected_kmp2,expected_kmp3,expected_kmp4,measured_kmp0,measured_kmp1,measured_kmp2,measured_kmp3,measured_kmp4,true_heel,expected_heel,measured_heel,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output=des_f.close_files(time_output,campaign_output,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,end_of_campaign_false_alarm_counter_output,melter_failure_false_alarm_counter_output,true_kmp0,true_kmp1,true_kmp2,true_kmp3,true_kmp4,expected_kmp0,expected_kmp1,expected_kmp2,expected_kmp3,expected_kmp4,measured_kmp0,measured_kmp1,measured_kmp2,measured_kmp3,measured_kmp4,true_heel,expected_heel,measured_heel,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
####### 
#
#
#
#######################################################################
#
# end main fuel fabrication model
#
#######################################################################
#
#
#
########################################################################
####### postprocessing
#
#
#
### system false alarm probability
#des_postproc.false_alarm_probability('system',home_dir,output_data_dir)
###
#
### plots
#des_postproc.make_plots(operation_time,total_campaign,storage_inventory_start,total_melter_failure,system_false_alarm_counter,home_dir,output_data_dir,output_figure_dir)
###
#
#
#
####### end postprocessing
#######################################################################
#
#
#
########################################################################
#      EOF
########################################################################
