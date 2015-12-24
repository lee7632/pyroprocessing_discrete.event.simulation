########################################################################
# R.A.Borrelli
# @TheDoctorRAB
# rev.27.October.2015
########################################################################
# 
# Functions for in-simulation data processing
# 
########################################################################
#
# imports
#
import os
import numpy
import shutil
#
########################################################################
#
# function list
#
# (1): get directory paths 
#
# input regime
# (2a): read system operation input data
# (2b): read storage buffer input data
# (2c): read equipment input data
# (2d): read system false alarm input data
# (2e): read edge transition input data
# (2f): read kmp input data
#
# output regime
# (3a):   open system output files
# (3a.i): open equipment output files
# (3b):   open material flow output files
# (3b.i): open process loss output files
# (3c):   open inventory output files
# (3d):   open system false alarm output files
# (3e):   open kmp output files
# (3f):   open equipment failure output files
# (3g):   open muf output files
#
# initialization regime
# (4a):   initialize system parameters
# (4b):   initialize material flow parameters
# (4b.i): initialize equipment process loss 
# (4c):   initialize inventory parameters
# (4d):   initialize system false alarm parameters
# (4e):   initialize equipment parameters
# (4f):   initialize muf parameters
#
# data writing regime
# (5a):   write system time
# (5a.i): write equipment time
# (5b):   write campaign 
# (5c):   write process counter 
# (5d):   write material flow 
# (5e):   write process loss 
# (5f):   write inventory 
# (5g):   write muf
# (5h):   write end of campaign false alarm
# (5i):   write equipment failure false alarm
# (5j):   write equipment failure
# (5k):   write kmp measurement data
#
# end of campaign regime
# (6a): end of campaign diagnostics
# (6b): reset campaign batch weights
#
########################################################################
#
#
########################################################################
#
# (1): get directory paths
#
# directories are created and input files are copied into them from the lib directory by pyroprocessing_command.py
# system locator file is created containing the directory paths in each subsystem folder
#
#######
def get_dir_path(root_dir,subsystem):
#######
    os.chdir(root_dir+'/simulation/meta.data') #get home directory
    home_dir=open('home.dir.inp').read()
    directory_path_file=open('fuel.fabrication_simulation.dir.inp').readlines() #get directory paths
    directory_paths=directory_path_file[0].split(',') #split path data and set directories
    input_dir=directory_paths[0]
    output_dir=directory_paths[1]
    edge_transition_dir=directory_paths[2]
    failure_distribution_dir=directory_paths[3]
    failure_equipment_dir=directory_paths[4]
    kmps_dir=directory_paths[5]
    process_states_dir=directory_paths[6]
    system_false_alarm_dir=directory_paths[7]
    data_dir=directory_paths[8]
    figures_dir=directory_paths[9]
    system_odir=directory_paths[10]
    material_flow_odir=directory_paths[11]
    inventory_odir=directory_paths[12]
    false_alarm_odir=directory_paths[13]
    kmps_odir=directory_paths[14]
    muf_odir=directory_paths[15]
    equipment_failure_odir=directory_paths[16]
    system_gdir=directory_paths[17]
    material_flow_gdir=directory_paths[18]
    inventory_gdir=directory_paths[19]
    false_alarm_gdir=directory_paths[20]
    kmps_gdir=directory_paths[21]
    muf_gdir=directory_paths[22]
    equipment_failure_gdir=directory_paths[23]
###
    return(input_dir,output_dir,edge_transition_dir,failure_distribution_dir,failure_equipment_dir,kmps_dir,process_states_dir,system_false_alarm_dir,data_dir,figures_dir,system_odir,material_flow_odir,inventory_odir,false_alarm_odir,kmps_odir,muf_odir,equipment_failure_odir,system_gdir,material_flow_gdir,inventory_gdir,false_alarm_gdir,kmps_gdir,muf_gdir,equipment_failure_gdir)
########################################################################
#
# (2a): read system operation input data
#
#######
def input_system_operation(process_states_dir):
#######
    os.chdir(process_states_dir) #change dir
    facility_operation=numpy.loadtxt('facility.operation.inp') #total time of facility operation; i.e., simulation time 
    process_time=numpy.loadtxt('process.operation.time.inp',usecols=[1]) #time for each vertex to process material
    storage_buffer_process_time=process_time[0]
    injection_casting_process_time=process_time[1]
    trimming_process_time=process_time[2]
    product_process_time=process_time[3]
###
    return(facility_operation,storage_buffer_process_time,injection_casting_process_time,trimming_process_time,product_process_time)
########################################################################
#
# (2b): read storage buffer input data
#
#######
def input_storage_buffer(process_states_dir):
#######
    os.chdir(process_states_dir) #change dir
    batch=numpy.loadtxt('batch.inp') #batch size
    unprocessed_storage_inventory=numpy.loadtxt('unprocessed.storage.inventory.inp') #total quantity of naterial in storage buffer at TIME=0
###
    return(batch,unprocessed_storage_inventory)
########################################################################
#
# (2c): read equipment input data
#
#######
def input_equipment(process_states_dir,failure_equipment_dir,failure_distribution_dir,equipment):
#######	
    os.chdir(process_states_dir) #change dir
    equipment_loss_fraction=numpy.loadtxt(equipment+'.loss.fraction.inp',usecols=[1]) #fraction of material left in/at/around the equipment; 1st element is the expected quantity, 2nd and 3rd are the range for the true quantity
    os.chdir(failure_equipment_dir) #change dir
    equipment_failure_type=numpy.loadtxt(equipment+'.failure.data.inp',usecols=[0],dtype=str) #type of equipment failure
    equipment_failure_rate=numpy.loadtxt(equipment+'.failure.data.inp',usecols=[1]) #corresponding equipment failure rate
    equipment_failure_maintenance_time=numpy.loadtxt(equipment+'.failure.data.inp',usecols=[2]) #time to repair each failure
    equipment_cleaning_time=numpy.loadtxt(equipment+'.failure.data.inp',usecols=[3]) #time to clean the equipment prior to equipment removal
    os.chdir(failure_distribution_dir) #change dir
    weibull_beta=numpy.loadtxt(equipment+'.weibull.beta.inp',usecols=[1]) #weibull distribution beta parameter for the melter
    weibull_eta=(1)/equipment_failure_rate #eta for weibull distribution is reciprocal of failure rate if beta = 1; assumes random failure
    equipment_failure_number=1
#    equipment_failure_number=len(int(equipment_failure_type)) #total number of possible failures, used if > 1
###
    return(equipment_loss_fraction,equipment_failure_type,equipment_failure_rate,equipment_failure_maintenance_time,equipment_cleaning_time,weibull_beta,weibull_eta,equipment_failure_number) 
########################################################################
#
# (2d): read system false alarm input data
#
#######
def input_system_false_alarm(system_false_alarm_dir,false_alarm_type):
#######
    os.chdir(system_false_alarm_dir) #change dir
    false_alarm_threshold=numpy.loadtxt(false_alarm_type+'.false.alarm.threshold.inp',usecols=[1]) #false alarm thresholds
    inspection_time=numpy.loadtxt(false_alarm_type+'.inspection.time.inp',usecols=[1]) #time elapsed for each inspection
    false_alarm_inspection_time=inspection_time #change if there are multiple false alarms per process
    false_alarm_threshold=false_alarm_threshold
###
    return(false_alarm_inspection_time,false_alarm_threshold) 
########################################################################
#
# (2e): read edge transition input data
#
#######
def input_edge_transition(edge_transition_dir):
#######
    os.chdir(edge_transition_dir) #change dir
    edge_transition=numpy.loadtxt('edge.transition.inp',usecols=[1]) #time elapsed on each edge transition
###
    return(edge_transition) 
########################################################################
#
# (2f): read kmp input data
#
#######
def input_kmps(kmps_dir):
#######
    os.chdir(kmps_dir) #change dir
    kmp_id=numpy.loadtxt('key.measurement.points.inp',usecols=[0]) #kmp identification numbers
    kmp_time=numpy.loadtxt('key.measurement.points.inp',usecols=[1]) #measurement time at each kmp
    kmp_uncertainty=numpy.loadtxt('key.measurement.points.inp',usecols=[2]) #measurement uncertainty at each kmp
    kmp_threshold=numpy.loadtxt('key.measurement.points.inp',usecols=[3]) #measurement threshold to trigger false alarms at each kmp
    maximum_kmp=len(kmp_id)
###
    return(kmp_id,kmp_time,kmp_uncertainty,kmp_threshold,maximum_kmp) 
########################################################################
#
# (3a): open system output files
#
#######
def output_system_operation(system_odir):
#######
    os.chdir(system_odir) #change dir
    system_time_output=open('facility.operation.time.out','w+')
    campaign_output=open('facility.campaign.out','w+')
###
    return(system_time_output,campaign_output)
########################################################################
#
# (3a.i): open equipment output files
#
#######
def output_process_operation(system_odir,equipment):
#######
    os.chdir(system_odir) #change dir
    failure_time_output=open(equipment+'failure.time.out','w+')
    process_counter_output=open(equipment+'.process.counter.out','w+')
###
    return(failure_time_output,process_counter_output)
########################################################################
#
# (3b): open material flow output files
#
#######
def output_material_flow(material_flow_odir):
#######
    os.chdir(material_flow_odir) #change dir
    batch_output=open('batch.out','w+')
    true_weight_output=open('true.weight.out','w+')
    expected_weight_output=open('expected.weight.out','w+')
    measured_weight_output=open('measured.weight.out','w+')
###
    return(batch_output,true_weight_output,expected_weight_output,measured_weight_output)
########################################################################
#
# (3b.i): open equipment loss output files
#
#######
def output_equipment_loss(material_flow_odir,equipment):
#######
    os.chdir(material_flow_odir) #change dir
    true_equipment_loss_output=open(equipment+'.true.loss.out','w+')
    expected_equipment_loss_output=open(equipment+'.expected.loss.out','w+')
    measured_equipment_loss_output=open(equipment+'.measured.loss.out','w+')
###
    return(true_equipment_loss_output,expected_equipment_loss_output,measured_equipment_loss_output)
########################################################################
#
# (3c): open inventory output files
#
#######
def output_inventory(inventory_odir):
#######
    os.chdir(inventory_odir) #change dir
    true_storage_inventory_output=open('true.storage.inventory.out','w+')
    expected_storage_inventory_output=open('expected.storage.inventory.out','w+')
    measured_storage_inventory_output=open('measured.storage.inventory.out','w+')
    true_processed_inventory_output=open('true.processed.inventory.out','w+')
    expected_processed_inventory_output=open('expected.processed.inventory.out','w+')
    measured_processed_inventory_output=open('measured.processed.inventory.out','w+')
    true_system_inventory_output=open('true_system.inventory.out','w+')
    expected_system_inventory_output=open('expected.system.inventory.out','w+')
    measured_system_inventory_output=open('measured.system.inventory.out','w+')
###
    return(true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output)  
########################################################################
#
# (3d): open system false alarm output files
#
#######
def output_false_alarm(false_alarm_odir,false_alarm_type):
#######
    os.chdir(false_alarm_odir) #change dir
    false_alarm_counter_output=open(false_alarm_type+'.false.alarm.counter.out','w+')
###
    return(false_alarm_counter_output)  
########################################################################
#
# (3e): open kmp output files
#
#######
def output_kmps(kmps_odir):
#######
    os.chdir(kmps_odir) #change dir
    true_kmp_output=open('true.kmp.out','w+')
    expected_kmp_output=open('expected.kmp.out','w+')
    measured_kmp_output=open('measured.kmp.out','w+')
###
    return(true_kmp_output,expected_kmp_output,measured_kmp_output)  
########################################################################
#
# (3f): open equipment failure output files
#
#######
def output_equipment_failure(equipment_failure_odir,equipment):
#######
    os.chdir(equipment_failure_odir) #change dir
    equipment_failure_total_counter_output=open(equipment+'.failure.total.counter.out','w+')
    equipment_probability_density_function_output=open(equipment+'.probability.density.function.out','w+')
    equipment_unreliability_function_output=open(equipment+'.unreliability.function.out','w+')
###
    return(equipment_failure_total_counter_output,equipment_probability_density_function_output,equipment_unreliability_function_output)  
########################################################################
#
# (3g): open muf output files
#
#######
def output_muf(muf_odir,equipment):
#######
    os.chdir(muf_odir) #change dir
    equipment_muf_output=open(equipment+'.muf.out','w+')
    equipment_mufc_output=open(equipment+'.mufc.out','w+')
###
    return(equipment_muf_output,equipment_mufc_output)  
########################################################################
#
# (4a): initialize system parameters
#
#######
def initialize_system():
#######
    operation_time=0 #simulation time
    total_campaign=1 #total campaigns processed over facility operation
###
    return(operation_time,total_campaign)
########################################################################
#
# (4b): initialize material flow parameters
#
#######
def initialize_material_flow():
#######
    total_batch=1 #total batches processed over facility operation
    true_weight=0 #true quantity processed per campaign
    expected_weight=0 #expected quantity processed per campaign
    measured_weight=0 #measured quantity processed per campaign
###
    return(total_batch,true_weight,expected_weight,measured_weight)
########################################################################
#
# (4b.i): initialize equipment process loss 
#
#######
def initialize_equipment_process_loss():
#######
    true_process_loss=0 #true quantity of heel per campaign
    expected_process_loss=0 #expected quantity of heel per campaign
    measured_process_loss=0 #measured quantity of heel per campaign
    accumulated_true_process_loss=0 #accumulated quantity of heel prior to failure; zeroed out on cleaning 
    accumulated_expected_process_loss=0 #expected quantity of heel prior to failure; zeroed out on cleaning
    accumulated_measured_process_loss=0 #measured quantity of heel prior to failure; zeroed out on cleaning 
###
    return(true_process_loss,expected_process_loss,measured_process_loss,accumulated_true_process_loss,accumulated_expected_process_loss,accumulated_measured_process_loss)
########################################################################
#
# (4c): initialize inventory parameters
#
#######
def initialize_inventory(unprocessed_storage_inventory):
#######
    true_storage_inventory=unprocessed_storage_inventory #true quantity of unprocessed material over facility operation
    expected_storage_inventory=unprocessed_storage_inventory #expected quantity of unprocessed material over facility operation
    measured_storage_inventory=unprocessed_storage_inventory #measured quantity of unprocessed material over facility operation
    true_processed_inventory=0 #true quantity of processed material over facility operation
    expected_processed_inventory=0 #expected quantity of processed material over facility operation
    measured_processed_inventory=0 #measured quantity of processed material over facility operation
    true_system_inventory=0 #true quantity of material transferred out of storage buffer over facility operation
    expected_system_inventory=0 #expected quantity of material transferred out of storage buffer over facility operation
    measured_system_inventory=0 #measured quantity of material transferred out of storage buffer over facility operation
    true_initial_inventory=0 #true inventory used for MUFc calculation
    expected_initial_inventory=0 #expected inventory used for MUFc calculation
    measured_initial_inventory=0 #measured inventory used for MUFc calculation
###
    return(true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,true_initial_inventory,expected_initial_inventory,measured_initial_inventory)
########################################################################
#
# (4d): initialize system false alarm parameters
#
#######
def initialize_false_alarm():
#######
    false_alarm_counter=0 #total false alarms due to end of campaign inspection
    false_alarm=False #false alarm flag
    false_alarm_test=0 #difference in selected material quantities compared to threshold to trigger false alarm
###
    return(false_alarm_counter,false_alarm,false_alarm_test)
########################################################################
#
# (4e): initialize equipment parameters
#
#######
def initialize_equipment():
#######
    equipment_failure_time=0 #time used to determine melter failures
    equipment_failure_counter=0 #total times the melter failed over facility operation
    equipment_failure_event=False #melter failure flag for an equipment failure
    equipment_process_counter=0 #total times the melter process was initiated over facility operation
    equipment_probability_density_function_evaluate=0 #pdf for melter failure distribution at operation_time
    equipment_probability_density_function_failure_evaluate=0 #pdf for melter failure distribution at failure_time
    equipment_unreliability_function_evaluate=0 #cdf for melter failure distribution at operation_time
    equipment_unreliability_function_failure_evaluate=0 #cdf for melter failure distribution at failure_time
    equipment_process_counter=0 #total times the process was initiated over facility operation
###
    return(equipment_failure_time,equipment_failure_counter,equipment_failure_event,equipment_process_counter,equipment_probability_density_function_evaluate,equipment_probability_density_function_failure_evaluate,equipment_unreliability_function_evaluate,equipment_unreliability_function_failure_evaluate,equipment_process_counter)
########################################################################
#
# (4f): initialize muf parameters
#
#######
def initialize_muf():
#######
    true_muf=0 #true quantity of muf over facility operation; zeroed out on cleaning; zeroed out on cleaning
    expected_muf=0 #expected quantity of muf over facility operation; zeroed out on cleaning
    measured_muf=0 #measured quantity of muf over facility operation; zeroed out on cleaning
    true_mufc=0 #true quantity of muf over facility campaign 
    expected_mufc=0 #expected quantity of muf over facility campaign; zeroed out on cleaning
    measured_mufc=0 #measured quantity of muf over facility campaign; zeroed out on cleaning
###
    return(true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc)
#########################################################################
#
# (5a): write system time 
#
#######
def write_system_time(operation_time,system_time_output):
#######
    system_time_output.write(str.format('%.4f'%operation_time)+'\n') #time data is written whenever operation time changes
###
    return(system_time_output)
########################################################################
#
# (5a.i): write equipment time 
#
#######
def write_system_time(failure_time,time_output):
#######
    time_output.write(str.format('%.4f'%failure_time)+'\n') #time data is written whenever operation time changes
###
    return(time_output)
########################################################################
#
# (5b): write campaign 
#
#######
def write_campaign(operation_time,total_campaign,campaign_output):
#######
    campaign_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%i'%total_campaign)+'\n')
###
    return(campaign_output)
########################################################################
#
# (5c): write process counter 
#
#######
def write_process_counter(operation_time,process_counter,process_counter_output):
#######
    process_counter_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%i'%process_counter)+'\n')
###
    return(process_counter_output)
########################################################################
#
# (5d): write material flow
#
#######
def write_material_flow(operation_time,total_batch,true_weight,expected_weight,measured_weight,batch_output,true_weight_output,expected_weight_output,measured_weight_output):
#######
    batch_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%i'%total_batch)+'\n') 
    true_weight_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_weight)+'\n')
    expected_weight_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_weight)+'\n')
    measured_weight_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_weight)+'\n')
###
    return(batch_output,true_weight_output,expected_weight_output,measured_weight_output)
########################################################################
#
# (5e): write process loss 
#
#######
def write_process_loss(operation_time,true_process_loss,expected_process_loss,measured_process_loss,true_process_loss_output,expected_process_loss_output,measured_process_loss_output):
#######
    true_process_loss_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_process_loss)+'\n')
    expected_process_loss_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_process_loss)+'\n')
    measured_process_loss_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_process_loss)+'\n')
###
    return(true_process_loss_output,expected_process_loss_output,measured_process_loss_output)
########################################################################
#
# (5f): write inventory 
#
#######
def write_inventory(operation_time,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_system_inventory,expected_system_inventory,measured_system_inventory,true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output):
#######
    true_storage_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_storage_inventory)+'\n') 
    expected_storage_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_storage_inventory)+'\n')
    measured_storage_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_storage_inventory)+'\n')
    true_processed_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_processed_inventory)+'\n')
    expected_processed_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_processed_inventory)+'\n')
    measured_processed_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_processed_inventory)+'\n')
    true_system_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_system_inventory)+'\n')
    expected_system_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_system_inventory)+'\n')
    measured_system_inventory_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_system_inventory)+'\n')
###
    return(true_storage_inventory_output,expected_storage_inventory_output,measured_storage_inventory_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,true_system_inventory_output,expected_system_inventory_output,measured_system_inventory_output)
########################################################################
#
# (5g): write muf 
#
#######
def write_muf(operation_time,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc,muf_output,mufc_output):
#######
    muf_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_muf)+'\t'+str.format('%.4f'%expected_muf)+'\t'+str.format('%.4f'%measured_muf)+'\n')    
    mufc_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_mufc)+'\t'+str.format('%.4f'%expected_mufc)+'\t'+str.format('%.4f'%measured_mufc)+'\n')    
###
    return(muf_output,mufc_output)
########################################################################
#
# (5h): write end of campaign false alarm 
#
#######
def write_end_of_campaign_false_alarm(operation_time,total_campaign,end_of_campaign_false_alarm_counter,end_of_campaign_false_alarm_threshold,end_of_campaign_false_alarm_test,end_of_campaign_false_alarm_counter_output):
#######
    end_of_campaign_false_alarm_counter_output.write(str.format('%i'%total_campaign)+'\t'+str.format('%i'%end_of_campaign_false_alarm_counter)+'\t'+str.format('%.4f'%end_of_campaign_false_alarm_threshold)+'\t'+str.format('%.4f'%end_of_campaign_false_alarm_test)+'\t'+str.format('%.4f'%operation_time)+'\n')
###
    return(end_of_campaign_false_alarm_counter_output)
########################################################################
#
# (5i): write equipment failure false alarm 
#
#######
def write_equipment_failure_false_alarm(operation_time,equipment_failure_time,total_campaign,equipment_failure_false_alarm_counter,equipment_failure_false_alarm_threshold,equipment_failure_false_alarm_test,equipment_failure_false_alarm_counter_output):
#######
    equipment_failure_false_alarm_counter_output.write(str.format('%i'%total_campaign)+'\t'+str.format('%i'%equipment_failure_false_alarm_counter)+'\t'+str.format('%.4f'%equipment_failure_false_alarm_threshold)+'\t'+str.format('%.4f'%equipment_failure_false_alarm_test)+'\t'+str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%equipment_failure_time)+'\n')
###
    return(equipment_failure_false_alarm_counter_output)
########################################################################
#
# (5j): write equipment failure
#
#######
def write_equipment_failure(operation_time,equipment_failure_time,total_campaign,equipment_failure_counter,equipment_process_counter,equipment_probability_density_function_evaluate,equipment_probability_density_function_failure_evaluate,equipment_unreliability_function_evaluate,equipment_unreliability_function_failure_evaluate,equipment_failure_total_counter_output,equipment_probability_density_function_output,equipment_unreliability_function_output):
#######
    equipment_failure_total_counter_output.write(str.format('%i'%total_campaign)+'\t'+str.format('%i'%equipment_process_counter)+'\t'+str.format('%i'%equipment_failure_counter)+'\t'+str.format('%.4f'%operation_time)+'\n')
    equipment_probability_density_function_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%equipment_probability_density_function_evaluate)+'\t'+str.format('%.4f'%equipment_failure_time)+'\t'+str.format('%.4f'%equipment_probability_density_function_failure_evaluate)+'\n')
    equipment_unreliability_function_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%equipment_unreliability_function_evaluate)+'\t'+str.format('%.4f'%equipment_failure_time)+'\t'+str.format('%.4f'%equipment_unreliability_function_failure_evaluate)+'\n')
###
    return(equipment_failure_total_counter_output,equipment_probability_density_function_output,equipment_unreliability_function_output)
########################################################################
#
# (5k): write kmp measurement data
#
#######
def kmp_write(operation_time,true_quantity,expected_quantity,measured_quantity,true_kmp_output,expected_kmp_output,measured_kmp_output,kmp_identifier):
#######
    true_kmp_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%true_quantity)+'\t'+str.format('%i'%kmp_identifier)+'\n')
    expected_kmp_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%expected_quantity)+'\t'+str.format('%i'%kmp_identifier)+'\n')
    measured_kmp_output.write(str.format('%.4f'%operation_time)+'\t'+str.format('%.4f'%measured_quantity)+'\t'+str.format('%i'%kmp_identifier)+'\n')
###
    return(true_kmp_output,expected_kmp_output,measured_kmp_output)
########################################################################
#
# (6a): end of campaign diagnostics
#
#######
def end_of_campaign(total_campaign,total_batch):
#######
    print 'Campaign',total_campaign,'complete','\n\n'
    total_campaign=total_campaign+1
    total_batch=total_batch+1
###
    return(total_campaign,total_batch)
########################################################################
#
# (6b): reset campaign batch weights
#
#######
def reset_batch_weight():
#######
    true_weight=0
    expected_weight=0
    measured_weight=0
###
    return(true_weight,expected_weight,measured_weight)
########################################################################
#
#
#
####### (g): trimmer
# Metal alloy is trimmed into fuel slugs
# Currently there are no failures or held up material
###
#
###
def trimmer(operation_time,delay,true_quantity,expected_quantity,trimmer_process_counter):
###
    print 'Slug trimming','\n\n'
    operation_time=operation_time+delay
    trimmer_process_counter=trimmer_process_counter+1
###
    return(operation_time,true_quantity,expected_quantity,trimmer_process_counter)
########################################################################
#
#
#
####### (h): product processing
# The final product is 'processed' with an associated delay time
# This is the final stage before the end of the campaign
###
#
###    
def product_processing(operation_time,delay,true_quantity,expected_quantity,true_processed_inventory,expected_processed_inventory):
###
    print 'Processing the final product','\n\n'
    operation_time=operation_time+delay
#
    true_processed_inventory=true_processed_inventory+true_quantity
    expected_processed_inventory=expected_processed_inventory+expected_quantity
    
###
    return(operation_time,true_processed_inventory,expected_processed_inventory)
###########################################################################
#
#
#
####### (i): mass balance
# Conducts mass balance
# This is needed after a campaign, alarm, inspection
# MUF is calculated and compared to true weight
# True weight is realistically never known
# Later on something more sophisticated will be built
###
#
###
def mass_balance(operation_time,delay,storage_inventory_start,true_storage_inventory,expected_storage_inventory,measured_storage_inventory,true_quantity,expected_quantity,measured_quantity,true_processed_inventory,expected_processed_inventory,measured_processed_inventory,true_muf,expected_muf,measured_muf,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,melter_failure_event,true_system_inventory,expected_system_inventory,measured_system_inventory):
### 
    operation_time=operation_time+delay
#
###
    true_mufc=0
    expected_mufc=0
    measured_mufc=0
    true_final_inventory=true_quantity
    expected_final_inventory=expected_quantity
    measured_final_inventory=measured_quantity
###
#
### compute MUFc
    true_mufc=abs(true_initial_inventory-true_final_inventory)
    expected_mufc=abs(expected_initial_inventory-expected_final_inventory)
    measured_mufc=abs(measured_initial_inventory-measured_final_inventory)
#
### compute system MUF
    if (melter_failure_event==False):
        true_muf=abs(true_system_inventory-true_processed_inventory)
        expected_muf=abs(expected_system_inventory-expected_processed_inventory)
        measured_muf=abs(measured_system_inventory-measured_processed_inventory)
    else:
        true_muf=abs(true_system_inventory-true_processed_inventory-true_final_inventory)
        expected_muf=abs(expected_system_inventory-expected_processed_inventory-expected_final_inventory)
        measured_muf=abs(measured_system_inventory-measured_processed_inventory-measured_final_inventory)
# end if    

    print 'Facility inspection','\n','Operation time','%.4f'%operation_time,'(d)','\n'
    print 'True storage buffer inventory','%.4f'%true_storage_inventory,'(kg)','\n','Expected storage buffer inventory','%.4f'%expected_storage_inventory,'(kg)','\n','Measured storage buffer inventory','%.4f'%measured_storage_inventory,'(kg)','\n'
    print 'True processed inventory','%.4f'%true_processed_inventory,'(kg)','\n','Expected processed inventory','%.4f'%expected_processed_inventory,'(kg)','\n','Measured processed inventory','%.4f'%measured_processed_inventory,'(kg)','\n'
    print 'True system inventory','%.4f'%true_system_inventory,'(kg)','\n','Expected system inventory','%.4f'%expected_system_inventory,'(kg)','\n','Measured system inventory','%.4f'%measured_system_inventory,'(kg)','\n'    
    print 'True campaign MUF','%.4f'%true_mufc,'(kg)','\n','Expected campaign MUF','%.4f'%expected_mufc,'(kg)','\n','Measured campaign MUF','%.4f'%measured_mufc,'(kg)','\n'
    print 'True system MUF','%.4f'%true_muf,'(kg)','\n','Expected system MUF','%.4f'%expected_muf,'(kg)','\n','Measured system MUF','%.4f'%measured_muf,'(kg)','\n'
###
    return(operation_time,true_muf,expected_muf,measured_muf,true_mufc,expected_mufc,measured_mufc)
########################################################################
#
#
#
####### (k): recycle storage
# Metal alloy is removed from the melter and moved to recycle on failure
###
#
###
def recycle_storage(operation_time,delay):
###
    print 'Material transferred to Recycle','\n\n'
    operation_time=operation_time+delay
###
    return(operation_time)
########################################################################
#
#
#
####### (m): Failure test
# Tests for a failure in equipment
# This is meant to be generalized for multiple equipment 
###
#
# failure control should be its own module
###
def failure_test(operation_time,equipment_failure_number,equipment_failure_type,equipment_failure_probability,failure_event,equipment_failure_counter,melter_process_counter):
###
#
###
# currently there is only a single general failure
# this needs to be the same to compare designs
# the failure analysis will have to be its own module later on
###
#
###
    print 'Failure test'
    print 'Number of failure types:',equipment_failure_number
    print 'Failure type:',equipment_failure_type[0]
    print 'Failure probability:','%.4f'%equipment_failure_probability[0],'\n'
###
#
###
# the old failure test just sampled from the standard normal distribution 
# if the corresponding probability range contained the prescribed frequency then a failure occurred
#
#    failure_test=0
#    lower_failure_test=0
#    upper_failure_test=0
#    lower_failure_pdf=0
#    upper_failure_pdf=0
#
#    failure_test=numpy.random.randn()    
#    lower_failure_test=failure_test-1
#    upper_failure_test=failure_test+1
#    lower_failure_pdf=scipy.stats.norm.pdf(lower_failure_test)
#    upper_failure_pdf=scipy.stats.norm.pdf(upper_failure_test)
#    print 'Test range:','%.4f'%lower_failure_test,'%.4f'%upper_failure_test
#    print 'Probability range:','%.4f'%lower_failure_pdf,'%.4f'%equipment_failure_probability[0],'%.4f'%upper_failure_pdf
#    if (lower_failure_pdf<=equipment_failure_probability[0]<=upper_failure_pdf):     
#        print 'Failure'
#        failure_event=True
#        equipment_failure_counter=equipment_failure_counter+1
#        print 'Failure #:',equipment_failure_counter,'\n\n'
#    elif (upper_failure_pdf<=equipment_failure_probability[0]<=lower_failure_pdf):
#        print 'Failure'
#        failure_event=True
#        equipment_failure_counter=equipment_failure_counter+1
#        print 'Failure #:',equipment_failure_counter,'\n\n'    
#    else:
#        print 'No failure','\n\n'
#        failure_event=False
###
#
### there is a failure every 1/equipment_failure_probability day
# this is a 'forced failure' where a failure occurs at about the same time for different designs
    print operation_time,equipment_failure_counter+1,operation_time*equipment_failure_probability[0]
###
    return(failure_event,equipment_failure_counter)
########################################################################
#
#
#
########################################################################
#
# (N): close output files
#
#######
def close_files(time_output,campaign_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_kmp0,true_kmp1,true_kmp2,true_kmp3,true_kmp4,expected_kmp0,expected_kmp1,expected_kmp2,expected_kmp3,expected_kmp4,measured_kmp0,measured_kmp1,measured_kmp2,measured_kmp3,measured_kmp4,true_heel,expected_heel,measured_heel,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output):
#######
    time_output.close()
    campaign_output.close()
    measured_storage_inventory_output.close()
    true_weight_output.close()
    expected_weight_output.close()
    measured_weight_output.close()
    true_muf_output.close()
    expected_muf_output.close()
    measured_muf_output.close()
    true_mufc_output.close()
    expected_mufc_output.close()
    measured_mufc_output.close()    
    true_processed_inventory_output.close()
    expected_processed_inventory_output.close()
    measured_processed_inventory_output.close()
    total_melter_failure_output.close()
    true_heel.close()
    expected_heel.close()
    measured_heel.close()
    measured_system_inventory_output.close()
    melter_process_counter_output.close()
    trimmer_process_counter_output.close()
###
    return(time_output,campaign_output,measured_storage_inventory_output,true_weight_output,expected_weight_output,measured_weight_output,true_muf_output,expected_muf_output,measured_muf_output,true_mufc_output,expected_mufc_output,measured_mufc_output,true_processed_inventory_output,expected_processed_inventory_output,measured_processed_inventory_output,total_melter_failure_output,true_kmp0,true_kmp1,true_kmp2,true_kmp3,true_kmp4,expected_kmp0,expected_kmp1,expected_kmp2,expected_kmp3,expected_kmp4,measured_kmp0,measured_kmp1,measured_kmp2,measured_kmp3,measured_kmp4,true_heel,expected_heel,measured_heel,measured_system_inventory_output,melter_process_counter_output,trimmer_process_counter_output)
#
########################################################################
#
#
#
#
#
#
####### (s): Melter cleaning procedure
# Cleans out the heel from the melter when there is a failure
# Sends the heel to the Recycle Storage and combines with the batch
# Heel must be measured at KMP3 if it is active
###
#
###
def melter_cleaning(operation_time,delay):
###
    print 'Melter cleaning','\n\n'
    operation_time=operation_time+delay
###
    return(operation_time)
########################################################################
#
#
#
####### (t): Maintenance
# Maintenance is performed on the equipment
# Currently this is only for the melter
###
#
###
def maintenance_melter(operation_time,delay,true_weight,expected_weight,measured_weight,accumulated_true_crucible,accumulated_expected_crucible,accumulated_measured_crucible,true_initial_inventory,expected_initial_inventory,measured_initial_inventory,true_muf,expected_muf,measured_muf):
###
    print 'Performing maintenance','\n\n'
    operation_time=operation_time+delay
#
    true_initial_inventory=true_weight+true_muf
    expected_initial_inventory=expected_weight+expected_muf
    measured_initial_inventory=measured_weight+measured_muf
#
    true_weight=true_weight+accumulated_true_crucible
    expected_weight=expected_weight+accumulated_expected_crucible
    measured_weight=measured_weight+accumulated_measured_crucible
#
    accumulated_true_crucible=0
    accumulated_expected_crucible=0
    accumulated_measured_crucible=0
###
    return(operation_time,true_weight,expected_weight,measured_weight,accumulated_true_crucible,accumulated_expected_crucible,accumulated_measured_crucible,true_initial_inventory,expected_initial_inventory,measured_initial_inventory)
########################################################################
#
# EOF
#
########################################################################
