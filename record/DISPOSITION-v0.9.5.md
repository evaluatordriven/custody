# Disposition — v0.9.5

**Approver:** Steve Moitozo II · **Decision:** given · **Time:** taken from the custody log's `disposition` event

**Given, as a v0.9.5 candidate.** This release asked whether a stranger can implement the standard from
its text alone, and measured it properly before changing anything. It makes one breaking change: each
evaluator that reads a batch must read both a clean and a planted control there (CL1-9). It also says
four things more plainly: CL1-17 does not judge unscored checks; CL2-3's half rule is stated as
arithmetic, with a worked example; an evidence value that is not an evidence file fails CR-2; and kept
records carry versioned names. Notes about a record's checker result are now written by
`tools/verify_note.py` from the checker's own words.

**The stranger test passed, in its third cycle.** Three implementers ran three fresh sessions each, on a
fresh set of twelve records per cycle. Cycle 1 was unobserved, and cycle 2 did not pass. In cycle 3, Seed
2.1 Turbo and MiniMax M3 each met the bar in two counted sessions. The bar holds that the last cycle
stands. Every session's scores are in `record/STRANGER-TEST-v0.9.5.md`.

**Acknowledged as unobserved:** Nemotron 3 Ultra's stranger-test checks. None of its three sessions in
cycle 3 was counted, because each read a control wrong.

**Also on record:**
- **A voided attempt.** A first attempt at cycle 3 is void and is not a cycle. Its planted control was
  built wrong and never validated. The void was declared after its sessions had been scored, and I
  ratified it.
- **A withdrawn disposition.** I first gave this disposition on a package whose CHANGELOG had overwritten
  v0.9.4's published history. That package was withdrawn, the history restored, and this disposition
  given anew.
- **The fixtures.** The blind key over all 111 fixtures matched the checker: 88 agreed outright, and the
  adjudicator upheld the checker in all 23 that did not.
- **Process errors.** The orchestrator's process errors are listed in the record's separation gaps.

**Carried to v0.9.6, whose theme is running the evaluation independently of the maker:**
- no model from the maker's family in any evaluation seat;
- two adjudicators who must agree;
- scripted acceptance checks for every step that writes into a release;
- a stranger-test gate that separates unclear text from one session's coding failure.
