# No custody record accompanies v0.9.8

**Status: no record. Not withheld — never produced.** Tag `v0.9.8` (`8a6bf1e`), cut 2026-11-04 from
`da2a3dd`.

Every release from v0.9.3 to v0.9.7 carries its record in this directory. This one does not, and this note
is here so that the absence reads as a decision with a reason rather than as an oversight. No check in this
repository failed when it shipped without one.

## Why it cannot be produced now

v0.9.8 was run as an **artifact repair**, not as a custody-instrumented job. Concretely:

- **The bar was not prior to the work.** A 35-gate bar was authored by the job's own Architect and frozen at
  its start on 2026-11-02, then amended during the job when the Owner ratified AMENDMENT-2. The referee that
  judged the work grew from 19 implemented gates to 36 checks while the work proceeded. Custody asks for a
  bar that exists before the work it measures; this one was written beside it.
- **No evaluator read a control.** No control case was planted for a reader, and there are no score rows
  from which a control's expected or actual outcome could be derived.
- **No approval of a bar digest was stamped when it was given.** The approvals that shaped the release were
  given in conversation.

A record is a set of claims about when things happened and who did what. Assembling one now would mean
taking those times from memory and a session log, and fitting the job's 36 mechanical checks into the
record's evaluator-check shape. The result would attest to a process that did not happen. `tools/make_record.py`
refuses a control whose outcome is typed rather than derived for precisely this reason; writing a record by
hand here would do what the builder is built to prevent.

## What v0.9.8 can and cannot claim

**It can claim** that five scoped items changed and that the change is evidenced: the items and their
reasons are in `CHANGELOG.md`, the diff is `da2a3dd..8a6bf1e`, nine test suites behave as they do at the
base commit, 118 shared fixtures show no change in verdict, level or failing requirement, and two
independent readers accepted the work.

**It cannot claim** that the release was evaluated under a bar frozen before the work began, by readers who
could not see the maker's answer, beside planted controls. That is what a custody record is for. It is
absent, and no amount of later writing supplies it.

**And none of the above can be checked from this repository.** The job directory — its bar, its referee, its
ledger — is not published here. That is the point: this note is an unattested statement by the maintainer
about a job no outsider can inspect, which is exactly what a custody record exists to replace. It is written
because silence would be worse, not because it is evidence.

## A second defect in the same release

`SPEC.md` at that tag reads `Version 0.9.8 · candidate · 2026-10-27`. The date is v0.9.7's; v0.9.8 was
tagged 2026-11-04, which is also the last day the specification changed. **The tag is not moved** — it is
published, and a header that names a different commit than the one tagged would be worse than the error.
The correction is made on `main` instead, so `main` and the tag now differ in this one line and nowhere
else. A reader comparing them should take the tag as what shipped and `main` as what the specification
actually says.

## How to read this beside the other records

The five records before this one are listed in `tools/verdicts.json` as unfreezable: they exist, and their
job inputs were not published, so they cannot be re-checked from this repository. This case is a different
failure — there is no record at all. A reader comparing v0.9.7 with v0.9.8 should not read them as
equivalent: v0.9.7 is answerable and cannot be re-run; v0.9.8 is not answerable.
