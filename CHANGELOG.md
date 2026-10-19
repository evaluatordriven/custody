# Changelog

Each release is a git tag, and each carries its own custody record in `record/`. Before 1.0.0 any release
may turn a record that read `OK` into one that reads `FAILED` (SPEC.md section 8); every such change is
listed here under **Breaking**.

## 0.9.3 (candidate)

**Added**
- A plain-language guide for reviewers (`docs/REVIEWERS-GUIDE.md`) and a glossary of every word the
  specification uses (`docs/GLOSSARY.md`), with a reading check in CI (`tools/readability.py`).
- `tools/explain.py`, which prints any record in plain words with the checker's answer.
- Routing `acknowledged`: some checks were unobserved and a given disposition names them all.
- A control may name the `dimension` it tests.
- `CHANGELOG.md`, `SECURITY.md` and `GOVERNANCE.md`.

**Breaking**
- CL1-6: `sameModelAsMaker` must be declared exactly when the evaluator's model is the maker's.
- CL1-9: a control whose outcome differs from its expected outcome voids its reader's observations in
  that batch (or in that dimension, if the control names one); those checks must read `unobserved`.
- CL1-11: if the maker approved the bar as buyer or specialist, a separation gap names the maker.
- CL1-14: the bar file is checked against `bar.digest`; without it, CL1-14 reads `NOT-CHECKABLE`.
- CL2-3: no buyer or specialist approval is by the maker; and for each dimension, evaluators from the
  maker's model family are no more than half of its readers.

**Fixed**
- The checker no longer applies CL1-15 to a baseline claim (SPEC.md: CL1-2 to CL1-14).
- `count.py` checks the license files themselves, not only the documents that name them.

## 0.9.2

**Added** an append-only, hash-chained custody log (`tools/record.py`) and building a record from it;
same-model sessions declared at CL1; "published" defined; the screening test's record.

**Breaking**
- CL1-6: a model evaluator that is a session of the maker's own model must declare `sameModelAsMaker`.

**Changed**
- CL2-3 now asks for at least one model evaluator differing from a model maker in both family and
  endpoint; others may share them. This loosened the rule, so no record that read `OK` became `FAILED`.

## 0.9.1

First published release.
