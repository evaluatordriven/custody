#!/usr/bin/env python3
"""Run the checker over every fixture and compare with fixtures/expected.json.

A failing fixture passes this test only if exactly one requirement reads FAILED and it is the one
named. Exit 0 when every fixture matches. Standard library only.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True  # no cache files in the tree (v0.9.5)
sys.path.insert(0, str(ROOT / "checker"))
from check import verify  # noqa: E402


FIX = ROOT / "fixtures"


def main():
    expected = json.loads((FIX / "expected.json").read_text())
    bad = 0
    for name, want in expected["cases"].items():
        record = json.loads((FIX / f"{name}.json").read_text())
        got = verify(record, str(FIX / "files"), str(FIX / "evidence"), str(FIX / "files" / "bar.md"))
        failed = sorted(k for k, v in got["requirements"].items() if v["status"] == "FAILED")
        problems = []
        for key in ("verdict", "levelAchieved", "routing"):
            if got[key] != want[key]:
                problems.append(f"{key} {got[key]!r} != {want[key]!r}")
        if (record.get("predicate") or {}).get("levelClaimed") != "baseline" and "BL-1" in got[
                "requirements"]:
            problems.append("BL-1 reported for a record that does not claim baseline (v0.9.5)")
        if failed != ([want["fails"]] if want["fails"] else []):
            problems.append(f"failed {failed} != [{want['fails']}]")
        print(f"{'ok  ' if not problems else 'FAIL'} {name}" + ("" if not problems else
                                                              "  " + "; ".join(problems)))
        bad += bool(problems)
    for edge, name in expected["boundaries"].items():
        lower, upper = edge.split("|")
        case = expected["cases"][name]
        if case["levelAchieved"] != lower or not case["fails"]:
            print(f"FAIL boundary {edge}: {name} does not pass {lower} and fail {upper}")
            bad += 1
    print(f"{len(expected['cases']) - bad if bad <= len(expected['cases']) else 0} of "
          f"{len(expected['cases'])} fixtures as expected" + (f"; {bad} problems" if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
