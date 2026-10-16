# Judge qualification bar — for the next job (v0.9.1)

**RATIFIED by the Owner, 2026-10-12 ("Yes"), Grok included** · Drafted by Claude Opus 5.5, the Maker of the spec these judges will
read: **a conflict**, since a Maker benefits from lenient judges. The pass rule below is strict on purpose,
and the Owner ratifies it. Nothing is tested until this is frozen (sha256 and timestamp).

## Purpose
Seat only reader-judges that have been shown able to say no, **before** the next job's bar freezes.
Qualified judges that are not seated become **reserves**, so a seat lost mid-batch has a proven
replacement waiting.

## Eligibility (decided before any test)
- **Not:** Anthropic (the Maker); the next job's answer-key author; its cold implementers.
- **Tier:** a flagship or pro model. No flash, lite or mini tiers: both lenient judges that lost seats
  were flash-class or gave lenient readings.
- **Serving:** a zero-data-retention provider that can be pinned with no fallback. A dated model ID is
  preferred.
- **Out:** Gemini 3.8 Flash and MiMo v2.6 Pro. Both missed planted defects aimed squarely at the gates
  they read, under the corrected protocol (FREEZE-ADDENDUM-1 entries 51, 55).
- **In, recorded:** **Grok 4.7.** Its batch 1 seat loss came on a self-state plant that the flawed
  batch-1 prompt routed to readers; the corrected protocol routes that class to the mechanical check only
  (entries 16, 20). This line is drawn before any qualification result exists.
- **In:** GLM 5.3 Flash (to re-confirm) and MiniMax M3. GLM is grandfathered despite its tier, because it
  is the one judge that held its seat through every batch. It must still pass this test.
- **Candidates:** three or four new families, listed by the smoke agent. Possibilities include ByteDance
  Seed, NVIDIA Nemotron, Meta Llama and Amazon Nova.

## Test set: written by DeepSeek v4.1 Flash, held from the Maker
Taken from the v0.9.0 candidate (revision 3): `SPEC.md`, `README.md` and `CONTRIBUTING.md`.

| Kind | Count | Tests |
|---|---|---|
| Contradiction | 2 | A sentence that contradicts another file, or the site snapshot |
| Omission | 2 | A requirement removed while something else still depends on it |
| Unsupported claim | 2 | Adoption, endorsement, or a level the record does not support |
| Label swap | 2 | Real and planted copies side by side, labelled at random; the judge must name the defective one |
| Clean | 4 | Unchanged, or editorial-only changes, to catch judges that fail everything |

## Protocol
1. **Smoke test** first: IDENTITY, CONTROL-FAIL, CONTROL-PASS on a pinned provider.
2. **Twelve items × two runs.** Each item in a fresh context, temperature 0, output cap 8,000 tokens.
   Order and labels randomized per run.
3. **The reply** is JSON: outcome (`conforms`, `does_not_conform` or `unobserved`), a verbatim quote as
   evidence, and the failure condition. One re-run is allowed only for an unparseable reply.

## Pass rule — all or nothing
1. **Every plant** reads `does_not_conform` on both runs.
2. **Every quote is verified by script** to appear **verbatim** in the text the judge was given. This
   catches a judge "quoting" something that is not there, which is how MiMo failed.
3. **Every clean copy** reads `conforms` on both runs.
4. **Every reply parses.**

Any miss means **not qualified**. No partial credit, and no re-testing a model that failed.

## Seating
- **Three seats** from qualified models, from three different families, cheapest first among equals.
- **The rest are reserves,** in qualification order.
- **Fewer than three qualify:** the Owner decides before the next bar freezes, never during a batch.

## Bounds and record
- **Budget:** $10 in total, at most $1.50 per candidate.
- **Run by** a non-Anthropic orchestrator; it reports pass/fail per model and per kind, with no test
  contents to the Maker.
- **Kept with the next job's bar:** the qualification results, frozen. Each seated judge's run log is
  its CL1-15 configuration evidence.

## Ratification items
1. Eligibility as above, **Grok included**.
2. DeepSeek v4.1 Flash as test author.
3. The $10 budget.
4. The candidate list, from the smoke agent, before testing.
