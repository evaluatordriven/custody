#!/usr/bin/env python3
"""Record custody events as they happen, in an append-only, hash-chained log (JSON Lines).

Each event is stamped with the clock time at which it is recorded and the sha256 of any files it names,
and it carries the hash of the event before it. Editing, removing or reordering an event breaks the
chain, and `verify` says where. Standard library only.

  record.py init   LOG --job NAME
  record.py add    LOG TYPE --actor NAME [--source TEXT] [--file PATH ...] [--data JSON]
  record.py verify LOG [--files]       check the chain; with --files, re-hash the named files
  record.py show   LOG

Suggested TYPEs: bar-frozen, approval, artifact-produced, check, control, external-read, disposition, note.
A recorded time is when the event was written down, by this clock. Say in --source what happened, and
when, if that differs.
"""
import argparse
import hashlib
import json
import pathlib
import sys
from datetime import datetime, timezone

GENESIS = "0" * 64


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")  # microseconds keep order


def parse(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00")) if ts else datetime.min.replace(
        tzinfo=timezone.utc)


def canon(entry):
    return json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def digest_file(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def read(log):
    p = pathlib.Path(log)
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def append(log, entry):
    events = read(log) if pathlib.Path(log).exists() else []
    entry["seq"] = len(events) + 1
    entry["prev"] = events[-1]["hash"] if events else GENESIS
    entry["hash"] = digest_text(canon(entry))
    with open(log, "a", encoding="utf-8") as f:
        f.write(canon(entry) + "\n")
    return entry


def verify(log, files=False):
    problems, prev, last_at = [], GENESIS, None
    for i, e in enumerate(read(log), 1):
        body = {k: v for k, v in e.items() if k != "hash"}
        if e.get("seq") != i:
            problems.append(f"event {i}: sequence number is {e.get('seq')}")
        if e.get("prev") != prev:
            problems.append(f"event {i}: does not follow the event before it (chain broken)")
        if digest_text(canon(body)) != e.get("hash"):
            problems.append(f"event {i}: content changed after it was recorded")
        if last_at is not None and parse(e.get("at")) < last_at:
            problems.append(f"event {i}: recorded earlier than the event before it")
        for path, h in (e.get("files") or {}).items() if files else []:
            if not pathlib.Path(path).is_file():
                problems.append(f"event {i}: file not found: {path}")
            elif digest_file(path) != h:
                problems.append(f"event {i}: file changed since recorded: {path}")
        prev, last_at = e.get("hash"), parse(e.get("at"))
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("init"); s.add_argument("log"); s.add_argument("--job", required=True)
    s = sub.add_parser("add"); s.add_argument("log"); s.add_argument("type")
    s.add_argument("--actor", required=True); s.add_argument("--source", default="")
    s.add_argument("--file", action="append", default=[]); s.add_argument("--data", default="{}")
    s = sub.add_parser("verify"); s.add_argument("log"); s.add_argument("--files", action="store_true")
    s = sub.add_parser("show"); s.add_argument("log")
    a = ap.parse_args()

    if a.cmd == "init":
        if pathlib.Path(a.log).exists():
            sys.exit(f"{a.log} already exists; a log is started once")
        e = append(a.log, {"type": "job-start", "at": now(), "actor": "record.py",
                           "source": "", "files": {}, "data": {"job": a.job}})
    elif a.cmd == "add":
        if not pathlib.Path(a.log).exists():
            sys.exit(f"{a.log} not found; run init first")
        e = append(a.log, {"type": a.type, "at": now(), "actor": a.actor, "source": a.source,
                           "files": {f: digest_file(f) for f in a.file}, "data": json.loads(a.data)})
    elif a.cmd == "verify":
        problems = verify(a.log, a.files)
        print("\n".join(problems) if problems else f"OK: {len(read(a.log))} events, chain intact")
        return 1 if problems else 0
    else:
        for e in read(a.log):
            print(f"{e['seq']:>3}  {e['at']}  {e['type']:<18} {e['actor']:<20} {e['source'][:60]}")
        return 0
    print(f"recorded event {e['seq']} ({e['type']}) at {e['at']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
