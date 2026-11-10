# Stranger test — status at v0.9.9

**Status: not passed; last cycle failed (v0.9.7 r2); suspended 2026-11-10.**

The method, its gate and its cycles 1–r2 are in `record/STRANGER-TEST.md`, `STRANGER-TEST-v0.9.5.md`,
`-v0.9.6.md` and `-v0.9.7.md`. This note records a decision about when the test runs, not a change to it. The
gate is unchanged and remains published as **unmet**.

## What suspension means

- **No routine per-release cycles.** A cycle is not run because a version was cut. Four were run that way and
  every one failed; repeating them on the same rhythm would spend the scarcest resource to learn the same
  thing.
- **One cycle is owed after v0.9.10.** It covers the requirements the last clarity measure scored below full
  agreement and that have since been rewritten: `CL1-10` (3 of 6 sessions) and `CL2-3` (18 of 24), both
  rewritten in v0.9.8 without a rerun, and `CL1-9`, which v0.9.10 touches. A rerun after the weak points are
  rewritten is the one case where the result could change.
- **Revival condition.** A release that changes a requirement the clarity measure scored below full agreement
  reopens the test for that release. Nothing else does.

## What suspension does not mean

- **It is not a withdrawal, and it is not a pass.** The last measured result is a failure and travels with the
  word "suspended" wherever the status appears. A gate whose last result is printed beside it lends no
  authority it has not earned.
- **The candidate label stands.** custody remains `candidate` while the test is suspended; the release level
  does not advance on the strength of a test that has not run.
- **A single reproduction read is not this test.** One outside reader reproducing one published record is a
  useful measurement of legibility, reported under its own name ("reproduction read: one reader, one record,
  N of M claims reproduced"). It is not an observation under this method and does not count toward the two
  observed readers a cycle requires.

## Why this note exists

Absence of a passing cycle and absence of the test look identical from outside. A reader who finds four
failures and then silence cannot tell a decision from an oversight, and the difference between "suspended with
a stated trigger" and "quietly dropped" is the whole of the claim that this method means anything.

*Decided 2026-11-10 on the Owner's instruction, following an outside review of all three repositories.*
