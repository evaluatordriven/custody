#!/usr/bin/env python3
"""Verify a custody log, confirm declared checks and controls were filed, and build the record.

Usage: release_record.py INPUTS.json RECORD.json --log LOG --declared DECLARED.json
"""
import argparse
import copy
import json
import pathlib
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import make_record  # noqa: E402
import record  # noqa: E402

CHECK_KEYS = ("dimension", "evaluator", "run", "batch")
NEED_CHECK = {"dimension", "evaluator", "run", "batch", "outcome"}
NEED_CONTROL = {"id", "batch", "evaluator", "case", "expected", "outcome"}


def check_tuple(obj):
    if not isinstance(obj, dict) or not set(CHECK_KEYS) <= set(obj.keys()):
        return None
    return (obj["dimension"], obj["evaluator"], obj["run"], obj["batch"])


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("inputs")
    ap.add_argument("record")
    ap.add_argument("--log", required=True)
    ap.add_argument("--declared", required=True)
    a = ap.parse_args()

    log_path = pathlib.Path(a.log)
    if not log_path.is_file():
        sys.exit(f"refused: log not found: {a.log}")
    problems = record.verify(a.log)
    if problems:
        sys.exit("refused: custody log does not verify:\n" + "\n".join(problems))

    try:
        declared = json.loads(pathlib.Path(a.declared).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        sys.exit(f"refused: cannot read --declared: {e}")
    if not (isinstance(declared, dict) and isinstance(declared.get("checks"), list)
            and isinstance(declared.get("controls"), list)):
        sys.exit("refused: DECLARED.json must be {\"checks\": [...], \"controls\": [...]}")

    events = record.read(a.log)
    built = max((i for i, e in enumerate(events) if e.get("type") == "artifact-produced"),
                default=-1)
    if built < 0:
        sys.exit("refused: no artifact-produced event in log")
    after = events[built + 1:]
    filed_checks = {check_tuple(e.get("data")) for e in after
                    if e.get("type") == "check" and NEED_CHECK <= set(e.get("data") or {})}
    filed_controls = {e["data"]["id"] for e in after
                      if e.get("type") == "control" and NEED_CONTROL <= set(e.get("data") or {})}

    for c in declared["checks"]:
        key = check_tuple(c)
        if key is None or set(c.keys()) != set(CHECK_KEYS):
            sys.exit(f"refused: malformed declared check {c!r}")
        if key not in filed_checks:
            sys.exit(f"refused: declared check {c!r} was not filed after artifact-produced")
    for cid in declared["controls"]:
        if not isinstance(cid, str) or not cid.strip():
            sys.exit(f"refused: malformed declared control id {cid!r}")
        if cid not in filed_controls:
            sys.exit(f"refused: declared control {cid!r} was not filed after artifact-produced")

    src = pathlib.Path(a.inputs)
    base = src.resolve().parent
    data = make_record.from_log(copy.deepcopy(json.loads(src.read_text(encoding="utf-8"))), a.log)
    out = {"_type": "https://in-toto.io/Statement/v1",
           "subject": make_record.subject(data.pop("subject"), base),
           "predicateType": "https://evaluatordriven.com/custody/v1",
           "predicate": make_record.resolve(data, base)}
    pathlib.Path(a.record).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {a.record}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
