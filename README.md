# Stair wear and usage-profile modelling

This repository contains code associated with collaborative work on mathematical
modelling of stair wear and usage patterns. Yizhe Hu is a coauthor of the associated
publication; the available code does not reliably assign individual contributions.

**Associated publication:** Mei, R., Xiang, C., and Hu, Y. (2025). *Research on Stair
Age and Usage Patterns Based on Linear Regression and Maximum Likelihood
Estimation*. 2025 International Conference on Digital Analysis and Processing,
Intelligent Computation (DAPIC).
[DOI: 10.1109/DAPIC66097.2025.00161](https://doi.org/10.1109/DAPIC66097.2025.00161).

This code release represents the supported **Archard-inspired simulation and
bounded profile-fitting subset**. The publication title is not a claim that this
release implements its full regression or maximum-likelihood analysis. The exact
mapping of competition scripts to the final publication is unconfirmed.

## Supported methods

- Retained Q8 material/step/user classes and cumulative wear update.
- Gaussian lateral foot placement, direction-dependent force centres and
  Poisson interval arrivals with peak/off-peak rates.
- Transparent Python port of Q2_1.m: two mirrored beta-profile components;
  a bounded scalar mean-square-error fit of the usage-mixture parameter.
- Independently generated profile recovery and one-day fictional wear simulation.

## Installation and example

Python 3.12. Run from the repository root:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python examples/synthetic_demo.py
```

The demo generates its own noiseless profile and fictional force/arrival scenario;
it writes `results/demo.json` and `results/mixture_fit.png`. The simulation starts
from a fresh step. These are software examples, not historical-stair measurements
or independent estimates of a real stair's age.

`src/stairwear/` separates original wear classes, simulation, the documented MATLAB
objective port and plotting. No source CSV/Excel files or publication manuscripts
are included. Example outputs are ignored by Git.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Tests check linear wear accumulation, directional force centres, input validation
and recovery of a known synthetic mixture parameter. MATLAB execution is not
claimed; the fit uses SciPy bounded scalar optimisation of the same MSE formula.

## Assumptions and limitations

**Dimensional issue preserved:** the source labels `K*F*s/H` as wear depth, but
with F in N, s in m and H in Pa it has volume dimensions. A contact-area factor
would be needed to convert it into depth. The original Gaussian force field is
also peak-scaled rather than normalised to integrate to total force. The public
code retains these equations and documents the issue; it is not a physically
validated age estimator.

`users_per_day` is stored but not used in Q8: arrivals are controlled by interval
rates. Changing interval length without rate rescaling changes expected daily
traffic. The integer up-count truncates `num_users*up_ratio`; it is not a binomial
draw. Hardcoded 500/900 N up/down force scales are retained source assumptions.

The beta function is an amplitude profile, not a probability density in lateral
coordinates: the original formula omits the 1/(2L) density Jacobian. Mixture fitting
does not identify age, hardness, wear coefficient and usage count separately.
MLE, publication regression, calibrated age uncertainty and real-data results are
not available in this compact release. [Methods](docs/methods.md),
[rights](docs/rights.md). Cite the article plus the exact software commit.

See [observed verification results](docs/verification.md) for executed checks and
their limits.
