# QUAL-REPORT-V096 — v0.9.6 seat qualifying tests

Written by `scripts/report_v2.py` from the score files in this folder. Runbook `AGENT-RUNBOOK-V096-QUAL.md`, sha256 `8129a7bf…ff3e6`, verified before use.

Owner rulings given during the run are in `V0.9.6-QUAL-LOG.jsonl`: the non-ZDR credential; the maker fallback chain (3.7 Flash → 3.8 Flash → 4 Argon, each with its own Q0 and projection); and the roster direction (MiMo as the second adjudicator beside GPT 6.1 Sol, GLM 5.3 as author, Grok 4.5/4.6/4.7 evaluated for Maker, DeepSeek 4.1 Flash 1017 and Kimi K3 for Orchestrator).

## Q0 — Availability and cost projection

| Candidate | Identifier | Answering host | Available | $/M in | $/M out |
|---|---|---|---|---|---|
| gpt-6.1-sol | `openai/gpt-6.1-sol` | OpenAI | yes | 1.0 | 5.0 |
| grok-4.7 | `x-ai/grok-4.7` | xAI | yes | 2.0 | 6.0 |
| mimo-v2.6-pro | `xiaomi/mimo-v2.6-pro` | Xiaomi | yes | 0.435 | 0.87 |
| kimi-k2.5 | `moonshotai/kimi-k2.5` | SiliconFlow | yes | 0.5 | 2.5 |
| qwen3.8 | `qwen/qwen3.8-max-0902` | Alibaba | yes | 2.0 | 6.0 |
| glm-5.3 | `z-ai/glm-5.3` | Z.AI | yes | 1.4 | 4.4 |
| gemini-3.7-flash | `google/gemini-3.7-flash` | Google | yes | 0.375 | 1.875 |

Projection: **$18.69** raw, $23.37 with contingency, against the $50 stop — cleared.


Maker candidates, each with its own Q0 (pin, host, price) before any session:

| Candidate | Identifier | Answering host | $/M in | $/M out |
|---|---|---|---|---|
| gemini-3.8-flash | `google/gemini-3.8-flash` | Google | 0.375 | 1.875 |
| gemini-4-argon | `google/gemini-4-argon` | Google | 2 | 10 |
| seed-2.0-code | `bytedance-seed/seed-2.0-code` | Seed | 0.5 | 3 |
| kimi-k2.7-code | `moonshotai/kimi-k2.7-code` | SiliconFlow | 0.8592 | 3.8 |
| deepseek-v3.2 | `deepseek/deepseek-v3.2` | GMICloud | 0.2088 | 0.3096 |
| grok-4.7 | `x-ai/grok-4.7` | xAI | 2 | 6 |
- **gemini-3.8-flash** — host Google, $0.375/$1.875 per M, revised total $34.84 → under the cap
- **gemini-4-argon** — host Google, $2.0/$10.0 per M, revised total $39.31 → under the cap

## Q1 — Adjudicators

| Candidate | Planted (need ≥18/20) | Settled choosing Y (need ≤2/28) | Contradictions (≤1) | Unresolved | Result |
|---|---|---|---|---|---|
| gpt-6.1-sol | 20/20 | 0/28 | 0 | 0 | **qualifies** |
| grok-4.7 | 19/20 | 0/28 | 0 | 1 | **qualifies** |
| mimo-v2.6-pro | 20/20 | 0/28 | 0 | 0 | **qualifies** |

**Seats:** gpt-6.1-sol, grok-4.7. The frame proposed GPT 6.1 Sol and Grok 4.7; that pair qualified and the proposal stands.

**Seated pair agreement:** 100.0% (need ≥80%).

**Withdrawn settled cases:** 0 (none).

## Q2 — Test author

| Candidate | Correct | Wrong | Held out | Accuracy (need ≥90%) | Result |
|---|---|---|---|---|---|
| kimi-k2.5 | 95 | 16 | 0 | 85.6% | does not qualify |
| qwen3.8 | 108 | 2 | 1 | 98.2% | **qualifies** |
| glm-5.3 | 109 | 2 | 1 | 98.2% | **qualifies** |

**Author seat:** glm-5.3

**Checker findings:** 1
- `cl1-fail-threshold-above-scale` — the author key and the checker disagree and both seated adjudicators chose the key. A finding for the v0.9.6 bar.

**Held out:** `cl1-fail-evidence-name-not-relative` (qwen3.8)

## Q3 — Maker

**Controls (before any session):** revision 1 passes M2, M3, M4, M5; revision 0 fails M3 reading FAIL on 106 of 111 revision-1 cases and fails M4 on questions 2 and 3; revision 1 changes exactly ['CR-2'].

### gemini-3.7-flash — does not qualify (0 of 3 sessions pass; M5 violation: False)

| Session | Round-trips | M1 | M2 | M3 | M4 | M5 | Result |
|---|---|---|---|---|---|---|---|
| 1 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 2 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 3 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
- session 1: diff does not apply: error: corrupt patch at line 51

- session 2: diff does not apply: error: patch failed: CHANGELOG.md:19
error: CHANGELOG.md: patch does not apply

- session 3: diff does not apply: error: patch fragment without header at line 34: @@ -211,6 +211,7 @@ Each release is a git tag and is citable by commit. No implementation is part of


### gemini-3.7-flash (re-run, Argon's exact conditions) — does not qualify (0 of 3 sessions pass; M5 violation: False)

| Session | Round-trips | M1 | M2 | M3 | M4 | M5 | Result |
|---|---|---|---|---|---|---|---|
| 1 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 2 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 3 | 0 | pass | pass | pass | **FAIL** | pass | fails |
- session 1: diff does not apply: error: corrupt patch at line 53
- session 2: diff does not apply: error: patch failed: CHANGELOG.md:19

### gemini-3.8-flash — does not qualify (0 of 3 sessions pass; M5 violation: False)

| Session | Round-trips | M1 | M2 | M3 | M4 | M5 | Result |
|---|---|---|---|---|---|---|---|
| 1 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 2 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 3 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
- session 1: no diff produced
- session 2: no diff produced
- session 3: no diff produced

### gemini-3.8-flash (re-run, Argon's exact conditions) — does not qualify (0 of 3 sessions pass; M5 violation: False)

| Session | Round-trips | M1 | M2 | M3 | M4 | M5 | Result |
|---|---|---|---|---|---|---|---|
| 1 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 2 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 3 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
- session 1: no diff produced
- session 2: no diff produced
- session 3: no diff produced

### gemini-4-argon — does not qualify (0 of 3 sessions pass; M5 violation: True)

| Session | Round-trips | M1 | M2 | M3 | M4 | M5 | Result |
|---|---|---|---|---|---|---|---|
| 1 | 0 | pass | pass | **FAIL** | **FAIL** | **FAIL** | fails |
| 2 | 0 | pass | pass | **FAIL** | **FAIL** | pass | fails |
| 3 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
- session 3: diff does not apply: error: patch fragment without header at line 83: @@ -217,3 +219,3 @@

### seed-2.0-code — does not qualify (0 of 3 sessions pass; M5 violation: False)

| Session | Round-trips | M1 | M2 | M3 | M4 | M5 | Result |
|---|---|---|---|---|---|---|---|
| 1 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 2 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 3 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
- session 1: diff does not apply: error: corrupt patch at line 71
- session 2: diff does not apply: error: corrupt patch at line 22
- session 3: diff does not apply: error: corrupt patch at line 58

### kimi-k2.7-code — does not qualify (0 of 3 sessions pass; M5 violation: False)

| Session | Round-trips | M1 | M2 | M3 | M4 | M5 | Result |
|---|---|---|---|---|---|---|---|
| 1 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 2 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 3 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
- session 1: no diff produced
- session 2: diff does not apply: error: corrupt patch at line 11
- session 3: diff does not apply: error: corrupt patch at line 27

### deepseek-v3.2 — does not qualify (0 of 3 sessions pass; M5 violation: False)

| Session | Round-trips | M1 | M2 | M3 | M4 | M5 | Result |
|---|---|---|---|---|---|---|---|
| 1 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 2 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 3 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
- session 1: no diff produced
- session 2: diff does not apply: error: patch fragment without header at line 3: @@ -88,4 +88,7 @@
- session 3: diff does not apply: error: corrupt patch at line 68

### grok-4.7 — does not qualify (0 of 3 sessions pass; M5 violation: False)

| Session | Round-trips | M1 | M2 | M3 | M4 | M5 | Result |
|---|---|---|---|---|---|---|---|
| 1 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 2 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
| 3 | 2 | **FAIL** | **FAIL** | n/a | n/a | n/a | fails |
- session 1: diff does not apply: error: corrupt patch at line 33
- session 2: diff does not apply: error: patch fragment without header at line 148: @@ -447,2 +449,3 @@
- session 3: no diff produced


## Q3 v2 — Maker re-scored under Amendment 1

Amendment `QUAL-AMENDMENT-1.md`, sha256 `8df57d58…8559b`, verified before use. It found that Q3's semantic gates scored the Architect's own design of revision 1 rather than whether D-1 and D-2 are closed. `score_maker_v2.py` (pinned `90629b1c…`) re-scores every existing session; **no new maker session was started.**

**Controls (all four held before any re-scoring):** revision 1 passes M3 v2, M4 v2 and M5 v2; revision 0 passes M3 v2 at 111/111 and **fails M4 v2**; a valid alternative design (BL-1 in scope for every claim) passes M3 v2 at 111/111; the broken checker (plant P2) fails M3 v2 at 108/111. That revision 0 reads 111/111 is the amendment's central point — its behaviour was already right, and v1's M3 was scoring revision 1's reporting choice.

### Per candidate

| Candidate | v1 passing | v2 passing | v1 verdict | v2 verdict |
|---|---|---|---|---|
| gemini-3.7-flash | 0 of 3 | 0 of 3 | does not qualify | does not qualify |
| gemini-3.7-flash (re-run) | 0 of 3 | 1 of 3 | does not qualify | does not qualify |
| gemini-3.8-flash | 0 of 3 | 0 of 3 | does not qualify | does not qualify |
| gemini-3.8-flash (re-run) | 0 of 3 | 0 of 3 | does not qualify | does not qualify |
| gemini-4-argon | 0 of 3 | 2 of 3 | does not qualify | **qualifies** |
| seed-2.0-code | 0 of 3 | 0 of 3 | does not qualify | does not qualify |
| kimi-k2.7-code | 0 of 3 | 0 of 3 | does not qualify | does not qualify |
| deepseek-v3.2 | 0 of 3 | 0 of 3 | does not qualify | does not qualify |
| grok-4.7 | 0 of 3 | 0 of 3 | does not qualify | does not qualify |

### Per session

| Candidate | Session | v1 M1/M2/M3/M4/M5 | v1 | v2 M1/M2/M3v2/M4v2/M5v2 | v2 |
|---|---|---|---|---|---|
| gemini-3.7-flash | 1 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| gemini-3.7-flash | 2 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| gemini-3.7-flash | 3 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| gemini-3.7-flash (re-run) | 1 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| gemini-3.7-flash (re-run) | 2 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| gemini-3.7-flash (re-run) | 3 | pass/pass/pass/**F**/pass | fails | pass/pass/pass/pass/pass | **passes** |
| gemini-3.8-flash | 1 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| gemini-3.8-flash | 2 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| gemini-3.8-flash | 3 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| gemini-3.8-flash (re-run) | 1 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| gemini-3.8-flash (re-run) | 2 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| gemini-3.8-flash (re-run) | 3 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| gemini-4-argon | 1 | pass/pass/**F**/**F**/**F** | fails | pass/pass/pass/pass/pass | **passes** |
| gemini-4-argon | 2 | pass/pass/**F**/**F**/pass | fails | pass/pass/pass/pass/pass | **passes** |
| gemini-4-argon | 3 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| seed-2.0-code | 1 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| seed-2.0-code | 2 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| seed-2.0-code | 3 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| kimi-k2.7-code | 1 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| kimi-k2.7-code | 2 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| kimi-k2.7-code | 3 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| deepseek-v3.2 | 1 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| deepseek-v3.2 | 2 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| deepseek-v3.2 | 3 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| grok-4.7 | 1 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| grok-4.7 | 2 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |
| grok-4.7 | 3 | **F**/**F**/–/–/– | fails | **F**/**F**/–/–/– | fails |

*F = FAIL, – = not assessable (a gate never reached).*

### What the amendment changes

**gemini-4-argon qualifies as Maker under v2.** Under v1 no candidate qualified. The difference is entirely in the semantic gates: v1's M3 failed any checker that listed BL-1 as `OK` for a non-baseline claim, which was revision 1's reporting choice rather than something D-1 required, and v1's M4 required NO to a question the brief left open.

Under the runbook's bar — at least two of three sessions pass M1–M5, and no session fails M5 — the qualification holds. The third session of the qualifying candidate failed at M1, so its M5 is not assessable rather than failed.

## Seats and consequence

The maker seat goes to **gemini-4-argon**, which qualified under v2 — 2 of 3 sessions pass M1–M5 and no session fails M5. Under v1 the same candidate read 0 of 3, so the verdict turns on the amendment, not on the model's output changing.

Two consequences follow from the runbook's own logic. The fallback no longer applies: Claude does not hold Maker, so **the Architect seat does not have to move off Claude** — the runbook's stated trigger was "if no Gemini qualifies." And the second adjudicator seat stays with MiMo v2.6 Pro, since grok-4.7's release for the Maker test is no longer needed to free a seat.

| Seat | Holder | Basis |
|---|---|---|
| Adjudicator 1 | **gpt-6.1-sol** | Qualified 20/20 planted, 0/28 settled Y |
| Adjudicator 2 | **mimo-v2.6-pro** | Qualified 20/20 planted, 0/28 settled Y; 100% agreement with GPT 6.1 Sol (48/48). Owner's direction; grok-4.7 also qualified (19/20) and was released for the Maker test |
| Test author | **glm-5.3** | 98.2% (109/111); qwen3.8 qualified as reserve (98.2%, 108/110) |
| Maker | **gemini-4-argon** | 2 of 3 sessions pass under v2 |
| Architect | **Claude** (unchanged) | Maker qualified, so the runbook's move-off-Claude trigger does not fire |
| Orchestrator | **VizH on DeepSeek 4.1 Flash 1017** | In post by standing ruling. **Not tested — no instrument exists.** See below |

## Orchestrator seat — not evaluated

The Owner asked for `deepseek/deepseek-v4.1-flash-1017` and `moonshotai/kimi-k3` to be evaluated for Orchestrator. Neither was evaluated, and the reason is structural rather than a choice:

- **The runbook does not test this seat.** "Orchestrator" appears once in it, on line 3, naming the operator of the run. Q1–Q3 cover adjudicators, author and maker only.

- **No instrument exists** anywhere in this job folder. A seat cannot be qualified against a rubric that has not been written.

- **The incumbent cannot author it.** This run was orchestrated on DeepSeek 4.1 Flash 1017. Authoring, running and grading an instrument for one's own seat is the separation failure E-DI exists to prevent, and it would also shape a contest Kimi K3 is judged in.

Both models exist on the router and were reachable. The seat is blocked on authorship, not on access.


## Run defects and deviations

Recorded here because they change how much weight the maker verdict deserves.

| Item | What happened | Effect |
|---|---|---|
| **Harness defect (mine)** | The maker diff was applied to an already-committed tree, then the gated step `Fixtures are up to date` ran `git diff --exit-code`, which always saw the maker's own change. A second fault: the regenerated fixtures were not committed, though the runbook has the harness run `generate.py`. | That step **could not pass for any candidate**. Gemini 4 Argon's pre-fix M2 results are void. Fixed (apply → commit → generate → commit → steps) and re-run; Argon then passed M1+M2 on its first attempt twice. Logged as event 11. |
| **`max_tokens` is mine** | The runbook specifies default sampling and says nothing about output caps. I set 60,000, then 65,536, then 16,384 for Grok. | Gemini 3.7 never approached its cap (max 47,989, every reply closed its fence), so its result stands. Gemini 3.8 hit 57,605 of 60,000 with empty content, which is why the cap was raised. Grok 4.7 was truncated mid-diff at 16,384 in one attempt — a harness limit, not a model failure. |
| **`git apply` strictness** | I used plain `git apply`, the literal reading of "applicable with `git apply`". `--recount` is standard and more forgiving. | Tested: 3.7's session 1 diff applies only with synthesized `diff --git` headers plus `--recount`, and then fails M5 by deleting CR-1. The strictness did not decide any candidate. |
| **Q2 batching** | Ran as three batches per candidate rather than one session. | Forced: Kimi K2.5's 111-record prompt measured 247,509 of its 262,144-token context. Matches v0.9.5's own D9 step, which was also three batches. All three authors ran identically. |
| **Spend understated 3×** | Successive counters missed `response.usage`, double-counted merged author files, and missed maker usage written to `q3-*-sessions.json`. | Figures quoted mid-run ($19.89, $33.56) were wrong. True total is below. |
| **Test authorship conflict** | The Maker test was written by Claude Opus 5.5, which is also its fallback beneficiary; M3 scores candidates against revision 1, which Claude also wrote. | Disclosed in the runbook. The control passes, so the gate is not impossible — but the maker verdict should be independently re-checked before ratification. |

## Spend and custody

**Spend:** $30.65 against a $60 cap; the stop-before-$50 gate cleared at Q0 and at each fallback's revised projection.

**Log:** `V0.9.6-QUAL-LOG.jsonl` — `OK: 16 events, chain intact`

