#!/usr/bin/env python3
"""Turn a plain inputs file into a custody/v1 record by computing every digest for you.

Usage: python3 tools/make_record.py INPUTS.json RECORD.json

INPUTS.json is the record's predicate written by hand, with three conveniences. Paths are relative
to INPUTS.json's folder.
  {"file": "bar.md"}               becomes {"sha256": "<digest of bar.md>"}
  {"evidenceFile": "harness.log"}  becomes {"name": "harness.log", "sha256": "<digest>"}
  "subject": {"files": ["a.md"]}   lists named files; {"dir": ".", "exclude": ["record/"]} lists
                                   every file under a folder except the excluded prefixes.
Standard library only.
"""
import hashlib
import json
import pathlib
import sys


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve(node, base):
    if isinstance(node, dict):
        if set(node) == {"file"}:
            return {"sha256": digest(base / node["file"])}
        if set(node) == {"evidenceFile"}:
            path = base / node["evidenceFile"]
            return {"name": path.name, "sha256": digest(path)}
        return {k: resolve(v, base) for k, v in node.items()}
    if isinstance(node, list):
        return [resolve(v, base) for v in node]
    return node


def subject(spec, base):
    if "files" in spec:
        names = spec["files"]
    else:
        root = base / spec["dir"]
        names = sorted(str(p.relative_to(root)).replace("\\", "/") for p in root.rglob("*")
                       if p.is_file() and not any(str(p.relative_to(root)).startswith(x)
                                                  for x in spec.get("exclude", [])))
        base = root
    return [{"name": n, "digest": {"sha256": digest(base / n)}} for n in names]


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src = pathlib.Path(sys.argv[1])
    base = src.resolve().parent
    data = json.loads(src.read_text(encoding="utf-8"))
    record = {"_type": "https://in-toto.io/Statement/v1",
              "subject": subject(data.pop("subject"), base),
              "predicateType": "https://evaluatordriven.com/custody/v1",
              "predicate": resolve(data, base)}
    pathlib.Path(sys.argv[2]).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {sys.argv[2]}")


if __name__ == "__main__":
    main()
