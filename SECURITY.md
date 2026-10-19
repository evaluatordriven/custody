# Security

**Reporting a problem.** If you find a way to make a record pass the checker when it should not, or a
flaw in the checker or the tools that could mislead someone relying on a record, please report it
privately through GitHub's "Report a vulnerability" button on this repository's Security tab. Please do
not open a public issue for it first.

**What counts.** A record that reads `OK` but breaks a requirement in SPEC.md; a digest, signature or
evidence check that can be bypassed; or tooling that writes something into a record that the inputs did
not say.

**What to expect.** An acknowledgement within a week. A fix is released as a new version, and
CHANGELOG.md says what changed and why, crediting the reporter unless they ask otherwise.

The specification itself makes no security promise beyond what SPEC.md section 7 states.
