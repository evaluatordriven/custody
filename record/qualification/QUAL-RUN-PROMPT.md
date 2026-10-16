# Judge qualification run

You are the **Orchestrator** for a judge-qualification test. Follow this file and the attached bar
(`JUDGE-QUALIFICATION-BAR.md`) exactly. You judge nothing yourself: scripts apply a fixed pass rule.
Python standard library only. Never print or log an API key. **If you are an Anthropic (Claude) model, stop
now:** the Maker must never see the test set.

## 0. Inputs — verify, stop on any mismatch

| File | sha256 |
|---|---|
| `JUDGE-QUALIFICATION-BAR.md` | `08a51b69e58a1c90a6b0196c2491f1afe1949e0ec12386b639de0c2cdaa839db` |
| The DeepSeek test-set zip (`items/`, `ANSWERS.json`) | given by the Owner |
| `smoke/MANIFEST.sha256` | given by the Owner (it must include all five candidates) |

## 1. Candidates — five, from `smoke/config.json`

Grok 4.7 · GLM 5.3 Flash · NVIDIA Nemotron 3 Ultra · Qwen 3.8 2.4T · Amazon Nova Pro v1 (substituted for the
retired Nova Premier; QUALIFICATION-FREEZE entry 7).

**Standby (entry 4):** if GLM 5.3 Flash is not qualified, test **GLM 5.3** (`z-ai/glm-5.3`) the same way,
within the same budget. Seating still takes one model per family.

Use each one's exact ID and pinned provider from `config.json`, with no fallback. Stop testing a candidate,
and mark it `not tested`, if any response comes from a different provider or model ID. A candidate must have
passed its three smoke tests to be tested at all.

## 2. Calls

- Fresh context per call (one user message), no tools, temperature 0, **output cap 8,000 tokens**.
- **429s and network faults** (no response, timeout, 5xx): wait, honoring `Retry-After` (otherwise 5 s,
  15 s, 45 s, 2 min), and retry up to 6 times. Log every attempt; these are not readings.
- **A cap fault**, meaning no visible answer because reasoning used the whole cap: retry once at 16,000
  tokens. This is not a reading either.
- **A reply that does not parse:** one re-run. If it still does not parse, the item is a **miss**.
- Call the candidates concurrently, one request at a time per candidate.

## 3. The test — 12 items × 2 runs per candidate

For each run, shuffle the item order and, for label-swap items, the labels; record the seed. Send each item's
gate text and document text. **Never send `ANSWERS.json` or the item's `kind`.** Ask for exactly:

`{"outcome": "conforms|does_not_conform|unobserved", "evidence": "<verbatim quote from the text>", "failure_condition": "<one sentence>"}`

For label-swap items, also ask which label is defective (`"defective_label": "<label>"`), and tell the model
that exactly one of the copies is defective.

## 4. Pass rule (from the bar) — scripted, all or nothing

For each candidate, over both runs:
1. **Every planted item** reads `does_not_conform`. For label swaps, the named `defective_label` must be
   correct. `unobserved` is a miss.
2. **Every quote is verified:** after collapsing runs of whitespace to single spaces, the `evidence`
   string must appear verbatim in the text that was sent. A quote that does not appear is a miss, even
   when the outcome is right.
3. **Every clean item** reads `conforms`. `unobserved` is a miss.
4. **Every reply parses** (after the one permitted re-run).

Any miss means **not qualified**. No partial credit, and no second attempt for any candidate.

## 5. Budget

At most **$1.50 per candidate** and **$10.00 in total**. Do not start a call that would cross either; mark
the candidate `incomplete — budget` instead.

## 6. Outputs — `qual-results/`

- **`QUAL-RESULTS-OWNER.md`** — a five-line summary (qualified, not qualified, incomplete, spend), then
  per candidate: pass or fail **per item kind**, the misses with the item number, run, outcome and quote
  check, and the cost.
- **`QUAL-RESULTS-MAKER.md`** — per candidate only: `qualified` / `not qualified` / `incomplete`, and for
  each miss, the item **kind** (contradiction, omission, unsupported claim, label swap, clean) and the
  failure type (wrong outcome, quote not found, wrong label, unparsed). **No item text, no item numbers,
  no quotes, no answers.**
- **`SEATING.md`** — the qualified models, ranked by: different families first, then lower cost, then
  qualification order. The top three are proposed seats; the rest are reserves.
- `calls/` (every request with the key redacted, every response), `readings.jsonl`, and `MANIFEST.sha256`.
