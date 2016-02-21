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
    """This class represents the entire facility.  

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
        # open files
        #######
        self.system_time_output=open(self.system_odir+'/facility.operation.time.out','w+')
        self.campaign_output=open(self.system_odir+'/facility.campaign.out','w+')

        #######
        # write data for TIME=Initial_Time
        #######
        self.system_time_output.write('%.4f\n'%(self.operation_time))
        self.campaign_output.write('%.4f\t%i\n'%(self.operation_time,self.total_campaign))

    def get_dir_path(self):

        return(self.input_dir,self.output_dir,self.edge_transition_dir,self.failure_distribution_dir,self.failure_equipment_dir,self.kmps_dir,self.process_states_dir,self.system_false_alarm_dir,self.data_dir,self.figures_dir,self.system_odir,self.material_flow_odir,self.inventory_odir,self.false_alarm_odir,self.kmps_odir,self.muf_odir,self.equipment_failure_odir,self.system_gdir,self.material_flow_gdir,self.inventory_gdir,self.false_alarm_gdir,self.kmps_gdir,self.muf_gdir,self.equipment_failure_gdir)

    def end_of_campaign(self):
        self.log_file.write('Campaign %i complete \n\n'%(self.total_campaign))
        self.total_campaign=self.total_campaign+1

    def close_files(self):
        self.log_file.close()
        self.system_time_output.close()
        self.campaign_output.close()

