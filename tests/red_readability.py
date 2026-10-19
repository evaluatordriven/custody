#!/usr/bin/env python3
"""Red test for tools/readability.py: each planted fault must turn the reading check red.

Copies the reviewer's guide, plants one fault at a time, and requires the check to report it. The
unplanted guide must pass. Needs textstat==0.7.13, like the check itself.
"""
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
GUIDE = ROOT / "docs" / "REVIEWERS-GUIDE.md"
TOOL = ROOT / "tools" / "readability.py"
LONG = ("This sentence has been written on purpose to run on and on, well past the limit that the "
        "reading target sets, so that the check has something long enough to catch here today.")
PLANTS = [
    ("an unglossed term used before its explanation",
     lambda t: t.replace("## The idea in one minute", "## The idea in one minute\n\nEvery evaluator "
                         "reads slowly.", 1), "term 'evaluator' first used without an explanation"),
    ("a 31-word sentence", lambda t: t.replace("## Warning signs", LONG + "\n\n## Warning signs", 1),
     "words > 30"),
    ("a hard, dense paragraph", lambda t: t + "\n\n" + " ".join(
        ["Institutionalised organisational accountability notwithstanding, interdependent "
         "verification methodologies necessitate considerable epistemological sophistication."] * 30),
     "Flesch-Kincaid grade"),
]


def run(path):
    p = subprocess.run([sys.executable, str(TOOL), str(path)], capture_output=True, text=True)
    return p.returncode, json.loads(p.stdout)[0]["problems"]


def main():
    code, problems = run(GUIDE)
    if code:
        print("the unplanted guide does not pass:", problems)
        return 1
    failed = 0
    text = GUIDE.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        for name, plant, expect in PLANTS:
            f = pathlib.Path(tmp) / "guide.md"
            f.write_text(plant(text), encoding="utf-8")
            code, problems = run(f)
            caught = code == 1 and any(expect in p for p in problems)
            failed += not caught
            print(("caught  " if caught else "MISSED  ") + name)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
