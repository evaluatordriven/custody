#!/usr/bin/env python3
"""Show each tools/count.py check failing on a planted case before it is trusted green.

Copies the repository to a temporary folder, plants one defect at a time, and expects count.py to
name it. Standard library only. Exit 0 when every plant is caught.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLANTS = [  # (file, text to append, words the problem report must contain)
    ("README.md", "\nImplementers MUST read this.\n", "keyword MUST outside"),
    ("CONTRIBUTING.md", "\n| **bar** | a second meaning |\n", "term 'bar' defined again"),
    ("README.md", "\nSee v0.9.7.\n", "version 0.9.7"),
    ("SPEC.md", "\n## 9. Padding *(normative)*\n\n" + "word " * 2400, "normative words"),
    ("README.md", "\nThis repository claims CL3.\n", "claims CL3 but no record"),
    ("SPEC.md", "\nFive reference checkers exist, in this repository.\n", "reference checker(s) exist"),
    ("README.md", "\nThe code is also offered under the MIT license.\n", "names license MIT"),
    ("SPEC.md", "\n| CR-9 | A planted requirement with no class. |  |\n", "CR-9 has no valid class"),
]


def problems(root):
    out = subprocess.run([sys.executable, "tools/count.py"], cwd=root, capture_output=True, text=True)
    return json.loads(out.stdout)["problems"]


def main():
    missed = 0
    if problems(ROOT):
        print("count.py is not green on the repository itself")
        return 1
    for name, text, expect in PLANTS + [("record/r.json", None, "claimed level (CL3)")]:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "repo"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git"))
            target = root / name
            target.parent.mkdir(exist_ok=True)
            if text is None:
                target.write_text(json.dumps({"predicate": {"specVersion": "0.9.2",
                                                            "levelClaimed": "CL3"}}))
            else:
                with open(target, "a", encoding="utf-8") as f:
                    f.write(text)
            caught = any(expect in p for p in problems(root))
            print(f"{'caught' if caught else 'MISSED'}  {name}: {expect}")
            missed += not caught
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
