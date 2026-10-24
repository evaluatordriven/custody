#!/usr/bin/env python3
"""Maker scoring, version 2 — implements QUAL-AMENDMENT-1.md (sha256 8df57d58…).

WHY: v1's semantic gates scored the Architect's own design of revision 1 rather than whether
D-1 and D-2 are closed. v2 scores the brief's actual tests.

  M3 v2  no regression: on a copy of r1 holding the session's checker, all 111 cases match
         fixtures/expected.json on verdict, level, routing and sorted failing IDs.
         Whether BL-1 is listed for a non-baseline claim is NOT scored.
  M4 v2  the brief's consistency test: Q1==Q2 per adjudicator; both answer new Q3 NO; both name
         the same Q4 ID; that ID is what the session's checker reports FAILED on
         cl1-fail-missing-violations-field.
  M5 v2  no unrelated change, allowing CR-2/BL-1 to change and seven rows to gain text.

Run: python3 -B score_maker_v2.py [controls|rescore|all]
"""
import json, pathlib, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import config as C
import q1lib as L
import q3lib as Q

ROOT = C.ROOT
EV = ROOT / "evidence"
R0 = Q.R0
R1 = Q.R1
SEATS = json.loads((ROOT / "score-q1.json").read_text())["seats"]

CANDIDATES = [
    ("gemini-3.7-flash", ""),
    ("gemini-3.7-flash (re-run)", "37r"),
    ("gemini-3.8-flash", "38"),
    ("gemini-3.8-flash (re-run)", "38r"),
    ("gemini-4-argon", "argon"),
    ("seed-2.0-code", "s2c"),
    ("kimi-k2.7-code", "k27c"),
    ("deepseek-v3.2", "ds32"),
    ("grok-4.7", "g47b"),
]

Q3_NEW = ("A record claims CL1, has no `readsBeforeFreeze` field, and meets every other "
          "requirement. Under this SPEC.md, does BL-1 or CR-2 read FAILED or NOT-CHECKABLE for "
          "it? Answer YES or NO, then quote the deciding sentence.")
Q4_TEXT = Q.APPENDIX_C[3][0]
M4V2 = [(Q.APPENDIX_C[0][0], "Q1"), (Q.APPENDIX_C[1][0], "Q2"), (Q3_NEW, "Q3"), (Q4_TEXT, "Q4")]

REQ_ROW = re.compile(r"^\| (CR|BL|CL\d)-\d+ \|")
MAY_GAIN = {"CL1-2", "CL1-4", "CL1-5", "CL1-11", "CL1-12", "CL2-1", "CL3-1"}
FREE = {"CR-2", "BL-1"}


# ---------- shared helpers ----------
def fresh(src, tag):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"v2-{tag}-"))
    tree = tmp / "evaluatordriven"
    shutil.copytree(src, tree)
    Q.git_init(tree)
    return tree


def apply_session(diff_text, tag):
    """Fresh r0 copy with the session diff applied and committed, generate.py run and committed."""
    tree = fresh(R0, tag)
    if not diff_text.strip():
        return None, "no diff produced"
    (tree.parent / "c.diff").write_text(diff_text)
    rc, out = Q.sh(f"git apply --whitespace=nowarn {tree.parent/'c.diff'}", tree)
    if rc != 0:
        return None, "diff does not apply: " + (out.strip().splitlines()[0] if out.strip() else "")
    Q.sh("git add -A && git -c user.email=v@local -c user.name=VizH commit -qm applied", tree)
    rg, go = Q.sh("python3 fixtures/generate.py", tree)
    if rg != 0:
        return None, "generate.py failed"
    Q.sh("git add -A && git -c user.email=v@local -c user.name=VizH commit -qm generated", tree)
    return tree, None


def load_checker(tree, tag):
    """Import the tree's checker/check.py as a module."""
    import importlib.util
    path = tree / "checker" / "check.py"
    spec = importlib.util.spec_from_file_location(f"chk_{tag}", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def reading(mod, tree, case):
    """(verdict, level, routing, sorted failing IDs) for one case, read from `tree`'s fixtures."""
    fix = tree / "fixtures"
    rec = json.loads((fix / f"{case}.json").read_text())
    g = mod.verify(rec, str(fix / "files"), str(fix / "evidence"), str(fix / "files" / "bar.md"))
    return (g["verdict"], g["levelAchieved"], g["routing"],
            tuple(sorted(k for k, v in g["requirements"].items() if v["status"] == "FAILED")))


def expected_v2():
    exp = json.loads((R1 / "fixtures" / "expected.json").read_text())["cases"]
    out = {}
    for name, w in exp.items():
        out[name] = (w["verdict"], w["levelAchieved"], w["routing"],
                     tuple([w["fails"]] if w["fails"] else []))
    return out


# ---------- M3 v2 ----------
def m3_v2(checker_path, tag):
    """Session's checker inside the r1 tree; all 111 must match expected.json on the four fields."""
    tree = fresh(R1, f"m3-{tag}")
    shutil.copy(checker_path, tree / "checker" / "check.py")
    mod = load_checker(tree, f"m3{tag}")
    exp = expected_v2()
    bad = []
    for case in sorted(exp):
        try:
            got = reading(mod, tree, case)
        except Exception as e:
            bad.append((case, f"raised {type(e).__name__}: {e}"))
            continue
        if got != exp[case]:
            bad.append((case, f"{got} != {exp[case]}"))
    return {"passes": not bad, "ok": len(exp) - len(bad), "bad": bad[:5], "total": len(exp)}


# ---------- M5 v2 ----------
def req_rows(path):
    rows = {}
    for line in pathlib.Path(path).read_text().splitlines():
        if REQ_ROW.match(line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows[cells[0]] = {"line": line, "text": cells[1] if len(cells) > 1 else ""}
    return rows


def collapse(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def m5_v2(tree):
    problems = []
    allowed = ("SPEC.md", "checker/check.py", "fixtures/", "tests/run_fixtures.py",
               "CHANGELOG.md", "schema/custody-v1.schema.json")
    rc, changed = Q.sh("git status --porcelain", tree)
    for line in changed.splitlines():
        if not line.strip():
            continue
        f = line[3:]
        if not (f in allowed or any(f.startswith(p) for p in allowed if p.endswith("/"))):
            problems.append(f"changed file outside the allowed set: {f}")
    r0r, s = req_rows(R0 / "SPEC.md"), req_rows(tree / "SPEC.md")
    if set(r0r) != set(s):
        problems.append(f"requirement ID set changed: +{sorted(set(s)-set(r0r))} "
                        f"-{sorted(set(r0r)-set(s))}")
    for rid in set(r0r) & set(s):
        if rid in FREE:
            continue
        if rid in MAY_GAIN:
            if collapse(r0r[rid]["text"]) not in collapse(s[rid]["text"]):
                problems.append(f"{rid} did not merely gain text")
            continue
        if r0r[rid]["line"] != s[rid]["line"]:
            problems.append(f"requirement row changed but is not CR-2/BL-1/May-gain: {rid}")
    h0 = [l for l in (R0 / "SPEC.md").read_text().splitlines() if l.startswith("#")]
    h1 = [l for l in (tree / "SPEC.md").read_text().splitlines() if l.startswith("#")]
    if h0 != h1:
        problems.append("heading lines changed")
    return {"passes": not problems, "problems": problems}


# ---------- M4 v2 ----------
def ask_q(slug, spec_text, q, tag, i):
    model, provider, _ = C.PIN[slug]
    evf = EV / f"harness-m4v2-{tag}-{slug}-q{i}.json"
    if evf.exists():
        prev = json.loads(evf.read_text())
        return L.content_of(prev.get("response") or {})
    prompt = f"{spec_text}\n\n---\n\nAnswer this question about the specification above.\n\n{q}"
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000,
            "provider": {"order": [provider], "allow_fallbacks": False}}
    st, d = L.post(body, key=C.load_key())
    evf.write_text(json.dumps({"label": f"harness-m4v2-{tag}-{slug}-q{i}",
                               "model_requested": model, "provider_requested": provider,
                               "http": st, "request": body, "response": d}, indent=1) + "\n")
    return L.content_of(d) if st == 200 else ""


def yesno(text):
    if not text:
        return None
    first = text.strip().splitlines()[0].upper()
    if re.match(r"^\W*NO\b", first):
        return "NO"
    if re.match(r"^\W*YES\b", first):
        return "YES"
    m = re.search(r"\b(NO|YES)\b", text[:300], re.I)
    return m.group(1).upper() if m else None


def reqid(text):
    if not text:
        return None
    m = re.search(r"\b(CR-\d+|BL-\d+|CL\d-\d+)\b", text[:600])
    return m.group(1) if m else None


def m4_v2(spec_text, checker_path, tag):
    """All four v2 conditions. Needs the ID the session's checker reports on the named fixture."""
    tree = fresh(R1, f"m4chk-{tag}")
    shutil.copy(checker_path, tree / "checker" / "check.py")
    mod = load_checker(tree, f"m4{tag}")
    target = reading(mod, tree, "cl1-fail-missing-violations-field")[3]
    detail = {"checker_failing_on_fixture": list(target)}
    if len(target) != 1:
        detail["note"] = "checker reports a non-singleton failing set on the reference fixture"
    out = {}
    for slug in SEATS:
        a = [yesno(ask_q(slug, spec_text, q, tag, i)) for i, (q, _) in enumerate(M4V2[:3], 1)]
        q4 = reqid(ask_q(slug, spec_text, M4V2[3][0], tag, 4))
        out[slug] = {"q1": a[0], "q2": a[1], "q3": a[2], "q4": q4}
    conds = {
        "q1_eq_q2_each": all(v["q1"] == v["q2"] and v["q1"] in ("YES", "NO") for v in out.values()),
        "q3_both_no": all(v["q3"] == "NO" for v in out.values()),
        "q4_same_id": len({v["q4"] for v in out.values()}) == 1 and None not in {v["q4"] for v in out.values()},
        "q4_matches_checker": len(target) == 1 and all(v["q4"] == target[0] for v in out.values()),
    }
    detail["answers"] = out
    detail["conditions"] = conds
    detail["passes"] = all(conds.values())
    return detail


# ---------- controls ----------
def alt_checker():
    """A valid alternative design: BL-1 in scope for every claim, returning at once unless baseline."""
    src = (R1 / "checker" / "check.py").read_text()
    old = 'scope = ["CR-1", "CR-2"] + (["BL-1"] if claim == "baseline" else []) + ['
    assert src.count(old) == 1, "scope line not found as expected"
    new = 'scope = ["CR-1", "CR-2", "BL-1"] + ['
    src = src.replace(old, new)
    p = pathlib.Path(tempfile.mkdtemp(prefix="alt-")) / "check.py"
    p.write_text(src)
    return p


def p2_checker():
    """Revision 1's checker with plant P2 applied (CL1-9 sees planted controls only)."""
    src = (R1 / "checker" / "check.py").read_text()
    a = ('for e in observed for kind, want in (("clean", "conforms"),\n'
         '                                                   ("planted", "does_not_conform"))')
    b = 'for e in observed for kind, want in (("planted", "does_not_conform"),)'
    assert src.count(a) == 1, "P2 anchor not found"
    p = pathlib.Path(tempfile.mkdtemp(prefix="p2-")) / "check.py"
    p.write_text(src.replace(a, b))
    return p


def run_controls():
    print("=== CONTROLS (any other outcome is a STOP) ===", flush=True)
    res = {}

    print("\n1. revision 1 must pass M3 v2, M4 v2, M5 v2")
    m3 = m3_v2(R1 / "checker" / "check.py", "ctl-r1")
    t1 = fresh(R1, "ctl-r1-tree")
    m5 = m5_v2(t1)
    m4 = m4_v2((R1 / "SPEC.md").read_text(), R1 / "checker" / "check.py", "ctl-r1")
    res["r1"] = {"m3": m3, "m4": m4, "m5": m5}
    print(f"   M3 v2 {m3['ok']}/{m3['total']} -> {'pass' if m3['passes'] else 'FAIL'}")
    print(f"   M4 v2 -> {'pass' if m4['passes'] else 'FAIL'}  {m4['conditions']}")
    print(f"   M5 v2 -> {'pass' if m5['passes'] else 'FAIL'} {m5['problems']}")

    print("\n2. revision 0 must pass M3 v2 and FAIL M4 v2")
    m3r0 = m3_v2(R0 / "checker" / "check.py", "ctl-r0")
    m4r0 = m4_v2((R0 / "SPEC.md").read_text(), R0 / "checker" / "check.py", "ctl-r0")
    res["r0"] = {"m3": m3r0, "m4": m4r0}
    print(f"   M3 v2 {m3r0['ok']}/{m3r0['total']} -> {'pass' if m3r0['passes'] else 'FAIL'}")
    print(f"   M4 v2 -> {'FAIL (as required)' if not m4r0['passes'] else 'PASS - CONTROL FAILED'}"
          f"  {m4r0['conditions']}")

    print("\n3. a valid alternative design must pass M3 v2 (111/111)")
    alt = alt_checker()
    m3alt = m3_v2(alt, "ctl-alt")
    res["alt"] = m3alt
    print(f"   M3 v2 {m3alt['ok']}/{m3alt['total']} -> {'pass' if m3alt['passes'] else 'FAIL'}")
    if m3alt["bad"]:
        print(f"   first bad: {m3alt['bad'][:2]}")

    print("\n4. a broken checker (plant P2) must fail M3 v2")
    p2 = p2_checker()
    m3p2 = m3_v2(p2, "ctl-p2")
    res["p2"] = m3p2
    print(f"   M3 v2 {m3p2['ok']}/{m3p2['total']} -> "
          f"{'FAIL (as required)' if not m3p2['passes'] else 'PASS - CONTROL FAILED'}")

    stops = []
    if not m3["passes"]:
        stops.append("revision 1 fails M3 v2")
    if not m4["passes"]:
        stops.append("revision 1 fails M4 v2")
    if not m5["passes"]:
        stops.append("revision 1 fails M5 v2")
    if not m3r0["passes"]:
        stops.append("revision 0 fails M3 v2")
    if m4r0["passes"]:
        stops.append("revision 0 PASSES M4 v2 (control did not fail)")
    if not m3alt["passes"]:
        stops.append("the valid alternative design fails M3 v2")
    if m3p2["passes"]:
        stops.append("the broken checker PASSES M3 v2 (plant not caught)")
    res["stop"] = stops
    print(f"\nSTOP conditions: {stops if stops else 'none - all four controls hold'}")
    (ROOT / "q3-controls-v2.json").write_text(json.dumps(res, indent=1) + "\n")
    return not stops


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    ok = run_controls()
    if not ok:
        print("\nSTOPPING: a control did not hold.")
        sys.exit(1)
    print("\nControls hold. Run the re-score with: score_maker_v2.py rescore")
