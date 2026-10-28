# Stranger test — v0.9.7 (candidate)

Written by `gen_stranger_doc_v097.py` from the cycle's score files.

## Method

Twelve fresh records per cycle, written by the test author, who never saw the checker. The answers were settled before any session ran: where the author's key and the checker agreed, that was the answer; where they disagreed, both adjudicators ruled with the record and the checker's code in front of them. A planted and a clean control were validated before any session ran. Three implementers, three fresh sessions each. A session counts only if it reads both controls correctly; it meets the gate at A >= 11 and B >= 10, where A is verdict, level and routing together and B is the sorted set of FAILED requirement IDs. The cycle passes when every observed implementer meets the gate, with at least two observed.

## Cycle r2

| implementer | counted | meeting | A | B | observed |
|---|---|---|---|---|---|
| MiniMax M3 | 0 of 3 | 0 | — | — | no |
| Nemotron 3 Ultra | 3 of 3 | 0 | 10, 10, 10 | 7, 8, 7 | yes |
| Seed 2.1 Turbo | 3 of 3 | 3 | 12, 12, 12 | 11, 10, 11 | yes |

**Result: cycle r2 does not pass.** 2 of the 3 implementers were observed, and 1 met the gate. The bar requires every observed implementer to meet the gate and at least two to be observed, so the cycle fails on Nemotron 3 Ultra. MiniMax M3 was unobserved.

## Session detail

| implementer | session | counted | A | B | meets | controls failed |
|---|---|---|---|---|---|---|
| MiniMax M3 | 1 | no | 1 | 0 | no | clean, planted |
| MiniMax M3 | 2 | no | 6 | 11 | no | clean |
| MiniMax M3 | 3 | no | 2 | 5 | no | clean, planted |
| Nemotron 3 Ultra | 1 | yes | 10 | 7 | no | — |
| Nemotron 3 Ultra | 2 | yes | 10 | 8 | no | — |
| Nemotron 3 Ultra | 3 | yes | 10 | 7 | no | — |
| Seed 2.1 Turbo | 1 | yes | 12 | 11 | yes | — |
| Seed 2.1 Turbo | 2 | yes | 12 | 10 | yes | — |
| Seed 2.1 Turbo | 3 | yes | 12 | 11 | yes | — |

A session that fails either control is not counted and its scores are not used.

## Clarity measure (I1)

For each requirement ID, the share of counted sessions whose FAILED set agrees with the answer on that ID, over all twelve records.

| requirement | share |
|---|---|
| BL-1 | 6/6 |
| CL1-1 | 6/6 |
| CL1-10 | 3/6 |
| CL1-11 | 6/6 |
| CL1-16 | 6/6 |
| CL1-17 | 6/6 |
| CL1-2 | 6/6 |
| CL1-3 | 6/6 |
| CL1-4 | 4/6 |
| CL1-9 | 5/6 |
| CL2-3 | 18/24 |
| CR-2 | 9/12 |

## Known issue carried by this candidate

**CL1-10 is open.** Both seated adjudicators ruled that SPEC.md requires the implementer's reading at CL1-10: where checks of one dimension return different outcomes, `disagreements` names that dimension and the checks. The record the answer was built from named only some of the checks whose outcomes differed. The frozen answer stands because it was settled before any session ran, so the scores are unaffected. No counted session reached the key's reading of CL1-10 on that record. This candidate ships with CL1-10 open and says so.

## J1

J1 (the CL1-10 repair) was withdrawn from this release under Amendment 2 rule 5 after three adjudicator splits. It moves to the next version. See the release record's separationGaps for the event numbers.

## Spend and custody

Every session's request and response is kept in the job's evidence folder, named by content, with the provider's report of which model and host answered. The job log is `V0.9.7-JOB-LOG.jsonl`.
