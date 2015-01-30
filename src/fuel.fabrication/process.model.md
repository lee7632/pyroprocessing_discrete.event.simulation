########################################################################
**R.A.Borrelli**
**@TheDoctorRAB* 
########################################################################



########################################################################
**Process model**
<br>There is a time lapse for each vertex and edge...set in preprocessing.
<br> System variables are listed in the glossary.
<br><br>**preprocessing**
<br> 0.    input parameters are read in, open data files  
<br> 1.    storage_inventory_start is loaded into Storage Buffer at TIME=0
<br><br>**start operation loop**
<br>2.	batch preparation in Storage Buffer...time lapse
<br>3.  edge transition from Storage Buffer to KMP0...time lapse
<br>4.  batch weight measurement at KMP0 and comparison to expected weight...time lapse
<br>5.	edge transition from KMP0 to Melter...time lapse
<br><br>6.  Melter process...time lapse
<br>		. failure test
<br><br>if failure start maintenance loop; see failure section for more details
<br>7.  edge transtion from Melter to KMP3...time lapse  
<br>8.  batch weight measurement at KMP3 and comparision to expected weight...time lapse
<br>9.  edge transition from KMP3 to Recycle Storage...time lapse
<br><br>10. conduct inspection...time lapse
<br>		. calculate MUFc, MUF
<br>		. MUF>0, unprocessed material is in the Melter, and the Melter needs to be cleaned
<br>		. even if this is the first failure, there will be material left over in the equipment upon transfer to recycle
<br>		. false alarm test
<br><br>11. conduct cleaning procedure to extract heel...time lapse
<br>12.	edge transition of heel from Melter to KMP3...time lapse
<br>13. heel weight measurement at KMP3 and comparision to expected weight...time lapse
<br>13. edge transition of heel from KMP3 to Recycle Storage...time lapse
<br><br>14. perform Maintenance...time lapse
<br><br>15. conduct inspection...time lapse (inspection is needed to restart operation) 
<br>		. calculate MUFc, MUF
<br>		. MUFc,MUF=0 because all unprocessed material is located in Recycle Storage
<br>		. false alarm test
<br><br> 16. edge transition from Recycle Storge of total material to KMP3...time lapse
<br>17. total weight measurement (batch+heel) at KMP3 and comparision to expected weight...time lapse
<br>18. edge transition of total material from KMP3 to Melter...time lapse
<br>19. Melter process...time lapse
<br>		. failure test
<br><br>if failure repeat loop, else continue on in the system 
<br>20. edge transition from Melter to KMP1...time lapse
<br>21. batch weight measurement at KMP1 and comparison to expected weight...time lapse
<br>22. edge transition from KMP1 to Trimmer...time lapse
<br><br>23. Trimmer process...time lapse
<br>		. failure test
<br>		. currently inactive
<br><br> Trimmer failure loop description
<br><br>24. edge transition from Trimmer to KMP2...time lapse
<br>25. batch weight measurement at KMP2 and comparison to expected weight...time lapse
<br>26. edge transition from KMP2 to Product Storage Buffer...time lapse
<br>27. processing at Product Storage Buffer (inventory updated)...time lapse
<br><br>28. conduct end of campaign inspection...time lapse
<br>		. calculate MUFc, MUF
<br>		. MUF>0 due to heel in the melter, no action taken 
<br>		. false alarm test
<br>		. currently no action on false alarm
<br><br>29. perform record keeping for batches, campaigns processed, reset campaign-based variables
<br><br>if facility operation still active go to 2
<br><br>**postprocessing**
<br>30. close data files
<br>31. compute false alarm probability
<br>32. make plots
<br><br>Data is written continutally with the write_output function as the code steps through the processes, but it is not indicated here because it would clutter up the process description.
<br><br>System false alarm data is written similarly in the false_alarm_write function.
<br>End of campaign false alarm data is written separately from melter failure false alarm data.
<br>KMP data is only recorded at a KMP event with the kmp_write function.
<br>Probability density function data is also written separately.
<br>Output writing is clearly indicated in the code.
########################################################################