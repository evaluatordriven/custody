# The bar: v0.9.6 of `smoitozo/evaluatordriven`

**Ratified** by the Owner, Steve Moitozo II, as buyer and specialist on 2026-10-23, effective when the
Orchestrator was seated. Drafted by Claude Opus 5.5 as **Architect only**. The Maker is Gemini 4 Argon,
so this is the first release in which the Architect does not make the artifact. This page inherits the
v0.9.5 bar **except where it changes it**. It names no private person, so it can be published as it
stands and CL1-14 checked against it. Nothing is built before it is frozen.

## The job
- **Start from:** the `v0.9.5` tag, `ce05088`.
- **Site ground truth:** site commit `136a280` (tree `0678e29`), confirmed live before freeze.
- **Theme: run the evaluation independently of the maker.** In v0.9.5 the process fell short of what
  the standard asks of others:
  - the Maker designed the test of its own work, and once changed the frame mid-test;
  - the Orchestrator wrote notes from intent rather than from output;
  - two of the Architect's instruments scored a preferred design rather than the rules.

  v0.9.6 seats a qualified, independent Maker, makes the process scripted and checkable, and adds a
  stranger-test measure that tells an unclear sentence from one session's coding failure.
- **Stated assumption, not a gate:** demand comes through Plumbline. The signal: *a team outside Ligonier
  asks for the records Plumbline produces.*

## Seats (qualified before this bar; the evidence ships in `record/qualification-v0.9.6/`)
| Seat | Holder | Qualified by |
|---|---|---|
| Maker | Gemini 4 Argon | 2 of 3 sessions rebuilt v0.9.5's revision 1 from its brief under the corrected scoring. All four controls held. Eight other models were tried; none qualified. |
| Architect (bar, runbooks, scoring, controls) | Claude Opus 5.5 | Not tested. Holds no making seat, and writes no artifact content. |
| Adjudicators (both must agree; a split is held out) | GPT 6.1 Sol, MiMo v2.6 Pro | 20/20 planted and 0/28 settled wrong each; 48/48 agreement |
| Test author (records, blind keys, controls) | GLM 5.3 | 98.2% blind over 111 fixtures. Reserve: Qwen 3.8 (98.2%). |
| Orchestrator | DeepSeek v4.1 Flash 1017 | Second seven-trap trial, built from v0.9.5's failures: every integrity trap passed, and it asked before choosing. Three other candidates ran or were routed; none did as well. |
| Stranger implementers | Seed 2.1 Turbo, MiniMax M3, Nemotron 3 Ultra | Unchanged, for continuity |
| Owner, buyer, specialist and approver | Steve Moitozo II | One person in several seats (disclosed) |

**Adjudicator** is this job's term, not the standard's. An adjudicator rules on disputed answers and is
not an evaluator in SPEC.md's sense: it files no check and reads no control. Its rulings, with the code
it read, are kept as evidence and published in the qualification and stranger-test records.

**Independence.**
- **Required by the standard:**
  - **CL1-6:** no evaluator is the maker or the bar's author, and no script evaluator's script is
    written by either.
  - **CL2-3,** if CL2 is ever claimed: the maker did not write the bar; one model evaluator differs from
    it in both family and endpoint; the maker's family is at most half of each dimension's evaluators.
- **Chosen for this release, for ratification:**
  - **(a)** The Maker's family is not among the stranger implementers. A same-family implementer is not
    a stranger.
  - **(b)** The Maker's family is neither the test author's nor an adjudicator's. Those seats decide the
    answers.
  - Argon (`gemini`) meets both.
- **Not required:** distinct families across the other seats.

## Scope: four items, nothing else
Every changed rule ships with a fixture that fails before the change and passes after.

| # | Item | Kind | Done when |
|---|---|---|---|
| I1 | **A clarity measure beside the gate.** For each requirement ID, the share of counted sessions in the last cycle whose `FAILED` set agrees with the answer on that ID. Published with the scores. A requirement read wrongly by most counted sessions is named in the disposition as a text defect. The pass rule itself is unchanged from v0.9.5. | Gate | Published for every cycle |
| I2 | **CL2-3 reads undisclosed families the least favourable way.** An undisclosed maker needs evaluators from at least two disclosed families. The half rule counts the largest disclosed family plus every undisclosed evaluator. | Rule | Fixtures for both of the Owner's examples (an Anthropic maker with OpenAI and DeepSeek evaluators; an undisclosed maker with Anthropic and OpenAI evaluators), each at the boundary |
| I3 | **Say what CL1-17 does when the scale is broken.** On a record whose dimension has an impossible threshold, the checker reports only CL1-2, while a blind key and both adjudicators also reported CL1-17. Add one sentence to CL1-17: it does not judge a check whose dimension's scale CL1-2 fails. | Editorial | `cl1-fail-threshold-above-scale` still reads CL1-2 only, and both adjudicators, given the new text and the code, agree the text and the checker match |
| I4 | **Publish the qualification.** `record/qualification-v0.9.6/` holds every qualifying runbook, scorer, control result and report, the corrected Maker scoring and the reason for it, and both Orchestrator trials. | Record | `count.py` clean, every file named in the record by digest |

**Out of scope:**
- guide and plain-view rewrites; purpose and audience;
- lineage records and CL4;
- a chain anchor;
- the Sigstore verifier (built when a record needs CL3);
- a `builder` field (carryover 28);
- crosswalks and certification;
- a CL2 claim. It is in reach with this seating, and deferred so that one release does not change both
  its seats and its level.

## The gate: the stranger test
As v0.9.5, with three changes:
- **Records** come from GLM 5.3, which never sees the checker.
- **Answers:** where GLM's key and the checker disagree, both adjudicators rule, each with SPEC.md, the
  record and `checker/check.py`. If they agree, that is the answer. If they split, the record is held
  out.
- **Published beside the scores:** I1's clarity measure.

Everything else is unchanged:
- three implementers, three fresh sessions each, on a fresh set of twelve records per cycle;
- a planted and a clean control, validated before any session runs;
- A ≥ 11 and B ≥ 10 in at least two counted sessions meets the bar;
- every observed implementer must meet it, and at least two must be observed;
- up to three cycles, each only after a normative revision the previous cycle's notes justify;
- every cycle published, and the last one stands.

## The other gates
| Gate | Passes when |
|---|---|
| D9 (GLM's blind key over every fixture) | The checker matches every blind case. Each mismatch goes to both adjudicators with the code, and a split is held out. |
| Red tests | Each changed rule's fixtures fail before and pass after |
| CI | Green on both Python versions |
| Own record | **OK at CL1** against the **unpacked release package**, publicly checkable except CL1-8 and CL1-15 |

## Process: rules for every seat (from v0.9.5's evidence)
1. **Adjudication with code.** Every ruling that can bear on whether the checker is right gets
   SPEC.md, the record and `checker/check.py`.
2. **Feedback to the Maker** always carries the shortfall. It carries a remedy only where the evaluator
   has real insight; a remedy is never invented.
3. **The Maker is blind.** It never sees a record, answer, control or implementer output, including
   through its own questions. It gets counts, requirement IDs and the adjudicators' sentence-level notes.
4. **Changes inside a loop** answer only what the evaluator reports. Anything else goes to the next bar.
5. **Scripted, not written.**
   - Every acceptance step is a script with an exact expected output.
   - A note may cite only output a script printed.
   - Published results about a record come from `tools/verify_note.py`.
   - Every check runs against the unpacked package.
6. **Kept by content.** Every file the log cites is first copied, write-once, to
   `evidence/<name>-<sha8>.<ext>`. Pins cite the kept copy. A growing file is cited by a snapshot. A
   correction is a new file with a new event, never an edit. `verify --files` comes back clean by
   construction.
7. **Instruments are fixed before use.** Every scoring script is pinned before its first scored run and
   never edited afterwards. Builders take their target tree and the producing event as required
   arguments.
8. **The Architect's instruments are read first.** Before any scored run, a seated adjudicator reads
   the runbook and the scorer together and lists every scored behaviour the rules don't require. Each
   item is fixed or justified before the run.
9. **File transfers** are verified by hash on the receiving machine, every file, every time.
10. **Freeze promptly** after ratification.

## Fallbacks
- **An implementer's sessions keep failing to run:** that implementer is unobserved, and there is no
  replacement seat.
- **The Maker cannot produce an applicable revision** after its two error round-trips: that revision
  counts as used. Claude cannot stand in, because it wrote this bar (CL2-3 (a)). Whether to seat another
  Maker is the Owner's decision, under a new bar.
- **The stranger test fails:** v0.9.6 ships as a candidate saying so, with every session's scores and
  the clarity measure.

## Bounds
3 revisions · **$40** in evaluation spend (two adjudicators now rule on every dispute) · 14 days from
freeze · at most **10** Owner decisions.

## Ratification items
1. The theme, and scope I1 to I4, with **one rule change** (I2), one editorial sentence (I3), and no
   breaking change. No existing fixture's expected answer changes.
2. The seats as qualified, with DeepSeek v4.1 Flash 1017 as Orchestrator.
3. Independence: the two required rules, and the two chosen rules (a) and (b).
4. The gate: v0.9.5's unchanged, with the clarity measure published beside it, and the adjudication
   and answer changes above.
5. The ten process rules.
6. The fallbacks and bounds.
