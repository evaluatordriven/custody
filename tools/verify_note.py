#!/usr/bin/env python3
"""Write, or check, a published note about a record's checker result (non-normative tooling).

    python3 tools/verify_note.py RECORD [--files DIR] [--bar FILE] [--evidence DIR] --title TEXT
    python3 tools/verify_note.py RECORD [...] --title TEXT --check NOTE.md

The first form prints a Markdown section: the title, the verdict, level and routing, and one line for
every requirement that does not read OK, with the checker's own words. Paste it whole; never retype it.
The second form finds the section with that title in NOTE.md and exits 1 if any of its lines differs
from what the checker says now. Results about a record are copied from the checker, never paraphrased
(a v0.9.4 lesson: four hand-written reasons were wrong). Standard library only.
"""
import argparse
import importlib.util
import json
import pathlib
import sys

sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parent.parent


def checker():
    spec = importlib.util.spec_from_file_location("check", ROOT / "checker" / "check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def note(report, title):
    lines = [f"## {title}", "",
             f"Verdict `{report['verdict']}`, level achieved `{report['levelAchieved']}`, routing "
             f"`{report['routing']}`. Each requirement that does not read `OK`, in the checker's own words:",
             ""]
    lines += [f"- **{rid}** — `{v['status']}`: {v['detail']}"
              for rid, v in report["requirements"].items() if v["status"] != "OK"]
    return lines


def section(text, title):
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            if inside:
                break
            inside = line == f"## {title}"
        if inside:
            out.append(line)
    while out and not out[-1].strip():
        out.pop()
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for arg in ("record", "--files", "--bar", "--evidence", "--check"):
        ap.add_argument(arg)
    ap.add_argument("--title", required=True)
    a = ap.parse_args()
    record = json.loads(pathlib.Path(a.record).read_text(encoding="utf-8"))
    want = note(checker().verify(record, a.files, a.evidence, a.bar), a.title)
    if not a.check:
        print("\n".join(want))
        return 0
    have = section(pathlib.Path(a.check).read_text(encoding="utf-8"), a.title)
    if have == want:
        print(f"note matches the checker: {a.title}")
        return 0
    for w, h in zip(want + [""] * len(have), have + [""] * len(want)):
        if w != h:
            print(f"differs:\n  checker: {w}\n  note:    {h}")
            break
    return 1


if __name__ == "__main__":
    sys.exit(main())
