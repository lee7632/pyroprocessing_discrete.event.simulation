########################################################################
# Malachi Tolman
# @tolman42
# rev.27.February.2016
########################################################################
#
# See class description
#
########################################################################
#
# Imports
#
import pdb
import numpy as np
from storage_unit_module import storage_unit_class
from edge_transition_module import edge_transition_class
from fuel_fabricator_module import fuel_fabricator_class
from final_storage_unit_module import final_storage_unit_class


class facility_command_class:
    """
    This class represents the entire facility.  

    Aside from keeping the variables pertinent to the entire facility, this class contains methods that its
    constituent parts can call upon (the branches can "talk up" to the root). For the most part, all of
    the facility operations are self contained in here.

    Initializing this object in a script starts up the entire facility, 
    which includes a large number of initializations that are derived from the input 
    files set by command and control.

    #######
    # Variables 
    #######
    operation_time = current amount of time in days that have passed.  Each method increments this by some
    amount

    total_campaign = essentially the number of batches that have been processed.  Each time a batch goes through
    the entire fuel fabrication process, this number gets incremented.

    expected_muf = used during inspections to determine how much muf (materials unaccounted for) resides
    in the facility aside from the storage units.

    measured_muf = used during inspections to determine how much muf resides in the facility as calculated
    by the deficit in what the storage units have measured coming in and out.

    log_file = file where every important activity gets written to.  This is the main file used to determine
    how operations occurred after the program is run.

    root_dir = directory specified in command and control where the log file gets written to.  Also this is
    where the simulation directory should be found considering that all input data is pulled from such

    subsystem = subsystem of the entire facility as specified by command and control.  For now, this can only
    be fuel fabrication.

    debugger = optional file available to write debugging statements to.

    total_operation_time = total amount of time in days that the facility will run for.  Once operation time
    has reached this number, the program will stop.

    end_of_campaign_time_delay = amount of time it takes to conduct inspections at the end of each campaign.

    end_of_campaign_alarm_threshold = weight of SNM in kg that will trigger the alarm.  This number is
    compared to the difference between expected and measured weight.  If the absolute value of such is greater
    than this, an alarm is triggered where the facility shuts down and conducts an inspection to verify the
    location of the SNM.

    facility_inspection_time = amount of time in days it takes to inspect the entire facility when an alarm
    is triggered.

    system_time_ouput = output file where just the operation time is written to.  Used for plotting.

    campaign_output = same as above only for the campaign number

    initial_inventory = total amont of SNM used at the beginning.  This number is important for calculating
    the muf.

    storage_unit = module that contains the storage buffer and one kmp (key measurement point).

    fuel_fabricator = module that does most of the work.  Contains the melter, trimmer, recycle storage, and
    two kmps.

    final_storage_unit = module that holds the finished product.  Contains the product storage and one kmp.
    """
    def __init__(self,root_dir,subsystem):
        """
        Although large, all this part does is read in the number of input files required to start up the
        facility.  A lot of these directories aren't used here, but are used in the initialization of 
        the components modules.
        """
        self.operation_time = 0
        self.total_campaign = 1
        self.expected_muf = 0
        self.measured_muf = 0
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
        self.end_of_campaign_alarm_threshold = np.loadtxt(self.system_false_alarm_dir+'/eoc.alarm.threshold.inp')
        self.facility_inspection_time = np.loadtxt(self.system_false_alarm_dir+'/facility.inspection.time.inp')

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
        # Initialize facility components 
        #######
        self.storage_unit = storage_unit_class(self)
        self.edge = edge_transition_class(self,0)
        self.fuel_fabricator = fuel_fabricator_class(self)
        self.final_storage_unit = final_storage_unit_class(self)

        #######
        # Log end of Preprocess
        #######
        self.log_file.write('END PREPROCESSING \n\n\n')

    def process_batch(self):
        """
        Method that processes the batch.  This acts as a liason between the component modules that
        do all the leg work.
        """
        batch = self.storage_unit.batch_preparation(self)
        self.edge.edge_transition(self, batch, self.storage_unit.kmp, self.fuel_fabricator.melter)
        self.fuel_fabricator.process_batch(self,batch)
        self.edge.edge_transition(self, batch, self.fuel_fabricator.trimmer, self.final_storage_unit.kmp)
        self.final_storage_unit.process_batch(self,batch)

    def write_to_log(self,message):
        """
        Self explanatory method.  A simple way to quickly write to the log file
        """
        self.log_file.write(message)

    def inspect(self):
        """
        Method that gets called whenever an alarm is set off.  Each components is inspected by personnel
        to verify exactly how much SNM is in each part.  The expected and measured weight of the storage units
        get updated to more accurately describe what they actually contain.
        """
        self.operation_time = self.operation_time + self.facility_inspection_time
        self.storage_unit.inspect(self)
        self.fuel_fabricator.inspect(self)
        self.final_storage_unit.inspect(self)

    def update_accountability(self):
        """
        Method that makes each child unit update their known inventory of expected weight and measured weight
        from their own children units.
        """
        self.storage_unit.update_accountability()
        self.fuel_fabricator.update_accountability()
        self.final_storage_unit.update_accountability()

    def account(self, batch=None, kmp=None):
        """
        Here the facility accounts for all materials.  It returns a true boolean if a weight discrepancy
        is found.

        Normally this routine simply inspects the materials found in the storage units.  But if a kmp is passed
        in, then it will also include the measured weights found there.

        #######
        # Return 
        #######
        True = discrepancy has been found and an inspection should occu.

        False = no discrepancy detected, thus the facility can continue to run as normal
        """
        #######
        # Reassignments for coding convenience 
        #######
        storage_unit = self.storage_unit
        fuel_fabricator = self.fuel_fabricator
        final_storage_unit = self.final_storage_unit

        #######
        #  Calculate MUF and account for materials
        #######
        self.update_accountability()
        if kmp == None:
            self.calculate_muf()

            self.write_to_log('--Accounting materials in facility--\n\n')
            self.write_to_log('First Storage Unit:\nTrue inventory - ' + \
                    '%.4f (kg)\nExpected inventory - %.4f (kg)\nMeasured inventory - %.4f (kg)\n\n' \
                    %(storage_unit.storage_buffer.inventory, storage_unit.expected_weight.total_weight,
                        storage_unit.measured_inventory))
            self.write_to_log('Last Storage Unit:\nTrue inventory - ' + \
                    '%.4f (kg)\nExpected inventory - %.4f (kg)\nMeasured inventory - %.4f (kg)\n\n' \
                    %(final_storage_unit.product_storage.inventory, final_storage_unit.expected_weight.total_weight,
                        final_storage_unit.measured_inventory))
            self.write_to_log('Recycle Storage:\nTrue inventory - ' + \
                    '%.4f (kg)\nExpected inventory - %.4f (kg)\nMeasured inventory - %.4f (kg)\n\n' \
                    %(fuel_fabricator.recycle_storage.inventory, 
                        fuel_fabricator.recycle_storage.expected_weight.total_weight,
                        fuel_fabricator.recycle_storage.measured_inventory))
            self.write_to_log('MUF:\n' + \
                    'True weight - %.4f (kg)\nExpected weight - %.4f (kg)\nMeasured weight - %.4f (kg)\n\n\n' \
                    %(fuel_fabricator.melter.heel.weight, self.expected_muf, self.measured_muf))
            return abs(self.expected_muf - self.measured_muf) > self.end_of_campaign_alarm_threshold

        else:
            self.calculate_muf(kmp = kmp)

            self.write_to_log('--Accounting materials in facility (including where the batch is)--\n\n')
            self.write_to_log('First Storage Unit:\nTrue inventory - ' + \
                    '%.4f (kg)\nExpected inventory - %.4f (kg)\nMeasured inventory - %.4f (kg)\n\n' \
                    %(storage_unit.storage_buffer.inventory, storage_unit.expected_weight.total_weight,
                        storage_unit.measured_inventory))
            self.write_to_log('Last Storage Unit:\nTrue inventory - ' + \
                    '%.4f (kg)\nExpected inventory - %.4f (kg)\nMeasured inventory - %.4f (kg)\n\n' \
                    %(final_storage_unit.product_storage.inventory, final_storage_unit.expected_weight.total_weight,
                        final_storage_unit.measured_inventory))
            self.write_to_log('Recycle Storage:\nTrue inventory - ' + \
                    '%.4f (kg)\nExpected inventory - %.4f (kg)\nMeasured inventory - %.4f (kg)\n\n' \
                    %(fuel_fabricator.recycle_storage.inventory, 
                        fuel_fabricator.recycle_storage.expected_weight.total_weight,
                        fuel_fabricator.recycle_storage.measured_inventory))
            self.write_to_log('%s:\nTrue inventory - '%(kmp.description) + \
                    '%.4f (kg)\nExpected inventory - %.4f (kg)\nMeasured inventory - %.4f (kg)\n\n' \
                    %(batch.weight, kmp.expected_weight.batch_weight, kmp.measured_weight))
            self.write_to_log('MUF:\n' + \
                    'True weight - %.4f (kg)\nExpected weight - %.4f (kg)\nMeasured weight - %.4f (kg)\n\n\n' \
                    %(fuel_fabricator.melter.heel.weight, self.expected_muf, self.measured_muf))
            return abs(self.expected_muf - self.measured_muf) > self.end_of_campaign_alarm_threshold
   

    def end_of_campaign(self):
        """
        This method brings in the relevant information from the facility components
        in order to calculate relevant values at the end of a campaign.  Such
        is outputted to the log file.
        """
        #######
        # Account for inspection time and begin logging 
        #######
        self.operation_time = self.operation_time + self.end_of_campaign_time_delay
        self.write_to_log('Facility inspection \nOperation time %.4f (d) \n\n\n'%(self.operation_time))

        if self.account():
            self.write_to_log('\nMISSING SNM DETECTED AT END OF CAMPAIGN %i!'%(self.total_campaign) + \
                    'CONDUCT INSPECTION IMMEDIATELY!\n\n\n') 
            self.inspect()
            if self.account():
                self.write_to_log('\n\n\nWARNING! DIVERSION DETECTED! STOP OPERATION IMMEDIATELY!!\n\n\n\n')

        self.write_to_log('Campaign %i complete \n\n\n'%(self.total_campaign))
        self.total_campaign=self.total_campaign+1

    def calculate_muf(self, kmp=None):
        """
        Since the MUF (materials unaccounted for) is used in multiple instances, this routine calculates the
        expected and measured muf based off of the expected and measured values at the storage units.

        If an alarm at a kmp was set off, then it and the batch it holds needs to be passed in as well.
        """
        #######
        # Reassignment for coding convenience 
        #######
        storage_unit = self.storage_unit
        fuel_fabricator = self.fuel_fabricator
        final_storage_unit = self.final_storage_unit
        
        if kmp == None:
            self.expected_muf = storage_unit.initial_inventory - storage_unit.expected_weight.total_weight - \
                    fuel_fabricator.recycle_storage.expected_weight.total_weight - \
                    final_storage_unit.expected_weight.total_weight 
            self.measured_muf = storage_unit.initial_inventory - storage_unit.measured_inventory - \
                    fuel_fabricator.recycle_storage.measured_inventory - final_storage_unit.measured_inventory

        else:
            self.expected_muf = storage_unit.initial_inventory - storage_unit.expected_weight.total_weight - \
                    fuel_fabricator.recycle_storage.expected_weight.total_weight - \
                    final_storage_unit.expected_weight.total_weight - kmp.expected_weight.batch_weight
            self.measured_muf = storage_unit.initial_inventory - storage_unit.measured_inventory - \
                    fuel_fabricator.recycle_storage.measured_inventory - final_storage_unit.measured_inventory - \
                    kmp.measured_weight

    def kmp_alarm(self, batch, kmp):
        """
        When a kmp discovers a discrepancy between the expected and measured weight, this routine is called.

        The kmp gets inspected as the storage units normally do by personnel.  This updates the expected
        and measured weight to be more accurate.  Than an entire facility inspection is conducted to ensure
        that no SNM is actually missing.
        """
        self.inspect()
        #######
        # "Inspect" the kmp to get correct measured and expected weight 
        #######
        self.write_to_log('\nInspecting %s: \n'%(kmp.description) + \
                'Expected weight was %.4f \nMeasured weight was %.4f \n'%(kmp.expected_weight.batch_weight, 
                    kmp.measured_weight))
        kmp.expected_weight.batch_weight = batch.weight
        kmp.measured_weight = batch.weight
        self.write_to_log('\nExpected weight now is %.4f \nMeasured weight now is %.4f\n\n'\
                %(kmp.expected_weight.batch_weight, kmp.measured_weight))
        if self.account(batch = batch, kmp = kmp):
            '\n\n\nWARNING! DIVERSION DETECTED! STOP ALL OPERATIONS IMMEDIATELY!\n\n\n\n'

    def close_files(self):
        """
        Close the files used for logging events and data output.
        """
        self.log_file.close()
        self.system_time_output.close()
        self.campaign_output.close()
        self.debugger.close()

