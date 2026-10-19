# Governance

**Maintainer.** Steve Moitozo II maintains this specification and decides what goes into each release.
For now there is one maintainer; that is a real limit, and it is stated here rather than hidden.

**How changes are decided.** Changes follow CONTRIBUTING.md: a change in behavior needs a real failing
record or a reproducible counterexample. Each release's decisions, and who made them, are kept in that
release's custody record and listed in CHANGELOG.md.

**Releases.** Each release is a git tag, citable by commit, and carries its own record. SPEC.md section 8
says which changes are breaking.

**Continuity.** The text is CC BY 4.0 and the code is Apache-2.0, so anyone may fork and continue the
work without asking. A fork that changes what a record means should publish its own predicate type,
rather than reuse `https://evaluatordriven.com/custody/v1`, so that records stay unambiguous.

**No certification.** There is no certifying body, assessor or registry. A custody record shows its own
account of how work was judged; it certifies nothing.
