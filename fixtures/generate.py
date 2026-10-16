#!/usr/bin/env python3
"""Regenerate fixtures/*.json and fixtures/expected.json. Deterministic; standard library only.

Each failing fixture changes one thing in a valid record and names the one requirement it breaks.
Run: python3 fixtures/generate.py
"""
import copy
import hashlib
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FILES = HERE / "files"
EVIDENCE = HERE / "evidence"


def sha(data):
    return {"sha256": hashlib.sha256(data).hexdigest()}


def text_digest(text):
    return sha(text.encode())


def write_inputs():
    FILES.mkdir(exist_ok=True)
    EVIDENCE.mkdir(exist_ok=True)
    (FILES / "report.md").write_text("# Quarterly vendor report\n\nThree vendors, one recommendation.\n")
    for name in ("harness-gpt.log", "harness-gemini.log", "signature-verification.txt"):
        (EVIDENCE / name).write_text(f"fixture evidence: {name}\nendpoint pinned; write tools off\n")


def ext(req, subject, name, reader="Dana Reyes"):
    return {"requirement": req, "subject": subject, "readBy": reader,
            "evidence": {"name": name, "sha256": sha((EVIDENCE / name).read_bytes())["sha256"]}}


def check(dim, ev, run, batch="B1", outcome="conforms", at="2026-10-03T10:00:00Z"):
    return {"dimension": dim, "evaluator": ev, "run": run, "batch": batch, "at": at,
            "outcome": outcome, "score": None,
            "failureCondition": f"{dim} reads does_not_conform if its criterion is not met",
            "evidence": text_digest(f"notes {dim} {ev} {run}") if outcome != "unobserved" else None,
            "unobserved": {"channel": "reader", "reason": "source not reachable"}
            if outcome == "unobserved" else None}


def base(level):
    bar = text_digest("bar: vendor report")
    model = lambda fam, ident, end: {"family": fam, "identifier": ident, "endpoint": end,
                                     "readOnly": True}
    p = {
        "specVersion": "0.9.2", "levelClaimed": level,
        "bar": {"digest": bar, "frozenAt": "2026-10-01T09:00:00Z", "author": "Morgan Lee",
                "dimensions": [{"id": "D1", "criterion": "Every figure cites its source", "scale": None},
                               {"id": "D2", "criterion": "The recommendation follows from the figures",
                                "scale": None}],
                "approvals": [{"role": "buyer", "by": "Avery Chen", "barDigest": bar,
                               "at": "2026-10-01T08:00:00Z", "adopted": None},
                              {"role": "specialist", "by": "Priya Nair", "barDigest": bar,
                               "at": "2026-10-01T08:30:00Z", "adopted": None}],
                "publishedAt": "https://example.org/bars/vendor-report" if level == "CL3" else None,
                "groundTruth": [{"name": "Q3 vendor price sheet", "version": "2026-09-30",
                                 "digest": text_digest("price sheet")}],
                "dissent": []},
        "maker": {"name": "Drafting Agent", "version": "1.4", "method": text_digest("method"),
                  "model": None},
        "producedAt": "2026-10-02T09:00:00Z",
        "instrument": {"rubric": text_digest("rubric"), "runner": text_digest("runner")},
        "evaluators": [{"id": "E1", "name": "Sam Ortiz", "kind": "person", "model": None,
                        "script": None}],
        "checks": [check("D1", "E1", 1), check("D2", "E1", 1)],
        "controls": [{"id": "K1", "batch": "B1", "evaluator": "E1", "case": text_digest("control"),
                      "expected": "does_not_conform", "outcome": "does_not_conform"}],
        "disagreements": [], "violations": [], "separationGaps": [],
        "retention": {"location": "s3://records/vendor-report", "public": False},
        "external": [],
        "disposition": {"state": "given", "by": "Avery Chen", "at": "2026-10-04T09:00:00Z",
                        "acknowledgesUnobserved": []},
    }
    if level in ("CL2", "CL3"):
        p["evaluators"] = [
            {"id": "E1", "name": "Reader GPT", "kind": "model", "script": None,
             "model": model("gpt", "gpt-6.1", "api.openai.example")},
            {"id": "E2", "name": "Reader Gemini", "kind": "model", "script": None,
             "model": model("gemini", "gemini-3.8-flash", "api.google.example")}]
        p["checks"] = [check(d, e, r) for e in ("E1", "E2") for d in ("D1", "D2") for r in (1, 2)]
        p["controls"] = [{"id": f"K{e}", "batch": "B1", "evaluator": e, "case": text_digest("ctl"),
                          "expected": "does_not_conform", "outcome": "does_not_conform"}
                         for e in ("E1", "E2")]
        p["spread"] = [{"dimension": d, "evaluator": e, "runs": 2, "agreement": 2}
                       for e in ("E1", "E2") for d in ("D1", "D2")]
        p["external"] = [ext("CL1-15", "E1", "harness-gpt.log"),
                         ext("CL1-15", "E2", "harness-gemini.log")]
    if level == "CL3":
        p["demonstrations"] = [{"dimension": d, "evaluator": e, "planted": text_digest(f"plant {d}"),
                                "outcome": "does_not_conform", "at": "2026-10-02T12:00:00Z"}
                               for e in ("E1", "E2") for d in ("D1", "D2")]
        p["external"].append(ext("CL3-3", "record", "signature-verification.txt"))
    subject = [{"name": "report.md", "digest": sha((FILES / "report.md").read_bytes())}]
    return {"_type": "https://in-toto.io/Statement/v1", "subject": subject,
            "predicateType": "https://evaluatordriven.com/custody/v1", "predicate": p}


def mutate(level, fn):
    r = base(level)
    fn(r, r["predicate"])
    return r


def dnc(p, i):  # turn check i into a does_not_conform with its violation recorded
    p["checks"][i]["outcome"] = "does_not_conform"
    p["violations"].append({"dimension": p["checks"][i]["dimension"], "description": "uncited figure"})


def unobs(p, i):
    p["checks"][i].update(outcome="unobserved", evidence=None,
                          unobserved={"channel": "reader", "reason": "source not reachable"})


def same_model(p, declared, level="CL1"):  # the evaluator E1 is a session of the maker's model
    gpt = {"family": "gpt", "identifier": "gpt-6.1", "endpoint": "api.openai.example",
           "readOnly": True}
    p["maker"]["model"] = dict(gpt)
    if level == "CL1":
        p["evaluators"][0].update(kind="model", model=dict(gpt))
        p["external"] = [ext("CL1-15", "E1", "harness-gpt.log")]
    if declared:
        p["evaluators"][0]["sameModelAsMaker"] = True


def late_bar(p):
    p["bar"]["frozenAt"] = "2026-10-02T10:00:00Z"


def runs_disagree(p):
    p["checks"][1]["outcome"] = "does_not_conform"  # E1, D1, run 2
    p["violations"].append({"dimension": "D1", "description": "one run found an uncited figure"})
    p["spread"][0]["agreement"] = 1
    p["disagreements"].append({"dimension": "D1", "checks": [0, 1], "note": "runs split"})


# name: (level, mutation, verdict, level achieved, routing, the one failing requirement or None)
CASES = {
    "cl1-pass-basic": ("CL1", lambda r, p: None, "OK", "CL1", "none", None),
    "cl1-pass-unobserved-acknowledged": ("CL1", lambda r, p: (unobs(p, 1), p["disposition"].update(
        acknowledgesUnobserved=["D2"])), "OK", "CL1", "to approver", None),
    "cl1-pass-not-yet-given-with-violation": ("CL1", lambda r, p: (dnc(p, 0), p["disposition"].update(
        state="not_yet_given")), "OK", "CL1", "to approver", None),
    "cl1-pass-adopted-specialist": ("CL1", lambda r, p: p["bar"]["approvals"][1].update(
        by="Avery Chen", adopted={"document": "WCAG", "version": "2.2"}), "OK", "CL1", "none", None),
    "cl1-fail-no-check-for-dimension": ("CL1", lambda r, p: p["checks"].pop(1),
                                        "FAILED", "none", "none", "CL1-7"),
    "cl1-fail-approval-bound-to-other-bar": ("CL1", lambda r, p: p["bar"]["approvals"][0].update(
        barDigest=text_digest("other bar")), "FAILED", "none", "none", "CL1-3"),
    "cl1-fail-evaluator-is-bar-author": ("CL1", lambda r, p: p["evaluators"][0].update(
        name="Morgan Lee"), "FAILED", "none", "none", "CL1-6"),
    "cl1-fail-violation-not-recorded": ("CL1", lambda r, p: p["checks"][0].update(
        outcome="does_not_conform"), "FAILED", "none", "none", "CL1-11"),
    "cl1-fail-dimension-scale-missing-floor": ("CL1", lambda r, p: p["bar"]["dimensions"][0].update(
        scale={"anchors": {"1": "poor", "5": "fully meets"}, "threshold": 3}),
        "FAILED", "none", "none", "CL1-2"),
    "cl1-fail-missing-disagreements-field": ("CL1", lambda r, p: p.pop("disagreements"),
                                             "FAILED", "none", "none", "CR-2"),
    "cl1-fail-missing-violations-field": ("CL1", lambda r, p: p.pop("violations"),
                                          "FAILED", "none", "none", "CL1-11"),
    "cl1-fail-no-control-in-batch": ("CL1", lambda r, p: p["controls"][0].update(batch="B9"),
                                     "FAILED", "none", "none", "CL1-9"),
    "cl1-fail-unobserved-not-acknowledged": ("CL1", lambda r, p: unobs(p, 1),
                                             "FAILED", "none", "to approver", "CL1-13"),
    "cl1-fail-tampered-artifact": ("CL1", lambda r, p: r["subject"][0].update(
        digest=text_digest("a different report")), "FAILED", "none", "none", "CL1-14"),
    "cl1-fail-bar-frozen-late": ("CL1", lambda r, p: late_bar(p), "FAILED", "none", "none", "CL1-1"),
    "cl1-fail-maker-method-missing": ("CL1", lambda r, p: p["maker"].pop("method"),
                                      "FAILED", "none", "none", "CL1-4"),
    "cl1-fail-not-a-custody-statement": ("CL1", lambda r, p: r.update(
        predicateType="https://slsa.dev/verification_summary/v1"), "FAILED", "none", "none", "CR-1"),
    "cl1-fail-scored-without-scale": ("CL1", lambda r, p: p["checks"][0].update(score=8),
                                      "FAILED", "none", "none", "CL1-2"),
    "cl1-fail-instrument-not-pinned": ("CL1", lambda r, p: p["instrument"].pop("runner"),
                                       "FAILED", "none", "none", "CL1-5"),
    "cl1-fail-conforms-without-evidence": ("CL1", lambda r, p: p["checks"][0].update(evidence=None),
                                           "FAILED", "none", "none", "CL1-8"),
    "cl1-fail-disagreement-not-recorded": ("CL1", lambda r, p: (
        p["checks"].append(check("D1", "E1", 2, outcome="does_not_conform")),
        p["violations"].append({"dimension": "D1", "description": "run 2 found an uncited figure"})),
        "FAILED", "none", "none", "CL1-10"),
    "cl1-fail-retention-missing": ("CL1", lambda r, p: p.pop("retention"),
                                   "FAILED", "none", "none", "CL1-12"),
    "cl1-pass-script-evaluator": ("CL1", lambda r, p: (p["evaluators"].append({
        "id": "S1", "name": "lint-figures", "kind": "script", "model": None,
        "script": {"name": "lint_figures.py", "author": "Lee Park", "digest": text_digest("lint")}}),
        p["checks"].append(check("D1", "S1", 1)), p["controls"].append({
            "id": "KS", "batch": "B1", "evaluator": "S1", "case": text_digest("control"),
            "expected": "does_not_conform", "outcome": "does_not_conform"})),
        "OK", "CL1", "none", None),
    "cl1-fail-script-evaluator-unpinned": ("CL1", lambda r, p: (p["evaluators"].append({
        "id": "S1", "name": "lint-figures", "kind": "script", "model": None, "script": None}),
        p["checks"].append(check("D1", "S1", 1))), "FAILED", "none", "none", "CL1-5"),
    "cl1-fail-script-written-by-maker": ("CL1", lambda r, p: (p["evaluators"].append({
        "id": "S1", "name": "lint-figures", "kind": "script", "model": None,
        "script": {"name": "lint_figures.py", "author": "Drafting Agent", "digest": text_digest("l")}}),
        p["checks"].append(check("D1", "S1", 1))), "FAILED", "none", "none", "CL1-6"),
    "cl1-pass-legacy-no-script-field": ("CL1", lambda r, p: p["evaluators"][0].pop("script"),
                                        "OK", "CL1", "none", None),
    "cl1-pass-same-model-session-declared": ("CL1", lambda r, p: same_model(p, True),
                                             "OK", "CL1", "none", None),
    "cl1-fail-same-model-session-undeclared": ("CL1", lambda r, p: same_model(p, False),
                                               "FAILED", "none", "none", "CL1-6"),
    "cl2-pass-same-model-session-declared": ("CL2", lambda r, p: same_model(p, True, "CL2"),
                                             "OK", "CL2", "none", None),
    "baseline-pass": ("baseline", lambda r, p: (late_bar(p), p.update(
        readsBeforeFreeze=["draft v1"])), "OK", "baseline", "none", None),
    "baseline-fail-no-reads-listed": ("baseline", lambda r, p: late_bar(p),
                                      "FAILED", "none", "none", "BL-1"),
    "baseline-fail-bar-frozen-at-same-instant": ("baseline", lambda r, p: (
        p["bar"].update(frozenAt=p["producedAt"]), p.update(readsBeforeFreeze=[])),
        "FAILED", "none", "none", "BL-1"),
    "cl1-unchecked-model-evaluator-settings-only": ("CL1", lambda r, p: p["evaluators"][0].update(
        kind="model", model={"family": "gpt", "identifier": "gpt-6.1", "endpoint": "api.example",
                             "readOnly": True}), "NOT-CHECKABLE", "none", "none", None),
    "cl2-pass-basic": ("CL2", lambda r, p: None, "OK", "CL2", "none", None),
    "cl2-pass-runs-disagree-recorded": ("CL2", lambda r, p: runs_disagree(p), "OK", "CL2", "none", None),
    "cl2-pass-legacy-evidence-tag": ("CL2", lambda r, p: [x.update(requirement="CL2-4")
                                                          for x in p["external"]],
                                     "OK", "CL2", "none", None),
    "cl2-pass-maker-is-other-model": ("CL2", lambda r, p: p["maker"].update(model={
        "family": "claude", "identifier": "opus-5.5", "endpoint": "api.anthropic.example",
        "readOnly": False}), "OK", "CL2", "none", None),
    "cl2-fail-one-run-only": ("CL2", lambda r, p: [p["checks"].pop(i) for i in (7, 5)],
                              "FAILED", "CL1", "none", "CL2-1"),
    "cl2-fail-evaluator-not-read-only": ("CL2", lambda r, p: p["evaluators"][1]["model"].update(
        readOnly=False), "FAILED", "CL1", "none", "CL2-2"),
    "cl2-pass-one-evaluator-shares-maker-family": ("CL2", lambda r, p: p["maker"].update(model={
        "family": "gpt", "identifier": "gpt-6.0", "endpoint": "api.other.example",
        "readOnly": False}), "OK", "CL2", "none", None),
    "cl2-fail-every-evaluator-shares-maker-family": ("CL2", lambda r, p: (p["maker"].update(model={
        "family": "gpt", "identifier": "gpt-6.0", "endpoint": "api.other.example",
        "readOnly": False}), p["evaluators"][1]["model"].update(family="gpt")),
        "FAILED", "CL1", "none", "CL2-3"),
    "cl2-fail-evidence-digest-mismatch": ("CL2", lambda r, p: p["external"][0]["evidence"].update(
        sha256="0" * 64), "FAILED", "none", "none", "CL1-15"),
    "cl2-unchecked-independence-asserted-only": ("CL2", lambda r, p: p.update(external=[]),
                                                 "NOT-CHECKABLE", "none", "none", None),
    "cl3-pass-basic": ("CL3", lambda r, p: None, "OK", "CL3", "none", None),
    "cl3-pass-unobserved-not-yet-given": ("CL3", lambda r, p: (
        [unobs(p, i) for i in (2, 3)], p["disposition"].update(state="not_yet_given"),
        p["disagreements"].append({"dimension": "D2", "checks": [2, 6],
                                   "note": "E1 could not observe; E2 read conforms"})),
        "OK", "CL3", "to approver", None),
    "cl3-pass-adopted-specialist": ("CL3", lambda r, p: p["bar"]["approvals"][1].update(
        by="Avery Chen", adopted={"document": "in-toto Statement", "version": "v1"}),
        "OK", "CL3", "none", None),
    "cl3-fail-demonstration-after-check": ("CL3", lambda r, p: p["demonstrations"][0].update(
        at="2026-10-05T00:00:00Z"), "FAILED", "CL2", "none", "CL3-1"),
    "cl3-fail-bar-not-published": ("CL3", lambda r, p: p["bar"].update(publishedAt=None),
                                   "FAILED", "CL2", "none", "CL3-2"),
    "cl3-fail-no-signature-entry": ("CL3", lambda r, p: p["external"].pop(2),
                                    "FAILED", "CL2", "none", "CL3-3"),
    "cl3-unchecked-signature-read-by-maker": ("CL3", lambda r, p: p["external"][2].update(
        readBy="Drafting Agent"), "NOT-CHECKABLE", "CL2", "none", None),
    "cl2-unchecked-independence-read-by-maker": ("CL2", lambda r, p: p["external"][0].update(
        readBy="Drafting Agent"), "NOT-CHECKABLE", "none", "none", None),
}
# Level boundaries: each passes the level below and fails the next for exactly one reason.
BOUNDARIES = {"none|CL1": "cl1-fail-bar-frozen-late", "CL1|CL2": "cl2-fail-one-run-only",
              "CL2|CL3": "cl3-fail-bar-not-published"}


def main():
    write_inputs()
    for old in HERE.glob("*.json"):
        old.unlink()
    expected = {}
    for name, (level, fn, verdict, achieved, routing, fails) in CASES.items():
        (HERE / f"{name}.json").write_text(json.dumps(mutate(level, fn), indent=2) + "\n")
        expected[name] = {"verdict": verdict, "levelAchieved": achieved, "routing": routing,
                          "fails": fails}
    # schema-invalid by shape, though the failing requirement is CL1-11 (which owns these fields)
    schema_invalid = ["cl1-fail-missing-violations-field", "cl1-fail-dimension-scale-missing-floor"]
    (HERE / "expected.json").write_text(json.dumps({"cases": expected, "boundaries": BOUNDARIES,
                                                    "schemaInvalid": schema_invalid},
                                                   indent=2) + "\n")
    print(f"wrote {len(CASES)} fixtures")


if __name__ == "__main__":
    main()
