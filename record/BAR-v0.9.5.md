# The bar — v0.9.5 of `smoitozo/evaluatordriven`

**RATIFIED 2026-10-22 by Steve Moitozo II ("Ratified", claude.ai chat, 09:47 ET) · FROZEN** · Drafted by Claude Opus 5.5, also the Maker (the Architect = Maker conflict,
recorded again). This page inherits the v0.9.4 bar **except where it changes it**. It names no private
person, so it can be published as it stands and CL1-14 checked against it. Nothing was built before it was
ratified and frozen.

## The job
- **Start from:** `c473a8c` on `main` (the `v0.9.4` tag `6b17364` plus the record correction).
- **Site ground truth:** site commit `3a83ce1` (content `7a3b07d`), confirmed live on 2026-10-22 (version
  v0.9.4; the two claims link `record/VERIFY.md` and `record/STRANGER-TEST.md`).
- **Theme: can a stranger implement the standard from its text alone?** v0.9.4's stranger test did not
  pass: one of five counted implementer runs met both thresholds (two uncounted diagnostic sessions also
  met them), and a single implementer swung from 11 of 12 to 5 of 12 on near-identical text. One session per implementer cannot tell a hard sentence from a bad draw.
  This release measures properly first, and fixes only what that measurement and v0.9.4's evidence point at.
- **Stated assumption, not a gate:** demand comes through Plumbline. The signal: *a team outside Ligonier
  asks for the records Plumbline produces.*

## Scope: six items, nothing else
Every changed rule ships with a fixture that fails before the change and passes after.

| # | Item | Kind | Done when |
|---|---|---|---|
| I1 | **The stranger test, measured properly** (the gate, below), in up to three cycles. | Gate | Run as designed; every cycle published whatever it says |
| I2 | **CL1-17 and unscored checks.** One sentence: a check whose `score` is `null` is not judged by CL1-17. | Editorial | Fixture: a record of unscored checks reads OK on CL1-17 |
| I3 | **CL2-3, said so it can be counted.** State the half rule as arithmetic (twice the evaluators of the maker's family is no more than the evaluators of that dimension), and give one non-normative worked example covering `undisclosed` and a check's own `endpoint`. | Editorial | Fixtures at exactly half, over half, and with `undisclosed` on each side |
| I4 | **Malformed evidence.** A non-normative worked example under "One defect, one failure": an `evidence` value that is not an evidence file fails CR-2, and CL1-8 reads `NOT-CHECKABLE`. | Editorial | Fixture; the adjudicator's two readings in v0.9.4 can no longer both be argued from the text |
| I5 | **A clean control for every evaluator.** CL1-9: each evaluator with an observed check in a batch reads at least one control expected `conforms` and at least one expected `does_not_conform` there. (Closes v0.9.4's known residual: a reader that rejects everything could pass on planted controls alone.) | **Breaking** | Fixtures: reader with only planted controls fails; reader with only clean controls fails |
| I6 | **Housekeeping from v0.9.4.** (a) Kept records get per-version names (`DISPOSITION-v0.9.5.md`), and no release overwrites an earlier one. (b) Results published about a record are written by a script from the checker's output, never by hand. (c) CHANGELOG 0.9.5 carries the correction of v0.9.4's four R12 reasons. (d) `explain.py`, `make_record.py` and CI run with no cache files written into the tree. | Tooling | count.py checks (a); a red test proves (b); CI green |

**Out of scope:** guide and plain-view rewrites; purpose and audience; lineage records; a chain anchor; the
Sigstore verifier (built when a record needs CL3); crosswalks; CL4; certification; evaluator competence
(Plumbline's); GitHub Actions version bumps unless CI breaks.

## The gate: the stranger test, measured properly
- **Implementers:** Seed 2.1 Turbo, MiniMax M3 and Nemotron 3 Ultra, **three fresh sessions each** (nine in
  all), same prompt, provider pinned with no fallback. No tools, no browsing; they never see a record, an
  answer or a score.
- **Records: a fresh twelve per cycle.** Kimi writes them from the current SPEC.md alone, blind to the checker, with
  the same coverage rules as v0.9.4 plus I2–I5. v0.9.4's twelve are retired: the Maker's revisions were
  informed by notes about them. Two controls, one planted and one clean, validated before any session runs.
- **Answers:** where Kimi's key and the reference checker disagree, MiMo rules **with SPEC.md in hand**; if
  MiMo gives no ruling twice, the record is dropped from the count with that reason. Records, answers and
  thresholds are hashed and logged before the first session.
- **Error round-trips:** at most two per session, and the harness pastes the program's own error output
  automatically; no person or model writes or summarises it.
- **Scoring, per session:** A = verdict, level and routing match; B = failing IDs match. A session that gets
  a control wrong is not counted.
- **Per implementer, by majority:** an implementer **meets** the bar if at least two of its counted
  sessions reach **A ≥ 11 and B ≥ 10** (of 12). With fewer than two counted sessions it is unobserved.
- **Pass:** **every** observed implementer meets the bar, and at least two are observed. Fewer than two
  observed: the test is unobserved, and v0.9.5 ships saying so.
- **Published with the result:** every session's A and B, so the spread is visible, not only the verdict.

**Cycles, decided now:** the test may run in **up to three cycles**. A new cycle runs only after a revision
that changes SPEC.md's normative text, justified by the previous cycle's sentence-level notes (the Maker
never sees records, answers or code). **Each cycle uses a fresh set of twelve records** and fresh
controls, written and validated as above before any session runs, so no revision can be fitted to the
cases that test it; retired sets stay held out for good. Each cycle is all nine sessions. **Every cycle's
scores are published**, and **the last cycle's result stands.** Nothing resets the count: if the third
cycle does not pass, the test fails. Cycles share the bar's three revisions; a revision made for any
other reason still counts against them.

## The other gates
| Gate | Passes when |
|---|---|
| D9 (blind key over every fixture) | The checker matches every blind case; non-blind cases held out |
| Red tests | Each changed rule's fixtures fail before and pass after |
| CI | Green on both Python versions |
| Own record | **OK at CL1** against the **unpacked release package**, publicly checkable except CL1-8 and CL1-15 |

## Seats
| Role | Who |
|---|---|
| Maker | Claude |
| Author (records, key, controls) | Kimi K2.5 |
| Orchestrator | DeepSeek v4.1 |
| Implementers (stranger test) | Seed 2.1 Turbo, MiniMax M3, Nemotron 3 Ultra |
| Adjudicator | MiMo, always with SPEC.md |
| Guide tester, human reader | **None this version, stated as a limit.** Those named privately stay held cold. |

## Process, from v0.9.4's lessons
- Every check runs against the **unpacked release package**, never the working folder.
- Evidence files are written once, then logged; nothing rewrites them while a check reads them.
- Each pending-events file is hash-checked **on the Owner's machine** after it is sent, not only the runbook.
- One finishing runbook; the Orchestrator reports once, with requirement IDs and counts only.

## Fallbacks
- **An implementer's sessions keep failing to run:** that implementer is unobserved; no replacement seat.
- **The stranger test fails:** v0.9.5 ships as a candidate saying so, with every session's scores; whether the
  standard continues as published is the Owner's decision, on that evidence.

## Bounds
3 revisions · **$15** in evaluation spend · 14 days from freeze · at most **10** Owner decisions.

## Ratified
1. Scope I1–I6, with **one breaking change** (I5).
2. The stranger test's design: three implementers × three fresh sessions, a fresh set of twelve records,
   majority per implementer, and **every observed implementer must meet the bar** (stricter than v0.9.4's
   "both of two", not easier).
3. Up to three test cycles, each on a fresh set of twelve records and only after a normative revision the
   previous cycle's notes justify; every cycle published; the last cycle stands; at most three, within
   the three revisions.
4. No guide tester or human reader, stated as a limit; the fallbacks and bounds above.
