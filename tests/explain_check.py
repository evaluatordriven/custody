#!/usr/bin/env python3
"""tools/explain.py must describe every fixture and the example without failing, and must show each
dimension and the checker's own verdict. It reports; it never judges."""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    bad = 0
    records = sorted((ROOT / "fixtures").glob("*.json")) + [ROOT / "examples" / "minimal" / "record.json"]
    for path in records:
        if path.name == "expected.json":
            continue
        r = json.loads(path.read_text(encoding="utf-8"))
        files = ROOT / ("examples/minimal" if "examples" in path.parts else "fixtures/files")
        args = [str(path), "--files", str(files), "--bar", str(files / "bar.md")]
        p = subprocess.run([sys.executable, str(ROOT / "tools" / "explain.py"), *args],
                           capture_output=True, text=True)
        verdict = subprocess.run([sys.executable, str(ROOT / "checker" / "check.py"), *args],
                                 capture_output=True, text=True)
        want = json.loads(verdict.stdout)["verdict"]
        dims = [d.get("id") for d in (r.get("predicate") or {}).get("bar", {}).get("dimensions", [])
                if isinstance(d, dict)]
        ok = p.returncode == 0 and f"THE CHECKER'S ANSWER: {want}" in p.stdout and all(
            f"- {d}:" in p.stdout for d in dims if d)
        if not ok:
            bad += 1
            print("FAIL", path.name, p.stderr.strip()[-200:])
    print(f"explain: {len(records) - 1 - bad} of {len(records) - 1} records described")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
