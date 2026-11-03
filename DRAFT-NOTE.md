# Draft Note — v0.9.8 (candidate)

## 1. Hunk inventory (N6)

1. `CHANGELOG.md` (@@ -4,6 +4,38 @@) — 0.9.8 release entry — `release mechanics` (summarizes `item 1`, `item 2`, `item 3`, `item 4`, `item 5`, and `release mechanics`)
2. `README.md` (@@ -11,7 +11,7 @@) — bump status version — `release mechanics`
3. `README.md` (@@ -91,9 +91,9 @@) — level table qualifier — `item 1`
4. `checker/check.py` (@@ -284,15 +284,30 @@) — total `cl1_10` referee — `item 5`
5. `tests/red_counts.py` (@@ -6,16 +6,26 @@) — dynamic planted version — `item 2`
6. `tests/red_counts.py` (@@ -42,7 +52,12 @@) — substitute planted version — `item 2`
7. `tests/red_counts.py` (@@ -52,7 +67,7 @@) — dynamic record specVersion — `item 2`
8. `tools/explain.py` (@@ -19,6 +19,14 @@) — level formatter and disclaimer — `item 1`
9. `tools/explain.py` (@@ -35,8 +43,13 @@) — header level and disclaimer — `item 1`
10. `tools/explain.py` (@@ -117,7 +130,9 @@) — footer level and disclaimer — `item 1`
11. `tools/make_record.py` (@@ -20,29 +20,53 @@) — docstring and `role_name` helper — `item 2`
12. `tools/make_record.py` (@@ -50,6 +74,18 @@) — resolve role-named packages — `item 2`
13. `tools/make_record.py` (@@ -68,13 +104,163 @@) — score loading and package checks — `item 2`, `item 4`
14. `tools/make_record.py` (@@ -89,7 +275,7 @@) — drop event outcome requirement — `item 2`
15. `tools/make_record.py` (@@ -105,13 +291,40 @@) — derive control outcomes, `x-on` — `item 2`, `item 4`
16. `tools/make_record.py` (@@ -128,7 +341,9 @@) — pass base and fix disposition — `item 2`, `item 4`

*(Note: `item 3` is the `SPEC.md` §5.3 pseudocode replacement for `CL2-3` and has no hunks outside `SPEC.md` other than its mention in `CHANGELOG.md`.)*

## 2. Record verdicts (G5.4)

Run at the base commit and at this commit, the one record in the repository (`examples/minimal/record.json`) reads `OK` / `CL1` at both. No record's verdict changed.

## 3. What changed and what did not

This draft addresses the five scoped items: (1) formatting `CL1`–`CL3` as `CLn · process` in `README.md` and `tools/explain.py` alongside a process-scope disclaimer; (2) hardening `tools/make_record.py` and `tests/red_counts.py` so control `expected`/`outcome` values are derived from score rows, packages are named by role without overwriting cited bytes, and planted test records are version-agnostic (computing the spec version dynamically from `SPEC.md`); (3) replacing `SPEC.md` §5.3's `CL2-3` conditional prose with a single fenced pseudocode block of unchanged meaning; (4) setting the disposition's package reference key to `x-on` in `tools/make_record.py`; and (5) making the `cl1_10` referee in `checker/check.py` total over malformed `checks` and `disagreements` shapes without crashing or accepting booleans/non-integers as indices (with corresponding `SPEC.md` `CL1-10` prose and a fixture per malformed shape in `fixtures/`). We also updated `CHANGELOG.md` and bumped the version string to `0.9.8`. We deliberately left `CL3-3`, signing, the JSON schema, and `record/` untouched.

## 4. Where to look hardest

The largest surface area and highest risk sit in `tools/make_record.py` (hunks 11–16 for `item 2` and `item 4`). Because prior callers and tests pass score rows, control events, and package references in several shapes (inline `scores` arrays/dicts in `INPUTS.json`, external `scores.tsv`/`scores.json` files, embedded `scoreRow` dicts on events, and legacy `on` vs `x-on` fields), `load_scores`, `parse_row`, `role_name`, and `check_packages` accept a wide range of alias keys and file names. A reviewer should look closely at whether that permissiveness in `parse_row` / `load_scores` could silently match an unintended row or mask a malformed score file, and whether `role_name`'s heuristics (`require_role=True` in `resolve` vs `require_role=False` in `check_packages` and `fix_disp`) reject any legitimate package string or let a path-like string slip through when converting `disposition["on"]` to `x-on` (`item 4`). In `tools/explain.py` (`item 1`), also verify whether gating the `CLn · process` formatting of `levelClaimed` in the header on `reached in LEVELS` is what you want when a record claims `CL2` but achieves `FAILED` or `baseline`.
