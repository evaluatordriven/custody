# Draft Note — v0.9.8 (candidate)

## 1. Hunk inventory (N6)

1. `CHANGELOG.md` (+35 -0) — 0.9.8 release entry — `release mechanics` (summarizes `item 1`, `item 2`, `item 3`, `item 4`, `item 5`, and `release mechanics`)
2. `DRAFT-NOTE.md` (+34 -0) — release draft note (hunk inventory and verdict comparison) — `release mechanics`
3. `README.md` (+5 -4) — bump status version and level table qualifier — `release mechanics`, `item 1`
4. `SPEC.md` (+68 -3) — bump version, `CL2-3` pseudocode block, and `CR-2` / `CL1-10` structural precedence — `release mechanics`, `item 3`, `item 5`
5. `checker/check.py` (+30 -10) — bump version and total `cl1_10` / `CR-2` structural precedence — `release mechanics`, `item 5`
6. `examples/minimal/inputs.json` (+1 -1) — bump specVersion to 0.9.8 — `release mechanics`
7. `examples/minimal/record.json` (+1 -1) — regenerate minimal record at 0.9.8 — `release mechanics`
8. `fixtures/expected.json` (+219 -3) — expected outcomes for 29 new malformed-shape fixtures (147 total) — `item 5`
9. `fixtures/generate.py` (+146 -6) — bump version and generate 29 `CL1-10` / `CR-2` malformed-shape fixtures — `release mechanics`, `item 5`
10. `tests/red_counts.py` (+19 -3) — dynamic planted version strings from `SPEC.md` — `item 2`
11. `tools/explain.py` (+62 -37) — `CLn · process` level formatter and custody disclaimer — `item 1`
12. `tools/make_record.py` (+288 -23) — derive control outcomes from scores, role-named packages, and `x-on` disposition references — `item 2`, `item 4`

## 2. Record verdicts (G5.4)

Run at the base commit and at this commit across all 118 shared fixtures, comparing `(verdict, levelAchieved, failing requirements)` produced zero differences—no record's verdict changed. `examples/minimal/record.json` reads `OK` / `CL1` at both commits, and `run_fixtures` reports 147 of 147 fixtures as expected.

## 3. What changed and what did not

This draft addresses the five scoped items: (1) formatting `CL1`–`CL3` as `CLn · process` in `README.md` and `tools/explain.py` alongside a process-scope disclaimer; (2) hardening `tools/make_record.py` and `tests/red_counts.py` so control `expected`/`outcome` values are derived from score rows, packages are named by role without overwriting cited bytes, and planted test records are version-agnostic (computing the spec version dynamically from `SPEC.md`); (3) replacing `SPEC.md` §5.3's `CL2-3` conditional prose with a single fenced pseudocode block of unchanged meaning; (4) setting the disposition's package reference key to `x-on` in `tools/make_record.py`; and (5) making the `cl1_10` referee in `checker/check.py` total over malformed `checks` and `disagreements` shapes without crashing or accepting booleans/non-integers as indices (with corresponding `SPEC.md` `CL1-10` prose and a fixture per malformed shape in `fixtures/`). We also updated `CHANGELOG.md` and bumped the version string to `0.9.8`. We deliberately left `CL3-3`, signing, the JSON schema, and `record/` untouched.

## 4. Where to look hardest

The largest surface area and highest risk sit in `tools/make_record.py` (hunks 11–16 for `item 2` and `item 4`). Because prior callers and tests pass score rows, control events, and package references in several shapes (inline `scores` arrays/dicts in `INPUTS.json`, external `scores.tsv`/`scores.json` files, embedded `scoreRow` dicts on events, and legacy `on` vs `x-on` fields), `load_scores`, `parse_row`, `role_name`, and `check_packages` accept a wide range of alias keys and file names. A reviewer should look closely at whether that permissiveness in `parse_row` / `load_scores` could silently match an unintended row or mask a malformed score file, and whether `role_name`'s heuristics (`require_role=True` in `resolve` vs `require_role=False` in `check_packages` and `fix_disp`) reject any legitimate package string or let a path-like string slip through when converting `disposition["on"]` to `x-on` (`item 4`). In `tools/explain.py` (`item 1`), also verify whether gating the `CLn · process` formatting of `levelClaimed` in the header on `reached in LEVELS` is what you want when a record claims `CL2` but achieves `FAILED` or `baseline`.

## Hunk map

Every hunk in `da2a3dd..HEAD`, by file and the scoped item it serves.
The 29 `fixtures/cl1-fail-*` files are **generated**, not written by hand: `fixtures/generate.py`
emits each shape and computes its evidence digests, so they all serve item 5 and are described
once, under `fixtures/generate.py`.

| file | hunks | item |
|---|---|---|
| `CHANGELOG.md` | 2 | 1–5 |
| `DRAFT-NOTE.md` | 1 | meta |
| `README.md` | 2 | 1 |
| `SPEC.md` | 3 | 3, 5 |
| `checker/check.py` | 4 | 3, 5 |
| `examples/minimal/inputs.json` | 1 | 5 |
| `examples/minimal/record.json` | 1 | 5 |
| `fixtures/cl1-fail-checks-dimension-list.json` | 1 | 5 |
| `fixtures/cl1-fail-checks-dimension-missing.json` | 1 | 5 |
| `fixtures/cl1-fail-checks-dimension-null.json` | 1 | 5 |
| `fixtures/cl1-fail-checks-entry-not-object.json` | 1 | 5 |
| `fixtures/cl1-fail-checks-outcome-list.json` | 1 | 5 |
| `fixtures/cl1-fail-checks-outcome-missing.json` | 1 | 5 |
| `fixtures/cl1-fail-checks-outcome-object.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-check-index-false.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-check-index-float.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-check-index-len.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-check-index-list.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-check-index-negative.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-check-index-null.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-check-index-string.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-check-index-true.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-checks-missing.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-checks-null.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-checks-number.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-checks-object.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-checks-singleton.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-checks-string.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-dimension-list.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-dimension-missing.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-dimension-null.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-dimension-number.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-entry-not-object.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-null.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-object.json` | 1 | 5 |
| `fixtures/cl1-fail-disagreements-string.json` | 1 | 5 |
| `fixtures/expected.json` | 3 | 5 |
| `fixtures/generate.py` | 12 | 5 |
| `tests/red_counts.py` | 5 | 2 |
| `tools/explain.py` | 22 | 1 |
| `tools/make_record.py` | 16 | 2 |

Total: 101 hunks across 41 files.
