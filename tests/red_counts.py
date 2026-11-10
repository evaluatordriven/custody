#!/usr/bin/env python3
"""Show each tools/count.py check failing on a planted case before it is trusted green.

Copies the repository to a temporary folder, plants one defect at a time, and expects count.py to
name it. Standard library only. Exit 0 when every plant is caught.
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent


def planted_version(root):
    version = re.search(r"\*\*Version (\d+\.\d+\.\d+)", (root / "SPEC.md").read_text(encoding="utf-8")).group(1)
    major, minor, patch = (int(x) for x in version.split("."))
    return f"{major}.{minor}.{patch + 1}"


VER = planted_version(ROOT)


def header_bits(text):
    """The version and date in SPEC.md's header, or stop: there is nothing to plant against."""
    m = re.search(r"\*\*Version (\d+\.\d+\.\d+) · [^·]+ · (\d{4}-\d{2}-\d{2})\*\*", text)
    if not m:
        sys.exit("SPEC.md's header carries no version and date in the expected shape")
    return m.group(1), m.group(2)


SPEC_TEXT = (ROOT / "SPEC.md").read_text(encoding="utf-8")
CUR, CUR_DATE = header_bits(SPEC_TEXT)  # the release SPEC.md names today, and the day it claims
PLANTS = [  # (file, text to append or (old, new) to change, words the report must contain)
    ("README.md", "\nImplementers MUST read this.\n", "keyword MUST outside"),
    ("CONTRIBUTING.md", "\n| **bar** | a second meaning |\n", "term 'bar' defined again"),
    ("README.md", f"\nSee v{VER}.\n", f"version {VER}"),
    ("SPEC.md", "\n## 9. Padding *(normative)*\n\n" + "word " * 2400, "normative words"),
    ("README.md", "\nThis repository claims CL3.\n", "claims CL3 but no record"),
    ("SPEC.md", "\nFive reference checkers exist, in this repository.\n", "reference checker(s) exist"),
    ("README.md", "\nThe code is also offered under the MIT license.\n", "names license MIT"),
    ("LICENSE", ("(CC BY 4.0)", "(CC BY-SA 4.0)"), "LICENSE names license CC BY-SA"),
    ("LICENSE-CODE", ("                                 Apache License\n",
                      "                                 MIT License\n"), "LICENSE-CODE names license MIT"),
    ("SPEC.md", "\n| CR-9 | A planted requirement with no class. |  |\n", "CR-9 has no valid class"),
    (".github/workflows/ci.yml", ("--evidence examples/minimal/evidence", ""), "quickstart drift"),
    ("SPEC.md", "\n| CL1-99 | A planted semantic requirement no fixture fails. | semantic |\n",
     "CL1-99 is semantic but no fixture fails for it"),
    ("record/DISPOSITION-latest.md", "\nA disposition with no version in its name.\n",
     "carries no version in its name"),
    # The three release rules (v0.9.9). Held by plants rather than by one green run: each was proved red in
    # a pull request body when it was written, and a proof that lives only in a PR body expires with it.
    ("CHANGELOG.md", (f"## {CUR} (candidate)", f"## {VER} (candidate)"), f"newest entry is {VER}"),
    ("SPEC.md", (f"**Version {CUR}", f"**Version {VER}"), f"has no record/custody-v{VER}.json"),
    ("SPEC.md", (f"{CUR_DATE}** · Predicate type", "2099-01-01** · Predicate type"),
     "which is in the future"),
    (f"record/RECORD-GAP-v{VER}.md", "# A gap note for a release nobody argued for\n",
     "permitted only for a release named in GAP_EXCEPTIONS"),
]


def problems(root):
    out = subprocess.run([sys.executable, "tools/count.py"], cwd=root, capture_output=True, text=True)
    return json.loads(out.stdout)["problems"]


def main():
    missed = 0
    if problems(ROOT):
        print("count.py is not green on the repository itself")
        return 1
    ver = planted_version(ROOT)
    plants = [
        (name, text if not isinstance(text, str) else text.replace(VER, ver), expect.replace(VER, ver))
        for name, text, expect in PLANTS
    ]
    for name, text, expect in plants + [("record/r.json", None, "claimed level (CL3)")]:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "repo"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git"))
            target = root / name
            target.parent.mkdir(exist_ok=True)
            if isinstance(text, tuple):  # a change inside the file, not an addition to it
                target.write_text(target.read_text(encoding="utf-8").replace(*text, 1),
                                  encoding="utf-8")
            elif text is None:
                target.write_text(json.dumps({"predicate": {"specVersion": ver,
                                                            "levelClaimed": "CL3"}}))
            else:
                with open(target, "a", encoding="utf-8") as f:
                    f.write(text)
            caught = any(expect in p for p in problems(root))
            print(f"{'caught' if caught else 'MISSED'}  {name}: {expect}")
            missed += not caught
    with tempfile.TemporaryDirectory() as tmp:  # a kept record may quote key words: not a problem
        root = pathlib.Path(tmp) / "repo"
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git"))
        (root / "record" / "kept-v0.0.1.md").write_text("A kept bar: the checker MUST stay small.\n")
        quoted = [p for p in problems(root) if "kept-v0.0.1.md" in p]
        print(f"{'ok    ' if not quoted else 'WRONG '}  record/kept-v0.0.1.md: a kept record may quote MUST")
        missed += bool(quoted)
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
