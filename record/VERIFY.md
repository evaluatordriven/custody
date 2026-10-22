# Checking the v0.9.3 record

Check it against the release, not the latest version: `git checkout v0.9.3`, then

    python3 checker/check.py record/custody-v0.9.3.json --files . --bar record/BAR-AMENDMENT-1.md

Without more, it reads `NOT-CHECKABLE` on one requirement, CL1-15: the files that show what the four
reader models and the cold implementer actually returned. Those files hold answers to test cases that
later versions reuse, so they are not public. The Owner keeps them and can produce them on request; a
verifier who has them passes `--evidence DIR` as well.

The CI run at the v0.9.3 tag failed because its quickstart step left out `--bar`. The fix came in the
next commit on `main` and changes nothing the record covers except that CI file.

## 2026-10-21 — the v0.9.3 record under v0.9.4's rules

Run with the release's checker and the private evidence: `FAILED`, no conformance level, routing
`acknowledged`. The record is untouched; the requirements moved.

- **CR-2** — `FAILED`: `maker.kind` is absent.
- **CL1-1** — `NOT-CHECKABLE`: no `startedAt`, so the bar cannot be placed before the work began.
- **CL1-4** — `FAILED`: the maker names no `kind` and no version.
- **CL1-8** — `NOT-CHECKABLE`: checks name evidence as bare digests, not evidence files.
- **CL1-9** — `FAILED`: a batch holds no clean control.
- **CL1-16** — `FAILED`: readings are filed under a script evaluator that is also the runner.

## 2026-10-22 — checking the v0.9.4 record

At tag `v0.9.4`: `python3 checker/check.py record/custody-v0.9.4.json --files . --bar record/BAR.md`.
Without the private evidence, CL1-8 and CL1-15 read `NOT-CHECKABLE`: the evidence holds held-out test
material. Every other requirement can be checked by anyone.
