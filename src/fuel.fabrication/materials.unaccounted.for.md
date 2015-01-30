########################################################################
**R.A.Borrelli**
<br>
**@TheDoctorRAB**
########################################################################



########################################################################
**MUF (system) and MUFc (campaign)**
<br>MUF is calculated:
   . end of campaign
   . on failure after moving bulk material to recycle storage
   . after maintenance to verify all material is accounted for  
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
