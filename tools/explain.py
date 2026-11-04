#!/usr/bin/env python3
"""Print a custody record in plain words, for reviewers (non-normative tooling).

    python3 tools/explain.py RECORD.json [--files DIR] [--evidence DIR] [--bar FILE]

It follows the six questions in docs/REVIEWERS-GUIDE.md and ends with the free checker's answer. It
only reports what the record says, and adds no judgement of its own. Standard library only.
"""
import argparse
import importlib.util
import json
import pathlib
import sys
from datetime import datetime

sys.dont_write_bytecode = True  # no cache files in the tree (v0.9.5)

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATE = {"given": "accepted", "not_yet_given": "not yet accepted", "declined": "declined"}
MADE_BY = {"person": "made by a person", "model": "made by an AI model", "script": "made by a script"}
OUTCOME = {"conforms": "conforms", "does_not_conform": "does not conform", "unobserved": "not observed"}
LEVELS = {"CL1", "CL2", "CL3"}
DISCLAIMER = ("   A conformance level does not certify the quality of the work, nor the substance "
              "or depth of the readings: a conforming record makes work answerable, not correct, "
              "and no requirement claims that conforming work is good (SPEC.md §1; README.md).")


def fmt_level(lv):
    return f"{lv} · process" if isinstance(lv, str) and lv in LEVELS else str(lv)


def checker():
    spec = importlib.util.spec_from_file_location("check", ROOT / "checker" / "check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def as_dict(v):
    return v if isinstance(v, dict) else {}


def as_list(v):
    return v if isinstance(v, list) else []


def fp(d):
    return str(as_dict(d).get("sha256", "?"))[:12] + "…"


def explain(r, report):
    r, report = as_dict(r), as_dict(report)
    p = as_dict(r.get("predicate"))
    bar, mk = as_dict(p.get("bar")), as_dict(p.get("maker"))
    claim = p.get("levelClaimed", "?")
    reached = report.get("levelAchieved")
    out = [f"CUSTODY RECORD — claims level {fmt_level(claim) if reached in LEVELS else claim}, "
           f"specification {p.get('specVersion', '?')}"]
    if reached in LEVELS:
        out.append(DISCLAIMER)
    out.append("")
    out.append("1. What was made?")
    subj = [as_dict(s) for s in as_list(r.get("subject"))]
    out += [f"   - {s.get('name')} (fingerprint {fp(s.get('digest'))})" for s in subj[:6]]
    out += [f"   - and {len(subj) - 6} more files, each with its own fingerprint"] if len(subj) > 6 else []
    out += [f"   Started: {p.get('startedAt', '?')}", f"   Finished: {p.get('producedAt', '?')}", ""]
    out.append("2. What was it measured against?")
    out.append(f"   The bar was written by {bar.get('author', '?')} and fixed at "
               f"{bar.get('frozenAt', '?')} (fingerprint {fp(bar.get('digest'))}).")
    try:
        frozen, started = (datetime.fromisoformat(str(x).replace("Z", "+00:00"))
                           for x in (bar.get("frozenAt"), p.get("startedAt")))
        order = ("before" if frozen < started else "at the same moment as" if frozen == started
                 else "after")
        out.append(f"   The bar was fixed {order} the work started.")
    except (ValueError, TypeError):
        out.append("   The record does not say when the work started.")
    for d in (as_dict(x) for x in as_list(bar.get("dimensions"))):
        out.append(f"   - {d.get('id')}: {d.get('criterion')}")
    for a in (as_dict(x) for x in as_list(bar.get("approvals"))):
        same = as_dict(a.get("barDigest")).get("sha256") == as_dict(bar.get("digest")).get("sha256")
        out.append(f"   Approved by {a.get('by')} as {a.get('role')}, at {a.get('at')}"
                   + ("" if same else " — WARNING: for a different bar"))
    for g in (as_dict(x) for x in as_list(bar.get("groundTruth"))):
        out.append(f"   Judged against: {g.get('name')}, version {g.get('version')}")
    for d in (as_dict(x) for x in as_list(bar.get("dissent"))):
        out.append(f"   Disagreement about the bar, from {d.get('by')}: {d.get('note')}")
    out.append("")
    out.append("3. Who made it?")
    model = as_dict(mk.get("model"))
    out.append(f"   {MADE_BY.get(str(mk.get('kind')), 'made by a maker of unstated kind').capitalize()}: "
               f"{mk.get('name', '?')}, version {mk.get('version', '?')}"
               + (f", using AI model {model.get('identifier')} ({model.get('family')} family)"
                  if model else ""))
    out += ["", "4. Who checked it?"]
    for e in (as_dict(x) for x in as_list(p.get("evaluators"))):
        m, s = as_dict(e.get("model")), as_dict(e.get("script"))
        line = f"   - {e.get('id')}: {e.get('name')}, a {e.get('kind')}"
        line += f", model {m.get('identifier')} ({m.get('family')} family)" if m else ""
        line += f", script written by {s.get('author')}" if s else ""
        line += " — a fresh session of the maker's own model, as declared" if e.get(
            "sameModelAsMaker") else ""
        out.append(line)
    out += ["", "5. What did they find?"]
    checks = [as_dict(x) for x in as_list(p.get("checks"))]
    for d in (as_dict(x) for x in as_list(bar.get("dimensions"))):
        mine = [c for c in checks if c.get("dimension") == d.get("id")]
        counts = {}
        for c in mine:
            k = OUTCOME.get(str(c.get("outcome")), str(c.get("outcome")))
            counts[k] = counts.get(k, 0) + 1
        summary = ", ".join(f"{n} {o}" for o, n in counts.items()) or "no checks"
        out.append(f"   - {d.get('id')}: {len(mine)} check{'' if len(mine) == 1 else 's'}: {summary}")
        for c in mine:
            if c.get("outcome") == "unobserved":
                u = as_dict(c.get("unobserved"))
                out.append(f"       not observed by {c.get('evaluator')}: tried {u.get('channel')}; "
                           f"{u.get('reason')}")
    for v in (as_dict(x) for x in as_list(p.get("violations"))):
        out.append(f"   Shortfall on {v.get('dimension')}: {v.get('description')}")
    for d in (as_dict(x) for x in as_list(p.get("disagreements"))):
        out.append(f"   Readers disagreed on {d.get('dimension')}: {d.get('note') or 'see the checks'}")
    ctl = [as_dict(x) for x in as_list(p.get("controls"))]
    caught = sum(1 for k in ctl if k.get("outcome") == k.get("expected"))
    out.append(f"   Planted tests: {len(ctl)}, of which {caught} came out as expected.")
    out += ["", "6. Who accepted it, and on what terms?"]
    ds = as_dict(p.get("disposition"))
    out.append(f"   {str(STATE.get(str(ds.get('state')), ds.get('state'))).capitalize()} by {ds.get('by')}, "
               f"at {ds.get('at')}")
    ack = [str(x) for x in as_list(ds.get("acknowledgesUnobserved"))]
    if ack:
        out.append("   Accepted knowing these were not observed: " + ", ".join(ack))
    out += ["", "Weak spots the record names (separation gaps):"]
    out += [f"   - {g}" for g in as_list(p.get("separationGaps"))] or ["   - none listed"]
    for x in (as_dict(x) for x in as_list(p.get("external"))):
        out.append(f"   Outside evidence for {x.get('requirement')} on {x.get('subject')}, "
                   f"read by {x.get('readBy')}")
    ret = as_dict(p.get("retention"))
    out.append(f"   Kept at {ret.get('location', '?')}; "
               + ("public." if ret.get("public") else "not public."))
    out += ["", f"THE CHECKER'S ANSWER: {report.get('verdict')}, level reached "
                f"{fmt_level(reached)}, next step: {report.get('routing')}"]
    if reached in LEVELS:
        out.append(DISCLAIMER)
    for rid, v in as_dict(report.get("requirements")).items():
        v = as_dict(v)
        if v.get("status") != "OK":
            out.append(f"   - {rid} {v.get('status')}: {v.get('detail')}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("record")
    ap.add_argument("--files")
    ap.add_argument("--evidence")
    ap.add_argument("--bar")
    a = ap.parse_args()
    r = json.loads(pathlib.Path(a.record).read_text(encoding="utf-8"))
    print(explain(r, checker().verify(r, a.files, a.evidence, a.bar)))


if __name__ == "__main__":
    sys.exit(main())
