# The bar — v0.9.4 of `smoitozo/evaluatordriven`

**RATIFIED 2026-10-20 by Steve Moitozo II ("Ratified", claude.ai chat) · FROZEN** · Drafted by Claude Opus 5.5, also the Maker (the Architect = Maker conflict,
recorded again). The same model was one of four reviewers in the 2026-10-20 round whose findings this bar
acts on; every finding used here was checked by script against the artifact. This page inherits bar v5.1,
the v0.9.1–v0.9.3 pages and v0.9.3 Amendment 1, **except where it changes them**. It names no private
person, so it can be published as it stands and CL1-14 checked against it.

## The job
- **Start from:** `136cb280ab9fed5a5c3fd4312083e7092567d57b` on `main` (the v0.9.3 tag `bba40b99` plus the
  CI fix; CI green). The v0.9.3 record verifies against the tag: OK, CL1, acknowledged, with the private
  evidence supplied.
- **Theme: make the record mean what it says.** Repair the contract; test whether a stranger can read it;
  add no public surface.
- **Why:** the v0.9.3 record passed its own checker while it filed all 25 model-read checks and all 16
  controls under a script, bound check evidence to nothing, broke the family rule, counted an uncalibrated
  human check, and held no clean control. The checker allowed each of these. (Source: four-model review,
  2026-10-20, re-verified.)
- **Site ground truth:** commit `d84c7b7` of the site repository (content at `72acf71`), the corrections-only
  release; confirmed live on 2026-10-20 (version line, checker line, `/custody/v1`).
- **Stated assumption, not a gate:** demand comes through Plumbline, which is rebasing on `custody/v1`.
  The signal, decided now: *a team outside Ligonier asks for the records Plumbline produces.*

## Scope: twelve items, nothing else
Every changed rule ships with a fixture that fails before the change and passes after (red, then green).

| # | Item | Kind | Done when |
|---|---|---|---|
| R1 | **Attribution.** Each check and control names the evaluator that actually read it. A script that scores readers' replies is recorded in `instrument.runner`, not as the evaluator of their readings. An evaluator listed in `evaluators` that appears on no check and no control fails the record. | Breaking | Fixtures: decorative evaluator fails; readings filed under a scoring script fail |
| R2 | **Controls for each evaluator.** CL1-9: every evaluator with an observed check in a batch reads at least one control in that batch. Every batch holds at least one control whose expected outcome is `conforms`. | Breaking | Fixtures: reader with no control fails; batch with only planted controls fails |
| R3 | **Check evidence binds to a file.** CL1-8: a check's evidence digest is checked against the file supplied with `--evidence`; without it, `NOT-CHECKABLE`, as CL1-15 already reads. | Breaking | Fixtures: mismatched file fails; missing file reads NOT-CHECKABLE |
| R4 | **Identity.** The checker enforces SPEC §4's family rule (lowercase, no version). `endpoint` is the host that answered, not a router; a check may carry its own `endpoint` when the answering host changed mid-record. An undisclosed family is recorded as `undisclosed`, and CL2-3 counts it as the maker's family. A model evaluator carries a `model` block at CL1. | Breaking | Fixtures for each rule |
| R5 | **Start time and maker kind.** Required `startedAt`: CL1-1 needs `bar.frozenAt` earlier than `startedAt`, and `startedAt` no later than `producedAt`; BL-1 covers a bar frozen after `startedAt`; a bar frozen at the same instant as `startedAt` is neither, said once, in one place. Required `maker.kind` (`person`, `model`, `script`); the plain view says who made the work. | Breaking | Fixtures for before, after, equal, missing; plain view shows both |
| R6 | **Score decides outcome.** SPEC states the rule and the checker enforces it: a scored check `conforms` if and only if `score ≥ threshold`; `floor` is the lowest score on the scale, and a score below `floor` or above the highest anchor is invalid. Producer policy (means, minimums, extra runs) sits on top and is never the outcome. | Breaking | Fixtures: outcome contradicting score fails; out-of-range score fails |
| R7 | **Bar authorship.** At CL1, a bar written by the maker requires an entry in `separationGaps` naming the maker. At CL2, the maker does not write the bar. | Breaking | Fixtures at CL1 and CL2 |
| R8 | **Name the limits** in SPEC §7 and one README line each: the custody log has no outside anchor (a rewritten or shortened chain verifies); the reference checker does not verify signatures, so CL3-3 reads `NOT-CHECKABLE` with it rather than passing a prose file, and SPEC names **Sigstore** (a DSSE-signed record, logged in Rekor) as the CL3-3 method a future verifier will check; a checker cannot tell whether a control could have failed; "held out" means held out from the maker of this record (the v0.9.3 VizH input, H1–H5), for CL1 controls and CL3 planted cases alike. The glossary's **signature** entry carries both senses: the approver's accountable acceptance, and the cryptographic signature CL3-3 checks. No new MUST, and no wording that casts iterating makers as suspect. | Editorial (CL3-3 reading: breaking) | Every unrelated fixture gives the same outcome; count.py clean |
| R9 | **Schema and checker agree** (`run ≥ 1`; `anchors` non-empty). | Fix | A test runs every fixture through both and fails on any difference |
| R10 | **Extension convention.** One sentence in SPEC §4: producer-specific fields go under keys beginning `x-`, anywhere in the predicate; verifiers ignore them; no requirement reads them. A non-normative line beside it: a record re-filed from an earlier instrument keeps its original times and carries its prior verdict under an `x-` key; it conforms only on its own fields. | Additive | Fixture with `x-` fields passes unchanged; fixture of a re-filed record with `x-` provenance passes |
| R11 | **Unbend the tooling.** Remove the 300-line cap on `check.py`; keep `count.py`'s cross-file agreement checks; add one: CI runs the README's quickstart lines exactly. Readability runs as advisory, not as a CI gate. | Tooling | A red test proves the quickstart drift check; CI green |
| R12 | **Re-run the v0.9.3 record** under the v0.9.4 checker, with its private evidence, on the Owner's machine, and publish the verdict and failing requirement IDs in `CHANGELOG.md` and `record/VERIFY.md`. The CHANGELOG entry opens: *the record has not changed; the requirements have. It still conforms to v0.9.3, the version it names.* `VERIFY.md` is appended to, never rewritten, and `custody-v0.9.3.json` is untouched. | Record | Published as it comes out, whatever it says |

**Also in this release:** the two unresolved v0.9.3 D9 cases, adjudicated before this key is frozen; a
CHANGELOG entry that lists every breaking change with what a producer must change.

**Out of scope:** guide and plain-view rewrites beyond what R5 needs; optional purpose and audience;
lineage records; a chain anchor field; crosswalks; retention periods; CL4; certification; evaluator
competence (process, which SPEC §1 excludes; it belongs to Plumbline).

## The decisive gate: the stranger test (replaces D1)
Two cold implementers, in fresh sessions, each get **only** `SPEC.md`, the schema, and twelve records with
their artifact files, bar files and evidence files. No checker, fixtures, guide, glossary or site. Each
writes a verifier and runs it on all twelve.

- **The records:** Kimi writes them from `SPEC.md` alone, blind to the checker, with an answer key giving
  verdict, level, routing and failing requirement IDs. They cover R1–R7 and include at least three that
  should read `OK` and at least one `NOT-CHECKABLE`.
- **Controls:** within the twelve, two cases have outcomes fixed and validated before the run, one planted
  and one clean. An implementer that gets either wrong is not counted (CL1-9 applied to ourselves).
- **Pass:** both counted implementers match the adjudicated answer on verdict, level and routing for at
  least 11 of 12 records, and on failing requirement IDs for at least 10 of 12.
- **Where they disagree:** the case goes to the key, the reference checker and SPEC.md. A difference traced
  to an ambiguous SPEC sentence is a defect in the standard, fixed in a revision. Disputes go to the
  adjudicator. Each such defect gets a note of five lines or fewer in CHANGELOG: the sentence, the two readings, the fix.
- **Thresholds and records are fixed before any implementer runs.**

## The other gates
| Gate | Reads | Passes when |
|---|---|---|
| D9 (blind key) | Kimi's blind key over every fixture, old and new | The checker matches every blind case; non-blind cases are held out |
| Red tests | Every R item's fixtures | Each fails before its change and passes after |
| CI | The workflow at the release commit | Green on both Python versions |
| Own record | v0.9.4's custody record under the v0.9.4 checker | **OK at CL1**, with every evaluator attributed and controlled under the new R1 and R2. The maker wrote the bar, so `separationGaps` names the maker (R7); CL2 is not claimed |

**No reader panel this version, stated as a limit.** The stranger test is the reading test of the
normative text.

## Seats
| Role | Who |
|---|---|
| Maker | Claude |
| Author (records, key, plants, controls) | Kimi K2.5 |
| Orchestrator | DeepSeek v4.1 |
| Cold implementers (stranger test) | **Seed 2.1 Turbo** and **MiniMax M3**, fresh sessions; replacement, at most one, **Nemotron 3 Ultra**. None is seated elsewhere in v0.9.4 or was in the 2026-10-20 review round. |
| Adjudicator | MiMo |
| Guide tester | **None this version.** The non-technical reviewer named privately stays held cold until the guide changes for a reason a record shows. |
| Human reader | **None this version, stated as a limit.** The human readers named privately stay held cold for v1.0. |

## Process: v0.9.3's lessons, built in from the freeze
- **One log** on the Owner's machine; the record built from it; no typed times. **Evidence files live in the
  same folder as the log.**
- **Each reading is filed under its reader,** never under the script that scored it.
- **The key prompt** allows all three routing words, and the key is written blind to the checker. Any line
  an orchestrator specifies or corrects is held out of D9.
- **Packets include every file the records point to,** bar and evidence included.
- **One finishing runbook,** with every fallback decided below. The orchestrator reports once.
- **CI's commands are the README's commands,** checked by script.

## Fallbacks, decided now
- **An implementer cannot produce a runnable verifier, or never reads the spec:** unobserved, then one
  named replacement (above). **Fewer than two counted:** the stranger test is unobserved,
  and v0.9.4 ships saying so.
- **The stranger test fails:** v0.9.4 ships as a candidate saying so, with the failing cases traced to
  SPEC sentences. Whether the standard continues as published is then the Owner's decision, on that
  evidence.
- **R12 reads FAILED:** expected; published as is.

## Bounds
3 revisions · **$15** in evaluation spend · 14 days from freeze · at most **10** Owner decisions.

## Ratified
1. Scope R1–R12, with **eight breaking changes** (R1–R7, and the CL3-3 reading in R8), shipped together.
2. R6's rule: conforms if and only if `score ≥ threshold`; `floor` is the bottom of the scale.
3. R8's CL3-3 reading: `NOT-CHECKABLE` with the reference checker, so no record reaches CL3 with it until a
   signature verifier ships; Sigstore is named as the method, and the verifier is built when a record needs CL3.
4. The stranger test as the decisive gate, with its thresholds (11 of 12, 10 of 12) and controls.
5. No reader panel, no guide tester and no human reader this version, each stated as a limit.
6. The fallbacks and bounds above, including **$15**.
