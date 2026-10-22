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

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATE = {"given": "accepted", "not_yet_given": "not yet accepted", "declined": "declined"}
MADE_BY = {"person": "made by a person", "model": "made by an AI model", "script": "made by a script"}
OUTCOME = {"conforms": "conforms", "does_not_conform": "does not conform", "unobserved": "not observed"}


def checker():
    spec = importlib.util.spec_from_file_location("check", ROOT / "checker" / "check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fp(d):
    return (d or {}).get("sha256", "?")[:12] + "…"


def explain(r, report):
    p = r.get("predicate", {})
    bar, mk = p.get("bar", {}), p.get("maker", {})
    out = [f"CUSTODY RECORD — claims level {p.get('levelClaimed', '?')}, "
           f"specification {p.get('specVersion', '?')}", ""]
    out.append("1. What was made?")
    subj = r.get("subject", [])
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
    except ValueError:
        out.append("   The record does not say when the work started.")
    for d in bar.get("dimensions", []):
        out.append(f"   - {d.get('id')}: {d.get('criterion')}")
    for a in bar.get("approvals", []):
        same = (a.get("barDigest") or {}).get("sha256") == (bar.get("digest") or {}).get("sha256")
        out.append(f"   Approved by {a.get('by')} as {a.get('role')}, at {a.get('at')}"
                   + ("" if same else " — WARNING: for a different bar"))
    for g in bar.get("groundTruth", []):
        out.append(f"   Judged against: {g.get('name')}, version {g.get('version')}")
    for d in bar.get("dissent", []):
        out.append(f"   Disagreement about the bar, from {d.get('by')}: {d.get('note')}")
    out.append("")
    out.append("3. Who made it?")
    model = mk.get("model") or {}
    out.append(f"   {MADE_BY.get(mk.get('kind'), 'made by a maker of unstated kind').capitalize()}: "
               f"{mk.get('name', '?')}, version {mk.get('version', '?')}"
               + (f", using AI model {model.get('identifier')} ({model.get('family')} family)"
                  if model else ""))
    out += ["", "4. Who checked it?"]
    for e in p.get("evaluators", []):
        m, s = e.get("model") or {}, e.get("script") or {}
        line = f"   - {e.get('id')}: {e.get('name')}, a {e.get('kind')}"
        line += f", model {m.get('identifier')} ({m.get('family')} family)" if m else ""
        line += f", script written by {s.get('author')}" if s else ""
        line += " — a fresh session of the maker's own model, as declared" if e.get(
            "sameModelAsMaker") else ""
        out.append(line)
    out += ["", "5. What did they find?"]
    checks = p.get("checks", [])
    for d in bar.get("dimensions", []):
        mine = [c for c in checks if c.get("dimension") == d.get("id")]
        counts = {}
        for c in mine:
            counts[OUTCOME.get(c.get("outcome"), c.get("outcome"))] = counts.get(
                OUTCOME.get(c.get("outcome"), c.get("outcome")), 0) + 1
        summary = ", ".join(f"{n} {o}" for o, n in counts.items()) or "no checks"
        out.append(f"   - {d.get('id')}: {len(mine)} check{'' if len(mine) == 1 else 's'}: {summary}")
        for c in mine:
            if c.get("outcome") == "unobserved":
                u = c.get("unobserved") or {}
                out.append(f"       not observed by {c.get('evaluator')}: tried {u.get('channel')}; "
                           f"{u.get('reason')}")
    for v in p.get("violations", []):
        out.append(f"   Shortfall on {v.get('dimension')}: {v.get('description')}")
    for d in p.get("disagreements", []):
        out.append(f"   Readers disagreed on {d.get('dimension')}: {d.get('note') or 'see the checks'}")
    ctl = p.get("controls", [])
    caught = sum(1 for k in ctl if k.get("outcome") == k.get("expected"))
    out.append(f"   Planted tests: {len(ctl)}, of which {caught} came out as expected.")
    out += ["", "6. Who accepted it, and on what terms?"]
    ds = p.get("disposition", {})
    out.append(f"   {str(STATE.get(ds.get('state'), ds.get('state'))).capitalize()} by {ds.get('by')}, "
               f"at {ds.get('at')}")
    if ds.get("acknowledgesUnobserved"):
        out.append("   Accepted knowing these were not observed: "
                   + ", ".join(ds["acknowledgesUnobserved"]))
    out += ["", "Weak spots the record names (separation gaps):"]
    out += [f"   - {g}" for g in p.get("separationGaps", [])] or ["   - none listed"]
    for x in p.get("external", []):
        out.append(f"   Outside evidence for {x.get('requirement')} on {x.get('subject')}, "
                   f"read by {x.get('readBy')}")
    ret = p.get("retention") or {}
    out.append(f"   Kept at {ret.get('location', '?')}; "
               + ("public." if ret.get("public") else "not public."))
    out += ["", f"THE CHECKER'S ANSWER: {report['verdict']}, level reached "
                f"{report.get('levelAchieved')}, next step: {report.get('routing')}"]
    for rid, v in report.get("requirements", {}).items():
        if v["status"] != "OK":
            out.append(f"   - {rid} {v['status']}: {v['detail']}")
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
