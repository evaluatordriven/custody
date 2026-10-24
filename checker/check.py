#!/usr/bin/env python3
"""Reference verifier for custody/v1 records (SPEC.md section 6). Not normative. Exit 0 OK,
1 FAILED, 2 NOT-CHECKABLE. Usage: check.py RECORD [--files DIR] [--evidence DIR] [--bar FILE]"""
import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime

STATEMENT = "https://in-toto.io/Statement/v1"
PREDICATE = "https://evaluatordriven.com/custody/v1"
OUTCOMES = {"conforms", "does_not_conform", "unobserved"}
HEX = re.compile(r"^[0-9a-f]{64}$")
TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$")
FAMILY = re.compile(r"^[a-z]+(-[a-z]+)*$")  # lowercase letters and hyphens, no version (SPEC 4)
HOST = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$")
UNDISCLOSED = "undisclosed"
OK, FAILED, NC = "OK", "FAILED", "NOT-CHECKABLE"


class Fail(Exception):
    """A requirement the record breaks."""


class Unchecked(Exception):
    """A requirement that what was supplied cannot decide."""


def need(bad):
    if bad:
        raise Fail("; ".join(bad[:5]))


def when(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def same(a, b):
    return a.strip().casefold() == b.strip().casefold()


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def relative(name):
    return not (os.path.isabs(name) or ".." in name.replace("\\", "/").split("/"))


def anchor_scores(anchors):
    """The scores an anchors object names, or None if any key is not a number."""
    try:
        return [float(k) for k in anchors]
    except (TypeError, ValueError):
        return None


def scale_ok(sc):
    """True when a scale is one CL1-2 accepts: numeric anchors, floor lowest, threshold inside."""
    if not (isinstance(sc, dict) and KIND["anchors"](sc.get("anchors"))
            and is_num(sc.get("threshold")) and is_num(sc.get("floor"))):
        return False
    scores = anchor_scores(sc["anchors"])
    return bool(scores) and sc["floor"] <= min(scores) and (
        sc["floor"] <= sc["threshold"] <= max(scores))


# ---- CR-2: field presence and type (SPEC.md section 4). "key:kind" pairs, "?" allows null --

KIND = {
    "str": lambda v: isinstance(v, str) and v.strip() != "", "text": lambda v: isinstance(v, str),
    "list": lambda v: isinstance(v, list), "dict": lambda v: isinstance(v, dict),
    "nonempty": lambda v: isinstance(v, list) and len(v) > 0, "bool": lambda v: isinstance(v, bool),
    "int": lambda v: is_num(v) and isinstance(v, int) and v >= 0,
    "pos": lambda v: is_num(v) and isinstance(v, int) and v >= 1,
    "num": lambda v: is_num(v),
    "ts": lambda v: isinstance(v, str) and bool(TS.match(v)),
    "digest": lambda v: isinstance(v, dict) and bool(HEX.match(str(v.get("sha256", "")))),
    "file": lambda v: KIND["digest"](v) and bool(str(v.get("name", "")).strip())
    and relative(str(v.get("name"))),  # an evidence file: a relative path (SPEC section 4)
    "family": lambda v: isinstance(v, str) and bool(FAMILY.match(v)),
    "host": lambda v: isinstance(v, str) and bool(HOST.match(v)),
    "anchors": lambda v: isinstance(v, dict) and len(v) > 0,
}


def S(text):
    return dict(pair.split(":") for pair in text.split())


PRED = S("specVersion:str levelClaimed:str bar:dict startedAt:ts producedAt:ts evaluators:nonempty "
         "checks:nonempty controls:nonempty disagreements:list external:list disposition:dict")
OWN = {"CL1-4": {"maker": S("name:str kind:str version:str method:digest model:dict?")},  # CR-2
       "CL1-5": {"instrument": S("rubric:digest runner:digest")},
       "CL1-12": {"retention": S("location:str public:bool")}}
ITEMS = {k: S(v) for k, v in {
    "bar": "digest:digest frozenAt:ts author:str dimensions:nonempty approvals:list "
           "publishedAt:str? groundTruth:list dissent:list",
    "bar.groundTruth": "name:str version:str digest:digest", "bar.dissent": "by:str note:str",
    "bar.approvals": "role:str by:str barDigest:digest at:ts adopted:dict?",
    "evaluators": "id:str name:str kind:str model:dict?",  # script: CL1-5
    "checks": "dimension:str evaluator:str run:pos batch:str at:ts outcome:str score:num? "
              "failureCondition:str evidence:file? unobserved:dict?",
    "controls": "id:str batch:str evaluator:str case:digest expected:str outcome:str",
    "disagreements": "dimension:str checks:list note:text",
    "external": "requirement:str subject:str evidence:file readBy:str",
    "disposition": "state:str by:str at:ts acknowledgesUnobserved:list",
    "spread": "dimension:str evaluator:str runs:pos agreement:int",
    "demonstrations": "dimension:str evaluator:str planted:digest outcome:str at:ts"}.items()}
OPTIONAL = {"checks": S("endpoint:host")}  # may be absent; checked when present
SUB = {"model": S("family:family identifier:str endpoint:host readOnly:bool"),
       "scale": S("anchors:anchors threshold:num floor:num"),
       "adopted": S("document:str version:str")}
ENUMS = {"levelClaimed": {"CL1", "CL2", "CL3", "baseline"}, "role": {"buyer", "specialist"},
         "kind": {"person", "model", "script"}, "outcome": OUTCOMES, "expected": OUTCOMES, "state":
         {"given", "not_yet_given", "declined"}, "requirement": {"CL1-15", "CL2-4", "CL3-3"}}


def fields(obj, spec, where, bad, optional=None):
    for key, kind in list(spec.items()) + [(k, v) for k, v in (optional or {}).items() if k in obj]:
        v = obj.get(key, ...)
        if v is ... or not ((kind.endswith("?") and v is None) or KIND[kind.rstrip("?")](v)):
            bad.append(f"{where}.{key} missing or not {kind}")
        elif key in ENUMS and v not in ENUMS[key]:
            bad.append(f"{where}.{key} is {v!r}")
        elif key in SUB and isinstance(v, dict):
            fields(v, SUB[key], f"{where}.{key}", bad)


def cr2(r, p, ctx):
    bad = []
    fields(p, PRED, "predicate", bad)
    extra = {"CL2": {"spread": "list"}, "CL3": {"spread": "list", "demonstrations": "list"}}
    fields(p, extra.get(p.get("levelClaimed"), {}), "predicate", bad)
    for path, spec in ITEMS.items():
        head, _, tail = path.partition(".")
        node = p.get(head)
        node = node.get(tail) if tail and isinstance(node, dict) else node
        for i, item in enumerate(node if isinstance(node, list) else [node] if node else []):
            fields(item if isinstance(item, dict) else {}, spec, f"{path}[{i}]", bad,
                   OPTIONAL.get(path))
    need(bad)


# ---- requirements (SPEC.md section 5) -------------------------------------------------------

def cr1(r, p, ctx):
    if r.get("_type") != STATEMENT or r.get("predicateType") != PREDICATE:
        raise Fail("_type or predicateType is wrong")
    subj = r.get("subject")
    if not KIND["nonempty"](subj) or not all(isinstance(s, dict) and KIND["str"](
            s.get("name")) and KIND["digest"](s.get("digest")) for s in subj):
        raise Fail("subject must be non-empty, each with a name and a sha256 digest")
    if not isinstance(r.get("predicate"), dict):
        raise Fail("predicate is not an object")


def cl1_1(r, p, ctx):
    frozen, started, produced = (when(t) for t in (p["bar"]["frozenAt"], p["startedAt"],
                                                   p["producedAt"]))
    if started > produced:
        raise Fail("startedAt is later than producedAt")
    if frozen >= started:
        raise Fail("bar.frozenAt is not earlier than startedAt: the bar came after the work "
                   "started, so only a baseline claim fits (or none, if frozen at that instant)")


def cl1_2(r, p, ctx):  # owns each dimension's fields, scale included (SPEC CR-2)
    bad = []
    for i, d in enumerate(x if isinstance(x, dict) else {} for x in p["bar"]["dimensions"]):
        fields(d, S("id:str criterion:str scale:dict?"), f"bar.dimensions[{i}]", bad)  # + SUB
    need(bad)
    if len({d["id"] for d in p["bar"]["dimensions"]}) != len(p["bar"]["dimensions"]):
        raise Fail("dimension ids are not unique")
    scored = {c["dimension"] for c in p["checks"] if c["score"] is not None}
    need([f"{d['id']} is scored but declares no anchors, threshold and floor"
          for d in p["bar"]["dimensions"] if d["id"] in scored and not d["scale"]])
    for d in (d for d in p["bar"]["dimensions"] if d["scale"]):
        sc = d["scale"]
        scores = anchor_scores(sc["anchors"])
        if scores is None:
            raise Fail(f"{d['id']}: every anchor must be keyed by a score")
        if not (sc["floor"] <= min(scores) and sc["floor"] <= sc["threshold"] <= max(scores)):
            raise Fail(f"{d['id']}: the floor must be the lowest score, and the threshold must lie "
                       "between the floor and the highest anchor")


def cl1_3(r, p, ctx):
    for role in ("buyer", "specialist"):
        mine = [a["barDigest"]["sha256"] for a in p["bar"]["approvals"] if a["role"] == role]
        if not mine or set(mine) != {p["bar"]["digest"]["sha256"]}:
            raise Fail(f"no {role} approval, or one bound to a different bar")


def owned(rid, p):
    bad = []
    for key, spec in OWN[rid].items():
        fields(p.get(key) if isinstance(p.get(key), dict) else {}, spec, f"predicate.{key}", bad)
    need(bad)


def cl1_5(r, p, ctx):
    owned("CL1-5", p)
    for e, s in ((e, e.get("script")) for e in p["evaluators"]):
        if e["kind"] == "script" and not (isinstance(s, dict) and s.get("name") and s.get("author")
                                          and KIND["digest"](s.get("digest"))):
            raise Fail(f"script evaluator {e['id']} does not name its script, author and digest")


def cl1_6(r, p, ctx):
    mk = p["maker"].get("model")
    for e, m in ((e, e.get("model")) for e in p["evaluators"]):
        if e["kind"] == "model" and not m:
            raise Fail(f"model evaluator {e['id']} carries no model block")
        names = [e["name"]] + ([e["script"]["author"]] if e["kind"] == "script" else [])
        for who, role in ((p["maker"]["name"], "maker"), (p["bar"]["author"], "bar author")):
            if any(same(n, who) for n in names):
                raise Fail(f"evaluator {e['id']} is, or was written by, the {role}")
        is_mk = bool(mk and m and same(m["identifier"], mk["identifier"]))
        if is_mk != bool(e.get("sameModelAsMaker")):  # declared exactly when true
            raise Fail(f"evaluator {e['id']} declares sameModelAsMaker untruly, or not at all")
        if same(e["name"], p["disposition"]["by"]):
            raise Fail(f"the approver is evaluator {e['id']}")


def cl1_7(r, p, ctx):
    need([f"no check filed for {d['id']}" for d in p["bar"]["dimensions"]
          if d["id"] not in {c["dimension"] for c in p["checks"]}])


def cl1_8(r, p, ctx):
    dims, evals = {d["id"] for d in p["bar"]["dimensions"]}, {e["id"] for e in p["evaluators"]}
    observed = []
    for where, c in ((f"checks[{i}]", c) for i, c in enumerate(p["checks"])):
        if c["dimension"] not in dims or c["evaluator"] not in evals:
            raise Fail(f"{where} names an unknown dimension or evaluator")
        u = c["unobserved"]
        if c["outcome"] == "unobserved":
            if not (u and u.get("channel") and u.get("reason")) or c["score"] is not None:
                raise Fail(f"{where} is unobserved without channel and reason, or is scored")
        elif c["evidence"] is None or c["unobserved"] is not None:
            raise Fail(f"{where} reads {c['outcome']} without evidence")
        else:
            observed.append((where, c["evidence"]))
    missing, wrong = [], []
    for where, ev in observed:  # every evidence file is bound to its digest (v0.9.4, R3)
        if not relative(ev["name"]):  # CR-2 fails it (one defect, one failure)
            raise Unchecked(f"{where} evidence name is not a relative path; see CR-2")
        path = os.path.join(ctx.evidence or "", ev["name"])
        if not ctx.evidence or not os.path.isfile(path):
            missing.append(ev["name"])
        elif sha256_file(path) != ev["sha256"]:
            wrong.append(f"{where} evidence file {ev['name']} does not match its digest")
    need(wrong)
    if missing:
        names = ", ".join(sorted(set(missing))[:5])
        raise Unchecked(f"check evidence not supplied (--evidence): {names}")


def cl1_9(r, p, ctx):
    for b in sorted({c["batch"] for c in p["checks"]}):
        here = [c for c in p["checks"] if c["batch"] == b]
        ctl = [k for k in p["controls"] if k["batch"] == b]
        observed = sorted({c["evaluator"] for c in here if c["outcome"] != "unobserved"})
        need([f"evaluator {e} reads in batch {b} but reads no {kind} control there"
              for e in observed for kind, want in (("clean", "conforms"),
                                                   ("planted", "does_not_conform"))
              if not any(k["evaluator"] == e and k["expected"] == want for k in ctl)])
    seen = [(c["batch"], c["evaluator"], c["dimension"]) for c in p["checks"]
            if c["outcome"] != "unobserved"]  # a missed control voids its reader's observations
    need([f"control {k['id']} came out wrong, yet its reader's checks still count" for k in
          p["controls"] if k["outcome"] != k["expected"] and any((b, e) == (k["batch"], k[
              "evaluator"]) and k.get("dimension") in (None, d) for b, e, d in seen)])


def cl1_10(r, p, ctx):
    named = {d["dimension"] for d in p["disagreements"]}
    for d in {c["dimension"] for c in p["checks"]}:
        if len({c["outcome"] for c in p["checks"] if c["dimension"] == d}) > 1 and d not in named:
            raise Fail(f"checks of {d} disagree and the disagreement is not recorded")
    dims = [c["dimension"] for c in p["checks"]]
    for d in p["disagreements"]:
        if len(d["checks"]) < 2 or any(not isinstance(i, int) or not 0 <= i < len(dims)
                                       or dims[i] != d["dimension"] for i in d["checks"]):
            raise Fail(f"disagreement on {d['dimension']} does not name two of its checks")


def cl1_11(r, p, ctx):  # owns violations and separationGaps, presence included (SPEC CR-2)
    bad = []
    fields(p, S("violations:list separationGaps:list"), "predicate", bad)
    for i, v in enumerate(x if isinstance(x, dict) else {} for x in p.get("violations") or []):
        fields(v, S("dimension:str description:str"), f"violations[{i}]", bad)
    need(bad)
    failed = {c["dimension"] for c in p["checks"] if c["outcome"] == "does_not_conform"}
    need([f"not in violations: {d}" for d in sorted(failed) if d not in
          {v["dimension"] for v in p["violations"]}])
    mk, gaps = p["maker"]["name"], " ".join(map(str, p["separationGaps"])).casefold()
    roles = [f"the {a['role']}" for a in p["bar"]["approvals"] if same(a["by"], mk)]
    roles += ["the bar's author"] if same(p["bar"]["author"], mk) else []
    need([f"{role} is the maker, and no separation gap names {mk}" for role in roles
          if mk.strip().casefold() not in gaps])


def cl1_13(r, p, ctx):
    d, unobserved = p["disposition"], {c["dimension"] for c in p["checks"]
                                       if c["outcome"] == "unobserved"}
    if d["state"] == "given" and not unobserved <= set(d["acknowledgesUnobserved"]):
        raise Fail("a given disposition does not acknowledge every unobserved dimension")


def cl1_14(r, p, ctx):
    if not (ctx.files and ctx.bar and os.path.isfile(ctx.bar)):
        raise Unchecked("artifact files (--files) or the bar file (--bar) not supplied")
    for s in r["subject"]:
        name, path = s["name"], os.path.join(ctx.files, s["name"])
        if not relative(name):
            raise Fail(f"subject name {name!r} is not a relative path")
        if not os.path.isfile(path):
            raise Unchecked(f"{name} not supplied")
        if sha256_file(path) != s["digest"]["sha256"]:
            raise Fail(f"{name} does not match its subject digest")
    if sha256_file(ctx.bar) != p["bar"]["digest"]["sha256"]:
        raise Fail("the bar file does not match bar.digest")


def external(p, ctx, req, subject, absent=Unchecked):
    tags = {req, "CL2-4"} if req == "CL1-15" else {req}  # SPEC.md section 8
    hits = [x for x in p["external"] if x["requirement"] in tags and x["subject"] == subject]
    if not hits:
        raise absent(f"no {req} evidence for {subject}")
    for x in hits:
        if same(x["readBy"], p["maker"]["name"]):
            raise Unchecked(f"{req} evidence for {subject} read only by the maker (A11)")
        name = x["evidence"].get("name", "")
        if not relative(name):  # CR-2 fails it (one defect, one failure)
            raise Unchecked(f"{req} evidence name is not a relative path; see CR-2")
        path = os.path.join(ctx.evidence or "", name)
        if not ctx.evidence or not os.path.isfile(path):
            raise Unchecked(f"{req} evidence file for {subject} not supplied (--evidence)")
        if sha256_file(path) != x["evidence"].get("sha256"):
            raise Fail(f"{req} evidence file for {subject} does not match its digest")


def cl1_15(r, p, ctx):
    for e in [e for e in p["evaluators"] if e["kind"] == "model"]:
        external(p, ctx, "CL1-15", e["id"])


def cl1_16(r, p, ctx):
    ids = {e["id"] for e in p["evaluators"]}
    need([f"control {k['id']} names an unlisted evaluator {k['evaluator']}"
          for k in p["controls"] if k["evaluator"] not in ids])
    runner = p["instrument"]["runner"]["sha256"]
    need([f"script evaluator {e['id']} is the instrument's runner: the readings it collects belong "
          "to the evaluators who gave them" for e in p["evaluators"] if e["kind"] == "script"
          and isinstance(e.get("script"), dict) and (e["script"].get("digest") or {}).get(
              "sha256") == runner])
    used = {c["evaluator"] for c in p["checks"]} | {k["evaluator"] for k in p["controls"]}
    need([f"evaluator {e} is listed but appears on no check and no control" for e in
          sorted(ids - used)])


def cl1_17(r, p, ctx):
    scales = {d["id"]: d["scale"] for d in p["bar"]["dimensions"]}
    for i, c in enumerate(p["checks"]):
        sc = scales.get(c["dimension"])
        if c["score"] is None or not scale_ok(sc):
            continue  # unscored, or CL1-2 reports the scale
        top = max(anchor_scores(sc["anchors"]))
        if not sc["floor"] <= c["score"] <= top:
            raise Fail(f"checks[{i}] score {c['score']} lies outside the scale {sc['floor']}-{top}")
        want = "conforms" if c["score"] >= sc["threshold"] else "does_not_conform"
        if c["outcome"] != want:
            raise Fail(f"checks[{i}] scores {c['score']} against threshold "
                       f"{sc['threshold']}, so it reads {want}; it reads {c['outcome']}")


def pairs(p):
    return {(c["evaluator"], c["dimension"]) for c in p["checks"]}


def cl2_1(r, p, ctx):
    spread = {(s["evaluator"], s["dimension"]): s for s in p["spread"]}
    for ev, dim in sorted(pairs(p)):
        runs = {c["run"]: c["outcome"] for c in p["checks"]
                if (c["evaluator"], c["dimension"]) == (ev, dim)}
        if len(runs) < 2:
            raise Fail(f"{ev} read {dim} in fewer than two runs")
        agree, s = Counter(runs.values()).most_common(1)[0][1], spread.get((ev, dim))
        if not s or s["runs"] != len(runs) or s["agreement"] != agree:
            raise Fail(f"spread for {ev}/{dim} missing or wrong: {len(runs)} runs, {agree} agree")


def cl2_2(r, p, ctx):
    for e in p["evaluators"]:
        if e["kind"] == "model" and not (e["model"] and e["model"].get("readOnly") is True):
            raise Fail(f"model evaluator {e['id']} lacks a model block with readOnly true")


def cl2_3(r, p, ctx):  # approvals, the bar's author, and model evaluators independent of the maker
    mk_name = p["maker"]["name"]
    need([f"the {a['role']} approval is by the maker" for a in p["bar"]["approvals"]
          if same(a["by"], mk_name)] + (["the maker wrote the bar"]
                                        if same(p["bar"]["author"], mk_name) else []))
    if p["maker"]["kind"] != "model":
        return
    mk = p["maker"]["model"]
    if not mk:
        raise Fail("the maker is a model but carries no model block to compare evaluators with")

    def hosts(e):  # every host that answered this evaluator's checks
        return {e["model"]["endpoint"]} | {c["endpoint"] for c in p["checks"]
                                           if c["evaluator"] == e["id"] and c.get("endpoint")}

    models = [e for e in p["evaluators"] if e["kind"] == "model" and e["model"]]
    disclosed = {e["model"]["family"].casefold() for e in models
                 if e["model"]["family"] != UNDISCLOSED
                 and not any(same(h, mk["endpoint"]) for h in hosts(e))}
    need_fams = 2 if mk["family"] == UNDISCLOSED else 1
    if models and len(disclosed - {mk["family"].casefold()}) < need_fams:
        raise Fail("no model evaluator differs from the maker in both family and endpoint")
    by_id = {e["id"]: e["model"]["family"].casefold() for e in models}
    for d in sorted({c["dimension"] for c in p["checks"]}):
        readers = {c["evaluator"] for c in p["checks"] if c["dimension"] == d}
        undisc = sum(1 for e in readers if by_id.get(e) == UNDISCLOSED)
        if mk["family"] == UNDISCLOSED:
            counts = Counter(by_id[e] for e in readers
                             if e in by_id and by_id[e] != UNDISCLOSED)
            same_fam = (max(counts.values()) if counts else 0) + undisc
        else:
            same_fam = undisc + sum(1 for e in readers
                                    if by_id.get(e) == mk["family"].casefold())
        if 2 * same_fam > len(readers):
            raise Fail(f"dimension {d}: over half its evaluators share the maker's model family")


def cl3_1(r, p, ctx):
    for ev, dim in sorted(pairs(p)):
        first = min(when(c["at"]) for c in p["checks"]
                    if (c["evaluator"], c["dimension"]) == (ev, dim))
        if not any(d["evaluator"] == ev and d["dimension"] == dim
                   and d["outcome"] == "does_not_conform" and when(d["at"]) < first
                   for d in p["demonstrations"]):
            raise Fail(f"{ev} was never shown failing a planted case on {dim} before reading it")


def cl3_2(r, p, ctx):
    need([] if re.match(r"https?://", str(p["bar"]["publishedAt"] or "")) else ["no URI"])


def cl3_3(r, p, ctx):
    external(p, ctx, "CL3-3", "record", absent=Fail)
    raise Unchecked("this checker does not verify Sigstore bundles; CL3-3 needs a verifier that "
                    "checks the signature, certificate and log entry itself (SPEC.md CL3-3)")


def bl_1(r, p, ctx):
    if p["levelClaimed"] != "baseline":
        return
    frozen, started, produced = (when(t) for t in (p["bar"]["frozenAt"], p["startedAt"],
                                                   p["producedAt"]))
    if not (frozen > started and started <= produced
            and isinstance(p.get("readsBeforeFreeze"), list)):
        raise Fail("a baseline needs a bar frozen strictly after startedAt, a startedAt no later "
                   "than producedAt, and readsBeforeFreeze")


CHECKS = {"CR-1": cr1, "CR-2": cr2, "BL-1": bl_1,
          "CL1-1": cl1_1, "CL1-2": cl1_2, "CL1-3": cl1_3,
          "CL1-4": lambda r, p, ctx: owned("CL1-4", p), "CL1-5": cl1_5, "CL1-6": cl1_6,
          "CL1-7": cl1_7, "CL1-8": cl1_8, "CL1-9": cl1_9, "CL1-10": cl1_10, "CL1-11": cl1_11,
          "CL1-12": lambda r, p, ctx: owned("CL1-12", p), "CL1-13": cl1_13, "CL1-14": cl1_14,
          "CL1-15": cl1_15, "CL1-16": cl1_16, "CL1-17": cl1_17,
          "CL2-1": cl2_1, "CL2-2": cl2_2, "CL2-3": cl2_3,
          "CL3-1": cl3_1, "CL3-2": cl3_2, "CL3-3": cl3_3}
LEVEL = {lv: [k for k in CHECKS if k.startswith(lv + "-")] for lv in ("CL1", "CL2", "CL3")}
NOT_FOR_BASELINE = ("CL1-1", "CL1-15")  # SPEC.md section 5: what a baseline claim is not held to


def verify(record, files=None, evidence=None, bar=None):
    ctx = argparse.Namespace(files=files, evidence=evidence, bar=bar)
    p = record.get("predicate") if isinstance(record, dict) else None
    claim = p.get("levelClaimed") if isinstance(p, dict) else None
    order = ["CL1", "CL2", "CL3"][:{"CL1": 1, "CL2": 2, "CL3": 3}.get(claim, 1)]
    scope = ["CR-1", "CR-2"] + (["BL-1"] if claim == "baseline" else []) + [
        k for lv in order for k in LEVEL[lv]
        if not (claim == "baseline" and k in NOT_FOR_BASELINE)]  # BL-1: baseline claims only
    results = {}
    for rid in scope:
        try:
            if rid != "CR-1" and results.get("CR-1", (OK,))[0] != OK:
                raise Unchecked("blocked: the record is not a custody/v1 statement (CR-1)")
            CHECKS[rid](record, p, ctx)
            results[rid] = (OK, "")
        except (Fail, Unchecked) as e:
            results[rid] = (FAILED if isinstance(e, Fail) else NC, str(e))
        except (KeyError, TypeError, AttributeError, ValueError) as e:
            results[rid] = (NC, f"blocked by a missing or malformed field ({e}); see CR-2")
    verdict = next((s for s in (FAILED, NC) if s in [v for v, _ in results.values()]), OK)

    def ok(ids):
        return all(results.get(i, (FAILED,))[0] == OK for i in ids)

    level = "baseline" if claim == "baseline" and ok(scope) else "none"
    if claim in ("CL1", "CL2", "CL3") and ok(["CR-1", "CR-2"]):
        met = [lv for i, lv in enumerate(order) if all(ok(LEVEL[x]) for x in order[:i + 1])]
        level = met[-1] if met else "none"
    checks = p.get("checks") if isinstance(p, dict) and isinstance(p.get("checks"), list) else []
    udims = {c.get("dimension") for c in checks if isinstance(c, dict)
             and c.get("outcome") == "unobserved"}
    ds = p["disposition"] if isinstance(p, dict) and isinstance(p.get("disposition"), dict) else {}
    ack = ds.get("state") == "given" and udims <= set(ds.get("acknowledgesUnobserved") or [])
    routing = ("to approver" if ds.get("state") == "not_yet_given" or (udims and not ack)
               else "acknowledged" if udims else "none")  # SPEC.md section 6
    return {"verdict": verdict, "levelClaimed": claim, "levelAchieved": level,
            "routing": routing, "requirements": {k: {"status": s, "detail": d}
                                                 for k, (s, d) in results.items()}}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for arg in ("record", "--files", "--evidence", "--bar"):  # see usage
        ap.add_argument(arg)
    a = ap.parse_args()
    try:
        with open(a.record, encoding="utf-8") as f:
            report = verify(json.load(f), a.files, a.evidence, a.bar)
    except (OSError, ValueError) as e:
        report = {"verdict": FAILED, "error": f"cannot read record: {e}"}
    print(json.dumps(report, indent=2))
    return {OK: 0, FAILED: 1, NC: 2}[report["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
