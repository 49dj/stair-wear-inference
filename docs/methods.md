# Source mapping and transparent changes

Q8.py supplies `archard_wear`, `Material`, `Step`, `User` and `Simulation`.
Their numerical equations are retained. The original main loop accumulated three
usage scenarios on the same step; it is excluded. New demos allocate a fresh step
and explicitly seed NumPy before each independent scenario.

Q2_1.m supplies the profile
`beta((x+L)/(2L);a,b)*lambda*u + beta((x+L)/(2L);b,a)*(1-u*lambda)`,
where `u=0.95/(1.05*(1-lambda+0.95*lambda/1.05))`.
The source fits lambda in [0,1] by fminbnd on MSE for each fixed a,b pair.
`estimation.py` ports exactly that profile and objective to SciPy's bounded
`minimize_scalar`; optimiser implementations and tolerances differ.

The private source divided an observed curve by a fixed calibration number. No
measurement or fitted calibration is copied into the independent demo. Synthetic
amplitude is generated directly by the profile equation. This code is a modelling
subset associated with collaborative research; provenance is not proof that all
components correspond to the final article. No MLE or linear-regression code has
been fabricated from the publication title.
