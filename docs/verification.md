# Verification, 7 October 2026

Tested with Python 3.12.10 on Windows; direct dependency versions are pinned in
`requirements.txt`. Editable package installation and `pip check` passed.

- `python -m pytest -q`: 3 tests passed.
- `python examples/synthetic_demo.py`: completed. Known noiseless mixture lambda
  0.35; estimate 0.3500000002921984; MSE about 2.38e-19.
- A fresh one-day fictional step simulation returned finite wear-grid values.

These checks establish equation/software consistency only. The preserved wear
quantity has the dimensional and force-normalisation limitations in the README;
the example does not validate physical depth or infer a historical stair's age.
MATLAB execution and full publication regression/MLE were not verified.

`CITATION.cff` passed validation against the official CFF 1.2 schema.
