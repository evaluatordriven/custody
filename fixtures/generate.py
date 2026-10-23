#!/usr/bin/env python3
"""Regenerate fixtures/*.json, fixtures/evidence/ and fixtures/expected.json. Deterministic; standard
library only.

Each failing fixture changes one thing in a valid record and names the one requirement it breaks.
Run: python3 fixtures/generate.py
"""
import hashlib
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FILES = HERE / "files"
EVIDENCE = HERE / "evidence"
SPEC_VERSION = "0.9.5"


def sha(data):
    return {"sha256": hashlib.sha256(data).hexdigest()}


def text_digest(text):
    return sha(text.encode())


def evidence_file(name, text):
    """Write one evidence file and return its reference: {name, sha256}."""
    (EVIDENCE / name).write_text(text)
    return {"name": name, "sha256": sha(text.encode())["sha256"]}


def write_inputs():
    FILES.mkdir(exist_ok=True)
    EVIDENCE.mkdir(exist_ok=True)
    for old in EVIDENCE.iterdir():
        old.unlink()
    (FILES / "report.md").write_text("# Quarterly vendor report\n\nThree vendors, one recommendation.\n")
    (FILES / "bar.md").write_text("bar: vendor report")  # every fixture's bar.digest is this file
    for name in ("harness-gpt.log", "harness-gemini.log"):
        evidence_file(name, f"fixture evidence: {name}\nendpoint pinned; write tools off\n")
    evidence_file("record.sigstore.json", '{"fixture": "a Sigstore bundle would go here"}\n')


def ext(req, subject, name, reader="Dana Reyes"):
    return {"requirement": req, "subject": subject, "readBy": reader,
            "evidence": {"name": name, "sha256": sha((EVIDENCE / name).read_bytes())["sha256"]}}


def check(dim, ev, run, batch="B1", outcome="conforms", at="2026-10-03T10:00:00Z"):
    observed = outcome != "unobserved"
    return {"dimension": dim, "evaluator": ev, "run": run, "batch": batch, "at": at,
            "outcome": outcome, "score": None,
            "failureCondition": f"{dim} reads does_not_conform if its criterion is not met",
            "evidence": evidence_file(f"reading-{dim}-{ev}-{run}.md", f"notes {dim} {ev} {run}\n")
            if observed else None,
            "unobserved": None if observed else {"channel": "reader",
                                                 "reason": "source not reachable"}}


def control(cid, ev, expected, batch="B1"):
    return {"id": cid, "batch": batch, "evaluator": ev, "case": text_digest(f"case {cid}"),
            "expected": expected, "outcome": expected}


def model(fam, ident, end, read_only=True):
    return {"family": fam, "identifier": ident, "endpoint": end, "readOnly": read_only}


def base(level):
    bar = text_digest("bar: vendor report")
    p = {
        "specVersion": SPEC_VERSION, "levelClaimed": level,
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
        "maker": {"name": "Drafting Agent", "kind": "model", "version": "1.4",
                  "method": text_digest("method"), "model": None},
        "startedAt": "2026-10-01T10:00:00Z",
        "producedAt": "2026-10-02T09:00:00Z",
        "instrument": {"rubric": text_digest("rubric"), "runner": text_digest("runner")},
        "evaluators": [{"id": "E1", "name": "Sam Ortiz", "kind": "person", "model": None,
                        "script": None}],
        "checks": [check("D1", "E1", 1), check("D2", "E1", 1)],
        "controls": [control("K1", "E1", "does_not_conform"), control("K2", "E1", "conforms")],
        "disagreements": [], "violations": [], "separationGaps": [],
        "retention": {"location": "s3://records/vendor-report", "public": False},
        "external": [],
        "disposition": {"state": "given", "by": "Avery Chen", "at": "2026-10-04T09:00:00Z",
                        "acknowledgesUnobserved": []},
    }
    if level in ("CL2", "CL3"):
        p["maker"]["model"] = model("claude", "opus-5.5", "api.anthropic.example", False)
        p["evaluators"] = [
            {"id": "E1", "name": "Reader GPT", "kind": "model", "script": None,
             "model": model("gpt", "gpt-6.1", "api.openai.example")},
            {"id": "E2", "name": "Reader Gemini", "kind": "model", "script": None,
             "model": model("gemini", "gemini-3.8-flash", "api.google.example")}]
        p["checks"] = [check(d, e, r) for e in ("E1", "E2") for d in ("D1", "D2") for r in (1, 2)]
        p["controls"] = [control(f"K{e}", e, "does_not_conform") for e in ("E1", "E2")] + [
            control(f"KC{e}", e, "conforms") for e in ("E1", "E2")]
        p["spread"] = [{"dimension": d, "evaluator": e, "runs": 2, "agreement": 2}
                       for e in ("E1", "E2") for d in ("D1", "D2")]
        p["external"] = [ext("CL1-15", "E1", "harness-gpt.log"),
                         ext("CL1-15", "E2", "harness-gemini.log")]
    if level == "CL3":
        p["demonstrations"] = [{"dimension": d, "evaluator": e, "planted": text_digest(f"plant {d}"),
                                "outcome": "does_not_conform", "at": "2026-10-02T12:00:00Z"}
                               for e in ("E1", "E2") for d in ("D1", "D2")]
        p["external"].append(ext("CL3-3", "record", "record.sigstore.json"))
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
    gpt = model("gpt", "gpt-6.1", "api.openai.example")
    p["maker"]["model"] = dict(gpt)
    if level == "CL1":
        p["evaluators"][0].update(kind="model", model=dict(gpt))
        p["external"] = [ext("CL1-15", "E1", "harness-gpt.log")]
    if declared:
        p["evaluators"][0]["sameModelAsMaker"] = True


def maker_gpt(p):  # the maker is gpt-6.0, answered by a host no evaluator uses
    p["maker"]["model"] = model("gpt", "gpt-6.0", "api.other.example", False)


def panel(p, fams):  # CL2 evaluators by model family ("person" for a person); maker is gpt-6.0
    maker_gpt(p)
    ids = [f"E{i}" for i in range(1, len(fams) + 1)]
    p["evaluators"] = [{"id": e, "name": f"Reader {e}", "kind": "person" if f == "person" else "model",
                        "script": None, "model": None if f == "person" else model(
                            f, f"{f}-{e.lower()}", f"api.{f}.{e.lower()}.example")}
                       for e, f in zip(ids, fams)]
    p["checks"] = [check(d, e, r) for e in ids for d in ("D1", "D2") for r in (1, 2)]
    p["controls"] = [control(f"K{e}", e, "does_not_conform") for e in ids] + [
        control(f"KC{e}", e, "conforms") for e in ids]
    p["spread"] = [{"dimension": d, "evaluator": e, "runs": 2, "agreement": 2}
                   for e in ids for d in ("D1", "D2")]
    p["external"] = [ext("CL1-15", e, "harness-gpt.log" if f == "gpt" else "harness-gemini.log")
                     for e, f in zip(ids, fams) if f != "person"]


def late_bar(p):  # frozen after the work was finished
    p["bar"]["frozenAt"] = "2026-10-02T10:00:00Z"


def runs_disagree(p):
    p["checks"][1]["outcome"] = "does_not_conform"  # E1, D1, run 2
    p["violations"].append({"dimension": "D1", "description": "one run found an uncited figure"})
    p["spread"][0]["agreement"] = 1
    p["disagreements"].append({"dimension": "D1", "checks": [0, 1], "note": "runs split"})


def script_evaluator(p, author="Lee Park", digest=None):
    p["evaluators"].append({"id": "S1", "name": "lint-figures", "kind": "script", "model": None,
                            "script": {"name": "lint_figures.py", "author": author,
                                       "digest": digest or text_digest("lint")}})
    p["checks"].append(check("D1", "S1", 1))
    p["controls"] += [control("KS", "S1", "does_not_conform"), control("KSC", "S1", "conforms")]


def scored(p, score, outcome, threshold=3, anchors=None):  # D1 scored 1-5, threshold 3
    p["bar"]["dimensions"][0]["scale"] = {"anchors": anchors if anchors is not None else
                                          {"1": "no figure cites a source", "3": "most do",
                                           "5": "every figure cites its source"},
                                          "threshold": threshold, "floor": 1}
    p["checks"][0].update(score=score, outcome=outcome)
    if outcome == "does_not_conform":
        p["violations"].append({"dimension": "D1", "description": f"scored {score}"})
        p["disposition"]["state"] = "not_yet_given"


def second_reader_without_control(p):
    p["evaluators"].append({"id": "E2", "name": "Jo Rivera", "kind": "person", "model": None,
                            "script": None})
    p["checks"].append(check("D1", "E2", 1))


def extensions(p):
    p["x-producer"] = {"loop": "plumbline", "passRule": "mean >= 7 and min >= 6"}
    p["bar"]["x-note"] = "frozen by the conductor"
    p["checks"][0]["x-servedBy"] = "inference host recorded per call"


def refiled(p):
    p["x-refiledFrom"] = {"instrument": "an earlier internal record format", "verdict": "accept",
                          "originalRecordDigest": text_digest("earlier record")}


# name: (level, mutation, verdict, level achieved, routing, the one failing requirement or None)
CASES = {
    "cl1-pass-basic": ("CL1", lambda r, p: None, "OK", "CL1", "none", None),
    "cl1-fail-control-missed-checks-still-observed": ("CL1", lambda r, p: p["controls"][0].update(
        outcome="conforms"), "FAILED", "none", "none", "CL1-9"),
    "cl1-pass-control-missed-checks-unobserved": ("CL1", lambda r, p: (
        p["controls"][0].update(outcome="conforms"), unobs(p, 0), unobs(p, 1),
        p["disposition"].update(acknowledgesUnobserved=["D1", "D2"])),
        "OK", "CL1", "acknowledged", None),
    "cl1-pass-control-missed-its-dimension-unobserved": ("CL1", lambda r, p: (p["controls"][0].update(
        outcome="conforms", dimension="D2"), unobs(p, 1), p["disposition"].update(
            acknowledgesUnobserved=["D2"])), "OK", "CL1", "acknowledged", None),
    "cl1-fail-control-missed-its-dimension-observed": ("CL1", lambda r, p: p["controls"][0].update(
        outcome="unobserved", dimension="D1"), "FAILED", "none", "none", "CL1-9"),
    "cl1-fail-bar-file-differs": ("CL1", lambda r, p: [x.update(text_digest("another bar")) for x in
                                  [p["bar"]["digest"]] + [a["barDigest"] for a in p["bar"]["approvals"]]],
                                  "FAILED", "none", "none", "CL1-14"),
    "cl1-fail-buyer-is-maker-undisclosed": ("CL1", lambda r, p: p["bar"]["approvals"][0].update(
        by="Drafting Agent"), "FAILED", "none", "none", "CL1-11"),
    "cl1-pass-buyer-is-maker-disclosed": ("CL1", lambda r, p: (p["bar"]["approvals"][0].update(
        by="Drafting Agent"), p["separationGaps"].append(
            "Drafting Agent made the work and also approved the bar as buyer")), "OK", "CL1", "none", None),
    "cl1-pass-unobserved-acknowledged": ("CL1", lambda r, p: (unobs(p, 1), p["disposition"].update(
        acknowledgesUnobserved=["D2"])), "OK", "CL1", "acknowledged", None),
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
    "cl1-fail-no-control-in-batch": ("CL1", lambda r, p: [k.update(batch="B9") for k in p["controls"]],
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
    "cl1-pass-script-evaluator": ("CL1", lambda r, p: script_evaluator(p), "OK", "CL1", "none", None),
    "cl1-fail-script-evaluator-unpinned": ("CL1", lambda r, p: (
        script_evaluator(p), p["evaluators"][-1].update(script=None)),
        "FAILED", "none", "none", "CL1-5"),
    "cl1-fail-script-written-by-maker": ("CL1", lambda r, p: script_evaluator(p, "Drafting Agent"),
                                         "FAILED", "none", "none", "CL1-6"),
    "cl1-pass-legacy-no-script-field": ("CL1", lambda r, p: p["evaluators"][0].pop("script"),
                                        "OK", "CL1", "none", None),
    "cl1-pass-same-model-session-declared": ("CL1", lambda r, p: same_model(p, True),
                                             "OK", "CL1", "none", None),
    "cl1-fail-same-model-declared-untruly": ("CL1", lambda r, p: (same_model(p, True), p["evaluators"][0][
        "model"].update(identifier="gpt-6.0")), "FAILED", "none", "none", "CL1-6"),
    "cl1-fail-same-model-declared-false": ("CL1", lambda r, p: (same_model(p, False), p["evaluators"][0]
                                           .update(sameModelAsMaker=False)), "FAILED", "none", "none", "CL1-6"),
    "cl1-fail-same-model-session-undeclared": ("CL1", lambda r, p: same_model(p, False),
                                               "FAILED", "none", "none", "CL1-6"),
    "cl2-pass-same-model-session-declared": ("CL2", lambda r, p: same_model(p, True, "CL2"),
                                             "OK", "CL2", "none", None),
    "baseline-pass": ("baseline", lambda r, p: (late_bar(p), p.update(
        readsBeforeFreeze=["draft v1"])), "OK", "baseline", "none", None),
    "baseline-pass-model-evaluator-without-external": ("baseline", lambda r, p: (late_bar(p), p.update(
        readsBeforeFreeze=["draft v1"]), p["evaluators"][0].update(kind="model", model=model(
            "gpt", "gpt-6.1", "api.openai.example"))), "OK", "baseline", "none", None),
    "baseline-fail-no-reads-listed": ("baseline", lambda r, p: late_bar(p),
                                      "FAILED", "none", "none", "BL-1"),
    "cl1-unchecked-model-evaluator-settings-only": ("CL1", lambda r, p: p["evaluators"][0].update(
        kind="model", model=model("gpt", "gpt-6.1", "api.example")),
        "NOT-CHECKABLE", "none", "none", None),
    "cl2-pass-basic": ("CL2", lambda r, p: None, "OK", "CL2", "none", None),
    "cl2-fail-buyer-is-maker": ("CL2", lambda r, p: (p["bar"]["approvals"][0].update(
        by="Drafting Agent"), p["separationGaps"].append(
            "Drafting Agent made the work and also approved the bar as buyer")),
        "FAILED", "CL1", "none", "CL2-3"),
    "cl2-pass-maker-family-two-of-four": ("CL2", lambda r, p: panel(p, ["gpt", "gpt", "gemini", "grok"]),
                                          "OK", "CL2", "none", None),
    "cl2-fail-maker-family-two-of-three": ("CL2", lambda r, p: panel(p, ["gpt", "gpt", "gemini"]),
                                           "FAILED", "CL1", "none", "CL2-3"),
    "cl2-fail-maker-family-outweighs-a-person": ("CL2", lambda r, p: panel(p, ["gpt", "gpt", "person"]),
                                                 "FAILED", "CL1", "none", "CL2-3"),
    "cl2-pass-runs-disagree-recorded": ("CL2", lambda r, p: runs_disagree(p), "OK", "CL2", "none", None),
    "cl2-pass-legacy-evidence-tag": ("CL2", lambda r, p: [x.update(requirement="CL2-4")
                                                          for x in p["external"]],
                                     "OK", "CL2", "none", None),
    "cl2-pass-maker-is-person": ("CL2", lambda r, p: p["maker"].update(
        name="Robin Hale", kind="person", version="n/a (person)", model=None),
        "OK", "CL2", "none", None),
    "cl2-fail-one-run-only": ("CL2", lambda r, p: [p["checks"].pop(i) for i in (7, 5)],
                              "FAILED", "CL1", "none", "CL2-1"),
    "cl2-fail-evaluator-not-read-only": ("CL2", lambda r, p: p["evaluators"][1]["model"].update(
        readOnly=False), "FAILED", "CL1", "none", "CL2-2"),
    "cl2-pass-one-evaluator-shares-maker-family": ("CL2", lambda r, p: maker_gpt(p),
                                                   "OK", "CL2", "none", None),
    "cl2-fail-every-evaluator-shares-maker-family": ("CL2", lambda r, p: (
        maker_gpt(p), p["evaluators"][1]["model"].update(family="gpt")),
        "FAILED", "CL1", "none", "CL2-3"),
    "cl2-fail-evidence-digest-mismatch": ("CL2", lambda r, p: p["external"][0]["evidence"].update(
        sha256="0" * 64), "FAILED", "none", "none", "CL1-15"),
    "cl2-unchecked-independence-asserted-only": ("CL2", lambda r, p: p.update(external=[]),
                                                 "NOT-CHECKABLE", "none", "none", None),
    "cl3-unchecked-signature-not-verified": ("CL3", lambda r, p: None,
                                             "NOT-CHECKABLE", "CL2", "none", None),
    "cl3-unchecked-unobserved-not-yet-given": ("CL3", lambda r, p: (
        [unobs(p, i) for i in (2, 3)], p["disposition"].update(state="not_yet_given"),
        p["disagreements"].append({"dimension": "D2", "checks": [2, 6],
                                   "note": "E1 could not observe; E2 read conforms"})),
        "NOT-CHECKABLE", "CL2", "to approver", None),
    "cl3-unchecked-adopted-specialist": ("CL3", lambda r, p: p["bar"]["approvals"][1].update(
        by="Avery Chen", adopted={"document": "in-toto Statement", "version": "v1"}),
        "NOT-CHECKABLE", "CL2", "none", None),
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

    # v0.9.4, R1: attribution
    "cl1-fail-evaluator-on-no-check-or-control": ("CL1", lambda r, p: p["evaluators"].append(
        {"id": "E9", "name": "Quinn Hale", "kind": "person", "model": None, "script": None}),
        "FAILED", "none", "none", "CL1-16"),
    "cl1-fail-control-names-unlisted-evaluator": ("CL1", lambda r, p: p["controls"].append(
        control("K9", "E9", "does_not_conform")), "FAILED", "none", "none", "CL1-16"),
    "cl1-fail-readings-filed-under-runner": ("CL1", lambda r, p: script_evaluator(
        p, digest=text_digest("runner")), "FAILED", "none", "none", "CL1-16"),
    # R2: controls for each evaluator, and a clean control in every batch
    "cl1-fail-reader-without-control": ("CL1", lambda r, p: second_reader_without_control(p),
                                        "FAILED", "none", "none", "CL1-9"),
    "cl1-fail-no-clean-control": ("CL1", lambda r, p: p["controls"].pop(1),
                                  "FAILED", "none", "none", "CL1-9"),
    "cl1-pass-unobserved-reader-needs-no-control": ("CL1", lambda r, p: (
        second_reader_without_control(p), unobs(p, 2), p["disposition"].update(
            acknowledgesUnobserved=["D1"]), p["disagreements"].append(
            {"dimension": "D1", "checks": [0, 2], "note": "E2 could not observe"})),
        "OK", "CL1", "acknowledged", None),
    # R3: check evidence binds to a file
    "cl1-fail-evidence-file-differs": ("CL1", lambda r, p: p["checks"][0]["evidence"].update(
        sha256=text_digest("other notes")["sha256"]), "FAILED", "none", "none", "CL1-8"),
    "cl1-unchecked-evidence-file-not-supplied": ("CL1", lambda r, p: p["checks"][0]["evidence"].update(
        name="reading-not-supplied.md"), "NOT-CHECKABLE", "none", "none", None),
    "cl1-fail-evidence-name-not-relative": ("CL1", lambda r, p: p["checks"][0]["evidence"].update(
        name="../files/report.md"), "FAILED", "none", "none", "CR-2"),
    # R4: identity
    "cl1-fail-family-not-lowercase": ("CL1", lambda r, p: (same_model(p, True), p["evaluators"][0][
        "model"].update(family="GPT")), "FAILED", "none", "none", "CR-2"),
    "cl1-fail-family-with-version": ("CL1", lambda r, p: (same_model(p, True), p["evaluators"][0][
        "model"].update(family="gpt-6")), "FAILED", "none", "none", "CR-2"),
    "cl1-fail-endpoint-not-a-host": ("CL1", lambda r, p: (same_model(p, True), p["evaluators"][0][
        "model"].update(endpoint="OpenRouter")), "FAILED", "none", "none", "CR-2"),
    "cl1-fail-check-endpoint-not-a-host": ("CL1", lambda r, p: p["checks"][0].update(
        endpoint="Some Router"), "FAILED", "none", "none", "CR-2"),
    "cl1-fail-model-evaluator-without-model-block": ("CL1", lambda r, p: p["evaluators"][0].update(
        kind="model"), "FAILED", "none", "none", "CL1-6"),
    "cl2-pass-check-endpoint-recorded": ("CL2", lambda r, p: (maker_gpt(p), [c.update(
        endpoint="api.google-mirror.example") for c in p["checks"] if c["evaluator"] == "E2"]),
        "OK", "CL2", "none", None),
    "cl2-fail-check-answered-by-makers-endpoint": ("CL2", lambda r, p: (maker_gpt(p), [c.update(
        endpoint="api.other.example") for c in p["checks"] if c["evaluator"] == "E2"]),
        "FAILED", "CL1", "none", "CL2-3"),
    "cl2-fail-undisclosed-family-counts-as-makers": ("CL2", lambda r, p: (
        maker_gpt(p), p["evaluators"][1]["model"].update(family="undisclosed")),
        "FAILED", "CL1", "none", "CL2-3"),
    "cl2-pass-undisclosed-family-beside-others": ("CL2", lambda r, p: panel(
        p, ["gemini", "grok", "undisclosed"]), "OK", "CL2", "none", None),
    # R5: start time and maker kind
    "cl1-fail-bar-frozen-after-start": ("CL1", lambda r, p: p["bar"].update(
        frozenAt="2026-10-01T11:00:00Z"), "FAILED", "none", "none", "CL1-1"),
    "cl1-fail-bar-frozen-at-start": ("CL1", lambda r, p: p["bar"].update(
        frozenAt=p["startedAt"]), "FAILED", "none", "none", "CL1-1"),
    "cl1-fail-started-after-produced": ("CL1", lambda r, p: p.update(
        startedAt="2026-10-02T10:00:00Z"), "FAILED", "none", "none", "CL1-1"),
    "cl1-fail-started-at-missing": ("CL1", lambda r, p: p.pop("startedAt"),
                                    "FAILED", "none", "none", "CR-2"),
    "cl1-fail-maker-kind-missing": ("CL1", lambda r, p: p["maker"].pop("kind"),
                                    "FAILED", "none", "none", "CL1-4"),
    "baseline-pass-bar-frozen-mid-work": ("baseline", lambda r, p: (p["bar"].update(
        frozenAt="2026-10-01T11:00:00Z"), p.update(readsBeforeFreeze=["outline"])),
        "OK", "baseline", "none", None),
    "baseline-fail-bar-frozen-at-same-instant": ("baseline", lambda r, p: (
        p["bar"].update(frozenAt=p["startedAt"]), p.update(readsBeforeFreeze=[])),
        "FAILED", "none", "none", "BL-1"),
    "cl2-fail-model-maker-without-model-block": ("CL2", lambda r, p: p["maker"].update(model=None),
                                                 "FAILED", "CL1", "none", "CL2-3"),
    # R6: score decides outcome
    "cl1-pass-scored": ("CL1", lambda r, p: scored(p, 4, "conforms"), "OK", "CL1", "none", None),
    "cl1-pass-scored-below-threshold": ("CL1", lambda r, p: scored(p, 2, "does_not_conform"),
                                        "OK", "CL1", "to approver", None),
    "cl1-fail-score-contradicts-outcome": ("CL1", lambda r, p: scored(p, 2, "conforms"),
                                           "FAILED", "none", "none", "CL1-17"),
    "cl1-fail-score-meets-threshold-reads-does-not-conform": ("CL1", lambda r, p: scored(
        p, 3, "does_not_conform"), "FAILED", "none", "to approver", "CL1-17"),
    "cl1-fail-score-above-scale": ("CL1", lambda r, p: scored(p, 6, "conforms"),
                                   "FAILED", "none", "none", "CL1-17"),
    "cl1-fail-threshold-above-scale": ("CL1", lambda r, p: scored(p, 4, "conforms", threshold=7),
                                       "FAILED", "none", "none", "CL1-2"),
    # R7: the maker wrote the bar
    "cl1-fail-maker-wrote-bar-undisclosed": ("CL1", lambda r, p: p["bar"].update(
        author="Drafting Agent"), "FAILED", "none", "none", "CL1-11"),
    "cl1-pass-maker-wrote-bar-disclosed": ("CL1", lambda r, p: (p["bar"].update(
        author="Drafting Agent"), p["separationGaps"].append("Drafting Agent made the work and "
                                                             "wrote the bar")), "OK", "CL1", "none", None),
    "cl2-fail-maker-wrote-bar": ("CL2", lambda r, p: (p["bar"].update(author="Drafting Agent"),
                                                      p["separationGaps"].append(
                                                          "Drafting Agent made the work and wrote the bar")),
                                 "FAILED", "CL1", "none", "CL2-3"),
    # v0.9.5, I5: a clean and a planted control for every reader
    "cl1-fail-reader-with-planted-control-only": ("CL1", lambda r, p: (
        second_reader_without_control(p), p["controls"].append(control("K3", "E2", "does_not_conform"))),
        "FAILED", "none", "none", "CL1-9"),
    "cl1-fail-reader-with-clean-control-only": ("CL1", lambda r, p: (
        second_reader_without_control(p), p["controls"].append(control("K3", "E2", "conforms"))),
        "FAILED", "none", "none", "CL1-9"),
    "cl1-pass-second-reader-with-both-controls": ("CL1", lambda r, p: (
        second_reader_without_control(p), p["controls"].extend(
            [control("K3", "E2", "does_not_conform"), control("K4", "E2", "conforms")])),
        "OK", "CL1", "none", None),
    "cl2-fail-one-reader-without-clean-control": ("CL2", lambda r, p: p["controls"].pop(3),
                                                  "FAILED", "none", "none", "CL1-9"),
    # v0.9.5, I2-I4: the wording, made into cases
    "cl1-pass-unscored-checks-not-judged-by-cl1-17": ("CL1", lambda r, p: None, "OK", "CL1", "none", None),
    "cl1-pass-no-reads-before-freeze-field": ("CL1", lambda r, p: None, "OK", "CL1", "none", None),
    "cl2-fail-maker-family-undisclosed": ("CL2", lambda r, p: p["maker"]["model"].update(
        family="undisclosed"), "FAILED", "CL1", "none", "CL2-3"),
    "cl1-fail-evidence-not-an-evidence-file": ("CL1", lambda r, p: p["checks"][0]["evidence"].pop("name"),
                                               "FAILED", "none", "none", "CR-2"),
    # R9: schema and checker agree
    "cl1-fail-run-zero": ("CL1", lambda r, p: p["checks"][0].update(run=0),
                          "FAILED", "none", "none", "CR-2"),
    "cl1-fail-anchors-empty": ("CL1", lambda r, p: scored(p, 4, "conforms", anchors={}),
                               "FAILED", "none", "none", "CL1-2"),
    # R10: extensions
    "cl1-pass-extension-fields": ("CL1", lambda r, p: extensions(p), "OK", "CL1", "none", None),
    "cl1-pass-refiled-with-provenance": ("CL1", lambda r, p: refiled(p), "OK", "CL1", "none", None),
}
# Level boundaries: each passes the level below and fails the next for exactly one reason.
BOUNDARIES = {"none|CL1": "cl1-fail-bar-frozen-late", "CL1|CL2": "cl2-fail-one-run-only",
              "CL2|CL3": "cl3-fail-bar-not-published"}
# Schema-invalid by shape, though the failing requirement is one that owns those fields itself.
SCHEMA_INVALID = ["cl1-fail-missing-violations-field", "cl1-fail-dimension-scale-missing-floor",
                  "cl1-fail-anchors-empty", "cl1-fail-maker-kind-missing"]


def main():
    write_inputs()
    for old in HERE.glob("*.json"):
        old.unlink()
    expected = {}
    for name, (level, fn, verdict, achieved, routing, fails) in CASES.items():
        (HERE / f"{name}.json").write_text(json.dumps(mutate(level, fn), indent=2) + "\n")
        expected[name] = {"verdict": verdict, "levelAchieved": achieved, "routing": routing,
                          "fails": fails}
    (HERE / "expected.json").write_text(json.dumps({"cases": expected, "boundaries": BOUNDARIES,
                                                    "schemaInvalid": SCHEMA_INVALID},
                                                   indent=2) + "\n")
    print(f"wrote {len(CASES)} fixtures")


if __name__ == "__main__":
    main()
