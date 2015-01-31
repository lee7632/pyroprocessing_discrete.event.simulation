########################################################################
**R.A.Borrelli**
<br>
**@TheDoctorRAB**
########################################################################



########################################################################
**MUF (system) and MUFc (campaign)**
<br>
<ul>
<b>MUF is calculated</b>
<li>end of campaign
<li>on failure after moving bulk material to recycle storage
<li>after maintenance to verify all material is accounted for  
</ul>
At the end of the campaign, MUF is calculated, but no further action is taken because it is 'known' that MUF is in the melter.
<br>This will not be the case once diversion is introduced into the model, since it would not be known if the MUF was in the melter or diverted. 
<br>MUF is calculated based on initial and final inventories.
<br>The inventories are determined by the state variables and location of material in the system.
<br>MUF and MUFc are independently calculated in order to verify both.
<ul>
<b>Once through campaign (no failure)</b>
<li>MUFc = KMP0 - KMP2
<li>KMP0 records inventory transferred from storage buffer
<li>KMP2 records product processed
<li>MUF = system inventory - processed inventory
<li>system inventory is running total transferred out of the storage buffer from KMP0
<li>processed inventory is running total from KMP2
</ul>
<ul>
<b>Failure</b>
<li>MUFc = KMP3 - KMP0
<li>KMP3 records material transferred out of melter to recycle storage
<li>MUF = system inventory - (processed inventory + KMP3)
<li>processed inventory is from prior campaign if the failure occurs
</ul>
After the failure inspection, the melter is cleaned, the heel is removed, also measured at KMP3, and transferred to recycle storage.
<ol>
<b>Note that KMP3 is needed twice</b>
<li>measures batch from meleter
<li>measures heel from melter; i.e., equipment cleaning.
</ol>
Therefore, all intracampaign material is in recycle storage at this point.
<br>The heel is the amount of material that accumulates in the melter (crucible), randomly during each melting event.
<br>Maintenance is conducted.
<ul>
<b>Restart inspection is needed upon completion of maintenance
<br>Confirm all the material is in the recycle storage and MUF = 0</b>
<li>MUFc = (KMP3(batch)+MUF)-(KMP3(batch)+KMP3(heel))
<li>verifies that previous system MUF is equal to heel
<li>use of KMP0 would not be correct here because KMP0 will always measure the the batch input quantity per campaign
<li>if failure occurs for campaign > 1, MUF in the melter is left from prior campaigns
<li>system MUF is then needed in MUFc calculation here for material from the prior campaignand based on overall material throughput
<li>(KMP3(batch)+KMP3(heel)) is total unprocessed material for the current campaign
<li>MUFc = 0 because all intracampaign material is accounted for and located in recycle storage
<li>MUF = system inventory-(processed inventory+(KMP3(batch)+KMP3(heel))
<li>system MUF = 0 
<li>processed and intracampaign material equals material input into the system over current facility time
</ul>
########################################################################
