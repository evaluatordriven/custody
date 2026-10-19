# v0.9.3 bar — Amendment 1 (Owner decision 4)

Made after an independent market and standards review (17 Oct 2026), before any reader gate was read.
It amends `V0.9.3-BAR.md` (sha256 `c8581ca1…`); everything not named here stands.

## Scope added (S7–S12), built as revision 1 of 3
| # | Item | Done when |
|---|---|---|
| S7 | **A missed control voids its reader's observations.** A control whose outcome differs from its expected outcome means that evaluator's checks in that batch read `unobserved`, or only those of the control's `dimension` if it names one. | Fixtures for both scopes, passing and failing |
| S8 | **The bar file is checked against `bar.digest`** (CL1-14), `NOT-CHECKABLE` without it, as with the work's files | A fixture whose bar file differs fails CL1-14 |
| S9 | **The maker approving the bar:** allowed at CL1 if a separation gap names the maker (CL1-11); not allowed at CL2 and above (CL2-3) | Fixtures: undisclosed fails at CL1; disclosed passes at CL1; fails at CL2 |
| S10 | **The checker applies to a baseline claim only what SPEC.md says** (CL1-2 to CL1-14) | A baseline fixture with a model evaluator and no external evidence passes |
| S11 | **`family`, `identifier` and `endpoint` defined** in one sentence each | In SPEC.md section 4 |
| S12 | **CHANGELOG.md, SECURITY.md, GOVERNANCE.md;** README states no certification body and one maintainer; SPEC.md section 8 says that, before 1.0.0, any release may make a breaking change and lists it in CHANGELOG.md | count.py clean |

## Consequences, stated
- **Earlier release records are checked by their own release's checker.** Under these rules the v0.9.2
  release record no longer verifies (one of its controls came out wrong while its reader's other checks
  still counted), which is the defect this amendment closes. S4's "done when" is read as: S4's own change
  breaks no earlier record.
- **The answer key and the rendered records follow the amended rules:** Kimi revises the key for S7–S10,
  with at least 3 new cases each, and every rendered record ships with its bar file.
- **The site** says the two people who decide what good means did not make the work. Under S9 that holds
  at CL2 and above, and at CL1 the overlap is disclosed. The site stays frozen as ground truth; a one-line
  edit is queued for after release.
- **Reader-panel controls carry over** (they test reading, not rules). No reader has read the real
  documents yet, so all gate readings are taken on revision 1.
