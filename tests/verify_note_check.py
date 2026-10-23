#!/usr/bin/env python3
"""tools/verify_note.py must copy the checker's words, and must catch a note that was retyped.

Writes a note for a failing fixture, checks that every line comes from the checker's report, then
plants a paraphrased reason and expects --check to refuse it. Standard library only.
"""
import json
import pathlib
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parent.parent
FIX = ROOT / "fixtures"
TOOL = str(ROOT / "tools" / "verify_note.py")
CASE = FIX / "cl1-fail-reader-with-planted-control-only.json"
ARGS = ["--files", str(FIX / "files"), "--bar", str(FIX / "files" / "bar.md"),
        "--evidence", str(FIX / "evidence"), "--title", "A fixture under this checker"]


def run(*extra):
    return subprocess.run([sys.executable, "-B", TOOL, str(CASE), *ARGS, *extra],
                          capture_output=True, text=True)


def main():
    problems = []
    written = run().stdout
    sys.path.insert(0, str(ROOT / "checker"))
    from check import verify  # noqa: E402
    report = verify(json.loads(CASE.read_text()), str(FIX / "files"), str(FIX / "evidence"),
                    str(FIX / "files" / "bar.md"))
    for rid, v in report["requirements"].items():
        if v["status"] != "OK" and f"- **{rid}** — `{v['status']}`: {v['detail']}" not in written:
            problems.append(f"the note does not carry the checker's words for {rid}")
    with tempfile.TemporaryDirectory() as tmp:
        good, bad = pathlib.Path(tmp) / "good.md", pathlib.Path(tmp) / "bad.md"
        good.write_text("# Notes\n\n" + written + "\n## Later\n")
        bad.write_text(good.read_text().replace(report["requirements"]["CL1-9"]["detail"],
                                                "a batch holds no clean control"))
        if run("--check", str(good)).returncode:
            problems.append("--check refuses a note copied from the checker")
        if not run("--check", str(bad)).returncode:
            problems.append("--check accepts a paraphrased reason")
    if problems:
        sys.exit("\n".join(problems))
    print("verify note: copies the checker's words, and refuses a paraphrased reason")


if __name__ == "__main__":
    main()
