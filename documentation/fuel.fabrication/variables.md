########################################################################
**R.A.Borrelli**
<br>
**@TheDoctorRAB**
########################################################################



########################################################################
**Equipment is a subset of process.**
<br>
**Processes are assembled into the system.**
<br>
**System > Processes > Equipment**
<br><br>
**Process variables**
<br>Variables are listed in alphabetical order because there are so many.
<br>A dummy variable means ones that are called in the function; i.e., multi-use.
<br>Variable list is for all files for the fuel fabrication model.
<br><br>true=actual material flow...unknown realistically
<br>expected=material flow...based on prior data cohorts realistically...set in preprocessing 
<br>measured=material flow...recorded at each KMP
<br><br>**Postprocessing variable notes**
<br>Variables in postprocessing are largely for making plots and not listed here.
<br>They are xmin,ymin,title, etc., and should be self-explanatory.
<br>There are a few dummy variables because the plot functions are resused several times.
<br>This all should be straighforward to a knowledgable coder.
<br><br>
<ul>
<b>A</b>
<li>accumulated_true_heel=true material accumulated in crucible
<li>accumulated_expected_heel=expected material accumulated in crucible
<li>accumulated_measured_heel=measured material accumulated in crucible
<li>alarm_test=dummy for false alarm testing
</ul>
<ul>
<b>B</b>
</ul>
<ul>
<b>C</b>
<li>crucible_fraction=expected_crucible,limits to true_crucible...set in preprocessing
</ul>
<ul>
<b>D</b>
<li>delay=dummy variable used in the functions for the time delays...all set in preprocessing
<li>_dir= any directory location...should be self explanatory (*o=output,*g=figures)
<li>directory_path_file=contains the directory paths for input and output...always in meta.data
</ul>
<ul>
<b>E</b>
<li>end_of_campaign_inspection_time=end of campaign inspection time
<li>edge_transition=transfer times along each edge...see system diagram...set in preprocessing
<li>equipment_=dummy variable for various equipment modules
<li>expected_initial/final_inventory=dummy variable used for MUFc calculation 
<li>expected_quantity=dummy variable for KMP measurement, false alarm test
<li>expected_kmpX=data file stores measured quantities at each KMP
<li>expected_system_inventory=running total of mass transfer from storage
<li>expected_storage_inventory=total expected mass in storage buffer
<li>expected_heel=expected material left in the crucible
<li>expected_weight=expected weight processed per campaign
<li>expected_crucible_fraction=expected fraction of material left in the crucible...set in preprocessing  
<li>expected_processed_inventory=total expected mass processed
<li>_expected_muf=total expected facility material unaccounted for per subsystem/equipment
<li>_expected_mufc=expected muf per campaign per subsystem/equipment
<li>_equipment_time=time elapsed at each equipment/vertex (not maintenance)...set in preprocessing
<li>equipment_failure_total_counter=total number of equipment failures over operation time
<li>equipment_failure_event=boolean to indicate a equipment failure occurred
<li>equipment_failure_number=number of failures that could occur in the equipment
<li>equipment_cleaning_time=time delay for the equipment to be cleaned...set in preprocessing
<li>equipment_failure_probability=associated probability for each equipment failure...set in preprocessing
<li>equipment_failure_maintenance_time=time for maintenance for each failure...set in preprocessing
<li>equipment_failure_false_alarm_threshold=threshold to trigger false alarm due to equipment failure...compared to alarm test...set in preprocessing 
<li>equipment_failure_inspection_time=equipment failure inspection time
<li>equipment_failure_type=type of equipment failure...set in preprocessing
<li>equipment_initiation_counter=counts the number of times the equipment is initiated
<li>equipment_failure_campaign_counter=total equipment failure per campaign
<li>_evaluate=function evaluate for whatever precedes _evaluate; also for dummy variables
</ul>
<ul>
<b>F</b>
<li>facility_operation=total number of days per year of facility operation...set in preprocessing 
<li>failure_event=dummy variable boolean to indicate a failure occurred
<li>failure_inspection_time=time to inspect due to failure
<li>_false_alarm_threshold=threshold to trigger false alarm...compared to alarm_test...set in preprocessing 
<li>_false_alarm_counter=counts false alarms 
<li>_false_alarm_threshold=threshold to trigger false alarms..not at KMPs...set in preprocessing
<li>_false_alarm=boolean to activate alarm
<li>_false_alarm_counter=counts total false alarms over facility_operation
<li>_false_alarm_attempt=number of total false alarm attempts
<li>_false_alarm_trigger=actual false alarm
<li>_false_alarm_error_probability=Type I error=false alarm probability
<li>false_alarm_identifier=dummy to indicate whether to use system false alarm or kmp false alarm
<li> _false_alarm_filename=name of file to output
<li>_false_alarm_test=difference in selected material quantities...compared to threshold to trigger false alarm
<li>_failure_time=time record to determine equipment failure; if there is a failure, failure_time resets to 0; i.e., there is a new probability distribution
<li>file_=part of the file names for saving, opening, writing, etc.; i.e., file_tree is directory structure
<li>filename=same thing
<li>_fines=process losses from trimming; i.e., muf
</ul>
<ul> 
<b>G</b>
<li>_graph=data files needed for plots
</ul>
<ul>
<b>H</b>
</ul>
<ul>
<b>I</b>
<li>inspection_time=dummy variable for time to inspect for end of campaign or failure...set in preprocessing
<li>inspection_time=contains all the inspection times...set in preprocessing
<li>injection_casting_time=injecting casting normal operation time
</ul>
<ul>     
<b>J</b>
</ul>
<ul>
<b>K</b>
<li>kmp_id=reads in the number of KMPs in the input file to determine maximum KMPs for the facility design...contains all kmp input data
<li>kmp_time=time at each kmp to conduct a measurement...set in preprocessing
<li>kmp_identifier=dummy variable for identifying the KMP location
<li>kmp_threshold=threshold at each KMP determining false alarm...set in preprocessing
<li>kmp_uncertainty=uncertainty at KMP...set in preprocessing...used as...true_quantity +/- N(0,measurement_uncertainty)
</ul>
<ul>
<b>L</b>
</ul>
<ul>
<b>M</b>
<li>maximum_kmp=maximum number of KMPs based on total processes
<li>material_quantity=dummy variable for writing data at a KMP
<li>measured_initial/final_inventory=dummy variable used for mufc 
<li>measured_quantity=dummy variable for KMP measurement, false alarm test
<li>measured_kmpX=stores quantities at each KMP
<li>measured_weight=measured weight of material at KMPx
<li>measured_heel=measured material left in the crucible
<li>measured_storage_inventory=total measured mass in storage buffer...at KMP0 
<li>measured_system_inventory=running total of mass transfer from storage
<li>measured_processed_inventory=total measured mass processed
<li>_measured_muf=total measured facility material unaccounted for per subsystem/equipment
<li>_measured_mufc=muf for specific campaign per subsystem/equipment
</ul> 
<ul>
<b>N</b>
</ul>
<ul>
<b>O</b>
<li>_output is for output data files...there are a lot of them
<li>operation_time=operation time of the facility 0<T<facility_operation...set in preprocessing
<li>_equipment_time=vertex operation times...set in preprocessing
</ul>
<ul>
<b>P</b>
<li>plot=data files needed to make plots
</ul>
<ul>
<b>Q</b>
</ul>
<ul>
<b>R</b>
</ul>
<ul>
<b>S</b>
<li>storage_inventory=current inventory in the storage buffer at time=T...eventually this will change with time with arrival of material
<li>slug_trimming_time=slug trimming normal operation time
</ul>
<ul>
<b>T</b>
<li>threshold=dummy variable for measurement threshold (for alarms)
<li>total_failure=dummy variable for counting failures
<li>total_campaign=total campaigns processed over facility_operation
<li>total_batch=total batches processed facility_operation
<li>true_quantity=dummy variable for KMP measurement, false alarm test
<li>true_kmpX=stores quantities at each KMP
<li>true_storage_inventory=total mass in storage buffer
<li>true_heel=true material left in the crucible per campaign
<li>true_weight=true weight of material transferred through the system
<li>true_crucible_fraction=quantity of material left in the crucible...randomized per melting process 
<li>true_system_inventory=running total of mass transfer from storage
<li>true_processed_inventory=total mass processed 
<li>_true_muf=total material unaccounted for per subsystem/equipment
<li>_true_mufc=muf for specific campaign per subsystem/equipment
<li>true_initial/final_inventory=dummy variable used for mufc 
<li>time_domain=dummy for time variable
<li>time_delay=dummy for time variable
<li>total_batch=batch size to be processed...set in preprocessing
</ul>
<ul>
<b>U</b>
<li>uncertainty=dummy variable for measurement uncertainty
<li>unprocessed_storage_inventory=total amount of material in the storage buffer...currently fixed amount...to be material arrival vertex
</ul>
<ul>
<b>V</b>
</ul>
<ul>
<b>W</b>
<li>weibull_beta_melter=beta parameter for the weibull distribution for failure testing
<li>weibull_eta_melter=eta parameter for the weibull distribution for failure testing
<li>weibull_beta=dummy variable
<li>weibull_eta=dummy variable
</ul>
<ul>
<b>X</b>
</ul>
<ul>
<b>Y</b>
</ul>
<ul>
<b>Z</b>
</ul>
########################################################################
