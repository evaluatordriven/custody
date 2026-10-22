#!/usr/bin/env python3
"""The custody recorder must catch tampering, and make_record --log must build a record that verifies.

Builds a small log from the minimal example: bar frozen, two approvals, work started, the work produced,
every check and control, a disposition. It checks that the record built from it reads OK at CL1, that its
times come from the log, and that an edited, reordered or truncated log is refused. Standard library
only.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
REC, MAKE, CHECK = (str(ROOT / p) for p in ("tools/record.py", "tools/make_record.py",
                                            "checker/check.py"))


def run(*args, ok=True):
    r = subprocess.run([sys.executable, *args], capture_output=True, text=True)
    if ok and r.returncode:
        sys.exit(f"command failed: {args}\n{r.stdout}{r.stderr}")
    return r


def main():
    tmp = pathlib.Path(tempfile.mkdtemp())
    ex = tmp / "ex"
    shutil.copytree(ROOT / "examples" / "minimal", ex)
    log = str(tmp / "job.jsonl")
    inputs = json.loads((ex / "inputs.json").read_text())
    import hashlib
    bar = hashlib.sha256((ex / "bar.md").read_bytes()).hexdigest()
    run(REC, "init", log, "--job", "log test")
    run(REC, "add", log, "bar-frozen", "--actor", "Casey Park")
    for role, who in (("buyer", "Casey Park"), ("specialist", "Riley Moss")):
        run(REC, "add", log, "approval", "--actor", who, "--data",
            json.dumps({"role": role, "barDigest": bar}))
    run(REC, "add", log, "work-started", "--actor", "Alex Kim")
    stale = dict(inputs["checks"][0], outcome="does_not_conform")
    run(REC, "add", log, "check", "--actor", stale["evaluator"], "--data", json.dumps(stale))
    run(REC, "add", log, "artifact-produced", "--actor", "Drafting Agent")
    run(REC, "add", log, "check", "--actor", "screening",
        "--data", json.dumps({"candidate": "x", "item": "07", "run": 1, "outcome": "holds up"}))
    for c in inputs["checks"]:
        run(REC, "add", log, "check", "--actor", c["evaluator"], "--data", json.dumps(c))
    for k in inputs["controls"]:
        run(REC, "add", log, "control", "--actor", k["evaluator"], "--data", json.dumps(k))
    d = {k: v for k, v in inputs["disposition"].items() if k not in ("by", "at")}
    run(REC, "add", log, "disposition", "--actor", inputs["disposition"]["by"],
        "--data", json.dumps(d))

    problems = []
    if run(REC, "verify", log, ok=False).returncode:
        problems.append("an untouched log does not verify")
    out = ex / "from-log.json"
    run(MAKE, str(ex / "inputs.json"), str(out), "--log", log)
    report = json.loads(run(CHECK, str(out), "--files", str(ex), "--bar", str(ex / "bar.md"),
                            "--evidence", str(ex / "evidence"), ok=False).stdout)
    if (report["verdict"], report["levelAchieved"]) != ("OK", "CL1"):
        problems.append(f"record built from the log reads {report['verdict']}/{report['levelAchieved']}")
    if len(json.loads(out.read_text())["predicate"]["checks"]) != len(inputs["checks"]):
        problems.append("a screening reading, or a check of an earlier artifact, leaked into the "
                        "record's checks")
    events = [json.loads(x) for x in pathlib.Path(log).read_text().splitlines()]
    pred = json.loads(out.read_text())["predicate"]
    started = next(e["at"] for e in events if e["type"] == "work-started")
    if (pred["bar"]["frozenAt"] != events[1]["at"] or pred["disposition"]["at"] != events[-1]["at"]
            or pred["startedAt"] != started):
        problems.append("record times do not come from the log")

    lines = pathlib.Path(log).read_text().splitlines()
    plants = {"edited": lines[:2] + [lines[2].replace("Casey Park", "Someone Else")] + lines[3:],
              "reordered": [lines[0], lines[2], lines[1]] + lines[3:],
              "truncated": lines[:1] + lines[2:]}
    for name, body in plants.items():
        bad = tmp / f"{name}.jsonl"
        bad.write_text("\n".join(body) + "\n")
        if not run(REC, "verify", str(bad), ok=False).returncode:
            problems.append(f"a {name} log verifies")
        if not run(MAKE, str(ex / "inputs.json"), str(tmp / "x.json"), "--log", str(bad),
                   ok=False).returncode:
            problems.append(f"make_record accepted a {name} log")
    shutil.rmtree(tmp)
    if problems:
        sys.exit("\n".join(problems))
    print("log check: recorder catches edited, reordered and truncated logs; record from log is OK/CL1")


if __name__ == "__main__":
    main()
