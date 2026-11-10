# No custody record accompanies v0.9.8

**Status: no record. Not withheld — never produced.** Tag `v0.9.8` (`8a6bf1e`), parent `ed664d5`, cut
2026-11-04. The release work runs `da2a3dd..8a6bf1e`; `da2a3dd` is the branch point sixteen commits back, not
the tag's parent.

Every release from v0.9.3 to v0.9.7 carries its record in this directory. This one does not, and this note is
here so that the absence reads as a decision with a reason rather than as an oversight. No check in this
repository failed when it shipped without one.

**This is the only note of its kind.** It covers v0.9.8 and cannot be reused. `tools/count.py` refuses a
release that neither carries a record nor declares its absence in a note named for its version, and permits a
gap note only for the releases listed in its `GAP_EXCEPTIONS` — v0.9.8 is the one entry, and a second gap would
need an edit to that list rather than another file. This note exists because the first of those checks did not.

## The release could not have claimed a level

This is not a paperwork gap. The instrument that produced v0.9.8's verdicts was **still being written while
they were produced.**

A 35-gate bar was authored by the job's own Architect and frozen at the job's start on 2026-11-02, then
amended during the job when the Owner ratified AMENDMENT-2. The referee that judged the work grew from 19
implemented gates to 36 checks as the work proceeded. A bar written beside the work, and an instrument that
changed underneath it, are the two things a custody record exists to rule out.

And a record would not have revealed it. `CL1-5` asks that the instrument be *named* — rubric and runner as
digests — not that it have been fixed while the work ran. A record could have named the final digests and
read `CL1` without recording that the earlier ones existed. That is an observation for the Architect, not
something this note decides.

## Why it cannot be produced now

- **No evaluator read a control.** No control case was planted for a reader, and there are no score rows from
  which a control's expected or actual outcome could be derived.
- **No approval of a bar digest was stamped when it was given.** The approvals that shaped the release were
  given in conversation, and the bar was amended after the freeze.

A record is a set of claims about when things happened and who did what. Assembling one now would mean taking
those times from memory and a session log, and fitting the job's 36 mechanical checks into the record's
evaluator-check shape. The result would attest to a process that did not happen. `tools/make_record.py`
refuses a control whose outcome is typed rather than derived for precisely this reason; writing a record by
hand here would do what the builder is built to prevent.

## What v0.9.8 can and cannot claim

**It can claim** that five scoped items changed and that the change is evidenced: the items and their reasons
are in `CHANGELOG.md`, the diff is `da2a3dd..8a6bf1e`, nine test suites behave as they do at the base commit,
118 shared fixtures show no change in verdict, level or failing requirement, and two independent readers
accepted the work.

**It cannot claim** that the release was evaluated under a bar frozen before the work began, by readers who
could not see the maker's answer, beside planted controls. That is what a custody record is for. It is absent,
and no amount of later writing supplies it.

**And none of the above can be checked from this repository.** The job directory — its bar, its referee, its
ledger — is not published here. That is the point: this note is an unattested statement by the maintainer
about a job no outsider can inspect, which is exactly what a custody record exists to replace. It is written
because silence would be worse, not because it is evidence.

## The changelog promised otherwise

`CHANGELOG.md` opened with *"Each release is a git tag, and each carries its own custody record in
`record/`."* That sentence was false for this release. It is amended, and the amendment is a correction
rather than an exception: the promise now reads *"or a note in `record/` saying why it does not,"* which is
what `tools/count.py` enforces. Leaving a promise the repository had already broken, three files away from
the note that explains the break, would be the same defect in a quieter form.

## A second defect in the same release

`SPEC.md` at that tag reads `Version 0.9.8 · candidate · 2026-10-27`. The date is v0.9.7's; v0.9.8 was tagged
2026-11-04, which is also the last day the specification changed. **The tag is not moved** — it is published,
and a header that names a different commit than the one tagged would be worse than the error. The correction
is made on `main` instead, so `SPEC.md` on `main` and `SPEC.md` at the tag now differ in this one line and
nowhere else. The trees differ by more than that — this note, the stranger-test note, the verdict machinery and
the release check all landed after the tag — but no other line of the specification does. A reader comparing
them should take the tag as what shipped and `main` as what the specification actually says.

## How to read this beside the other records

The five records before this one are listed in `tools/verdicts.json` as unfreezable: they exist, and their job
inputs were not published, so they cannot be re-checked from this repository. This case is a different
failure — there is no record at all. A reader comparing v0.9.7 with v0.9.8 should not read them as equivalent:
v0.9.7 is answerable and cannot be re-run; v0.9.8 is not answerable.
