# Stranger test — v0.9.6 (candidate)

Written by `gen_stranger_doc.py` from the cycle's score files and its corrected cycle file.

## Method

Twelve fresh records per cycle, written by the test author, who never saw the checker. The answers were settled before any session ran: where the author's key and the checker agreed, that was the answer; where they disagreed, both adjudicators ruled with the record and the checker's code in front of them. A planted and a clean control were validated before any session ran. Three implementers, three fresh sessions each. A session counts only if it reads both controls correctly; it meets the gate at A >= 11 and B >= 10, where A is verdict, level and routing together and B is the sorted set of FAILED requirement IDs. The cycle passes when every observed implementer meets the gate, with at least two observed.

## Cycle 1

| implementer | counted | meeting | A | B | observed |
|---|---|---|---|---|---|
| minimax | 1 of 3 | 0 | [5, 10, 5] | [0, 10, 0] | no |
| nemotron | 2 of 3 | 0 | [7, 9, 10] | [9, 7, 8] | yes |
| seed | 3 of 3 | 3 | [12, 12, 11] | [11, 12, 12] | yes |

**Result: cycle 1 does not pass.** Observed implementers were nemotron, seed: 2 of the 3 implementers were observed, and 1 met the gate. The bar requires every observed implementer to meet the gate and at least two to be observed, so the cycle fails on nemotron.

## Rulings

12 disagreements were the implementer's error; 1 was a text finding, where both adjudicators read the specification the implementer's way; 0 were held out.

## Known issue carried by this candidate

**CL1-10 is open.** Both seated adjudicators ruled that SPEC.md requires the implementer's reading at CL1-10: where checks of one dimension return different outcomes, `disagreements` names that dimension and the checks. The record the answer was built from named only two of the four checks whose outcomes differed. The frozen answer stands because it was settled before any session ran, so the scores are unaffected; the text is not fixed, because the Maker's revision did not apply and the revision counts as used. This candidate ships with CL1-10 open and says so.

## Clarity measure (I1)

For each requirement ID, the share of counted sessions whose FAILED set agrees with the answer on that ID, over all twelve records.

| requirement | share |
|---|---|
| CL1-11 | 0.5 |
| CL1-17 | 0.5 |
| CL1-10 | 0.6667 |
| CL2-3 | 0.6667 |
| CR-2 | 0.6667 |
| CL1-8 | 0.8333 |
| CL2-1 | 0.8333 |
| BL-1 | 1.0 |
| CL1-1 | 1.0 |
| CL1-12 | 1.0 |
| CL1-13 | 1.0 |
| CL1-14 | 1.0 |
| CL1-15 | 1.0 |
| CL1-16 | 1.0 |
| CL1-2 | 1.0 |
| CL1-3 | 1.0 |
| CL1-4 | 1.0 |
| CL1-5 | 1.0 |
| CL1-6 | 1.0 |
| CL1-7 | 1.0 |
| CL1-9 | 1.0 |
| CL2-2 | 1.0 |
| CR-1 | 1.0 |

## Beside the frozen scores

rec05-cl2-undisclosed-maker-two-families read as both adjudicators read it: {'verdict': 'FAILED', 'levelAchieved': 'none', 'routing': 'none', 'failing': ['CL1-10']}. The frozen scores are the cycle's scores; these are published beside them.

| implementer | session | frozen A/B | under the adjudicators' reading | meets |
|---|---|---|---|---|
| seed | 1 | 12/11 | 11/10 | yes |
| seed | 2 | 12/12 | 11/11 | yes |
| seed | 3 | 11/12 | 10/11 | no |
| minimax | 2 | 10/10 | 11/11 | yes |
| nemotron | 2 | 9/7 | 9/7 | no |
| nemotron | 3 | 10/8 | 11/8 | no |

## Spend and custody

Every session's request and response is kept in the job's evidence folder, named by content, with the provider's report of which model and host answered. The job log is `V0.9.6-JOB-LOG.jsonl`.
