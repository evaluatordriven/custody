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
                 own fields (a check needs dimension, evaluator, run, batch and outcome; a control
                 needs id, batch, evaluator and case). A control's `expected` and `outcome` are
                 derived from its score row (or scores.tsv / scores.json in the log's folder) and any
                 disagreement or missing score row exits nonzero; other events of those types, such
                 as screening readings, are skipped and counted. Checks and controls count only if
                 recorded after the last `artifact-produced` event: earlier ones read an artifact
                 that has since been replaced. A check's `at` is always its event's time. Packages
                 cited by events are named by role (such as package-<role>.tar.gz, not source paths)
                 and verified against their cited digests so no rebuild can overwrite cited bytes.
  disposition    the last `disposition` event: its data, with `by` = actor and `at` = its time. Any
                 package it was given on is written as `x-on` (converting legacy `on`). With no such
                 event, the state comes from INPUTS.json, but `at` is the time the record is built:
                 a typed time is never used.
Fields the log does not supply come from INPUTS.json as before.
Standard library only.
"""
import csv
import hashlib
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True  # no cache files in the tree (v0.9.5)
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def role_name(val, role=None, require_role=False):
    if role:
        r = str(role).strip()
        if "/" in r or "\\" in r:
            sys.exit(f"package role {role!r} encodes a path instead of a role name")
        return r if r.startswith("package-") else f"package-{r}.tar.gz"
    s = str(val).strip() if val is not None else ""
    if s.startswith("package-") and "/" not in s and "\\" not in s:
        return s
    if require_role:
        sys.exit(f"package {val!r} lacks an explicit role name; pass 'role' (e.g. 'role': 'candidate')")
    if "/" in s or "\\" in s or ("." in s and not s.endswith(".tar.gz")):
        sys.exit(f"package {val!r} names a source file or path and lacks an explicit role name")
    return f"package-{s}.tar.gz"


def resolve(node, base):
    if isinstance(node, dict):
        if set(node) == {"file"}:
            return {"sha256": digest(base / node["file"])}
        if set(node) == {"evidenceFile"}:
            path = base / node["evidenceFile"]
            return {"name": path.name, "sha256": digest(path)}
        if "package" in node and set(node) <= {"package", "role", "sha256"}:
            p = base / node["package"]
            pkg = base / role_name(node["package"], node.get("role"), require_role=True)
            b = p.read_bytes()
            h = hashlib.sha256(b).hexdigest()
            if "sha256" in node and node["sha256"] != h:
                sys.exit(f"package {pkg.name} digest mismatch against cited {node['sha256']}")
            if pkg.exists() and digest(pkg) != h:
                sys.exit(f"refusing to overwrite cited package {pkg.name} with different bytes")
            if not pkg.exists():
                pkg.write_bytes(b)
            return {"name": pkg.name, "sha256": h}
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


def norm_out(v):
    if v is None:
        return None
    s = str(v).strip()
    low = s.lower()
    if low in ("conforms", "pass", "passed", "ok", "true", "clean", "1"):
        return "conforms"
    if low in ("does_not_conform", "fail", "failed", "false", "planted", "0"):
        return "does_not_conform"
    if low == "unobserved":
        return "unobserved"
    return s


def parse_row(row):
    if not isinstance(row, dict):
        return None
    exp = norm_out(row.get("expected") or row.get("want") or row.get("kind") or row.get("type"))
    out = norm_out(row.get("outcome") or row.get("actual") or row.get("result")
                   or row.get("verdict") or row.get("status"))
    if not exp and "planted" in row:
        exp = "does_not_conform" if row["planted"] in (True, "true", "1", 1) else "conforms"
    if not out and "passed" in row:
        val = row["passed"] in (True, "true", "1", 1, "pass")
        out = exp if val else ("conforms" if exp == "does_not_conform" else "does_not_conform")
    if not out and "caught" in row:
        val = row["caught"] in (True, "true", "1", 1, "yes")
        out = exp if val else ("conforms" if exp == "does_not_conform" else "does_not_conform")
    if exp and out:
        return (exp, out)
    return None


def load_scores(data, events, base, log_path):
    scores = {}

    def add(row, cid=None, ev=None, b=None):
        res = parse_row(row)
        if not res:
            return
        cid = cid or row.get("id") or row.get("control") or row.get("control_id") or row.get("case")
        ev = ev or row.get("evaluator") or row.get("reader")
        b = b or row.get("batch")
        if cid:
            scores[str(cid)] = res
            if ev:
                scores[(str(cid), str(ev))] = res
            if b and ev:
                scores[(str(cid), str(b), str(ev))] = res

    for key in ("scores", "scoreRows", "controlScores", "score_rows"):
        rows = data.pop(key, None)
        if isinstance(rows, list):
            for r in rows:
                add(r)
        elif isinstance(rows, dict):
            for k, r in rows.items():
                add(r, cid=k)
    sfile = data.pop("scoreFile", None) or data.pop("scoresFile", None)
    dirs = [log_path.parent, base] if log_path else [base]
    cand = [base / sfile] if sfile else []
    for d in dirs:
        for name in ("scores.tsv", "scores.csv", "scores.json", "scores.jsonl",
                     "control_scores.tsv", "control_scores.csv", "control_scores.json",
                     "controls.tsv", "controls.csv"):
            if (d / name) not in cand:
                cand.append(d / name)
    for p in cand:
        if not p.is_file():
            continue
        txt = p.read_text(encoding="utf-8").strip()
        if not txt:
            continue
        if p.suffix == ".json":
            obj = json.loads(txt)
            if isinstance(obj, list):
                for r in obj:
                    add(r)
            elif isinstance(obj, dict):
                for k, r in obj.items():
                    if isinstance(r, list):
                        for item in r:
                            add(item)
                    else:
                        add(r, cid=k)
        elif p.suffix == ".jsonl":
            for line in txt.splitlines():
                if line.strip():
                    add(json.loads(line))
        else:
            delim = "\t" if p.suffix == ".tsv" or "\t" in txt.splitlines()[0] else ","
            for r in csv.DictReader(txt.splitlines(), delimiter=delim):
                add(r)
    for e in events:
        if e.get("type") in ("score", "score-row", "control-score", "scores"):
            d = e.get("data") or {}
            add(d.get("scoreRow") or d.get("score_row") or d)
    return scores


def check_packages(events, dirs):
    seen = {}
    for e in events:
        d = e.get("data")
        if not isinstance(d, dict):
            continue
        pkgs = []
        if e.get("type") in ("package", "package-built", "artifact-produced", "disposition"):
            for k in ("package", "x-on", "on", "artifact"):
                if k in d:
                    pkgs.append((d[k], d.get("sha256") or d.get("digest"), d.get("role")))
        for sub in d.values():
            if isinstance(sub, dict) and ("name" in sub or "package" in sub) and "sha256" in sub:
                pkgs.append((sub.get("name") or sub.get("package"), sub["sha256"], sub.get("role")))
        for pkg, h, role in pkgs:
            if isinstance(pkg, dict):
                h = h or pkg.get("sha256") or (pkg.get("digest") or {}).get("sha256")
                role = role or pkg.get("role")
                pkg = pkg.get("name") or pkg.get("package") or pkg.get("role")
            if isinstance(h, dict):
                h = h.get("sha256")
            if not pkg and not role:
                continue
            rname = role_name(pkg, role)
            if h and HEX64.match(str(h)):
                if rname in seen and seen[rname] != h:
                    sys.exit(f"package {rname} digest changed across rebuilds ({seen[rname]} != {h})")
                seen[rname] = str(h)
                found = False
                for folder in dirs:
                    for cand in ({str(pkg), rname} if pkg else {rname}):
                        f = folder / cand
                        if f.is_file():
                            found = True
                            if digest(f) != str(h):
                                sys.exit(f"cited package {cand} does not match its sha256 {h}")
                if not found:
                    sys.exit(f"cited package {rname} not found")


def fix_disp(disp):
    out = dict(disp)
    role = out.pop("role", None)
    if "on" in out:
        val = out.pop("on")
        out.setdefault("x-on", role_name(val, role) if isinstance(val, str) else val)
    if "x-on" in out and isinstance(out["x-on"], str):
        out["x-on"] = role_name(out["x-on"], role)
    return out


def from_log(data, log, base=None):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import record  # tools/record.py
    problems = record.verify(log)
    if problems:
        sys.exit("custody log does not verify; nothing written:\n" + "\n".join(problems))
    log_path = pathlib.Path(log).resolve()
    base = base or log_path.parent
    events = record.read(log)
    check_packages(events, [log_path.parent, base])
    scores = load_scores(data, events, base, log_path)
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
            "control": {"id", "batch", "evaluator", "case"},
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
            if kind == "control":
                ctls = []
                for e in fit:
                    d = dict(e["data"])
                    cid = str(d["id"])
                    ev = str(d["evaluator"])
                    b = str(d["batch"])
                    sr = (scores.get((cid, b, ev)) or scores.get((cid, ev)) or scores.get(cid)
                          or parse_row(d.get("scoreRow") or d.get("score_row") or d.get("score")))
                    if not sr:
                        sys.exit(f"control {cid}: missing score row")
                    exp, out = sr
                    if ("expected" in d and d["expected"] is not None
                            and norm_out(d["expected"]) != exp):
                        sys.exit(f"control {cid}: event expected {d['expected']!r} "
                                 f"disagrees with score row {exp!r}")
                    if ("outcome" in d and d["outcome"] is not None
                            and norm_out(d["outcome"]) != out):
                        sys.exit(f"control {cid}: event outcome {d['outcome']!r} "
                                 f"disagrees with score row {out!r}")
                    for k in ("scoreRow", "score_row", "score"):
                        d.pop(k, None)
                    d["expected"], d["outcome"] = exp, out
                    ctls.append(d)
                data[field] = ctls
            else:
                data[field] = [dict(e["data"], at=e["at"]) if kind == "check" else dict(e["data"])
                               for e in fit]
    done = [e for e in events if e["type"] == "disposition"]
    if done:
        data["disposition"] = fix_disp(dict(done[-1]["data"], by=done[-1]["actor"],
                                            at=done[-1]["at"]))
    elif "disposition" in data:
        data["disposition"] = fix_disp(dict(data["disposition"], at=record.now()))
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
        data = from_log(data, log, base)
    elif "disposition" in data and isinstance(data["disposition"], dict):
        data["disposition"] = fix_disp(data["disposition"])
    record = {"_type": "https://in-toto.io/Statement/v1",
              "subject": subject(data.pop("subject"), base),
              "predicateType": "https://evaluatordriven.com/custody/v1",
              "predicate": resolve(data, base)}
    pathlib.Path(sys.argv[2]).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {sys.argv[2]}")


if __name__ == "__main__":
    main()

