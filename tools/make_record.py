#!/usr/bin/env python3
"""Turn a plain inputs file into a custody/v1 record by computing every digest for you.

Usage: python3 tools/make_record.py INPUTS.json RECORD.json [--log JOB-LOG.jsonl]

INPUTS.json is the record's predicate written by hand, with three conveniences. Paths are relative
to INPUTS.json's folder.
  {"file": "bar.md"}               becomes {"sha256": "<digest of bar.md>"}
  {"evidenceFile": "harness.log"}  becomes {"name": "harness.log", "sha256": "<digest>"}
  "subject": {"files": ["a.md"]}   lists named files; {"dir": ".", "exclude": ["record/"]} lists
                                   every file under a folder except the excluded prefixes.

With --log, the times and events come from a custody log kept by tools/record.py as the work happened,
instead of being typed into INPUTS.json. The log must verify (an intact chain) or nothing is written.
From the log:
  bar.frozenAt   the time of the last `bar-frozen` event
  bar.approvals  the `approval` events after it: {role, by: actor, at, barDigest, adopted}
  startedAt      the time of the first `work-started` event: the earliest the work is known to have
                 begun, so a bar frozen (or frozen again) after it shows as frozen after the start
  producedAt     the time of the last `artifact-produced` event
  checks, controls, external
                 the `data` of each `check`, `control` and `external` event that carries that entry's
                 own fields (a check needs dimension, evaluator, run, batch and outcome); other events
                 of those types, such as screening readings, are skipped and counted. Checks and
                 controls count only if recorded after the last `artifact-produced` event: earlier
                 ones read an artifact that has since been replaced. A check's `at` is always its
                 event's time.
  disposition    the last `disposition` event: its data, with `by` = actor and `at` = its time. With
                 no such event, the state comes from INPUTS.json, but `at` is the time the record is
                 built: a typed time is never used.
Fields the log does not supply come from INPUTS.json as before.
Standard library only.
"""
import hashlib
import json
import pathlib
import sys

sys.dont_write_bytecode = True  # no cache files in the tree (v0.9.5)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve(node, base):
    if isinstance(node, dict):
        if set(node) == {"file"}:
            return {"sha256": digest(base / node["file"])}
        if set(node) == {"evidenceFile"}:
            path = base / node["evidenceFile"]
            return {"name": path.name, "sha256": digest(path)}
        return {k: resolve(v, base) for k, v in node.items()}
    if isinstance(node, list):
        return [resolve(v, base) for v in node]
    return node


def subject(spec, base):
    if "files" in spec:
        names = spec["files"]
    else:
        root = base / spec["dir"]
        names = sorted(str(p.relative_to(root)).replace("\\", "/") for p in root.rglob("*")
                       if p.is_file() and not any(str(p.relative_to(root)).startswith(x)
                                                  for x in spec.get("exclude", [])))
        base = root
    return [{"name": n, "digest": {"sha256": digest(base / n)}} for n in names]


def from_log(data, log):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import record  # tools/record.py
    problems = record.verify(log)
    if problems:
        sys.exit("custody log does not verify; nothing written:\n" + "\n".join(problems))
    events = record.read(log)
    frozen = [i for i, e in enumerate(events) if e["type"] == "bar-frozen"]
    if frozen:
        data["bar"]["frozenAt"] = events[frozen[-1]]["at"]
        data["bar"]["approvals"] = [
            {"role": e["data"]["role"], "by": e["actor"], "at": e["at"],
             "barDigest": {"sha256": e["data"]["barDigest"]}, "adopted": e["data"].get("adopted")}
            for e in events[frozen[-1] + 1:] if e["type"] == "approval"]
    started = [e for e in events if e["type"] == "work-started"]
    if started:
        data["startedAt"] = started[0]["at"]
    produced = [e for e in events if e["type"] == "artifact-produced"]
    if produced:
        data["producedAt"] = produced[-1]["at"]
    need = {"check": {"dimension", "evaluator", "run", "batch", "outcome"},
            "control": {"id", "batch", "evaluator", "case", "expected", "outcome"},
            "external": {"requirement", "subject", "evidence", "readBy"}}
    built = max((i for i, e in enumerate(events) if e["type"] == "artifact-produced"), default=-1)
    for kind, field in (("check", "checks"), ("control", "controls"), ("external", "external")):
        typed = [e for i, e in enumerate(events) if e["type"] == kind
                 and (kind == "external" or i > built)]
        stale = sum(1 for i, e in enumerate(events) if e["type"] == kind and kind != "external"
                    and i <= built)
        if stale:
            print(f"skipped {stale} '{kind}' event(s) recorded before the artifact was produced",
                  file=sys.stderr)
        fit = [e for e in typed if need[kind] <= set(e.get("data") or {})]
        if len(fit) < len(typed):
            print(f"skipped {len(typed) - len(fit)} '{kind}' event(s) without the record's fields",
                  file=sys.stderr)
        if fit:
            data[field] = [dict(e["data"], at=e["at"]) if kind == "check" else dict(e["data"])
                           for e in fit]
    done = [e for e in events if e["type"] == "disposition"]
    if done:
        data["disposition"] = dict(done[-1]["data"], by=done[-1]["actor"], at=done[-1]["at"])
    elif "disposition" in data:
        data["disposition"] = dict(data["disposition"], at=record.now())
    return data


def main():
    args = sys.argv[1:]
    log = None
    if "--log" in args:
        i = args.index("--log")
        log, args = args[i + 1], args[:i] + args[i + 2:]
    if len(args) != 2:
        sys.exit(__doc__)
    sys.argv[1:] = args
    src = pathlib.Path(args[0])
    base = src.resolve().parent
    data = json.loads(src.read_text(encoding="utf-8"))
    if log:
        data = from_log(data, log)
    record = {"_type": "https://in-toto.io/Statement/v1",
              "subject": subject(data.pop("subject"), base),
              "predicateType": "https://evaluatordriven.com/custody/v1",
              "predicate": resolve(data, base)}
    pathlib.Path(sys.argv[2]).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {sys.argv[2]}")


if __name__ == "__main__":
    main()
