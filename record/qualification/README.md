# The screening test's record

Before the previous release was evaluated, we screened AI models to find readers that could be trusted
to judge it. Each candidate read short passages, some with a deliberately planted mistake and some clean,
and had to find every mistake without flagging clean text. evaluatordriven.com promised to publish this
record with the next version. This is it, kept as it was written at the time.

| File | What it is |
|---|---|
| `JUDGE-QUALIFICATION-BAR.md` | The screening test's own bar: who could sit it, what it contained, and the pass rule, frozen before anyone was tested |
| `QUALIFICATION-FREEZE.md` | The log of the screening: every ruling, exclusion and result, in order |
| `QUAL-RUN-PROMPT.md`, `QUAL-RUN-PROMPT-R2.md` | The instructions the orchestrating agent followed in round 1 and round 2 |

## What happened

Eight models sat the test across two rounds. One, GLM 5.3, qualified. It later missed a planted defect in
the real evaluation, so that release's reader-judged checks were recorded as unobserved.

## The test's own flaws

The screening test had flaws of its own, and they shaped the results:

1. **The label scorer was too literal.** On side-by-side items the scorer expected "A" where models
   correctly answered "COPY A", the label exactly as shown. The Owner ruled that answers be read by the
   label they name, and the retained answers were re-scored, with no new calls.
2. **One item's question was badly worded.** The Owner found that a reader's objection to it was
   defensible, and the item was dropped for every candidate.
3. **The pass rule allowed no error at all.** One miss in 22 readings disqualified a model. With items
   that had not been checked in advance, that rule magnified every flaw in the test.
4. **The items were not validated before use.** No one confirmed each item's answer before it was used to
   judge others.

Some misses were real all the same: models passed over planted omissions and unsupported claims. In the
real evaluation that followed, one model quoted a requirement that had been deleted. **The honest reading is both:** the judges had real weak spots, and the
test overstated them by an amount it could not measure.

## What changed because of it

The next version's screening test is checked before use. Two people confirm every answer, the scorer reads
labels and quotes tolerantly, and the pass rule allows one defensible miss on clean text. Every
candidate, including any that passed before, sits the new test.

The test items and their answers are held by the Owner. They are not published here, so that a future
reader cannot study them.
