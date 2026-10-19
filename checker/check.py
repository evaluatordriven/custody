#!/usr/bin/env python3
"""Reference verifier for custody/v1 records (SPEC.md section 6). Not normative. Exit 0 OK,
1 FAILED, 2 NOT-CHECKABLE. Usage: check.py RECORD [--files DIR] [--evidence DIR] [--bar FILE]"""
import argparse, hashlib, json, os, re, sys  # noqa: E401 - standard library only
from collections import Counter
from datetime import datetime

STATEMENT = "https://in-toto.io/Statement/v1"
PREDICATE = "https://evaluatordriven.com/custody/v1"
OUTCOMES = {"conforms", "does_not_conform", "unobserved"}
HEX = re.compile(r"^[0-9a-f]{64}$")
TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$")
OK, FAILED, NC = "OK", "FAILED", "NOT-CHECKABLE"


class Fail(Exception): """A requirement the record breaks."""  # noqa: E701


class Unchecked(Exception): """A requirement that what was supplied cannot decide."""  # noqa


def need(bad):
    if bad: raise Fail("; ".join(bad[:5]))  # noqa: E701


when = lambda ts: datetime.fromisoformat(ts.replace("Z", "+00:00"))  # noqa: E731
same = lambda a, b: a.strip().casefold() == b.strip().casefold()  # noqa: E731


is_num = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)  # noqa: E731
sha256_file = lambda path: hashlib.sha256(open(path, "rb").read()).hexdigest()  # noqa: E731


# ---- CR-2: field presence and type (SPEC.md section 4). "key:kind" pairs, "?" allows null --

KIND = {
    "str": lambda v: isinstance(v, str) and v.strip() != "", "text": lambda v: isinstance(v, str),
    "list": lambda v: isinstance(v, list), "dict": lambda v: isinstance(v, dict),
    "nonempty": lambda v: isinstance(v, list) and len(v) > 0, "bool": lambda v: isinstance(v, bool),
    "int": lambda v: is_num(v) and isinstance(v, int) and v >= 0, "num": lambda v: is_num(v),
    "ts": lambda v: isinstance(v, str) and bool(TS.match(v)),
    "digest": lambda v: isinstance(v, dict) and bool(HEX.match(str(v.get("sha256", "")))),
    "file": lambda v: KIND["digest"](v) and bool(str(v.get("name", "")).strip()),
}
S = lambda text: dict(pair.split(":") for pair in text.split())  # noqa: E731
PRED = S("specVersion:str levelClaimed:str bar:dict producedAt:ts evaluators:nonempty "
         "checks:nonempty controls:nonempty disagreements:list external:list disposition:dict")
OWN = {"CL1-4": {"maker": S("name:str version:str method:digest model:dict?")},  # see CR-2
       "CL1-5": {"instrument": S("rubric:digest runner:digest")},
       "CL1-12": {"retention": S("location:str public:bool")}}
ITEMS = {k: S(v) for k, v in {
    "bar": "digest:digest frozenAt:ts author:str dimensions:nonempty approvals:list "
           "publishedAt:str? groundTruth:list dissent:list",
    "bar.groundTruth": "name:str version:str digest:digest", "bar.dissent": "by:str note:str",
    "bar.approvals": "role:str by:str barDigest:digest at:ts adopted:dict?",
    "evaluators": "id:str name:str kind:str model:dict?",  # script: CL1-5
    "checks": "dimension:str evaluator:str run:int batch:str at:ts outcome:str score:num? "
              "failureCondition:str evidence:digest? unobserved:dict?",
    "controls": "id:str batch:str evaluator:str case:digest expected:str outcome:str",
    "disagreements": "dimension:str checks:list note:text",
    "external": "requirement:str subject:str evidence:file readBy:str",
    "disposition": "state:str by:str at:ts acknowledgesUnobserved:list",
    "spread": "dimension:str evaluator:str runs:int agreement:int",
    "demonstrations": "dimension:str evaluator:str planted:digest outcome:str at:ts"}.items()}
SUB = {"model": S("family:str identifier:str endpoint:str readOnly:bool"),
       "scale": S("anchors:dict threshold:num floor:num"),
       "adopted": S("document:str version:str")}
ENUMS = {"levelClaimed": {"CL1", "CL2", "CL3", "baseline"}, "role": {"buyer", "specialist"},
         "kind": {"person", "model", "script"}, "outcome": OUTCOMES, "expected": OUTCOMES, "state":
         {"given", "not_yet_given", "declined"}, "requirement": {"CL1-15", "CL2-4", "CL3-3"}}


def fields(obj, spec, where, bad):
    for key, kind in spec.items():
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
            fields(item if isinstance(item, dict) else {}, spec, f"{path}[{i}]", bad)
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
    if when(p["bar"]["frozenAt"]) >= when(p["producedAt"]):
        raise Fail("bar.frozenAt is not earlier than producedAt: only a baseline claim fits")


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




def cl1_6(r, p, ctx):
    mk = p["maker"].get("model")
    for e, m in ((e, e.get("model")) for e in p["evaluators"]):
        names = [e["name"]] + ([e["script"]["author"]] if e["kind"] == "script" else [])
        for who, role in ((p["maker"]["name"], "maker"), (p["bar"]["author"], "bar author")):
            if any(same(n, who) for n in names):
                raise Fail(f"evaluator {e['id']} is, or was written by, the {role}")
        is_mk = bool(mk and m and same(m["identifier"], mk["identifier"]))
        if is_mk != bool(e.get("sameModelAsMaker")):  # declared exactly when true (S2)
            raise Fail(f"evaluator {e['id']} declares sameModelAsMaker untruly, or not at all")
        if same(e["name"], p["disposition"]["by"]):
            raise Fail(f"the approver is evaluator {e['id']}")


def cl1_7(r, p, ctx):
    need([f"no check filed for {d['id']}" for d in p["bar"]["dimensions"]
          if d["id"] not in {c["dimension"] for c in p["checks"]}])


def cl1_8(r, p, ctx):
    dims, evals = {d["id"] for d in p["bar"]["dimensions"]}, {e["id"] for e in p["evaluators"]}
    for where, c in ((f"checks[{i}]", c) for i, c in enumerate(p["checks"])):
        if c["dimension"] not in dims or c["evaluator"] not in evals:
            raise Fail(f"{where} names an unknown dimension or evaluator")
        u = c["unobserved"]
        if c["outcome"] == "unobserved":
            if not (u and u.get("channel") and u.get("reason")) or c["score"] is not None:
                raise Fail(f"{where} is unobserved without channel and reason, or is scored")
        elif c["evidence"] is None or c["unobserved"] is not None:
            raise Fail(f"{where} reads {c['outcome']} without evidence")


def cl1_9(r, p, ctx):
    for b, readers in ((b, {c["evaluator"] for c in p["checks"] if c["batch"] == b})
                       for b in sorted({c["batch"] for c in p["checks"]})):
        if not any(k["batch"] == b and k["evaluator"] in readers for k in p["controls"]):
            raise Fail(f"batch {b} has no control read by one of its evaluators")
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
    need([f"the {a['role']} is the maker, and no separation gap names {mk}" for a in
          p["bar"]["approvals"] if same(a["by"], mk) and mk.strip().casefold() not in gaps])


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
        if os.path.isabs(name) or ".." in name.split("/"):
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
        path = os.path.join(ctx.evidence or "", x["evidence"].get("name", ""))
        if not ctx.evidence or not os.path.isfile(path):
            raise Unchecked(f"{req} evidence file for {subject} not supplied (--evidence)")
        if sha256_file(path) != x["evidence"].get("sha256"):
            raise Fail(f"{req} evidence file for {subject} does not match its digest")


pairs = lambda p: {(c["evaluator"], c["dimension"]) for c in p["checks"]}  # noqa: E731


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


def cl2_3(r, p, ctx):  # approvals and at least one model evaluator independent of the maker
    need([f"the {a['role']} approval is by the maker" for a in p["bar"]["approvals"]
          if same(a["by"], p["maker"]["name"])])
    mk, models = p["maker"]["model"], [e["model"] for e in p["evaluators"] if e["model"]]
    if mk and models and not any(not same(m["family"], mk["family"]) and not same(
            m["endpoint"], mk["endpoint"]) for m in models):
        raise Fail("no model evaluator differs from the maker in both family and endpoint")
    fam = {e["id"] for e in p["evaluators"]  # the maker's family is at most half of each dimension
           if mk and e["model"] and same(e["model"]["family"], mk["family"])}
    for d in sorted({c["dimension"] for c in p["checks"]}):
        readers = {c["evaluator"] for c in p["checks"] if c["dimension"] == d}
        if 2 * len(readers & fam) > len(readers):
            raise Fail(f"dimension {d}: over half its evaluators share the maker's model family")


def cl1_15(r, p, ctx):
    for e in [e for e in p["evaluators"] if e["kind"] == "model"]:
        external(p, ctx, "CL1-15", e["id"])


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


cl3_3 = lambda r, p, ctx: external(p, ctx, "CL3-3", "record", absent=Fail)  # noqa: E731


def bl_1(r, p, ctx):
    if p["levelClaimed"] == "baseline" and not (when(p["bar"]["frozenAt"]) > when(p["producedAt"])
                                               and isinstance(p.get("readsBeforeFreeze"), list)):
        raise Fail("a baseline needs a bar frozen strictly after producedAt, and readsBeforeFreeze")


def cl1_5(r, p, ctx):
    owned("CL1-5", p)
    for e, s in ((e, e.get("script")) for e in p["evaluators"]):
        if e["kind"] == "script" and not (isinstance(s, dict) and s.get("name") and s.get("author")
                                          and KIND["digest"](s.get("digest"))):
            raise Fail(f"script evaluator {e['id']} does not name its script, author and digest")


own = {k: (lambda k: lambda r, p, ctx: owned(k, p))(k) for k in OWN}  # CL1-4, CL1-12
CHECKS = {"CR-1": cr1, "CR-2": cr2, "BL-1": bl_1, **{f"CL1-{i}": f for i, f in enumerate(
    [cl1_1, cl1_2, cl1_3, own["CL1-4"], cl1_5, cl1_6, cl1_7, cl1_8, cl1_9, cl1_10, cl1_11,
     own["CL1-12"], cl1_13, cl1_14, cl1_15], 1)}, "CL2-1": cl2_1, "CL2-2": cl2_2, "CL2-3": cl2_3,
    "CL3-1": cl3_1, "CL3-2": cl3_2, "CL3-3": cl3_3}
LEVEL = {lv: [k for k in CHECKS if k.startswith(lv + "-")] for lv in ("CL1", "CL2", "CL3")}


def verify(record, files=None, evidence=None, bar=None):
    ctx = argparse.Namespace(files=files, evidence=evidence, bar=bar)
    p = record.get("predicate") if isinstance(record, dict) else None
    claim = p.get("levelClaimed") if isinstance(p, dict) else None
    order = ["CL1", "CL2", "CL3"][:{"CL1": 1, "CL2": 2, "CL3": 3}.get(claim, 1)]
    scope = ["CR-1", "CR-2", "BL-1"] + [k for lv in order for k in LEVEL[lv]
                                        if not (claim == "baseline" and k in ("CL1-1", "CL1-15"))]
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
    ok = lambda ids: all(results.get(i, (FAILED,))[0] == OK for i in ids)
    level = "baseline" if claim == "baseline" and ok(scope) else "none"
    if claim in ("CL1", "CL2", "CL3") and ok(["CR-1", "CR-2", "BL-1"]):
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
    [ap.add_argument(arg) for arg in ("record", "--files", "--evidence", "--bar")]  # see usage
    a = ap.parse_args()
    try:
        report = verify(json.load(open(a.record, encoding="utf-8")), a.files, a.evidence, a.bar)
    except (OSError, ValueError) as e:
        report = {"verdict": FAILED, "error": f"cannot read record: {e}"}
    print(json.dumps(report, indent=2))
    return {OK: 0, FAILED: 1, NC: 2}[report["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
