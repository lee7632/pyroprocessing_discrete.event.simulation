########################################################################
**R.A.Borrelli**
<br>
**@TheDoctorRAB** 
########################################################################



########################################################################
**Introduction**
<br>This the discrete event simulation (DES) module for the fuel fabrication system in pyroprocessing.
<br>U,TRU,Zr arrive into the system into a storage buffer.
<br>Materials are melted by injection casting to form metal rods.
<br>The metal rods are trimmed to make fuel slugs.
<br>The fuel slugs are 'processed' into a final storage bufer.
<br><br>Although a fairly simple process, it quickly becomes complicated, due to measurement events (KMPx), equipment failures, subsequent maintenance, false alarms.
<br>The code tracks inventory processed, batch weight per campaign, materials unaccounted for (MUF), along with all the above.
<br>Data, data, data.
<br><br>Operationally, the goal is to process as many campaigns within the operation time.
<br>Equipment failures would affect operational goals due to maintenance delays.
<br>Safeguardability comes in because plutonium is being processed.
<br>The MUF cannot be so large as to indicate there was a diversion. 
<br>So, optimization is needed between processing as much material as possible, but minimizing MUF and potential false alarms. 
<br><br>It is largely a matter of materials accounting and tracking operation time.
<br>Accurate materials accounting is essential to safeguardability. 
<br>It is intended that this initial code is a test run for pyroprocessing and DES.
<br>Later, this will become its own class and integrate with the other pyroprocessing systems to form the safeguardability assessment model.
########################################################################


########################################################################
**File tree**
<br>mainflow_fuel_fabrication: command and control for fuel fabrication
<br>io_functions: data initialization and writing as the simulation progresses
<br>postprocessing_plot: all of the plots
########################################################################


########################################################################
**Simulation notes**
<br>One campaign = the processing of one batch.
<br>1 time unit = 1 DAY.
<br>Mass is based on kg.
<br>Results are the number of batches processed per operational period.
<br>False alarm probability is functionally dependent on equipment falure rate.
########################################################################


########################################################################
**Vertices** 
<br>0. storage
<br>1. melter/injection casting 
<br>2. trimmer
<br>3. recycle
<br>4. product
<br>x. maintenance
<br><br>State changes only occur at these vericies. 
<br>Realistically, the true weight is unknown until it is measured (KMPs). 
<br><br>Maintence is outside of the main process loop because it is triggered on an equipment failure. 
<br>Material would not flow to maintenance realistically.
<br>The cleaning procedure is essentially embedded in the maintenance module.
<br>Cleaning is needed to remove the heel from the melter equipment.
<br>Equipment cannot be removed for maintenance unless SNM is cleaned out.
<br><br>The index for each vertex is its label in the code; i.e., process_time[1] is the time elapsed for melting.  
########################################################################


########################################################################
**System diagram**
<br>See fuel.fabrication.md for the actual diagram.
<br><br>KMP(0): storage transfer to melter
<br>KMP(1): melter to trimmer
<br>KMP(2): trimmer to final processing
<br>KMP(3): melter to recycle
<br>KMP(-3): recycle back to melter (KMP4 in output)
<br><br>The KMPs will eventually be able to be turned 'on' or 'off' for different facility configurations.
<br>Then, the model is run to quantify the safeguardability of each design proposal. 
########################################################################
