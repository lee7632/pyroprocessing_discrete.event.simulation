########################################################################
# Malachi Tolman
# @tolman42
# rev.25.February.2016
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
import numpy as np

class facility_command_class:
    """
    This class represents the entire facility.  

    Initializing this object in a script starts up the entire facility, 
    which includes a large number of initializations that are derived from the input 
    files set by command and control.
    """
    def __init__(self,root_dir,subsystem):
        self.operation_time = 0
        self.total_campaign = 1
        self.log_file = open(root_dir + '/log.txt','w')
        self.root_dir = root_dir
        self.subsystem = subsystem
        self.debugger = open(root_dir + '/debugger.txt','w')

        #######
        # Begin Preprocessing
        #######
        self.log_file.write('Fuel fabrication \n\nPREPROCESSING\n')
       
        #######
        # obtain all the directories
        #######
        home_dir=open(self.root_dir+'/simulation/meta.data/home.dir.inp').read()
        directory_path_file=open(self.root_dir+'/simulation/meta.data/fuel.fabrication_simulation.dir.inp').readlines() #get directory paths
        directory_paths=directory_path_file[0].split(',') #split path data and set directories
        self.input_dir=directory_paths[0]
        self.output_dir=directory_paths[1]
        self.edge_transition_dir=directory_paths[2]
        self.failure_distribution_dir=directory_paths[3]
        self.failure_equipment_dir=directory_paths[4]
        self.kmps_dir=directory_paths[5]
        self.process_states_dir=directory_paths[6]
        self.system_false_alarm_dir=directory_paths[7]
        self.data_dir=directory_paths[8]
        self.figures_dir=directory_paths[9]
        self.system_odir=directory_paths[10]
        self.material_flow_odir=directory_paths[11]
        self.inventory_odir=directory_paths[12]
        self.false_alarm_odir=directory_paths[13]
        self.kmps_odir=directory_paths[14]
        self.muf_odir=directory_paths[15]
        self.equipment_failure_odir=directory_paths[16]
        self.system_gdir=directory_paths[17]
        self.material_flow_gdir=directory_paths[18]
        self.inventory_gdir=directory_paths[19]
        self.false_alarm_gdir=directory_paths[20]
        self.kmps_gdir=directory_paths[21]
        self.muf_gdir=directory_paths[22]
        self.equipment_failure_gdir=directory_paths[23]
       
        #######
        # read input data
        #######
        self.total_operation_time=np.loadtxt(self.process_states_dir+'/facility.operation.inp')\
                #Total time in days that the facility will run for
        self.end_of_campaign_time_delay = np.loadtxt(self.system_false_alarm_dir+'/system.inspection.time.inp',
                usecols=[1]) #Amount of time it takes to do end of campaign inspection

        #######
        # open files
        #######
        self.system_time_output=open(self.system_odir+'/facility.operation.time.out','w+')
        self.campaign_output=open(self.system_odir+'/facility.campaign.out','w+')

        #######
        # write data for TIME=Initial_Time
        #######
        self.system_time_output.write('%.4f\n'%(self.operation_time))
        self.campaign_output.write('%.4f\t%i\n'%(self.operation_time,self.total_campaign))

        ######
        # Initial parameters (used more than once) 
        ######
        self.initial_inventory = np.loadtxt(self.process_states_dir+'/unprocessed.storage.inventory.inp') \
                #Total weight of the initial inventory found in the storage buffer at the start of the process

        #######
        # Log end of Preprocess
        #######
        self.log_file.write('END PREPROCESSING \n\n\n')

    def write_to_log(self,message):
        """
        Self explanatory method.  A simple way to quickly write to the log file
        """
        self.log_file.write(message)

    def get_dir_path(self):

        return(self.input_dir,self.output_dir,self.edge_transition_dir,self.failure_distribution_dir,
                self.failure_equipment_dir,self.kmps_dir,self.process_states_dir,self.system_false_alarm_dir,
                self.data_dir,self.figures_dir,self.system_odir,self.material_flow_odir,self.inventory_odir,
                self.false_alarm_odir,self.kmps_odir,self.muf_odir,self.equipment_failure_odir,self.system_gdir,
                self.material_flow_gdir,self.inventory_gdir,self.false_alarm_gdir,self.kmps_gdir,self.muf_gdir,
                self.equipment_failure_gdir)

    def get_process_times(self):

        return(self.facility_operation,self.storage_buffer_process_time,self.injection_casting_process_time,
                self.trimming_process_time,self.product_process_time)

    def end_of_campaign(self,storage_buffer,kmp0,kmp2,product_storage):
        """
        This method brings in the relevant information from the facility components
        in order to calculate relevant values at the end of a campaign.  Such
        is outputted to the log file.
        """
        self.operation_time = self.operation_time + self.end_of_campaign_time_delay
        self.write_to_log('Facility inspection \nOperation time %.4f (d) \n\n'%(self.operation_time))
        ######
        # Calculate and output storage buffer inventory (measured comes from kmp0) 
        ######
        self.write_to_log('True storage buffer inventory %.4f (kg) \nExpected storage buffer inventory %.4f (kg) \nMeasured storage buffer inventory %.4f (kg) \n\n'\
                %(storage_buffer.inventory, storage_buffer.inventory, 
                    self.initial_inventory - kmp0.cumulative_weight))
        ######
        # Output processed inventory
        # True and expected are in product storage, measured comes from kmp2
        ######
        self.write_to_log('True processed inventory %.4f (kg) \nExpected processed inventory %.4f (kg) \nMeasured processed inventory %.4f (kg) \n\n'\
                %(product_storage.true_cumulative_inventory, 
                    product_storage.expected_cumulative_inventory, kmp2.cumulative_weight))
        ######
        # Calculate and Output system inventory 
        # True and expected system inventory is found from what left the storage buffer
        # Meausred comes from kmp0
        ######
        self.write_to_log('True system inventory %.4f (kg) \nExpected system inventory %.4f (kg) \nMeasured system inventory %.4f (kg) \n\n'\
                %(self.initial_inventory-storage_buffer.inventory, 
                    self.initial_inventory-storage_buffer.inventory,
                    kmp0.cumulative_weight))
        ######
        # Calculate and output campaign MUF
        # True and expected found from product storage and storage buffer batch size
        # Measured comes from kmp0 and 2
        ######
        self.write_to_log('True campaign MUF %.4f (kg) \nExpected campaign MUF %.4f (kg) \nMeasured campaign MUF %.4f (kg) \n\n'\
                %(storage_buffer.batch_size - product_storage.true_campaign_inventory,
                    storage_buffer.batch_size - product_storage.expected_campaign_inventory,
                    kmp0.batch_weight - kmp2.batch_weight))
        ######
        # Calculate and output total MUF thus far 
        ######
        self.write_to_log('True system MUF %.4f (kg) \nExpected system MUF %.4f (kg) \nMeasured system MUF %.4f (kg) \n\n'\
                %(self.initial_inventory - storage_buffer.inventory - product_storage.true_cumulative_inventory,
                    self.initial_inventory - storage_buffer.inventory - \
                            product_storage.expected_cumulative_inventory,
                    kmp0.cumulative_weight - kmp2.cumulative_weight))
        self.write_to_log('Campaign %i complete \n\n\n'%(self.total_campaign))
        self.total_campaign=self.total_campaign+1

    def close_files(self):
        self.log_file.close()
        self.system_time_output.close()
        self.campaign_output.close()
        self.debugger.close()

