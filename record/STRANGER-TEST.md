# The stranger test — v0.9.4

**Method.** Two cold implementers, each in a fresh session, given only SPEC.md, its JSON Schema, and twelve
custody records written by a third party who never saw the reference checker. Each wrote one verifier and ran
it on all twelve. An answer key, frozen before either ran, gives each record's verdict, level, routing and
failing requirement IDs. An implementer who gets a control record wrong is not counted. Pass requires both
counted implementers to match verdict, level and routing on at least 11 of 12 and failing IDs on at least 10.

## Run 1, against revision 0's text
- Seed 2.1 Turbo: 11 of 12, 10 of 12; both controls correct; counted; met both thresholds.
- MiniMax M3: 9 of 12, 9 of 12; both controls correct; counted; short of both thresholds.
- Nemotron 3 Ultra: 8 of 12, 7 of 12 — an extra reading. Its seat was taken because the orchestrator
  wrongly judged MiniMax unable to produce a runnable verifier; MiniMax could.
- Process notes: the orchestrator sent MiniMax a false diagnosis in an error round-trip (it said the file
  ended mid-statement; it did not), and MiniMax received three round-trips where the runbook allows two.
  The third exists because the second was defective.

## Revision 1 and why
All three implementers missed the same record group on CL2-3, and one record had the adjudicator ruling
CL1-8 two different ways. Revision 1 split CL2-3 into (a)–(c), added "One defect, one failure" to section 5,
and stated in section 6 which requirements are in scope. That changed the normative text, so the Owner's
decision 1 applied: one re-run, on the final text.

## The re-run, against revision 1's text
- MiniMax M3: 10 of 12, 9 of 12; both controls correct; counted; short of both thresholds by one.
- Seed 2.1 Turbo: 5 of 12, 1 of 12; **not counted** — it failed both controls, reading CL1-17 as failed on
  every record, including the one that should conform.

**The stranger test did not pass.**

## The diagnostic (uncounted; decides nothing about this release)
Two fresh Seed sessions on revision 0's text and two on revision 1's, to tell a wording effect from chance
on CL1-17.

- revision 0, session 1: 11 of 12, 10 of 12; both controls correct; CL1-17 failed on 0 records.
- revision 0, session 2: not obtained — the provider returned nothing in time.
- revision 1, session 1: not obtained — the provider returned nothing in time.
- revision 1, session 2: 11 of 12, 11 of 12; both controls correct; CL1-17 failed on 0 records.

What it shows: the same implementer reads CL1-17 correctly on revision 0's text and, in a fresh session on
revision 1's text, reads it correctly on all twelve records and meets both thresholds. The failed re-run's
"CL1-17 failed on every record" does not reproduce. Two obtained sessions cannot separate wording from
chance statistically, but the one session on revision 1's text that did arrive contradicts the wording
hypothesis and points at the re-run's own generation. The diagnostic remains uncounted and decides nothing
about this release; it is evidence against proposing revision 2.

## Carried to v0.9.5
- At least three sessions per implementer, scored by majority, so one session's bad generation is not read
  as a property of the text.
- CL1-17 and unscored checks: the text permits a verifier to fire it where no score exists.
- CL2-3: "no more than half" and `undisclosed` — implementers read both the other way, twice.
- CL1-8: one record had the adjudicator rule it both ways; the standard needs to say which.
