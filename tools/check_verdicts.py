#!/usr/bin/env python3
"""A frozen verdict per published record, and the exact command that produces it.

A checker change must reproduce every row, or it moved a published verdict and the freeze exception does not
cover it. A record whose inputs are not in this repository cannot be frozen: it is listed under `unfreezable`
with the reason, never silently omitted, because a table that quietly leaves rows out freezes nothing.

    python3 tools/check_verdicts.py [--json OUT]

Exit 0 every row matches, 1 a row drifted, 2 the table could not be read.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "tools" / "verdicts.json"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json")
    ap.add_argument("--table", help="the verdict table (default: tools/verdicts.json)")
    ap.add_argument("--records", help="the record directory to check coverage of (default: record/)")
    a = ap.parse_args(argv)
    table = Path(a.table) if a.table else TABLE
    records = Path(a.records) if a.records else (ROOT / "record")
    if not table.is_file():
        print(f"no table at {table}")
        return 2
    data = json.loads(table.read_text(encoding="utf-8"))
    rows = data.get("rows") or []
    checker = ROOT / "checker" / "check.py"
    out, bad = [], 0
    print(f"checker sha256 {__import__('hashlib').sha256(checker.read_bytes()).hexdigest()}")
    for row in rows:
        r = subprocess.run([sys.executable, str(checker), row["record"], "--files", row["files"],
                            "--evidence", row["evidence"], "--bar", row["bar"]],
                           cwd=ROOT, capture_output=True, text=True)
        try:
            got = json.loads(r.stdout)
        except json.JSONDecodeError:
            print(f"FAIL     {row['record']:44} no JSON (exit {r.returncode}): {r.stderr.strip()[:120]}")
            bad += 1
            continue
        want, failed = row["expect"], sorted(k for k, v in got["requirements"].items()
                                             if v.get("status") == "FAILED")
        ok = (got["verdict"] == want["verdict"] and got["levelAchieved"] == want["levelAchieved"]
              and failed == sorted(want["failed"]))
        print(f"{'PASS' if ok else 'FAIL':8} {row['record']:44} "
              f"{got['verdict']}/{got['levelAchieved'] or '-'} failed={failed}")
        out.append({"record": row["record"], "command": row.get("command"), "ok": ok, "failed": failed})
        bad += 0 if ok else 1
    for u in data.get("unfreezable") or []:
        print(f"UNFROZEN {u['record']:44} {u['why']}")
    # A new record must be frozen, not parked. Only the entries marked legacy - the ones published before this
    # table existed - are tolerated here: anything newer needs a row, which needs its inputs in this repo.
    legacy = {u["record"] for u in data.get("unfreezable") or [] if u.get("legacy")}
    frozen = {r["record"] for r in rows}
    parked = {u["record"] for u in data.get("unfreezable") or []}
    for name in sorted(parked - legacy):
        print(f"FAIL     {name:44} is not marked legacy: a record published after the table needs a verdict row")
        bad += 1
    for path in sorted(records.glob("*.json")):
        rel = f"record/{path.name}"
        if rel not in frozen and rel not in parked:
            print(f"FAIL     {rel:44} has no verdict row: a new record must be frozen and re-checkable")
            bad += 1
    if a.json:
        Path(a.json).write_text(json.dumps({"rows": out}, indent=2) + "\n", encoding="utf-8")
    print(f"VERDICTS {len(rows) - bad} of {len(rows)} match; "
          f"{len(data.get('unfreezable') or [])} record(s) cannot be frozen")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
