**Input file description**
<br>
The directory tree should be the same for each subsystem so the functions can be the same.
<br>
<br>
**edge.transition.inp**
<br>
time elapsed on an edge
<br>
no state change
<br>
starting.edge.location to ending.edge.location | edge transition time [d]
<br>
<br>
**weibull.beta.inp**
<br>
failure distribution used for the injection casting equipment (beta, eta)
<br>
eta is failure rate specific to equipment
<br>
failure type | beta value
<br>
<br>
**melter.failure.data.inp**
<br>
simulate melter failure
<br>
failure type | failure rate [1/d] | time to repair [d]
<br>
<br>
**key.measurement.points.inp**
<br>
kmp activity
<br>
kmp# | measurement time [d] | measurement uncertainty | measurement threshold
<br><br>
**batch.inp**
<br>
batch size for injection casting equipment
<br>
batch size [kg]
<br><br>
**facility.operation.inp**
<br>
total operating days of the facility per year
<br>
operating time [d]
<br><br>
**melter.crucible.fraction.inp**
<br>
a random amount of material is always left in the crucible after operation
<br>
expected quantity [kg]
<br>
upper limit of true quantity [kg]
<br>
lower limit of true quantity [kg]
<br><br>
**process.operation.time**
<br>
time of operation for each vertex in the subsystem
<br>
vertex | operation time [d]
<br><br>
**unprocessed.storage.inventory.inp**
<br>
starting amount of material in the storage buffer
<br>
in the full pyroprocessing facility, this would be zero at the start of operation
<br>
unprocessed material [kg]
<br><br>
**false.alarm.threshold.inp**
<br>
threshold to trigger false alarm as part of operation
<br>
operation event | threshold
<br><br>
**inspection.time.inp**
<br>
inspection time associated with each false alarm event
<br>
operation event | inspection time [d]
