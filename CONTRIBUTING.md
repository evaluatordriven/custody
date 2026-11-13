# Contributing

## Three kinds of change

| Kind | What it is | What it needs |
|---|---|---|
| **Behavioral** | Anything that could change whether a record reads `OK`, `FAILED`, or `NOT-CHECKABLE` — the checker, the fixtures, the schema, or a normative requirement | A failing record from real use, or a reproducible counterexample, attached to the issue |
| **Structural** | Changes what the repository refuses without moving any verdict: `tools/count.py`, `tools/check_verdicts.py`, `tests/`, CI | The check proved to fail on the defect it names, before it is trusted, and a reader who is not its author |
| **Editorial** | Wording, typos, examples, layout | A declaration in the pull request: *no semantic change* |

A behavioral change without a failing record or counterexample is closed, not argued. Records made to
test this specification itself do not count as real use.

A behavioral change to the checker, the fixtures or the schema is itself a job: the bar is frozen before the
change, a reader who could not see the maker's answer reads it, and the release carrying it ships a record.
Version 0.9.8 shipped without one — `record/RECORD-GAP-v0.9.8.md` says why — and `count.py` now refuses a
release that neither carries a record nor declares its absence.

## How to file a failing record

1. Run `python3 checker/check.py your-record.json --files your-artifact-folder`.
2. Open an issue with the record, the report, and one sentence on what you expected instead.
3. Remove anything confidential first; digests are enough for most reports.

## Releases

At most one release a month while the version starts with 0, quarterly after 1.0. Versions follow
Semantic Versioning 2.0.0; `SPEC.md` section 8 says what counts as a major change. Every release is a
git tag, and is cited by its commit.

### Release packaging classes (do not collapse them)

A PR that moves `SPEC.md`'s version is not automatically a shippable release. Name the class:

| Class | What is true | CI / merge |
|---|---|---|
| **Docs candidate** | Version header and release docs only; no new `record/custody-vX.Y.Z.json`, or the file is not claimed as the release record | May be red on `count.py` until a real record or an allowed gap note exists. Do not merge as if shipped. |
| **Record file present** | `record/custody-vX.Y.Z.json` exists and `specVersion` matches the release | `count.py` can go green. That only means the named file exists and `specVersion` matches. It does not run `checker/check.py`, and it does not reject a hollow file. Not enough to merge. |
| **Frozen verdicts** | The published record also has a re-checkable row in `tools/verdicts.json` (inputs in-tree) | Required for any new `record/*.json`. `check_verdicts.py` stays red until that row exists and reproduces. Parking under `unfreezable` without `legacy: true` is refused; legacy is only for the pre-table records `record/custody-v0.9.3.json` through `record/custody-v0.9.7.json`. Do not freeze FAILED/none, or a hollow file, to buy a green run. |
| **Gap note** | `record/RECORD-GAP-vX.Y.Z.md` explains why this release has no record | Bounded exception (see existing 0.9.8 note). Do not spend it to paper over a hollow emit. |

**Hollow record:** a JSON file under `record/` whose bar/maker/instrument/controls are empty nulls is **not** a release record. Prefer honest absence (or a gap note when allowed) over freezing FAILED/none to green CI. A unittest **runner** is not a custody **bar** (bar needs author, frozenAt, dimensions, approvals bound to a digest).

## Before you open a pull request

```sh
python3 fixtures/generate.py && python3 tests/run_fixtures.py && python3 tools/count.py
```

All three must pass. A new requirement arrives with a fixture that fails for it and only it.
