# The stranger test — v0.9.5

**Method.** Twelve fresh records per cycle, written by a session that sees SPEC.md and the schema only.
Two controls (one planted, one clean) are validated before anything is frozen; the answers are hashed
and logged before the first session runs. Three implementers — Seed 2.1 Turbo, MiniMax M3 and Nemotron 3
Ultra — each run three fresh sessions, provider pinned with no fallback, no tools. A = verdict, level and
routing match (of 12); B = the failing requirement IDs match (of 12). A session that gets either control
wrong is not counted. An implementer meets the bar when at least two of its counted sessions reach
A >= 11 and B >= 10; the cycle passes when every observed implementer meets it and at least two are
observed. Every disagreement in a counted session goes to an independent adjudicator.

## Cycle 1 — unobserved

| implementer | session | counted | A | B |
|---|---|---|---|---|
| Seed 2.1 Turbo | s1 | yes | 9 | 12 |
| Seed 2.1 Turbo | s2 | yes | 11 | 11 |
| Seed 2.1 Turbo | s3 | no | 8 | 11 |
| MiniMax M3 | s1 | no | 4 | 2 |
| MiniMax M3 | s2 | no | 5 | 2 |
| MiniMax M3 | s3 | no | 4 | 0 |
| Nemotron 3 Ultra | s1 | yes | 10 | 9 |
| Nemotron 3 Ultra | s2 | no | 8 | 11 |
| Nemotron 3 Ultra | s3 | no | 6 | 11 |

- **Seed 2.1 Turbo**: 2 counted, 1 meeting both thresholds — does not meet the bar.
- **MiniMax M3**: 0 counted, 0 meeting both thresholds — unobserved.
- **Nemotron 3 Ultra**: 1 counted, 0 meeting both thresholds — unobserved.

**Cycle 1 result: unobserved.** Observed: Seed 2.1 Turbo.

**Adjudicator's notes.** 7 disagreement(s); 0 found a sentence two careful readers can read two ways.

## Cycle 2 — does not pass

| implementer | session | counted | A | B |
|---|---|---|---|---|
| Seed 2.1 Turbo | s1 | yes | 10 | 8 |
| Seed 2.1 Turbo | s2 | yes | 11 | 11 |
| Seed 2.1 Turbo | s3 | no | 4 | 0 |
| MiniMax M3 | s1 | yes | 11 | 9 |
| MiniMax M3 | s2 | no | 4 | 10 |
| MiniMax M3 | s3 | no | 5 | 9 |
| Nemotron 3 Ultra | s1 | no | 4 | 0 |
| Nemotron 3 Ultra | s2 | yes | 8 | 9 |
| Nemotron 3 Ultra | s3 | yes | 10 | 9 |

- **Seed 2.1 Turbo**: 2 counted, 1 meeting both thresholds — does not meet the bar.
- **MiniMax M3**: 1 counted, 0 meeting both thresholds — unobserved.
- **Nemotron 3 Ultra**: 2 counted, 0 meeting both thresholds — does not meet the bar.

**Cycle 2 result: does not pass.** Observed: Nemotron 3 Ultra, Seed 2.1 Turbo.

**Adjudicator's notes.** 15 disagreement(s); 1 found a sentence two careful readers can read two ways.
- **RULING: AMBIGUOUS** — clause: **CL2-3**, its closing sentence ("In (b) and (c), a `family` recorded as `undisclosed`, on either side, counts as the maker's"). 1. Reading 1 (→ B): only a value literally recorded `undisclosed` is equated with the maker's family; here that is the maker's own family, so eval1's `gpt` is "different from the maker's" and (b) holds — CL2-3 OK. 2. Reading 2 (→ A): `undisclosed` is a stand-in for an unknown family, so nothing can be shown different from it; every model evaluator counts as the maker's, so no evaluator differs and (b) fails — CL2-3 FAILED. 3. "on eithe

## A voided attempt at cycle 3

A first attempt at cycle 3 is void and is not a cycle; the Owner ratified the void. Its planted
control was built with a wrong evidence digest, so the control never validated, and its nine sessions
ran when the runbook said stop. No result is taken from it. The cycle 3 below ran on twelve fresh
records, frozen before any session.

## Cycle 3 — passes

| implementer | session | counted | A | B |
|---|---|---|---|---|
| Seed 2.1 Turbo | s1 | yes | 12 | 11 |
| Seed 2.1 Turbo | s2 | yes | 12 | 11 |
| Seed 2.1 Turbo | s3 | no | 4 | 0 |
| MiniMax M3 | s1 | no | 4 | 0 |
| MiniMax M3 | s2 | yes | 12 | 12 |
| MiniMax M3 | s3 | yes | 11 | 10 |
| Nemotron 3 Ultra | s1 | no | 4 | 9 |
| Nemotron 3 Ultra | s2 | no | 6 | 9 |
| Nemotron 3 Ultra | s3 | no | 4 | 0 |

- **Seed 2.1 Turbo**: 2 counted, 2 meeting both thresholds — meets the bar.
- **MiniMax M3**: 2 counted, 2 meeting both thresholds — meets the bar.
- **Nemotron 3 Ultra**: 0 counted, 0 meeting both thresholds — unobserved.

**Cycle 3 result: passes.** Observed: MiniMax M3, Seed 2.1 Turbo.

**Adjudicator's notes.** 4 disagreement(s); 0 found a sentence two careful readers can read two ways.

## The result

Cycle 1 was unobserved, cycle 2 did not pass, a first attempt at cycle 3 was void, and cycle 3 passed with two implementers observed and both meeting the bar; the last cycle's result stands, so **the stranger test passes for v0.9.5**.
