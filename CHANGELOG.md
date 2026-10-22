# Changelog

Each release is a git tag, and each carries its own custody record in `record/`. Before 1.0.0 any release
may turn a record that read `OK` into one that reads `FAILED` (SPEC.md section 8); every such change is
listed here under **Breaking**.

## 0.9.4 (candidate)

Theme: make the record mean what it says. Four independent reviewers read the v0.9.3 release record
against its checker and found that it passed while filing every model reading under a script, binding
check evidence to nothing, and holding no clean control. Each fix below closes one of those holes.

**The v0.9.3 record under this release's rules.** The record has not changed; the requirements have. It
still conforms to v0.9.3, the version it names. Run under this release's checker with its private
evidence, it reads **FAILED**, achieving **no conformance level**, routing **acknowledged**. Each
requirement that does not read `OK`:

- **CR-2** — `FAILED`: `maker.kind` is absent.
- **CL1-1** — `NOT-CHECKABLE`: the record carries no `startedAt`, so the bar cannot be placed before the work began.
- **CL1-4** — `FAILED`: the maker names no `kind` and no version.
- **CL1-8** — `NOT-CHECKABLE`: its checks name evidence as bare digests, not evidence files.
- **CL1-9** — `FAILED`: a batch holds no clean control.
- **CL1-16** — `FAILED`: readings are filed under a script evaluator that is also the instrument's runner.

**Breaking** (what a producer must change)
- `startedAt` is required. CL1-1: the bar is frozen before the work **started**, not just before it was
  finished, and `startedAt` is no later than `producedAt`. BL-1: a baseline's bar is frozen after
  `startedAt`. *Add the time work began; `tools/make_record.py --log` takes it from the first
  `work-started` event.*
- `maker.kind` is required: `person`, `model` or `script` (CL1-4). *Add it.*
- CL1-8: a check's `evidence` is an evidence file, `{name, sha256}`, and the file supplied with
  `--evidence` must match; without it, CL1-8 reads `NOT-CHECKABLE`. *Change each check's evidence from a
  digest to a named file, and keep the file.*
- CL1-9: every evaluator with an observed check in a batch reads a control in that batch, and every batch
  holds at least one clean control (expected `conforms`). *Give each reader its own control, and add a
  clean one.*
- CL1-16 (new): every listed evaluator appears on a check or a control; every control names a listed
  evaluator; no script evaluator's script is the instrument's runner. *File each reading under the
  evaluator who gave it.*
- CL1-17 (new): a scored check conforms exactly when its score reaches the threshold, and its score lies
  between the floor and the highest anchor. CL1-2: anchors are keyed by score, none below the floor, and
  the threshold lies inside the scale. *Make outcomes follow scores; keep any mean or minimum as your own
  rule for what happens next.*
- Model identity (CR-2): `family` is lowercase letters and hyphens with no version, or `undisclosed`;
  `endpoint` is a host name with at least one dot. A check may carry its own `endpoint`. CL1-6: a model
  evaluator carries a `model` block. CL2-3: an undisclosed family counts as the maker's; a check's own
  endpoint counts as its evaluator's. *Write `gpt`, not `GPT` or `gpt-6`; write the answering host, not
  the router.*
- CL1-11 and CL2-3: a maker who wrote the bar is named in `separationGaps` at CL1, and is not allowed at
  CL2. CL2-3 also needs `maker.model` when `maker.kind` is `model`.
- CL3-3: the signature is a Sigstore bundle (a DSSE envelope logged in Rekor). A verifier reads `OK`
  only if it verifies the bundle itself; the reference checker does not, so it reads `NOT-CHECKABLE`, and
  no record reaches CL3 with it.
- `run` must be 1 or more, in the checker as in the schema.

**Added**
- Extensions: producers may add fields under keys beginning `x-`; verifiers ignore them (SPEC.md
  section 4), with a note on re-filing older records.
- SPEC.md section 7 names four limits: the custody log has no outside anchor; a control cannot show the
  case was hard; "held out" means held out from this record's maker; signing publishes the signer.
- The plain view states who made the work and whether the bar was fixed before the work started. The
  glossary gives both senses of "signature".

**Clarified** (revision 1, after the stranger test's first run; the rules did not change)
- CL2-3 is split into parts (a), (b) and (c), and says where `undisclosed` applies.
- "One defect, one failure" (SPEC.md section 5): a missing or malformed field fails the requirement that
  checks it; another requirement that cannot be decided without it reads `NOT-CHECKABLE`. The reference
  checker already worked this way; an evidence name that is not a relative path now fails CR-2 alone,
  as this rule says.
- Section 6 says which requirements are in scope for each claim.

**Stranger test** — run 1, read against revision 0's text
- Seed 2.1 Turbo: A 11 of 12, B 10 of 12; both controls correct; counted; met both thresholds.
- MiniMax M3: A 9 of 12, B 9 of 12; both controls correct; counted; short of both thresholds.
- Nemotron 3 Ultra, an extra reading (its seat was taken on an orchestration error): A 8 of 12, B 7 of 12.
- Adjudicator's note, rec-10: the reference checker's reading upheld — CR-2 fails and CL1-8 reads
  `NOT-CHECKABLE`. The same adjudicator later read CL1-8 as failing on the same record; both cannot stand,
  and this entry records that it ruled both ways.
- Adjudicator's note, rec-11: CL2-3 — "no more than half" is inclusive of exactly half, so the record
  conforms; the implementers' readings were wrong.
- Run 1's result: the stranger test did not pass.

**Stranger test — the re-run** (decision 1, against this release's text, one run only)
- Seed 2.1 Turbo: **not counted** — it failed **both** controls: the clean one flipped to FAILED, and the
  planted one gained a failing ID. Its verifier reads CL1-17 as failed on every record. A 5 of 12, B 1 of 12.
- MiniMax M3: counted; A 10 of 12, B 9 of 12; short of both thresholds.
- The re-run does not pass: one implementer short and one not counted. The stranger test fails, and this
  release ships as a candidate saying so.
- **The stranger test did not pass; see `record/STRANGER-TEST.md`.**

**Changed**
- `count.py` no longer caps the checker at 300 lines (the cap pushed the code into one-liners), and now
  fails if CI and README.md run different quickstart commands. CI runs those commands exactly, and checks
  that the committed example record is the one they build.
- The reading-level check runs in CI as advisory, not as a gate.
- `count.py` skips `record/`: kept records, such as a release's bar, are quoted word for word and may
  use words the specification reserves (revision 2).
- `count.py` treats earlier releases' records in `record/` as history.

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
