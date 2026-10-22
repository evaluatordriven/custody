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

## 2026-10-22 — correction to "the v0.9.3 record under v0.9.4's rules"

The verdict, level, routing and requirement IDs in that section are right. Four of its reasons are not
what the checker reports: they were written in prose instead of copied from its output. The checker's own
reasons (the v0.9.4 checker on tag `v0.9.3`, with `--files . --bar record/BAR-AMENDMENT-1.md`):

- **CR-2** — `FAILED`: `predicate.startedAt` is missing, and evaluators' `model.family` and
  `model.endpoint` are not in the required form (for example `GPT`, and `OpenRouter` for the endpoint).
- **CL1-4** — `FAILED`: `maker.kind` is missing, and `maker.model`'s `family` and `endpoint` are not in
  the required form.
- **CL1-9** — `FAILED`: evaluator R1 reads in batch `v093-batch` but reads no control there. (The batch also
  holds no clean control.)
- **CL1-16** — `FAILED`: four listed evaluators (`gpt-6.1-sol`, `grok-4.7`, `glm-5.3`, `qwen-3.8`) appear on
  no check and no control.

The CL1-1 and CL1-8 lines were right. Without the private evidence, CL1-15 also reads `NOT-CHECKABLE`.
`CHANGELOG.md` carries the same four reasons; it is one of the release's fingerprinted files, so it is not
edited in place, and v0.9.5's entry carries this correction.
