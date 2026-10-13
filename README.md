# Evaluator Driven — the custody record

A specification for the record kept with a piece of evaluated work: what the work was measured against,
who measured it, what they found, and who decided. The record makes work answerable, not correct.

**Who this is for**
- **Implementers** who want work they hand off, or receive, to carry its own account.
- **Reviewers** in procurement, security, or legal who need to check that account.

**Status: v0.9.1, candidate.** Early. One reference checker exists, in this repository. Nobody is known
to have adopted this specification, and nothing here implies endorsement by anyone. This repository's own
custody record, in `record/`, claims CL1. It does not reach CL2; its separation gaps say why.

**Limits, stated first**
- The evidence base is one author's work and a handful of jobs.
- The reference checker verifies a record's shape and internal consistency. It cannot tell whether a
  reading was honest; that is what independent evaluators and the approver are for.
- External evidence (CL1-15, CL3-3) is only as good as the party who read it.
- No signing tool ships here yet. CL3 records point to verification output produced elsewhere.
- Reader-judged checks for v0.9.1 are unobserved: the one model judge that qualified missed a planted
  defect during evaluation. Human readers are part of the v1.0 gate.

## Quickstart

Python 3.10 or newer, standard library only:

```sh
git clone https://github.com/smoitozo/evaluatordriven && cd evaluatordriven
python3 tools/make_record.py examples/minimal/inputs.json examples/minimal/record.json
python3 checker/check.py examples/minimal/record.json --files examples/minimal
```

The second command turns a hand-written inputs file into a record, computing every digest. The third
checks it and prints a report; exit code 0 means `OK`, 1 `FAILED`, 2 `NOT-CHECKABLE`.

To make your own: copy `examples/minimal/`, replace the files with yours, edit `inputs.json`, and run
the same two commands.

## What is here

| Path | What it is |
|---|---|
| `SPEC.md` | The specification. Its *(normative)* sections define conformance. |
| `schema/custody-v1.schema.json` | The record's shape, for JSON Schema 2020-12 validators |
| `checker/check.py` | Reference verifier (not normative) |
| `tools/make_record.py` | Builds a record from a plain inputs file |
| `tools/count.py` | Checks this repository's own size limits and cross-file agreement |
| `examples/minimal/` | A one-page memo, its bar, and a CL1 record |
| `fixtures/` | Passing and failing records, one named reason per failure; `generate.py` rebuilds them |
| `tests/` | Runs the checker over the fixtures |
| `record/` | This repository's own custody record, which claims CL1 |

## Levels at a glance

The requirements live in `SPEC.md` section 5; this is only orientation.

| Level | In one line |
|---|---|
| CL1 | All four moves: bar first and approved, work pinned, read independently beside a control, record kept with a named decision |
| CL2 | CL1, plus repeated runs with their spread, and model readers on a separate family and endpoint |
| CL3 | CL2, plus each reader shown failing a held-out planted case first, and a signed, logged record |
| baseline | The bar came after the work: a valid description, with no level |

## Licenses

- Text (`SPEC.md`, documentation): **CC BY 4.0**, © 2026 Steve Moitozo II — see `LICENSE`.
- Code (`checker/`, `tools/`, `fixtures/`, `tests/`, `schema/`): **Apache-2.0** — see `LICENSE-CODE`.
- Patents: the author's non-assertion pledge — see `PATENTS.md`.
- Copyright notice for the code: `NOTICE`.

## Lineage

Condensed from a private working corpus and checked against evaluatordriven.com. The corpus is lineage,
not evidence: nothing here depends on it, and it is not public.
