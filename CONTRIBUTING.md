# Contributing

## Two kinds of change

| Kind | What it is | What it needs |
|---|---|---|
| **Behavioral** | Anything that could change whether a record reads `OK`, `FAILED`, or `NOT-CHECKABLE` | A failing record from real use, or a reproducible counterexample, attached to the issue |
| **Editorial** | Wording, typos, examples, layout | A declaration in the pull request: *no semantic change* |

A behavioral change without a failing record or counterexample is closed, not argued. Records made to
test this specification itself do not count as real use.

## How to file a failing record

1. Run `python3 checker/check.py your-record.json --files your-artifact-folder`.
2. Open an issue with the record, the report, and one sentence on what you expected instead.
3. Remove anything confidential first; digests are enough for most reports.

## Releases

At most one release a month while the version starts with 0, quarterly after 1.0. Versions follow
Semantic Versioning 2.0.0; `SPEC.md` section 8 says what counts as a major change. Every release is a
git tag, and is cited by its commit.

## Before you open a pull request

```sh
python3 fixtures/generate.py && python3 tests/run_fixtures.py && python3 tools/count.py
```

All three must pass. A new requirement arrives with a fixture that fails for it and only it.
