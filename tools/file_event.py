#!/usr/bin/env python3
"""Append a validated check or control event to a custody log through tools/record.py.

Usage: file_event.py LOG check|control --actor NAME --data-file DATA.json
                     [--evidence-dir DIR] [--source TEXT]
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import record  # noqa: E402

OUTCOMES = {"conforms", "does_not_conform", "unobserved"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HOST = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$")
ZERO_DIGEST = "0" * 64
CHECK_REQ = {"dimension", "evaluator", "run", "batch", "outcome", "score",
             "failureCondition", "evidence", "unobserved"}
CHECK_OPT = {"endpoint"}
CONTROL_REQ = {"id", "batch", "evaluator", "case", "expected", "outcome"}
CONTROL_OPT = {"dimension"}


def non_empty_str(v):
    return isinstance(v, str) and v.strip() != ""


def whole_pos(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 1


def num_or_null(v):
    return v is None or (isinstance(v, (int, float)) and not isinstance(v, bool))


def relative_path(name):
    return isinstance(name, str) and name.strip() != "" and not (
        os.path.isabs(name) or ".." in name.replace("\\", "/").split("/"))


def valid_digest(d, allow_zero=True):
    if not (isinstance(d, dict) and set(d.keys()) == {"sha256"}):
        return False
    h = d.get("sha256")
    return isinstance(h, str) and bool(HEX64.match(h)) and (allow_zero or h != ZERO_DIGEST)


def validate_check(data, evidence_dir):
    if not isinstance(data, dict):
        return "check data must be a JSON object"
    missing = CHECK_REQ - set(data.keys())
    if missing:
        return f"check missing required field(s): {', '.join(sorted(missing))}"
    extra = set(data.keys()) - CHECK_REQ - CHECK_OPT - {k for k in data if k.startswith("x-")}
    if extra:
        return f"check has unexpected field(s): {', '.join(sorted(extra))}"
    for k in ("dimension", "evaluator", "batch", "failureCondition"):
        if not non_empty_str(data.get(k)):
            return f"check.{k} must be a non-empty string"
    if not whole_pos(data.get("run")):
        return "check.run must be a whole number of at least 1"
    outcome = data.get("outcome")
    if outcome not in OUTCOMES:
        return f"check.outcome {outcome!r} is not conforms, does_not_conform or unobserved"
    if not num_or_null(data.get("score")):
        return "check.score must be a number or null"
    if "endpoint" in data and not (isinstance(data["endpoint"], str)
                                   and HOST.match(data["endpoint"])):
        return "check.endpoint must be a lowercase host name"
    ev, unobs = data.get("evidence"), data.get("unobserved")
    if outcome == "unobserved":
        if ev is not None or data.get("score") is not None:
            return "an unobserved check must have evidence=null and score=null"
        if not (isinstance(unobs, dict) and non_empty_str(unobs.get("channel"))
                and non_empty_str(unobs.get("reason"))):
            return "an unobserved check needs unobserved={channel, reason}"
    else:
        if unobs is not None:
            return f"a {outcome} check must have unobserved=null"
        if not (isinstance(ev, dict) and set(ev.keys()) == {"name", "sha256"}
                and relative_path(ev.get("name")) and isinstance(ev.get("sha256"), str)
                and HEX64.match(ev["sha256"])):
            return "check.evidence must be {name, sha256}"
        if not evidence_dir:
            return "--evidence-dir is required to verify check.evidence"
        path = pathlib.Path(evidence_dir) / ev["name"]
        if not path.is_file():
            return f"evidence file not found: {path}"
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != ev["sha256"]:
            return f"evidence digest mismatch for {ev['name']}"
    return None


def validate_control(data):
    if not isinstance(data, dict):
        return "control data must be a JSON object"
    missing = CONTROL_REQ - set(data.keys())
    if missing:
        return f"control missing required field(s): {', '.join(sorted(missing))}"
    extra = set(data.keys()) - CONTROL_REQ - CONTROL_OPT - {k for k in data if k.startswith("x-")}
    if extra:
        return f"control has unexpected field(s): {', '.join(sorted(extra))}"
    for k in ("id", "batch", "evaluator"):
        if not non_empty_str(data.get(k)):
            return f"control.{k} must be a non-empty string"
    if "dimension" in data and data["dimension"] is not None and not non_empty_str(
            data["dimension"]):
        return "control.dimension must be a non-empty string or null"
    if not valid_digest(data.get("case"), allow_zero=False):
        return "control.case must be a non-zero sha256 digest"
    for k in ("expected", "outcome"):
        if data.get(k) not in OUTCOMES:
            return f"control.{k} {data.get(k)!r} is not conforms, does_not_conform or unobserved"
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("log")
    ap.add_argument("kind", choices=("check", "control"))
    ap.add_argument("--actor", required=True)
    ap.add_argument("--data-file", required=True)
    ap.add_argument("--evidence-dir")
    ap.add_argument("--source", default="")
    a = ap.parse_args()

    if not non_empty_str(a.actor):
        sys.exit("refused: --actor must be a non-empty string")
    log_path = pathlib.Path(a.log)
    if not log_path.is_file():
        sys.exit(f"refused: log not found: {a.log}")
    problems = record.verify(a.log)
    if problems:
        sys.exit("refused: log does not verify:\n" + "\n".join(problems))
    try:
        data = json.loads(pathlib.Path(a.data_file).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        sys.exit(f"refused: cannot read --data-file: {e}")

    err = validate_check(data, a.evidence_dir) if a.kind == "check" else validate_control(data)
    if err:
        sys.exit(f"refused: {err}")

    files = {}
    if a.kind == "check" and data.get("evidence") is not None:
        ev_path = str(pathlib.Path(a.evidence_dir) / data["evidence"]["name"])
        files[ev_path] = record.digest_file(ev_path)
    entry = record.append(a.log, {"type": a.kind, "at": record.now(), "actor": a.actor,
                                  "source": a.source, "files": files, "data": data})
    print(f"recorded event {entry['seq']} ({entry['type']}) at {entry['at']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
