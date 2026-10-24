# Runbook: v0.9.6 seat qualifying tests

**Orchestrator:** VizH (DeepSeek v4.1), on the Owner's machine, in `~/evaluatordriven/v096/`. **Architect:**
Claude Opus 5.5 (author of this runbook). These tests decide the v0.9.6 seats before any bar is drafted
or frozen. Nothing here changes the standard.

**Disclosed conflict.** The Architect is the fallback Maker if Gemini 3.7 Flash does not qualify. The
Maker test is therefore scored only against what already shipped. The Architect's own revision 1 must
pass the same scoring as a clean control, and revision 0 must fail it as a planted control (§Q3).

## Rules for this run (carryovers 30–32, in force from here on)
1. **Log.** `record.py init V0.9.6-QUAL-LOG.jsonl`. Log each output as it happens.
2. **Kept by content.** Every file an event cites is first copied, write-once, to
   `evidence/<name>-<first 8 of sha256>.<ext>`, and the event cites that copy. Never edit a cited file. A
   correction is a new file with a new event.
3. **Scripted acceptance.** Every acceptance line below is checked by a script that prints the exact value.
   A note may cite only output a script printed. Any miss is a **STOP**.
4. **Instruments fixed before use.** Every script you write for scoring is pinned (sha256 in a log note)
   before its first scored run, and not edited after. If it is wrong, write a new one, pin it, and log
   why.
5. **Python** runs with `PYTHONDONTWRITEBYTECODE=1` and `-B`.
6. **Model calls:** a fresh session for every call; provider pinned, no fallback; no tools; default
   sampling settings, recorded. Every request and response is saved as
   `evidence/harness-<test>-<model>-<case>-<ask>.json`, together with the provider's report of which model
   and host answered.

## Inputs (verify each sha256 before use; any mismatch is a STOP)
| File | sha256 |
|---|---|
| `../v095/evaluatordriven-v0.9.5-candidate.zip` (revision 0) | `a807aae8b659e26e9a073255c67e8d584fc40699c6735312ee0c1149b2162de5` |
| `../v095/evaluatordriven-v0.9.5-candidate-rev1.zip` (revision 1) | `d8261b2b89a545d78cb445275f33e3c7f5db405b878dc4ec28130718c6896ec0` |
| `../v095/evaluatordriven-v0.9.5-rc8.zip` (published v0.9.5) | `887c6a3ad73b5851a27a07402ca638da4de3352c5176f516a068a4320680406a` |
| `../v095/REVISION-BRIEF-c1.md` | logged in the v0.9.5 job log; check against that log's hash |
| `make_plants.py` (this folder) | `49d4fc98405e710d9fba020a680227098d85ad10336514cceb2b1449177f2b52` |

Unzip each zip into its own new empty folder: `r0/`, `r1/`, `pub/`. In each, the repository is
`<folder>/evaluatordriven`.

**Spend cap:** $60. **STOP** before any call that would take the total past $50.

## Q0. Availability, then the cost projection
For each candidate: GPT 6.1 Sol, Grok 4.7, MiMo (the same model and route as v0.9.5), Kimi K2.5, Qwen 3.8,
GLM 5.3, Gemini 3.7 Flash.
- Pin the provider with no fallback, send one short call, and log: the exact identifier, the answering
  host, the price per million input and output tokens, and the sampling settings.
- A candidate that cannot be pinned is **unavailable** and does not run. Log it with the reason.
- Project the total spend of Q1–Q3 from these prices and the token counts of the real inputs. If the
  projection exceeds $50, **STOP** and report the projection.

## Q1. Adjudicators: GPT 6.1 Sol, Grok 4.7, MiMo
**Cases (24).**
- **Planted (10).** Run `python3 -B make_plants.py pub/evaluatordriven plants`. Acceptance:
  `plants/flips.json` has sha256 `3dbcd77cf5294e7aa5294ae0c8b45e2fba987d46a3f76e061883b3088e710a99`. Each
  of the 10 fixtures it lists is one case. Code shown: that plant's `check-<plant>.py`. Reading X: the
  published `fixtures/expected.json`. Reading Y: that planted copy's output.
- **Settled (14).** The 23 cases v0.9.5's D9 sent to adjudication (the blind key differed from the
  checker, and the ruling upheld the checker). Acceptance: exactly 23 found, and on each the key's reading
  differs from `expected.json`. Drop any that appear among the 10 planted cases. Order the rest by
  fixture name, then take `random.Random(96).sample(rest, 14)`. Code shown: the published
  `checker/check.py`. Reading X: `expected.json`. Reading Y: the v0.9.5 blind key's reading.
- **A reading** is the verdict, level achieved, routing, and the sorted failing IDs.

**Asks.** Every candidate gets every case **twice**, in fresh sessions. The first ask shows X as A and Y
as B; the second shows Y as A and X as B. Use the prompt in Appendix A, with the published `SPEC.md`, the
schema, the case record and its `files/` and `evidence/`, and the code shown. Neutral case names
throughout.

**Scoring** (`score_adj.py`, written and pinned by you). Parse `RULING: A | B | AMBIGUOUS` and map it
back to X, Y or ambiguous.
- **Correct** means the ruling chose X.
- **Contradiction** means the two asks map to different choices.
- **Withdrawn case.** A settled case where at least two of the three candidates choose Y on both asks is
  withdrawn from scoring. Report it as a possible text finding for the v0.9.6 bar.

**A candidate qualifies when all three hold:**
- planted: at least **18 of 20** asks correct;
- settled: at most **2** asks choose Y (ambiguous costs nothing);
- at most **1** contradiction across all 24 cases.

**Seats.** If both qualify, GPT 6.1 Sol and Grok 4.7. Otherwise, the qualifiers, ranked by planted
correct, then settled correct. Report the seated pair's agreement: the share of asks where both chose the
same non-ambiguous reading. Below 80%, **STOP** and report. Fewer than two qualifiers: **STOP** and report.

## Q2. Test author: Kimi K2.5, Qwen 3.8, GLM 5.3 (needs Q1's pair)
**Cases.** Repeat v0.9.5's D9 key step for each candidate: neutral names, shuffled, the map kept private.
Use all 111 published fixtures, except `expected.json`, with `files/` and `evidence/` beside them. Each
candidate gets a fresh session with SPEC.md, the schema and that folder only, and the v0.9.5 D9 prompt
unchanged. It never sees the checker.

**Scoring** (`score_author.py`, pinned). Per case:
- The key matches the published checker on verdict, level, routing and failing IDs: **correct**.
- A mismatch goes to both seated adjudicators, through Appendix A with the real code and the key as Y:
  - both choose X: **wrong**;
  - both choose Y: **correct**, and log a **checker finding** for the v0.9.6 bar;
  - they split, or either is ambiguous: **held out**.
- A case whose key names no SPEC.md sentence is **wrong**.

**Qualifies** at **≥ 90%** correct of the cases not held out. **Seat:** the highest qualifying accuracy;
on a tie, the lower cost. Report all three candidates, and every checker finding with its fixture name.

## Q3. Maker: Gemini 3.7 Flash (needs Q1's pair for M4)
**Sessions.** Three fresh sessions. Each gets the Appendix B prompt, `REVISION-BRIEF-c1.md`, and from
`r0/evaluatordriven`:
- in full: `SPEC.md`, `checker/check.py`, `fixtures/generate.py`, `tests/run_fixtures.py`,
  `tools/count.py`, `.github/workflows/ci.yml`, `schema/custody-v1.schema.json`, `CHANGELOG.md`;
- a listing of every file path.

The reply is one unified diff.

**Harness**, per session, on a fresh copy of `r0/evaluatordriven`:
1. `git apply` the diff.
2. Run `python3 fixtures/generate.py`.
3. Run every `ci.yml` step except the advisory reading-level step, on Python 3.12 or the closest
   available (log which).

At most **two** error round-trips per session. The harness sends the failing command's own output,
copied by code, under this line only: "Your diff failed with this output. Reply with a corrected unified
diff against the original revision 0 tree." No person or model writes, shortens or explains it.

**Scoring** (`score_maker.py`, pinned). Each session passes M1 to M5:
- **M1 Applies.** The final diff applies, and `generate.py` runs.
- **M2 CI.** Every gated CI step passes.
- **M3 Behaviour matches what shipped.** Copy `r1/evaluatordriven`, put the session's `checker/check.py`
  in it, and run `tests/run_fixtures.py`. All 111 cases must read `ok`.
- **M4 The text closes D-1 and D-2.** Each seated adjudicator gets the session's `SPEC.md` and the four
  questions in Appendix C, in one fresh session per question. Every answer must equal the expected answer
  in Appendix C.
- **M5 No unrelated change.**
  - Changed files are limited to `SPEC.md`, `checker/check.py`, `fixtures/**`, `tests/run_fixtures.py`,
    `CHANGELOG.md` and `schema/custody-v1.schema.json`.
  - In `SPEC.md`, the set of requirement IDs (table rows matching `^\| (CR|BL|CL\d)-\d+ \|`) is unchanged.
  - Every requirement row other than CR-2 and BL-1 is byte-identical to revision 0.
  - Every heading line (starting with `#`) is unchanged.

**Controls, run before any session.** The tree of `r1/evaluatordriven` (the shipped revision 1) must pass
M2 to M5. The tree of `r0/evaluatordriven` must fail M3 and fail M4. Acceptance for these two controls:
- revision 0's checker reads `FAIL` on 106 of the 111 revision-1 cases;
- revision 1 changes exactly one requirement row, CR-2.

If either control comes out otherwise, **STOP**.

**Qualifies** if at least **two of three** sessions pass M1 to M5, and **no session fails M5**. A session
that changes unrelated rules is disqualifying however the others do.

## Q4. Report, then STOP
Write `QUAL-REPORT-V096.md` **by script from the score files**, then **STOP**. It covers:
- per candidate: available or not, the identifier and host, pass or fail, and each threshold's number;
- the seats this produces, against the frame's proposal;
- the seated adjudicator pair's agreement rate;
- the author checker findings and any withdrawn settled cases;
- spend against the cap, and the log's verify line.

**If Gemini does not qualify,** state the consequence. The fallback Maker is Claude, so the Architect
seat must move off Claude (the frame proposes Grok 4.7), and the second adjudicator seat goes to the next
qualifier. The seats are the Owner's decision, made when the bar is ratified.

---

## Appendix A — adjudicator prompt (verbatim)
> You are adjudicating how a custody record should be read under the specification below. You are given
> SPEC.md, the JSON schema, one record with its files and evidence, and the source code of a checker.
> Two readings of the record follow, labelled A and B. Each gives the verdict, the level achieved, the
> routing, and the requirement IDs that read FAILED. The checker's code may be correct or may contain a
> defect; SPEC.md governs. Decide which reading SPEC.md requires. Reply with exactly one line `RULING: A`,
> `RULING: B`, or `RULING: AMBIGUOUS` (only if two careful readers of SPEC.md could defend both), then the
> SPEC.md sentence that decides it, quoted, then at most three sentences of reasons.

## Appendix B — maker prompt (verbatim)
> You maintain the Evaluator Driven specification. Below are files from the repository at revision 0, a
> list of every file in it, and an evaluator's revision brief. Revise the repository to close D-1 and D-2
> in the brief; D-3 asks nothing of you. Change only what the brief requires: the normative text, and
> whatever must change with it (the checker, `fixtures/generate.py`, the tests, the schema, a CHANGELOG
> line). Add at least one fixture through `fixtures/generate.py` that fails under revision 0's checker and
> passes under yours. Do not edit generated fixture files; the harness runs `fixtures/generate.py` after
> applying your change. Reply with one unified diff against the repository root (`a/` and `b/` paths),
> applicable with `git apply`, and nothing else.

## Appendix C — text questions for M4 (verbatim; one fresh session each, SPEC.md attached)
1. "Using only the BL-1 requirement and the `readsBeforeFreeze` row of section 4's table: a record claims
   CL1 and has no `readsBeforeFreeze` field. Is it held to BL-1? Answer YES or NO, then quote the
   deciding sentence." **Expected: NO.**
2. "Using only the opening paragraph of section 5: the same record. Is it held to BL-1? Answer YES or
   NO, then quote the deciding sentence." **Expected: NO.**
3. "The same record. Does CR-2 report it for the missing `readsBeforeFreeze`? Answer YES or NO, then
   quote the deciding sentence." **Expected: NO.**
4. "A record claiming CL1 omits the `violations` field. Under CR-2 and 'one defect, one failure', which
   single requirement reports it? Answer with one requirement ID, then quote the deciding sentence."
   **Expected: CL1-11.**
