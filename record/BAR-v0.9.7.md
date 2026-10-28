# The bar: v0.9.7 of `evaluatordriven/custody`

**Ratified** by the Owner, Steve Moitozo II, as buyer and specialist on 2026-10-25 ("Proceed with A.
Ratified"). Drafted by Claude Opus 5.5 as **Architect only**. This page inherits the v0.9.6 bar **except where it changes it**. It names no
private person, so it can be published as it stands and CL1-14 checked against it. Nothing is built before
it is frozen.

## The job
- **Start from:** the `v0.9.6` tag, `3e3ca58`, now at `github.com/evaluatordriven/custody`.
- **Site ground truth:** the site commit that carries the doctrine and repo-move edits, confirmed live before
  freeze. (`dc7dc4c` until then.)
- **Theme: keep the public promise, and make the record-keeping mechanical.**
  - The site says in three places that "the next version fixes" CL1-10. v0.9.7 ships that fix, or those
    sentences change before it is published.
  - v0.9.6's errors were in hand-made steps, not in judgement: eleven checks filed in the wrong shape, a
    package carrying `.git`, figures typed rather than printed, and a revision that would not apply. v0.9.7
    replaces each of those steps with a pinned tool that refuses the error.
- **Stated assumption, not a gate:** demand comes through Plumbline. The signal: *a team outside Ligonier
  asks for the records Plumbline produces.*

## Seats
As v0.9.6, unchanged: Maker Gemini 4 Argon; adjudicators GPT 6.1 Sol and MiMo v2.6 Pro (both must agree;
a split is held out); test author GLM 5.3 (reserve Qwen 3.8); Orchestrator DeepSeek v4.1 Flash 1017;
stranger implementers Seed 2.1 Turbo, MiniMax M3, Nemotron 3 Ultra; Owner, buyer, specialist and approver
Steve Moitozo II (one person in several seats, disclosed). The Architect remains **not tested** (doctrine
v0.1 §6 names the gap; carried to the doctrine's v0.2).

**Independence:** as v0.9.6, the two required rules (CL1-6, CL2-3) and the two chosen rules (a) and (b).

## Scope: seven items, nothing else
Every changed rule ships with a fixture that fails before the change and passes after.

| # | Item | Carryover | Kind | Done when |
|---|---|---|---|---|
| J1 | **Fix CL1-10.** Both adjudicators found that the checker accepts a disagreement naming only some of the differing checks (rec05, cycle c1), and the text does not settle whether it should. Make the text decide, and the checker match it. Starting point: the Maker's v0.9.6 rewrite in `sessions/session-4.json` (evidence, never applied). | 44 | **Rule, breaking (must ship)** | Fixtures at the boundary (rec05's case among them); both adjudicators, given the new text and the code, agree that text and checker match; listed under **Breaking** in the CHANGELOG |
| J2 | **Control cases carry real digests.** The checker fails a control whose case digest is absent or all zeros. | 45 | Rule, **breaking** | Fixtures for absent and all-zero digests; listed under **Breaking** in the CHANGELOG |
| J3 | **Say why CL2-3(b) requires a different endpoint.** One sentence: it guards against one operator controlling both the work and its judge. The rule itself is unchanged. | 51 | Editorial | No fixture's expected answer changes |
| J4 | **Revisions apply with `git apply --recount`.** It recomputes only the hunk-header counts from the diff's content. Every diff v0.9.6 rejected on miscounted headers applies under it. Whole-file delivery waits for evidence that `--recount` is not enough. | 42 | Process | Fixed in the runbook before freeze; never changed after a failure. v0.9.6's three rejected diffs apply in a dry run |
| J5 | **Acceptance checks a revision's scope.** A revision that changes any normative row its brief does not name fails acceptance. | 43 | Process | A planted out-of-scope revision is refused in a dry run |
| J6 | **Two record tools in the repository:** `tools/file_event.py` writes one schema-valid check or control event at the moment it happens; `tools/release_record.py` verifies and assembles at the end, files nothing, and refuses if a declared check or control is missing. Neither shares code with the checker; the spec does not depend on them. | 46, 48 | Tools | Fixture tests that refuse each planted bad input: a wrong outcome word, an all-zero case digest, a missing evidence file, a check in a non-record shape |
| J7 | **Packaging is checked in a real clone.** The packaging step refuses any `.git` in the package or the subject, runs `count.py` (version identity included) before any package is logged, and runs the public check inside a simulated publication (unzip, `git init`, commit, clone). | 50 | Process | A planted package carrying `.git` is refused in a dry run |

**Out of scope, and where it goes:**
- **The Orchestrator harness as Plumbline's conductor (47) and the Orchestrator's requalification inside
  it (49).** These belong to Plumbline, not to the custody record, and building them inside this release
  would change its tooling and its seats at once. They run as a separate Plumbline job. v0.9.7 gets their
  core benefit through J6 and J7: the steps that failed by hand become pinned tools.
- Loosening CL2-3(b)'s endpoint clause (51): kept until a team that reaches every model through one cloud
  host actually asks. No rule without a job that needs it.
- Everything v0.9.6 left out of scope, unchanged.

## The gate: the stranger test
As v0.9.6, unchanged: GLM 5.3's records, answers ruled by both adjudicators with the code, the clarity
measure published beside the scores, three implementers × three sessions, A ≥ 11 and B ≥ 10, every
observed implementer meets it and at least two are observed, up to three cycles, every cycle published.

## The other gates
As v0.9.6 (D9, red tests, CI on both Python versions, own record **OK at CL1** against the unpacked
package, publicly checkable except CL1-8 and CL1-15), plus:

| Gate | Passes when |
|---|---|
| Record built by the tools | Every check and control in the release record was written by `file_event.py` at the time it happened, and `release_record.py` assembled the record without error |
| Promise kept | J1 shipped, or the site's three "the next version fixes it" sentences have changed |

## Process
v0.9.6's ten rules, unchanged, plus:
11. **No hand-filed events.** A check or control reaches the log only through `file_event.py`.
12. **A note's figures come from tool output.** Any number or hash in a note must appear verbatim in that
    step's printed output.

## Fallbacks
- **J1 cannot be made to pass both adjudicators:** v0.9.7 does not ship it. The site's three sentences
  change first, and the release says so.
- **The stranger test fails:** v0.9.7 ships as a candidate saying so, as v0.9.6 did.
- **The Maker cannot produce an acceptable revision** in its bounds: as v0.9.6.

## Bounds
3 revisions · **$40** evaluation spend · 14 days from freeze · at most **10** Owner decisions, with the
count reported in the release.

## Amendment 1 (2026-10-26, before work started)
**Ruled** by the Owner, Steve Moitozo II, on 2026-10-26 ("Proceed with Option A"); **ratified** when his
buyer and specialist approvals of this text's digest are logged. Drafted by Claude Opus 5.5 as
**Architect only**. Made after the bar was frozen and before `work-started`; no Maker
session had run and nothing had been scored. It changes J1's kind, and two things that follow from it:
J1's done-when adds the CHANGELOG listing that SPEC.md section 8 requires of every breaking change, and
ratification item 1 counts two breaking changes. No threshold, gate, seat, fallback or bound moves.
(Revision 3 corrects this sentence, which in revision 2 said the amendment changed J1's kind "and nothing
else"; the pre-read of revision 2 found that untrue. Nothing else in the bar changes.)

- **Why.** Every stricter reading of CL1-10 turns some record that reads `OK` under v0.9.6 into `FAILED`,
  which SPEC.md section 8 calls breaking; the only non-breaking J1 writes the v0.9.6 checker's behaviour
  into the text, and that change has no fixture that can fail before it. The frozen bar ratified one
  breaking change, so it could not be met as written.
- **The rule J1 makes the text decide.** From a disagreement's entry alone, a reader can see that the
  dimension's checks returned different outcomes: the disagreement names, for each outcome that
  dimension's checks returned, at least one check that returned it. A disagreement naming only checks
  that agree reads `FAILED`.
- **What it does and does not break.** No v0.9.6 fixture and no record published with v0.9.1 to v0.9.6
  changes its CL1-10 result (measured before ratification; the script and its output are kept). rec05,
  which names one check of each outcome, reads `OK` under the rule; both adjudicators had read the
  v0.9.6 text as failing it, and the release says so.

## Ratification items
1. The theme, and scope J1 to J7: two rule changes (J1, J2), **both breaking** (J2, kept as breaking: the
   Owner chose option A on 2026-10-25; J1, by Amendment 1), one editorial sentence (J3), and three
   process or tooling items.
2. The harness (47) and Orchestrator requalification (49) moved to a separate Plumbline job.
3. J4: `git apply --recount`, the fix the evidence supports (Owner, 2026-10-25); whole files only if v0.9.7 shows a failure `--recount` cannot fix.
4. J3: keep CL2-3(b)'s endpoint clause and state its reason.
5. The seats and independence, unchanged.
6. The gates, the two added process rules, the fallbacks and the bounds.
