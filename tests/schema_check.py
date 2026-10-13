#!/usr/bin/env python3
"""Validate fixtures with a third-party JSON Schema 2020-12 validator (CI only: pip install jsonschema).

Passing fixtures and fixtures that fail a semantic requirement must be schema-valid; fixtures that fail a
structural requirement (CR-1, CR-2, CL1-4, CL1-5, CL1-12) must be schema-invalid.
"""
import json
import pathlib
import sys

from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parent.parent
STRUCTURAL = {"CR-1", "CR-2", "CL1-4", "CL1-5", "CL1-12"}


def main():
    schema = json.loads((ROOT / "schema" / "custody-v1.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    exp = json.loads((ROOT / "fixtures" / "expected.json").read_text())
    cases, extra = exp["cases"], set(exp.get("schemaInvalid", []))
    records = {n: ROOT / "fixtures" / f"{n}.json" for n in cases}
    records["examples/minimal"] = ROOT / "examples" / "minimal" / "record.json"
    bad = 0
    for name, path in records.items():
        valid = validator.is_valid(json.loads(path.read_text()))
        want = cases.get(name, {}).get("fails") not in STRUCTURAL and name not in extra
        print(f"{'ok  ' if valid == want else 'FAIL'} {name}: schema-{'valid' if valid else 'invalid'}")
        bad += valid != want
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
