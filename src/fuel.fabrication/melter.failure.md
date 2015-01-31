########################################################################
**R.A.Borrelli**
<br>
**@TheDoctorRAB**
########################################################################



########################################################################
**Melter failure**
<br>A weibull distribution is used to simulate a general, random melter failure.
<br>Weibull is useful when there is not a lot of data available.
<br><br>weibull distribution pdf: f(t)=(beta/eta)((t/eta)^(beta-1))exp(-(t/eta)^beta)
<br>weibull distribution cdf: F(t)=1-exp(-(t/eta)^beta)
<br><br>F(t) = unreliability function
<br>With increasing time, F(t) approaches 1, so the probability of a failure increases; i.e, the equipment wears out.
<br><br>If failures are assumed to be random, then beta=1.0.
<br>Then, eta=1/failure rate.
<ul>
<b>Two times are recorded over the system<b>
<li>operation_time is the 'real' time; i.e., the simulation ends when operation_time >= facility_operation
<li>failure_time 'shadows' operation_time; it advances with the same time lapse for the edges and vertices
<li>f(t) and F(t) are evaluated using failure_time
<li>when a failure occurs, however, failure_time is reset; i.e., failure_time = 0
<li>reset of failure_time implies that new equipment is installed with a 'new' failure distribution
<li>so a new piece of equipment installed, for example, at 0.75*facility_operation, it will not be as likely to fail, as it should not
</ul>
<ul>
<b>Procedure</b>
<li>melter process begins
<li>at halfway through the melter operation time, failure test is initiated
<li>F(t=failure_time) is computed
<li>a random number (n) between (0,1) is generated from the uniform distribution
<li>failure occurs if n < F(t)
<li>therefore, if F(t) is close to 1; i.e., later in facility operation, it is more likely n < F(t); i.e., more likely the equipment fails
<li>if there is no failure the second half of the melter operation time elapses
<li>if there is a failure, maintenance loop starts
</ul>
########################################################################
