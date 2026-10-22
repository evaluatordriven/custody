# Disposition — v0.9.4

**Approver:** Steve Moitozo II · **Decision:** given · **Time:** taken from the custody log's `disposition` event

**Given, as a v0.9.4 candidate.** This release repairs the contract that the v0.9.3 record passed while
breaking: readings are filed under the evaluators who gave them; every reader reads a control, and every
batch holds a clean one; check evidence binds to a file; model identity has a stated form; the bar must
be frozen before the work **started**; scores decide outcomes; a maker who wrote the bar says so. Under
these rules the v0.9.3 record reads `FAILED` (CR-2, CL1-1, CL1-4, CL1-8, CL1-9, CL1-16): the record has not
changed; the requirements have.

**Acknowledged as not passing: the stranger test.** Two cold implementers, given only SPEC.md and its
schema, did not both reach the threshold. In the first run one met it and one fell short; after a
wording-only revision, the one re-run left one implementer short and the other not counted, having
failed its controls. An uncounted diagnostic found that failure came from that session's own code, not
the wording. The full account is in `record/STRANGER-TEST.md`. Acknowledged as unobserved: that
implementer's re-run check.

**Also on record:** the blind key over all 103 fixtures matched the checker on every case; every changed
rule fails under the v0.9.3 checker and passes under v0.9.4; the orchestrator's process errors in the
stranger test are listed in the record's separation gaps. **Carried to v0.9.5, whose theme is whether a
stranger can implement the standard from its text alone:** a stranger test of at least three sessions
per implementer, scored by majority; CL1-17 and unscored checks; CL2-3; CL1-8 on malformed evidence; and
a clean control for every evaluator, not only every batch.
