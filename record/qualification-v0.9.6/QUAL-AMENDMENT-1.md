# Amendment 1 to AGENT-RUNBOOK-V096-QUAL.md (sha256 8129a7bf…): Maker scoring, version 2

Applies only after the Owner's **"Proceed"** on this file. Q0–Q2 are unchanged.

## The defect (the Architect's, found by the Orchestrator)
Q3's semantic gates scored **the Architect's own design of revision 1**, not whether D-1 and D-2 are
closed. The brief they were built from says "whatever form you choose" and "the replacement prose is
yours". The gates contradicted that brief in three places:
- **M3** used revision 1's `tests/run_fixtures.py`, which fails any checker that *lists* BL-1 (as `OK`)
  for a non-baseline record. That is a reporting choice revision 1 made, not something D-1 required.
  - Gemini 4 Argon's checker matches revision 1 on verdict, level, routing and failing IDs on all 111
    cases, and reads 5/111 only because of that rule. A hand-made variant of revision 1 that lists BL-1
    as `OK` reads the same 5/111.
  - Revision 0's checker, with that rule set aside, reads 111/111. D-1 and D-2 were text defects, and
    revision 0's behaviour was already right.
- **M4** expected NO to "is it held to BL-1?". A maker who makes BL-1 apply to every record and read
  `OK` unless the claim is baseline closes D-1 just as well. The brief's own test is **consistency**:
  "a reader who reads only BL-1 and the §4 row must reach the same answer as a reader who reads only
  §5's scope line."
- **M5** allowed only CR-2 and BL-1 to change. The brief's other route for D-2 is to state fields
  "where they are required", and that means adding text to the rows that own them.

The disclosed conflict was real. The clean control (revision 1 must pass) proved only that the
Architect's design passes. No control checked that a different valid design passes.

## Scoring version 2 (`score_maker_v2.py`, new and pinned; `score_maker.py` stays pinned and unused)
- **M1, M2:** unchanged.
- **M3 v2, no regression.** On a copy of `r1/evaluatordriven` holding the session's `checker/check.py`,
  every one of the 111 cases has verdict, level achieved, routing and the sorted failing IDs equal to
  `fixtures/expected.json`. Whether BL-1 is listed for a non-baseline claim is not scored.
- **M4 v2, the brief's test.** Each seated adjudicator gets the session's `SPEC.md`, with one fresh
  session per question, using these questions:
  1. Appendix C question 1, unchanged.
  2. Appendix C question 2, unchanged.
  3. *Replaces Appendix C question 3:* "A record claims CL1, has no `readsBeforeFreeze` field, and meets
     every other requirement. Under this SPEC.md, does BL-1 or CR-2 read FAILED or NOT-CHECKABLE for
     it? Answer YES or NO, then quote the deciding sentence."
  4. Appendix C question 4, unchanged, scored as below.

  **A session passes M4 v2 when all four hold:**
  - each adjudicator's answers to questions 1 and 2 are the same as each other;
  - both adjudicators answer question 3 **NO**;
  - both adjudicators name the **same** single ID for question 4;
  - that ID is the one the session's checker reports `FAILED` on revision 1's fixture
    `cl1-fail-missing-violations-field`.
- **M5 v2, no unrelated change.**
  - Files, headings and the set of requirement IDs: as in M5.
  - CR-2 and BL-1 may change freely.
  - The rows of CL1-2, CL1-4, CL1-5, CL1-11, CL1-12, CL2-1 and CL3-1 may only **gain** text: each
    revision-0 row's requirement text, compared case-insensitively with whitespace collapsed, appears
    whole inside the new row.
  - Every other requirement row is byte-identical to revision 0.

## Controls, run before any re-scoring (any other outcome is a STOP)
- **Revision 1:** passes M3 v2, M4 v2 and M5 v2.
- **Revision 0:** passes M3 v2 (its behaviour was right) and **fails M4 v2**.
- **A valid alternative design:** revision 1's checker changed so that BL-1 is in scope for every claim
  and returns at once unless the claim is baseline. It **passes M3 v2** (111/111).
- **A broken checker:** revision 1's checker with plant P2 from `make_plants.py` applied **fails M3 v2**.

## Re-score, no new maker calls
1. Re-score **every session of every candidate already run** that has a final diff, under v2.
2. M4 v2 needs new adjudicator calls only for sessions that pass M1, M2, M3 v2 and M5 v2.
3. Buy no new candidate until this re-score is reported.
4. Report v1 and v2 side by side for every session, written by script from the score files, then
   **STOP**.

## Not changed here
The Appendix B prompt still asks for "a fixture that fails under revision 0's checker". Because D-1 and
D-2 were text defects, that line pushes makers to change behaviour. It matters only if new maker
sessions are bought. If they are, it becomes amendment 2, applied to every candidate.
