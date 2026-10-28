#!/usr/bin/env python3
"""Exercise tools/file_event.py and tools/release_record.py: each refusal and a full build."""
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

ROOT = pathlib.Path(__file__).resolve().parent.parent
RECORD_PY = [sys.executable, str(ROOT / "tools" / "record.py")]
FILE_EVENT = [sys.executable, str(ROOT / "tools" / "file_event.py")]
RELEASE_RECORD = [sys.executable, str(ROOT / "tools" / "release_record.py")]
CHECK_PY = [sys.executable, str(ROOT / "checker" / "check.py")]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
    return path


def lines(log):
    return [ln for ln in log.read_text(encoding="utf-8").splitlines() if ln.strip()]


def must_refuse(label, cmd, log, before, record_out=None):
    res = run(cmd)
    after = lines(log)
    if res.returncode == 0:
        sys.exit(f"FAIL {label}: expected non-zero exit, got 0")
    if after != before:
        sys.exit(f"FAIL {label}: log changed ({len(before)} -> {len(after)} lines)")
    if record_out is not None and record_out.exists():
        sys.exit(f"FAIL {label}: record file was written")
    print(f"ok   refused: {label}")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp)
        ev_dir = d / "evidence"
        ev_dir.mkdir()
        (d / "memo.md").write_text("# Memo\n", encoding="utf-8")
        (d / "bar.md").write_text("# Bar\n", encoding="utf-8")
        (d / "method.md").write_text("method\n", encoding="utf-8")
        (d / "rubric.md").write_text("rubric\n", encoding="utf-8")
        (d / "runner.md").write_text("runner\n", encoding="utf-8")
        ev_text = "D1 reading notes\n"
        (ev_dir / "reading-D1.md").write_text(ev_text, encoding="utf-8")
        ev_ref = {"name": "reading-D1.md", "sha256": sha(ev_text)}
        bar_sha = sha("# Bar\n")

        log = d / "custody.jsonl"
        assert run(RECORD_PY + ["init", str(log), "--job", "test"]).returncode == 0
        assert run(RECORD_PY + ["add", str(log), "bar-frozen", "--actor", "Morgan Lee",
                                "--file", str(d / "bar.md")]).returncode == 0
        for role, who in (("buyer", "Avery Chen"), ("specialist", "Priya Nair")):
            assert run(RECORD_PY + ["add", str(log), "approval", "--actor", who,
                                    "--data", json.dumps({"role": role,
                                                          "barDigest": bar_sha})]).returncode == 0
        assert run(RECORD_PY + ["add", str(log), "work-started", "--actor", "Drafting Agent"]
                   ).returncode == 0

        good_check = {
            "dimension": "D1", "evaluator": "E1", "run": 1, "batch": "B1",
            "outcome": "conforms", "score": None,
            "failureCondition": "fails if uncited",
            "evidence": ev_ref, "unobserved": None,
        }
        good_control = {
            "id": "K1", "batch": "B1", "evaluator": "E1",
            "case": {"sha256": sha("planted control case")},
            "expected": "does_not_conform", "outcome": "does_not_conform",
        }
        clean_control = {
            "id": "K2", "batch": "B1", "evaluator": "E1",
            "case": {"sha256": sha("clean control case")},
            "expected": "conforms", "outcome": "conforms",
        }

        df = d / "event.json"
        snap = lines(log)

        # Refusal 1: outcome word not in {conforms, does_not_conform, unobserved}
        write_json(df, dict(good_check, outcome="passed"))
        must_refuse("invalid check outcome", FILE_EVENT + [
            str(log), "check", "--actor", "Sam Ortiz", "--data-file", str(df),
            "--evidence-dir", str(ev_dir)], log, snap)

        write_json(df, dict(good_control, expected="passed"))
        must_refuse("invalid control expected outcome", FILE_EVENT + [
            str(log), "control", "--actor", "Sam Ortiz", "--data-file", str(df)], log, snap)

        # Refusal 2: score neither a number nor null (including boolean)
        write_json(df, dict(good_check, score="high"))
        must_refuse("string score", FILE_EVENT + [
            str(log), "check", "--actor", "Sam Ortiz", "--data-file", str(df),
            "--evidence-dir", str(ev_dir)], log, snap)
        write_json(df, dict(good_check, score=True))
        must_refuse("bool score", FILE_EVENT + [
            str(log), "check", "--actor", "Sam Ortiz", "--data-file", str(df),
            "--evidence-dir", str(ev_dir)], log, snap)

        # Refusal 3: control case absent or all zeros
        no_case = dict(good_control)
        no_case.pop("case")
        write_json(df, no_case)
        must_refuse("control case absent", FILE_EVENT + [
            str(log), "control", "--actor", "Sam Ortiz", "--data-file", str(df)], log, snap)

        write_json(df, dict(good_control, case={"sha256": "0" * 64}))
        must_refuse("control case all zeros", FILE_EVENT + [
            str(log), "control", "--actor", "Sam Ortiz", "--data-file", str(df)], log, snap)

        # Refusal 4: evidence not {name, sha256}, missing from --evidence-dir, or digest differs
        write_json(df, dict(good_check, evidence={"sha256": ev_ref["sha256"]}))
        must_refuse("evidence missing name", FILE_EVENT + [
            str(log), "check", "--actor", "Sam Ortiz", "--data-file", str(df),
            "--evidence-dir", str(ev_dir)], log, snap)

        write_json(df, dict(good_check, evidence={"name": "missing.md", "sha256": "a" * 64}))
        must_refuse("evidence file missing", FILE_EVENT + [
            str(log), "check", "--actor", "Sam Ortiz", "--data-file", str(df),
            "--evidence-dir", str(ev_dir)], log, snap)

        write_json(df, dict(good_check, evidence={"name": "reading-D1.md", "sha256": "b" * 64}))
        must_refuse("evidence digest differs", FILE_EVENT + [
            str(log), "check", "--actor", "Sam Ortiz", "--data-file", str(df),
            "--evidence-dir", str(ev_dir)], log, snap)

        # Refusal 5: check missing a field, or run not a whole number >= 1
        missing_fc = dict(good_check)
        missing_fc.pop("failureCondition")
        write_json(df, missing_fc)
        must_refuse("check missing field", FILE_EVENT + [
            str(log), "check", "--actor", "Sam Ortiz", "--data-file", str(df),
            "--evidence-dir", str(ev_dir)], log, snap)

        for bad_run in (0, -1, 1.5, True, "1"):
            write_json(df, dict(good_check, run=bad_run))
            must_refuse(f"check run={bad_run!r}", FILE_EVENT + [
                str(log), "check", "--actor", "Sam Ortiz", "--data-file", str(df),
                "--evidence-dir", str(ev_dir)], log, snap)

        # File a pre-production check & control, then produce the artifact
        write_json(df, good_check)
        assert run(FILE_EVENT + [str(log), "check", "--actor", "Sam Ortiz",
                                 "--data-file", str(df), "--evidence-dir", str(ev_dir)]
                   ).returncode == 0
        assert run(RECORD_PY + ["add", str(log), "artifact-produced", "--actor", "Drafting Agent",
                                "--file", str(d / "memo.md")]).returncode == 0

        inputs = {
            "specVersion": "0.9.6", "levelClaimed": "CL1",
            "subject": {"files": ["memo.md"]},
            "bar": {"digest": {"file": "bar.md"}, "author": "Morgan Lee",
                    "dimensions": [{"id": "D1", "criterion": "Every figure cites its source",
                                    "scale": None}],
                    "publishedAt": None, "groundTruth": [], "dissent": []},
            "maker": {"name": "Drafting Agent", "kind": "model", "version": "1.0",
                      "method": {"file": "method.md"}, "model": None},
            "instrument": {"rubric": {"file": "rubric.md"}, "runner": {"file": "runner.md"}},
            "evaluators": [{"id": "E1", "name": "Sam Ortiz", "kind": "person", "model": None}],
            "disagreements": [], "violations": [], "separationGaps": [],
            "retention": {"location": "local", "public": False}, "external": [],
            "disposition": {"state": "given", "by": "Avery Chen", "acknowledgesUnobserved": []},
        }
        inputs_path = write_json(d / "inputs.json", inputs)
        decl_path = write_json(d / "declared.json", {
            "checks": [{"dimension": "D1", "evaluator": "E1", "run": 1, "batch": "B1"}],
            "controls": ["K1", "K2"],
        })
        rec_path = d / "record.json"

        # release_record refuses when declared check/controls were not filed after artifact-produced
        snap = lines(log)
        must_refuse("declared check/control not filed after artifact-produced",
                    RELEASE_RECORD + [str(inputs_path), str(rec_path), "--log", str(log),
                                      "--declared", str(decl_path)], log, snap, rec_path)

        # Now file the post-production check and controls
        write_json(df, good_check)
        assert run(FILE_EVENT + [str(log), "check", "--actor", "Sam Ortiz",
                                 "--data-file", str(df), "--evidence-dir", str(ev_dir),
                                 "--source", "run 1"]).returncode == 0
        for ctl in (good_control, clean_control):
            write_json(df, ctl)
            assert run(FILE_EVENT + [str(log), "control", "--actor", "Sam Ortiz",
                                     "--data-file", str(df)]).returncode == 0

        # Refusal when only one of the declared controls was filed: test an unfiled control id
        bad_decl = write_json(d / "bad_declared.json", {
            "checks": [{"dimension": "D1", "evaluator": "E1", "run": 1, "batch": "B1"}],
            "controls": ["K1", "K2", "K999"],
        })
        snap = lines(log)
        must_refuse("unfiled control in declared",
                    RELEASE_RECORD + [str(inputs_path), str(rec_path), "--log", str(log),
                                      "--declared", str(bad_decl)], log, snap, rec_path)

        # Assemble the record with release_record.py (log must remain unchanged)
        snap = lines(log)
        res = run(RELEASE_RECORD + [str(inputs_path), str(rec_path), "--log", str(log),
                                    "--declared", str(decl_path)])
        assert res.returncode == 0, res.stderr
        assert lines(log) == snap, "release_record.py must not append to the log"
        assert rec_path.is_file()
        chk = run(CHECK_PY + [str(rec_path), "--files", str(d), "--bar", str(d / "bar.md"),
                              "--evidence", str(ev_dir)])
        assert chk.returncode == 0, chk.stdout + chk.stderr
        print("ok   filed check and controls, assembled record, checker returned OK")

        # Refusal 6: tampered log does not verify (both file_event and release_record refuse)
        tampered = lines(log)
        tampered[-1] = tampered[-1].replace('"K2"', '"K2-tampered"')
        log.write_text("\n".join(tampered) + "\n", encoding="utf-8")
        rec2 = d / "record2.json"
        write_json(df, good_control)
        must_refuse("file_event on tampered log", FILE_EVENT + [
            str(log), "control", "--actor", "Sam Ortiz", "--data-file", str(df)], log, tampered)
        must_refuse("release_record on tampered log", RELEASE_RECORD + [
            str(inputs_path), str(rec2), "--log", str(log), "--declared", str(decl_path)],
            log, tampered, rec2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
