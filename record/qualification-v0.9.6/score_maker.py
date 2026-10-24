#!/usr/bin/env python3
"""Q3 scoring: M1-M5 per session and the qualify rule, from the saved final diffs.

Qualifies if at least two of three sessions pass M1 to M5, and no session fails M5.
"""
import json, pathlib, shutil, sys, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import config as C
import q1lib as L
import q3lib as Q
import run_q3 as M

ROOT = C.ROOT


def build_tree(diff_text, tag):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"sc-{tag}-"))
    tree = tmp / "evaluatordriven"
    shutil.copytree(Q.R0, tree)
    Q.git_init(tree)
    (tmp / "c.diff").write_text(diff_text)
    rc, out = Q.sh(f"git apply --whitespace=nowarn {tmp/'c.diff'}", tree)
    return tree, rc, out


def score_session(s, spec_seats):
    tag = f"s{s['session']}"
    diff = (ROOT / f"q3-s{s['session']}-final.diff").read_text()
    res = {"session": s["session"], "round_trips": len(s.get("attempts", [])) - 1}
    if not diff.strip():
        res.update({"m1": False, "m2": False, "m3": None, "m4": None, "m5": None,
                    "passes": False, "note": "no diff produced"})
        return res
    tree, rc, out = build_tree(diff, tag)
    res["apply_rc"] = rc
    if rc != 0:
        res.update({"m1": False, "m2": False, "m3": None, "m4": None, "m5": None,
                    "passes": False, "note": f"diff does not apply: {out[-300:]}"})
        return res
    rc_gen, gen_out = Q.sh("python3 fixtures/generate.py", tree)
    res["m1"] = rc_gen == 0
    if not res["m1"]:
        res.update({"m2": False, "m3": None, "m4": None, "m5": None, "passes": False,
                    "note": f"generate.py failed: {gen_out[-300:]}"})
        return res
    ok, steps = Q.m2(tree)
    res["m2"] = ok
    res["failing_steps"] = [x["step"] for x in steps if x["rc"] != 0]

    m3 = Q.m3(tree / "checker" / "check.py")
    res["m3"] = m3["passes"]
    res["m3_ok"] = m3["ok_count"]

    m5 = Q.m5(tree)
    res["m5"] = m5["passes"]
    res["m5_problems"] = m5["problems"]

    m4 = Q.m4((tree / "SPEC.md").read_text(), spec_seats, tag=f"m4-{tag}")
    res["m4"] = all(v["passes"] for v in m4.values())
    res["m4_detail"] = {k: [{"q": a["q"], "want": a["want"], "got": a["got"]}
                            for a in v["answers"]] for k, v in m4.items()}
    res["passes"] = all(res[k] for k in ("m1", "m2", "m3", "m4", "m5"))
    return res


def main():
    seats = json.loads((ROOT / "score-q1.json").read_text())["seats"]
    sessions = json.loads((ROOT / "q3-sessions.json").read_text())
    out = []
    for s in sessions:
        r = score_session(s, seats)
        out.append(r)
        print(f"session {r['session']}: M1={r.get('m1')} M2={r.get('m2')} M3={r.get('m3')} "
              f"M4={r.get('m4')} M5={r.get('m5')} -> {'PASSES' if r.get('passes') else 'fails'}"
              + (f"  {r.get('note','')}" if r.get("note") else ""), flush=True)
    passed = sum(1 for r in out if r.get("passes"))
    m5_violation = any(r.get("m5") is False for r in out)
    qualifies = passed >= 2 and not m5_violation
    print(f"\npassed {passed} of 3; any M5 failure: {m5_violation} -> "
          f"{'QUALIFIES' if qualifies else 'does NOT qualify'}")
    (ROOT / "score-q3.json").write_text(json.dumps(
        {"sessions": out, "passed_sessions": passed, "m5_violation": m5_violation,
         "qualifies": qualifies, "seats_used": seats}, indent=1) + "\n")


if __name__ == "__main__":
    main()
