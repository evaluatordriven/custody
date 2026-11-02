"""Examples declare the release's version: every examples/**/{inputs,record}.json specVersion equals SPEC.md's."""
import json, re, sys
from pathlib import Path
root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
m = re.search(r"\*\*Version (\d+\.\d+\.\d+)", (root / "SPEC.md").read_text(encoding="utf-8"))
if not m:
    sys.exit("SPEC.md: no '**Version x.y.z' line")
want, bad = m.group(1), []
files = sorted(root.glob("examples/**/inputs.json")) + sorted(root.glob("examples/**/record.json"))
def found(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "specVersion": yield v
            else: yield from found(v)
    elif isinstance(o, list):
        for v in o: yield from found(v)
for f in files:
    for v in found(json.loads(f.read_text(encoding="utf-8"))):
        if v != want: bad.append(f"{f.relative_to(root)}: specVersion {v}, SPEC.md is {want}")
print("\n".join(bad) or f"OK: {len(files)} example files declare {want}")
sys.exit(1 if bad or not files else 0)
