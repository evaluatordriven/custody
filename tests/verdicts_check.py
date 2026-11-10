#!/usr/bin/env python3
"""The verdict gate's failure paths, exercised: a guard nobody has seen fail is a guard nobody knows works.

Two behaviours are planted and must be refused, and one must be tolerated:

  caught  a record with no verdict row                    -> "has no verdict row"
  caught  a new record parked under unfreezable           -> "is not marked legacy"
  ok      a legacy record parked under unfreezable        -> tolerated, exit 0

Run: python3 tests/verdicts_check.py
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "check_verdicts.py"


def run(table: dict, records: list[str]) -> tuple[int, str]:
    d = Path(tempfile.mkdtemp(prefix="verdicts-"))
    rec = d / "record"
    rec.mkdir()
    for name in records:
        (rec / name).write_text("{}\n", encoding="utf-8")
    t = d / "verdicts.json"
    t.write_text(json.dumps(table), encoding="utf-8")
    r = subprocess.run([sys.executable, str(TOOL), "--table", str(t), "--records", str(rec)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def main() -> int:
    bad = 0

    code, out = run({"rows": [], "unfreezable": []}, ["custody-v9.9.9.json"])
    if code == 1 and "has no verdict row" in out:
        print("caught  a record with no verdict row: a new record must be frozen and re-checkable")
    else:
        print(f"FAIL    a record with no verdict row was not refused (exit {code})\n{out}")
        bad += 1

    code, out = run({"rows": [], "unfreezable": [{"record": "record/custody-v9.9.9.json", "why": "x"}]},
                    ["custody-v9.9.9.json"])
    if code == 1 and "is not marked legacy" in out:
        print("caught  a new record parked under unfreezable: a record published after the table needs a row")
    else:
        print(f"FAIL    a new record was parked under unfreezable (exit {code})\n{out}")
        bad += 1

    code, out = run({"rows": [], "unfreezable": [{"record": "record/custody-v0.9.3.json", "legacy": True,
                                                  "why": "job inputs not published"}]},
                    ["custody-v0.9.3.json"])
    if code == 0:
        print("ok      a legacy record parked under unfreezable: tolerated, as the table intends")
    else:
        print(f"FAIL    a legacy record was refused (exit {code})\n{out}")
        bad += 1

    print(f"VERDICTS-CHECK {'pass' if bad == 0 else 'fail'} ({3 - bad}/3)")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
