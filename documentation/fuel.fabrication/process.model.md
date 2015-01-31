########################################################################
**R.A.Borrelli**
<br>
**@TheDoctorRAB** 
########################################################################



########################################################################
**Process model**
<br>There is a time lapse for each vertex and edge...set in preprocessing.
<br>System variables are listed in the glossary.
<ol>
<b>preprocessing</b>
<li>input parameters are read in, open data files  
<li>storage_inventory_start is loaded into Storage Buffer at TIME=0
<br><br><b>start operation loop</b>
<li>batch preparation in Storage Buffer...time lapse
<li>edge transition from Storage Buffer to KMP0...time lapse
<li>batch weight measurement at KMP0 and comparison to expected weight...time lapse
<li>edge transition from KMP0 to Melter...time lapse
<br><br><li>Melter process...time lapse
<ul>
<li>failure test
</ul>
<br>if failure start maintenance loop; see failure section for more details
<br><br><li>edge transtion from Melter to KMP3...time lapse  
<li>batch weight measurement at KMP3 and comparision to expected weight...time lapse
<li>edge transition from KMP3 to Recycle Storage...time lapse
<br><br><li>conduct inspection...time lapse
<ul>
<li>calculate MUFc, MUF
<li>MUF>0, unprocessed material is in the Melter, and the Melter needs to be cleaned
<li>even if this is the first failure, there will be material left over in the equipment upon transfer to recycle
<li>false alarm test
</ul>
<br><li>conduct cleaning procedure to extract heel...time lapse
<li>edge transition of heel from Melter to KMP3...time lapse
<li>heel weight measurement at KMP3 and comparision to expected weight...time lapse
<li>edge transition of heel from KMP3 to Recycle Storage...time lapse
<li>perform Maintenance...time lapse
<br><br><li>conduct inspection...time lapse (inspection is needed to restart operation) 
<ul>
<li>calculate MUFc, MUF
<li>MUFc,MUF=0 because all unprocessed material is located in Recycle Storage
<li>false alarm test
</ul>
<br><li>edge transition from Recycle Storge of total material to KMP3...time lapse
<li>total weight measurement (batch+heel) at KMP3 and comparision to expected weight...time lapse
<li>edge transition of total material from KMP3 to Melter...time lapse
<br><br><li>Melter process...time lapse
<ul>
<li>failure test
</ul>
<br>if failure repeat loop, else continue on in the system 
<br><br><li>edge transition from Melter to KMP1...time lapse
<li> batch weight measurement at KMP1 and comparison to expected weight...time lapse
<li> edge transition from KMP1 to Trimmer...time lapse
<br><br><li>Trimmer process...time lapse
<ul>
<li>failure test
<li>currently inactive
</ul>
<br><b>Trimmer failure loop description</b>
<br><br><li>edge transition from Trimmer to KMP2...time lapse
<li>batch weight measurement at KMP2 and comparison to expected weight...time lapse
<li>edge transition from KMP2 to Product Storage Buffer...time lapse
<li>processing at Product Storage Buffer (inventory updated)...time lapse
<br><br><li>conduct end of campaign inspection...time lapse
<ul>
<li>calculate MUFc, MUF
<li>MUF>0 due to heel in the melter, no action taken 
<li>false alarm test
<li>currently no action on false alarm
</ul>
<br><li>perform record keeping for batches, campaigns processed, reset campaign-based variables
<br><br>if facility operation still active go to 2
<br><b>end operation loop</b>
<br><br><b>postprocessing</b>
<li>close data files
<li>compute false alarm probability
<li>make plots
</ol>
<br>Data is written continutally with the write_output function as the code steps through the processes, but it is not indicated here because it would clutter up the process description.
<br><br>System false alarm data is written similarly in the false_alarm_write function.
<br>End of campaign false alarm data is written separately from melter failure false alarm data.
<br>KMP data is only recorded at a KMP event with the kmp_write function.
<br>Probability density function data is also written separately.
<br>Output writing is clearly indicated in the code.
########################################################################
