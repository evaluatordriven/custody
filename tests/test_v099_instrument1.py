#!/usr/bin/env python3
"""JOB 35 — INSTRUMENT 1. The Maker's bar over the v0.9.9 release DOCUMENTS.

Written by the Architect (Playbook §6). This file is the bar; it is not the work. The Owner ratified
the split ("Proceed with A", 2026-11-11): the v0.9.9 custody record is NOT a Maker deliverable, and
nothing this file COLLECTS asks the Maker to write one. The record is Instrument 2 — see SEQUENCING
below and the ``Instrument2Sequencing`` class, which is where this file says so out loud.

CLONE-PORTABLE. This file reads nothing from the environment. No ``JOB35_PACKET``, no
``JOB35_MIN_CONTROLS``, no ``RED_AT_BASE_THIS_RUN``, no ``JOB35_SUBJECT``. Its subject is the checkout
it lives in, and it runs in one wall-clock second, so any tree can run it at any time by any runner.
The command is:

    python3 -m unittest discover -s tests -p 'test_v099_instrument1.py' -v

SEQUENCING — the count.py crux, decided here and written into the cases. At the base commit
``tools/count.py:120-123`` fails a release tree that carries neither ``record/custody-v<version>.json``
nor ``record/RECORD-GAP-v<version>.md``, and ``tools/count.py:44`` (``GAP_EXCEPTIONS = {"0.9.8"}``)
refuses a gap note for any other release; measured on this tree on 2026-11-11, a documents-only 0.9.9
tree (a) with no gap note exits 1 on the no-record problem, (b) with a planted ``RECORD-GAP-v0.9.9.md``
exits 1 on the gap-not-permitted problem, and (c) with BOTH a record and a gap note still exits 1 on the
gap-not-permitted problem, because the glob at ``tools/count.py:124`` is not gated on the record's
absence. So count.py green is IMPOSSIBLE on a documents-only tree, and since Instrument 1 is the bar the
Maker is measured against, Instrument 1 requires count.py green over the zero problems that are the
Maker's, names the record problem as Instrument 2's gate, and refuses any documents-only tree that
manages to go green — because on a frozen count.py the only way a documents-only tree reaches exit 0 is
a gap note, and a gap note on 0.9.9 is the exception v0.9.8 argued for and nobody else may take.
Per case: test_02 requires zero count.py problems other than the named record problem and REDDENS if
that problem is absent; test_03 refuses the alternatives (it requires the version problem be gone and
the gap-not-permitted problem be absent). The sequencing itself is no longer a Maker case: tests 12 and
12b asserted a property the documents alone cannot satisfy, so they are carried in
``Instrument2Sequencing`` — the Orchestrator's release gate — and are not collected by the Maker's
command below. At base both of them fail on their own opening assertion, because SPEC.md declares
count.py's GAP_EXCEPTIONS release and neither has a subject yet; neither is skipped, and the block
above that class states the measured reading.

WHAT THIS FILE ASKS FOR, in the order the cases run. Nothing below is a custody-record claim.

  test_00  THE RELEASE GATE — the release actually was cut. The case asserts
           ``measure_release_lands(self.subject)`` reports NOTHING: SPEC.md declares a version STRICTLY
           LATER than ``git show <base>:SPEC.md`` (the base read from the tree's own history), the
           newest CHANGELOG entry names that version, both examples declare it, the header's date is
           real and strictly later than the base header's, and no gap note carries the release's
           name. It is RED at base because every one of those is false on an un-released tree, and it
           must also report a planted un-released copy — sensitivity is proved, conformance is
           required. When there is no git history to read, the base cannot be derived and the case
           fails loudly rather than guessing a base the documents cannot pin.
  test_01  the SPEC header names the release, states a status, is dated in the past and strictly later
           than the header it replaces, and the header and the newest CHANGELOG entry name one release.
  test_02  count.py over this tree reports ZERO problems except the release's missing record, and does
           report that one.
  test_03  the two problems that must be gone are the ones a Maker can fix from the documents: no
           current document names a version other than the release's (CONTRIBUTING.md:16's stale stamp),
           and no RECORD-GAP note names the release. Measured beside test_02, not folded into it.
  test_04  the two example files declare the release, and tests/example_version_check.py exits 0.
  test_05  SPEC.md's movement is confined to its header line and the VERSION TOKEN of section 4's
           ``specVersion`` EXAMPLE cell: every section-5 requirement row is the base commit's, id for
           id and text for text, every other cell of section 4's field table is the base commit's
           (``specVersion``'s required? cell is compared by its answer, and its example cell is
           compared with version tokens masked, so the digits may move and the prose around them may
           not), and no other text moved. This is what makes "changes no requirement" a measurement.
  test_06  the cadence amendment, in the Owner's wording, in CONTRIBUTING.md's Releases section,
           READ ACROSS A LINE WRAP (a wrapped sentence is the same sentence); the release's own
           CHANGELOG entry says the release changed no requirement, in any phrasing that says so; and
           an entry that says a requirement DID move is refused.
  test_07  CONTRIBUTING.md:16 names the release its gap note explains and no longer carries a bare
           ``0.9.x`` token that count.py reads. THE MEASUREMENT, in both directions: the case reddens
           if a token survives, it reddens if the fact the sentence states has been dropped, and it
           reddens if the sentence claims THIS release shipped without a record on a tree that ships
           no note for it — which is a false claim however the sentence is worded.
  test_08  README.md, CONTRIBUTING.md and DRAFT-NOTE.md are consistent with the release and with each
           other, and each still states what it stated at the base commit (no paragraph dropped).
           DRAFT-NOTE.md's hunk inventory must name NO path this job freezes once the release is cut:
           a note that still carries the base commit's 41-claim frozen inventory fails, however its
           version line was bumped. On the base tree the note legitimately still carries those claims
           and the case measures that (the note is the base commit's, and the claims are reported);
           the zero verdict applies to a cut tree. This case is GREEN at base.
  test_09  every current document and NOTICE: no bare non-release version token, the two license names
           unchanged, and every digest in examples/minimal/record.json checked against the bytes of the
           file it names — a doctored subject digest fails, and so does the frozen checker's exit.
  test_10  **FOOTPRINT.** Everything this bar writes goes through one gate into a private temp root; a
           copy of the subject carries every file at identical bytes; a planted write outside the root
           is refused AND the gate's refusal is proven by the file not appearing.
  test_11  **BYTES-MOVE.** No stored record's bytes change while the bar runs, proven on a plant that
           rewrites one and is caught.
  test_12  (INSTRUMENT 2, not collected here) a documents-only tree past GAP_EXCEPTIONS cannot be
           count.py green: no record reports the record problem, a gap note is refused, and a record
           plus a gap note is still refused. RED before the release moves past the exception, GREEN
           after — never skipped.
  test_12b (INSTRUMENT 2, not collected here) the record gate for the subject: zero Maker problems,
           zero record problem, count.py exit 0, and record/custody-v<version>.json on disk. RED
           until Instrument 2's record exists, GREEN once it does.
  test_13  every remaining GREEN-at-base case bites. Each plant is run here for real.
  test_14  **VERSION FROM THE DOCUMENT.** This bar carries no ``0.x.y`` literal and no spec-version
           flag, and ``release_version()`` follows a planted header.

BASE READING, measured 2026-11-11 on the job tree (clone of custody 534d8738 + this uncommitted file),
clone-portable, no environment. The command, which is the Maker's command:

    python3 -m unittest discover -s tests -p 'test_v099_instrument1.py' -v

Reading at base: exit 1, **1 RED — ``test_00`` — and 13 GREEN**, zero skips.
RED: 00. GREEN: 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 13, 14.

test_00 is the release gate: a tree that has not been released must not pass it, and a Maker who does
nothing cannot satisfy it. Every other case is GREEN at base and carries live plants run inside its
own body, so a GREEN here is "this property holds of the base tree, and the case still knows how to
say when it does not". That is the whole base reading; a docstring in this file that claims any other
case is RED at base is wrong, and the measured list above is what to check it against.

Every case here is a property of FILES. Not one of them reads a custody record, a log, or a verdict row.
Standard library only. ``sys.dont_write_bytecode`` is set at import so a run leaves no ``__pycache__``.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

# -- the fixed facts of this job, none of them a version the release will adopt -------------------
# The base commit and the date its header carries. Both are properties of the tree's history, not of
# the release being cut, so they are not version literals: the release's own digits are read off
# SPEC.md at run time and never appear below.
BASE_COMMIT = "534d8738f2331ae98b5085bbb03fd7653bb9f7d9"
BASE_HEADER_DATE = "2026-11-04"
# The version whose gap exception count.py's GAP_EXCEPTIONS names (tools/count.py:44). Named here
# because the exception is a fact about count.py that this bar cites; it is not asserted anywhere.
GAP_EXCEPTION_VERSION = "0.9.8"
# The prefix every release of this line carries. Used to recognise a version-shaped token, never to
# assert one: a document that names "0.9.q" is a token like any other and count.py will refuse it.
VERSION_LINE_PREFIX = "0.9."

# count.py's sentence for a release that carries neither a record nor a gap note saying why
# (tools/count.py:120-123). The bar matches this text so that the problem is CARRIED and named, not
# filtered by a predicate of this file's invention.
RECORD_PROBLEM_RE = re.compile(r"^release (\S+) has no record/custody-v\1\.json and no "
                               r"record/RECORD-GAP-v\1\.md saying why")
# count.py's sentence for a gap note on a release that may not take one (tools/count.py:127-128).
GAP_PROBLEM_RE = re.compile(r"declares a gap for (?P<v>\S+); a gap note is permitted only")
# count.py's sentence for a stale version token (tools/count.py:151).
STALE_PROBLEM_RE = re.compile(r"^version (\S+) in (?P<file>.+?) disagrees with SPEC\.md (\S+)")

HEADER_RE = re.compile(
    r"\*\*Version (?P<v>\d+\.\d+\.\d+) · (?P<status>[^·\n]+) · (?P<date>\d{4}-\d{2}-\d{2})\*\*")
# The section-4 row whose fourth cell holds an example version. Matched by its shape, so the row is
# found whatever number it currently shows.
SPEC_VERSION_ROW_RE = re.compile(r"^\|\s*`specVersion`\s*\|[^|\n]*\|[^|\n]*\|[^|\n]*\|\s*$", re.M)
# The same section-4 row matched with the backticks taken off the field name. Both shapes name the
# row; which one a tree carries is not measured here (that is a readability question, and test_09
# measures tokens, not backticks). Section 4's whole-table masking uses this broader shape, so a
# required cell cannot be flipped by re-typing the field name.
SPEC_VERSION_ROW_LOOSE_RE = re.compile(r"^\|\s*`?specVersion`?\s*\|[^|\n]*\|[^|\n]*\|[^|\n]*\|\s*$", re.M)
# Columns of section 4's table: | field | type | required? | notes |
# One row of that table: a first cell that is a field name — `name`, `bar.digest`, `checks[]`, or one
# level deeper `bar.dimensions[].scale`. Matched by shape, so the table is read whatever it lists.
REQ_FIELD_ROW_RE = re.compile(r"^\|\s*`?[a-z][\w.]*(?:\[\])?(?:\.[\w.[\]]+)?`?\s*\|[^\n]*$", re.M)
SPEC_FIELD_REQUIRED_COLUMN = 2
# The placeholder a required cell carries when section 4 says a field is NOT required. Any other
# value in that cell — `yes`, an empty cell — is not the base's answer and is reported.
SPEC_FIELD_NOT_REQUIRED = "not required"
# One requirement row of SPEC.md section 5: | ID | text | class |
REQ_ROW_RE = re.compile(r"^\|\s*(?P<id>(?:CR-\d+|CL[123]-\d+|BL-\d+))\s*\|(?P<rest>.*)$", re.M)
# The Owner's cadence amendment, verbatim ("Owner rulings" #2, 2026-11-11). The Owner's words, not
# the Architect's, and not the Specialist's: it is quoted and required to appear as a sentence.
CADENCE_AMENDMENT = "a release that changes no requirement does not count toward the monthly cadence"
# Phrasings that state the release changed no requirement. A set, so a paraphrase passes and an entry
# that says nothing about requirements does not.
CADENCE_CLAIM_PATTERNS = (
    re.compile(r"\bno requirement (changed|changes|is changed|has changed|was changed)\b", re.I),
    re.compile(r"\bchanges? (no|not) requirements?\b", re.I),
    re.compile(r"\bno change to (any|the) requirement", re.I),
    re.compile(r"\brequirement set is unchanged\b", re.I),
)
# An entry that claims a requirement DID move: a requirement id named as a bullet under **Breaking**.
CADENCE_CONTRADICTION_RE = re.compile(
    r"\*\*Breaking\*\*[^\n]*\n(?:[^\n]*\n){0,40}?[ \t]*(?:-|•|\*)[ \t]*(?:CL[123]|CR|BL)-\d+", re.I)
# What tests/example_version_check.py derives, restated so a plant can be read the same way.
EXAMPLES = ("examples/minimal/inputs.json", "examples/minimal/record.json")
# The current documents count.py:146-151 parses for a stray version token (it skips record/ and
# CHANGELOG.md), plus the schema file, plus NOTICE. This bar measures the same set and adds the two
# example files; both are JSON, and a token in one of them is a token count.py does not see.
CURRENT_DOCUMENTS = ("README.md", "CONTRIBUTING.md", "DRAFT-NOTE.md", "GOVERNANCE.md", "SECURITY.md",
                     "NOTICE", "PATENTS.md", "SPEC.md")

# facts this bar requires each document to keep STATING, so that "make it consistent" cannot be done by
# deleting the sentence that made it inconsistent. Each pair is (document, a regex it must match). The
# regexes are phrases the base commit already carries; none of them is the bar's requirement, they are
# the release's own previous claims, and their survival is what test_08 measures. They are matched
# against the file with its whitespace flattened, so a reflow is not a deletion.
CONTRIBUTING_REQUIRED_PHRASES = (
    ("CONTRIBUTING.md", re.compile(r"a reader who could not see the maker's answer reads it", re.I),
     "the statement that an independent reader reads the bar before the change"),
    ("CONTRIBUTING.md", re.compile(r"count\.py`? now refuses", re.I),
     "the statement that count.py now refuses a release with neither a record nor a declared absence"),
    ("CONTRIBUTING.md", re.compile(r"ships a record", re.I),
     "the statement that the release carrying a behavioral change ships a record"),
)

# Sentences that are STABLE across a release: the cadence paragraph and its neighbours. They are
# compared with version tokens masked, so the Owner's amendment inserted into the cadence sentence
# reads as a rewrite of it and a deletion reads as a deletion. test_07's check (c) measures the same
# property at sentence granularity; this constant exists so the property has one stated set of
# sentences to compare — the ones the release is allowed to touch — rather than every sentence.
UNSTABLE_PREFIXES = ("At most one release a month", "Versions follow Semantic Versioning",
                     "Every release is a git tag")
README_REQUIRED_PHRASES = (
    ("README.md", re.compile(r"this release's record claims CL1", re.I),
     "this release's record claims CL1"),
    ("README.md", re.compile(r"no reader panel, guide tester or human reader", re.I),
     "the statement that this release had no reader panel"),
    ("README.md", re.compile(r"## Quickstart", re.I), "the Quickstart section"),
)
DRAFT_NOTE_REQUIRED_PHRASES = (
    ("DRAFT-NOTE.md", re.compile(r"Hunk inventory", re.I), "the hunk inventory"),
    ("DRAFT-NOTE.md", re.compile(r"## \d+\.\s", re.M), "its numbered sections"),
)


# ---------------------------------------------------------------------------------------------
# One code path. Every measurement is a plain function of a tree root. The subject, a copy of the
# subject, and a planted copy are all just roots.
# ---------------------------------------------------------------------------------------------
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """Run a child process. Nothing in this function chooses WHAT to measure; it passes the
    environment through so tools/count.py sees the same interpreter settings the bar was started
    with, and adds only PYTHONDONTWRITEBYTECODE so a run leaves no cache in the tree."""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, env=env)


def read_header(root: Path) -> re.Match | None:
    return HEADER_RE.search((root / "SPEC.md").read_text(encoding="utf-8"))


def release_version(root: Path) -> str:
    """The version the document declares. Never a literal, never a flag."""
    m = read_header(root)
    if m is None:
        raise AssertionError("SPEC.md carries no `**Version X.Y.Z · status · YYYY-MM-DD**` header")
    return m.group("v")


def version_tokens(text: str) -> list[str]:
    """Every version-shaped token the way count.py reads one: a bare X.Y.Z (tools/count.py:149)."""
    return re.findall(r"\b[vV]?(0\.\d+\.\d+)\b", text)


def _body_without_versions(text: str) -> str:
    """The text with every version-shaped token replaced by a mark, so two documents that differ only
    in which release they are about compare equal. Used to prove each document still says what it said,
    not to excuse the tokens: test_09 and test_02 measure the tokens themselves."""
    return re.sub(r"\b[vV]?0\.\d+\.\d+\b", "<version>", text)


# -- 00 ---------------------------------------------------------------------------------------
def base_version(root: Path) -> tuple[str | None, str]:
    """(version, how) — the release the tree REPLACES, read from the tree's own evidence, never a
    literal and never a flag.

    Clone-portable, in descending order of authority, and every step is measured, not assumed:

      1. ``git show <BASE_COMMIT>:SPEC.md`` — a clone carries ``.git``, so this is the normal path.
         This is what a bar means when it says "the base commit". Verified: a fresh ``git clone`` of
         this tree answers it.
      2. If there is no history to read (a bare tarball, or the base commit is not in this clone's
         history), the base CANNOT be derived from the documents, and this function returns None with
         the reason. It does NOT fall back to the CHANGELOG's previous entry or to the highest
         ``record/custody-vX.Y.Z.json``: those were measured and REJECTED, because cutting a release
         does not remove the previous release from either. On the un-released tree the CHANGELOG's
         newest entry is the header's own release and the highest record is one release behind, so a
         header equal to the newest CHANGELOG entry would read as "later than the record's release"
         and the gate would be GREEN with nothing cut — the exact defect this bar exists to prevent.
         A base the documents cannot pin must fail loudly, not be guessed.

    ``how`` is a short string naming which path was used, or why no base could be derived, so a case
    can print it and an evaluator can see the base was derived rather than assumed.
    """
    base_spec = git_show(root, BASE_COMMIT, "SPEC.md")
    if base_spec is not None:
        m = HEADER_RE.search(base_spec)
        if m is not None:
            return m.group("v"), f"git show {BASE_COMMIT[:12]}:SPEC.md"
    return None, ("no git history to read: a bare tarball cannot pin the base commit's release, and "
                  "the CHANGELOG/record fallback was measured and rejected (it lets an un-released "
                  "tree pass). Run this bar in a clone, which carries .git")


def version_key(v: str) -> tuple[int, int, int]:
    major, minor, patch = (int(x) for x in v.split("."))
    return major, minor, patch


def base_header_date(root: Path) -> tuple[str | None, str]:
    """The date the replaced header carried, from the base SPEC.md, or from the base release's own
    CHANGELOG entry if history is unavailable. (None, why) when neither exists."""
    base_spec = git_show(root, BASE_COMMIT, "SPEC.md")
    if base_spec is not None:
        m = HEADER_RE.search(base_spec)
        if m is not None:
            return m.group("date"), f"git show {BASE_COMMIT[:12]}:SPEC.md header"
    bv, _ = base_version(root)
    if bv is not None:
        changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
        m = re.search(rf"^#{{0,3}}\s*{re.escape(bv)}\b.*?(\d{{4}}-\d{{2}}-\d{{2}})", changelog,
                      flags=re.M | re.S)
        if m is not None:
            return m.group(1), f"CHANGELOG.md's {bv} entry"
    return None, "neither the base SPEC.md nor a dated base CHANGELOG entry exists"


def measure_release_lands(root: Path) -> list[str]:
    """THE RELEASE GATE. The release must actually have been cut, and every claim below is measured
    against the tree's OWN history, not against a literal and not against a flag:

      * the working SPEC.md header declares a version STRICTLY LATER than the base commit's, and not
        in the future;
      * the newest CHANGELOG.md entry names that same version;
      * both examples/minimal/*.json declare that same version;
      * the header's date is a real day, not in the future, and strictly later than the base
        header's date.

    On an un-released tree (a 0.9.8 tree, where the base is 0.9.8) EVERY one of these is false by
    construction: the version is equal and not later, the changelog names the base release, the
    examples declare the base release, and the header date equals the base header's date. That is
    why this function is RED at base and green only on a tree that has been released — a Maker who
    does nothing cannot pass it.

    The version is never a literal: it is read from this tree's header, and the base is read from
    this tree's history. Nothing here knows which number the next release will carry.
    """
    bad: list[str] = []
    m = read_header(root)
    if m is None:
        return ["SPEC.md: no `**Version X.Y.Z · status · YYYY-MM-DD**` header"]
    version = m.group("v")
    base_v, base_how = base_version(root)
    if base_v is None:
        return [f"SPEC.md: the base release cannot be derived ({base_how}); a release gate with no "
                f"base has nothing to measure, so this case will not pass by default"]
    # (1) strictly later than the base, and a real version
    if version_key(version) <= version_key(base_v):
        bad.append(f"SPEC.md: the header declares {version}, which is not later than the base "
                   f"release {base_v} (derived from {base_how}); the release has not been cut")
    # (2) the newest CHANGELOG entry names this same version
    changelog = (root / "CHANGELOG.md")
    if not changelog.is_file():
        bad.append("CHANGELOG.md: missing")
    else:
        newest = re.search(r"^#{0,3}\s*(\d+\.\d+\.\d+)\b",
                           changelog.read_text(encoding="utf-8"), flags=re.M)
        if newest is None:
            bad.append("CHANGELOG.md: no version heading at all")
        elif newest.group(1) != version:
            bad.append(f"CHANGELOG.md: the newest entry is {newest.group(1)}, not {version}; a "
                       f"release whose changelog has no entry for it has not been documented")
    # (3) both examples declare this same version
    for rel, found in examples_declaring(root).items():
        if not found:
            bad.append(f"{rel}: carries no specVersion")
        for v in found:
            if v != version:
                bad.append(f"{rel}: specVersion {v!r}, not the release {version!r}")
    # (4) the header date: real, not future, and strictly later than the base header's date
    try:
        dated = datetime.date.fromisoformat(m.group("date"))
    except ValueError:
        bad.append(f"SPEC.md: header date {m.group('date')!r} is not a calendar day")
    else:
        if dated > datetime.date.today():
            bad.append(f"SPEC.md: header is dated {dated.isoformat()}, which is in the future")
        base_date, date_how = base_header_date(root)
        if base_date is None:
            bad.append(f"SPEC.md: the base header's date cannot be derived ({date_how}); a release "
                       f"whose date is not later than the header it replaces is un-released")
        else:
            try:
                if dated <= datetime.date.fromisoformat(base_date):
                    bad.append(f"SPEC.md: header is dated {dated.isoformat()}, which is not strictly "
                               f"later than the base header's date {base_date} (from {date_how}); "
                               f"a later release carries a later date")
            except ValueError:
                bad.append(f"SPEC.md: base header date {base_date!r} is not a calendar day")
    # (5) no gap note carries the release's name: this release ships a record (Instrument 2)
    gap = root / "record" / f"RECORD-GAP-v{version}.md"
    if gap.is_file():
        bad.append(f"record/{gap.name}: a gap note carries the release's name; this release ships a "
                   f"record (Instrument 2), and a gap is the exception {GAP_EXCEPTION_VERSION} "
                   f"argued for")
    return bad


def git_show(root: Path, rev: str, rel: str) -> str | None:
    """The bytes of one file at a commit, or None when the tree cannot answer. A tarball with no git
    gets None, and the case that needs it says so rather than comparing a file to itself."""
    r = run(["git", "show", f"{rev}:{rel}"], root)
    return r.stdout if r.returncode == 0 else None


# -- 01 ---------------------------------------------------------------------------------------
def measure_header(root: Path) -> list[str]:
    """The header names the release, states a status, is dated in the past and strictly later than the
    header it replaces, and section 4's example is the release's own version."""
    bad: list[str] = []
    m = read_header(root)
    if m is None:
        return ["SPEC.md: no `**Version X.Y.Z · status · YYYY-MM-DD**` header"]
    declared = m.group("v")
    if m.group("status").strip() == "":
        bad.append("SPEC.md: header carries no status word")
    try:
        dated = datetime.date.fromisoformat(m.group("date"))
    except ValueError:
        return bad + [f"SPEC.md: header date {m.group('date')!r} is not a calendar day"]
    if dated > datetime.date.today():
        bad.append(f"SPEC.md: header is dated {dated.isoformat()}, which is in the future")
    if dated <= datetime.date.fromisoformat(BASE_HEADER_DATE):
        bad.append(f"SPEC.md: header is dated {dated.isoformat()}, which is not strictly later than "
                   f"the release it replaces ({BASE_HEADER_DATE})")
    text = (root / "SPEC.md").read_text(encoding="utf-8")
    row = SPEC_VERSION_ROW_RE.search(text)
    if row is not None:
        cells = [c.strip() for c in row.group(0).strip().strip("|").split("|")]
        shown = version_tokens(cells[-1]) if cells else []
        wrong = sorted(v for v in shown if v != declared)
        if wrong:
            bad.append(f"SPEC.md: section 4's specVersion example says {wrong[0]} but the header says "
                       f"{declared}")
    newest = re.search(r"^#{0,3}\s*(\d+\.\d+\.\d+)",
                       (root / "CHANGELOG.md").read_text(encoding="utf-8"), flags=re.M)
    if newest is None:
        bad.append("CHANGELOG.md: no version heading at all")
    elif newest.group(1) != declared:
        bad.append(f"CHANGELOG.md: newest entry is {newest.group(1)} but SPEC.md says {declared}")
    return bad


# -- 02 / 03: count.py, split along the line that decides who owns the problem ------------------
def count_problems(root: Path) -> tuple[int, list[str], str]:
    """(exit code, problems, stderr). count.py writes its report as JSON on stdout."""
    r = run([sys.executable, "tools/count.py"], root)
    try:
        out = json.loads(r.stdout)
    except json.JSONDecodeError:
        return r.returncode, [], (r.stdout or "") + (r.stderr or "")
    return r.returncode, list(out.get("problems") or []), (r.stderr or "")


def partition_count(problems: list[str], version: str) -> dict[str, list[str]]:
    """Split count.py's problems into the ones Instrument 2's record closes, the two that are the
    Maker's to fix from the documents, and everything else (which is the Maker's too, unnamed here)."""
    record, gap, stale, rest = [], [], [], []
    for p in problems:
        rm = RECORD_PROBLEM_RE.match(p)
        if rm and rm.group(1) == version:
            record.append(p)
            continue
        gm = GAP_PROBLEM_RE.search(p)
        if gm and gm.group("v") == version:
            gap.append(p)
            continue
        sm = STALE_PROBLEM_RE.match(p)
        if sm:
            stale.append(p)
            continue
        rest.append(p)
    return {"record": record, "gap": gap, "stale": stale, "rest": rest}


def measure_count_except_record(root: Path) -> list[str]:
    """Every count.py problem EXCEPT the release's missing record must be zero, and the record problem
    must be present. Both halves matter: the first is the Maker's bar, the second is the proof that the
    problem was carried and named rather than filtered away by a predicate that matches nothing.

    A zero exit is read against the release: on a tree that declares the GAP_EXCEPTIONS release, a zero
    exit IS the ordinary green and there is no record problem to carry; on any other release, a zero
    exit is the ordinary green only when the release's record is on disk, and otherwise it can only
    have come from a gap note count.py's glob did not refuse.
    """
    version = release_version(root)
    code, problems, err = count_problems(root)
    if not problems and code != 0:
        return [f"tools/count.py exited {code} with no parseable problem list: {err.strip()[:300]}"]
    record_on_disk = (root / "record" / f"custody-v{version}.json").is_file()
    if code == 0:
        if version == GAP_EXCEPTION_VERSION or record_on_disk:
            return []
        return [f"tools/count.py exited 0 on a tree that declares {version}, carries no record for "
                f"it, and has no gap note on disk. That green is not a pass: on a frozen count.py "
                f"(GAP_EXCEPTIONS = {{\"{GAP_EXCEPTION_VERSION}\"}}) a documents-only tree reaches "
                f"exit 0 only through a gap note, and a gap note on {version} is refused. Either the "
                f"record exists — which is Instrument 2's output, not the Maker's — or a gap note "
                f"was planted"]
    parts = partition_count(problems, version)
    bad = [f"count.py: {p}" for p in parts["stale"] + parts["rest"]]
    if not parts["record"]:
        bad.append(f"count.py reported no missing-record problem for {version}, so this case cannot "
                   f"show it carried that problem rather than filtering it away")
    return bad


def measure_count_maker_problems(root: Path) -> list[str]:
    """The two problems that are the Maker's — a stale version token, and a gap note carrying the
    release's name — are absent. The record problem is Instrument 2's and is not required here."""
    version = release_version(root)
    code, problems, err = count_problems(root)
    if not problems and code != 0:
        return [f"tools/count.py exited {code} with no parseable problem list: {err.strip()[:300]}"]
    parts = partition_count(problems, version)
    bad = [f"count.py: {p}" for p in parts["stale"] + parts["gap"]]
    # A zero exit on the GAP-EXCEPTION release, or on a tree whose record is on disk, is the ordinary
    # green. On any other tree it is the signature of a gap note that count.py's glob
    # (tools/count.py:124-128) did not refuse.
    if not parts["record"] and code == 0 and version != GAP_EXCEPTION_VERSION \
            and not (root / "record" / f"custody-v{version}.json").is_file():
        bad.append(f"count.py exited 0 on a documents-only tree for {version}; see test_02 — a "
                   f"green here came from a gap note")
    return bad


# -- 04 ---------------------------------------------------------------------------------------
def examples_declaring(root: Path) -> dict[str, list[str]]:
    """path -> every specVersion value the file carries, found by walking it, exactly as
    tests/example_version_check.py walks it."""
    out: dict[str, list[str]] = {}
    for rel in EXAMPLES:
        p = root / rel
        if not p.is_file():
            out[rel] = ["<missing>"]
            continue
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            out[rel] = [f"<not JSON: {e}>"]
            continue
        found: list[str] = []

        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == "specVersion":
                        found.append(str(v))
                    else:
                        walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)

        walk(doc)
        out[rel] = found
    return out


def measure_examples(root: Path) -> list[str]:
    version = release_version(root)
    bad: list[str] = []
    for rel, found in examples_declaring(root).items():
        if not found:
            bad.append(f"{rel}: carries no specVersion")
        for v in found:
            if v != version:
                bad.append(f"{rel}: specVersion {v!r} but SPEC.md declares {version!r}")
    r = run([sys.executable, "tests/example_version_check.py"], root)
    if r.returncode != 0:
        body = (r.stdout or "").strip() or (r.stderr or "").strip()
        bad.append(f"tests/example_version_check.py exited {r.returncode}: {body[:400]}")
    return bad


def spec_field_rows(text: str, loose: bool = False) -> dict[str, list[str]]:
    """field -> the row's cells, for section 4's field table. A field's identity is its first cell with
    the backticks taken off, so the row is found whether or not the document typesets the name."""
    pat = SPEC_VERSION_ROW_LOOSE_RE if loose else REQ_FIELD_ROW_RE
    out: dict[str, list[str]] = {}
    for m in pat.finditer(text):
        cells = [c.strip() for c in m.group(0).strip().strip("|").split("|")]
        if not cells:
            continue
        key = cells[0].replace("`", "").strip()
        if key:
            out[key] = cells
    return out


def _required_cell_normalised(cell: str) -> str:
    """The required? cell, reduced to the two answers section 4 can give: NOT required, or required.
    An empty cell is required (the table's contract is that a field with nothing in that cell is
    required), and `no` is the other way of saying not-required. Everything else reads as required —
    which is deliberate: `yes` and `no` are different answers and must not compare equal."""
    flat = cell.replace("`", "").strip().lower()
    if flat in ("", "yes", "y") or flat == "required" or flat.startswith("yes,"):
        return "required"
    if flat.startswith(("not required", "no", "optional", "n/a")):
        return SPEC_FIELD_NOT_REQUIRED
    return f"<unread: {cell.strip()[:40]}>"


def measure_spec_section4(root: Path) -> list[str]:
    """SECTION 4's FIELD TABLE, cell by cell against the base commit.

    This release changes no requirement, so the table that says what a record must carry moves in
    exactly one place: ``specVersion``'s example note, which names the release. Every other cell of
    every row — the field name, its type, whether it is required, and its notes — is the base
    commit's, compared as text. The required? cell is ALSO compared by its answer, so a flip from
    required to not-required is reported in the terms a reader cares about even when both cells are
    non-empty.

    Why the measurement is per cell and not a whole-row mask: the section-4 ``specVersion`` row is the
    one row a release may touch, and an earlier revision exempted the whole row. Masking the row
    masked its required cell too, so flipping `yes` to `no` — which turns a required field into an
    optional one, a requirement change — passed. It is the example note that moves; the row is not
    exempt.

    Red on: a row removed or added; a type, required or notes cell changed outside the example note;
    the example note left naming a version that is not the release; the example note's PROSE reworded
    while a version token survives; the specVersion row's required answer changed; the field name
    re-typed.

    THE EXAMPLE CELL IS NOT EXEMPT — ONLY THE VERSION TOKEN IN IT IS. An earlier revision skipped the
    notes cell of ``specVersion`` wholesale, on the reasoning that the example value is the one thing
    the release moves. That skipped the prose around the token too: rewriting
    ``This document's version, e.g. `0.9.8``` to ``The version this document declares, for example
    `0.9.8``` kept a version token in the cell and passed, although the row is a requirement's
    definition and this release changes no requirement. The cell is now compared with version tokens
    masked, so the digits may move to the release and the words around them may not.
    """
    base_spec = git_show(root, BASE_COMMIT, "SPEC.md")
    if base_spec is None:
        return [f"SPEC.md: cannot read SPEC.md at {BASE_COMMIT[:12]}; section 4's table cannot be "
                f"shown unmoved and this case will not claim it was"]
    current = (root / "SPEC.md").read_text(encoding="utf-8")
    version = release_version(root)
    then = spec_field_rows(base_spec)
    now = spec_field_rows(current)
    if not then:
        return [f"SPEC.md at {BASE_COMMIT[:12]}: no section-4 field rows parsed; the comparison "
                f"measured nothing and this case will not pass on it"]
    bad: list[str] = []
    gone = sorted(set(then) - set(now))
    new = sorted(set(now) - set(then))
    if gone:
        bad.append(f"SPEC.md: section 4 field(s) {gone} are gone; this release changes no requirement")
    if new:
        bad.append(f"SPEC.md: section 4 field(s) {new} are new; a new field is a requirement change")
    for field in sorted(set(then) & set(now)):
        a, b = then[field], now[field]
        n = min(len(a), len(b))
        for col in range(1, n):
            left, right = a[col], b[col]
            if field == "specVersion" and col == len(a) - 1 == len(b) - 1:
                # The example cell: its version TOKEN is the release's to move (measured below), but
                # the prose around the token is not. Compare with version tokens masked to a mark, so
                # a reworded note that keeps a valid token still reads as a reworded note.
                left, right = (_body_without_versions(left), _body_without_versions(right))
            if left != right:
                bad.append(f"SPEC.md: section 4's `{field}` row changed in column {col + 1}: base "
                           f"{a[col]!r} -> now {b[col]!r}. Two cells of that row move — the example "
                           f"note, and nothing else — and this release changes no requirement")
        if len(a) != len(b):
            bad.append(f"SPEC.md: section 4's `{field}` row has {len(b)} cells where the base commit "
                       f"has {len(a)}")
        if field == "specVersion":
            ra = _required_cell_normalised(a[SPEC_FIELD_REQUIRED_COLUMN])
            rb = _required_cell_normalised(b[SPEC_FIELD_REQUIRED_COLUMN])
            if ra != rb:
                bad.append(f"SPEC.md: section 4 says `specVersion` is {rb!r} where the base commit "
                           f"says {ra!r}. That is a requirement change, and this release changes no "
                           f"requirement")
            note = b[-1] if b else ""
            shown = version_tokens(note)
            if not shown:
                bad.append(f"SPEC.md: section 4's `specVersion` example note carries no version: "
                           f"{note!r}")
            elif [v for v in shown if v != version]:
                bad.append(f"SPEC.md: section 4's `specVersion` example says "
                           f"{[v for v in shown if v != version]} but the release is {version}")
    return bad


# -- 05 ---------------------------------------------------------------------------------------
def requirement_rows(text: str) -> dict[str, str]:
    """id -> requirement text, whitespace-collapsed. Section 5's rows are `| ID | text | class |`."""
    out: dict[str, str] = {}
    for m in REQ_ROW_RE.finditer(text):
        cells = [c.strip() for c in m.group("rest").split("|")]
        if len(cells) < 2:
            continue
        out[m.group("id")] = " ".join("|".join(cells[:-1]).split())
    return out


def vrow_with(row: str, version: str) -> str:
    """The section-4 `specVersion` row with its example cell set to `version`. Used by a plant that
    makes the example disagree with the header; the row's shape is kept."""
    cells = row.strip().strip("|").split("|")
    if len(cells) < 4:
        return row
    cells[-1] = f" This document's version, e.g. `{version}` "
    return "|" + "|".join(cells) + "|"


def _spec_body_without_header(text: str) -> str:
    """SPEC.md with the header line and the VERSION TOKEN of section 4's ``specVersion`` example
    replaced by fixed marks. Those two are the only places a release may move.

    The row is masked in ONE cell, and inside that cell only the version token is masked — not the
    prose around it. Earlier revisions went further in two steps, and each step hid a real change:
    the first replaced the entire row with a template,
    ``| `specVersion` | string | yes | <example removed> |``, which wrote back a required cell the
    document may not hold, so a tree that flipped that cell to ``no`` was compared against a template
    that said ``yes``; the second masked the whole notes cell, which erased the difference between
    ``This document's version, e.g. `0.9.8``` and ``The version this document declares, for example
    `0.9.8```. Only the digits move with the release (see measure_spec_section4, which compares every
    other cell, and this one with its tokens masked). Masking is by shape so a move is recognised as a
    move; the field name is matched with or without backticks so re-typing it does not smuggle a
    change past this comparison either.
    """
    text = HEADER_RE.sub("**Version <removed>**", text, count=1)

    def mask_example(m: re.Match) -> str:
        cells = m.group(0).strip().strip("|").split("|")
        if len(cells) < 4:
            return "<example removed>"
        cells[-1] = " " + _body_without_versions(cells[-1]) + " "
        return "|" + "|".join(cells) + "|"

    return SPEC_VERSION_ROW_LOOSE_RE.sub(mask_example, text, count=1)


def measure_spec_change(root: Path) -> list[str]:
    """No requirement moved, in either of the two places SPEC.md states one.

      * SECTION 5: every row is the base commit's, id for id and text for text, and no requirement id
        was added or removed.
      * SECTION 4: every cell of every field row is the base commit's except ``specVersion``'s example
        value. Measured per cell by ``measure_spec_section4``, so a required cell cannot be flipped
        behind a whole-row mask.
      * THE REST: no other text changed, with the header and the example value masked.
    """
    base_spec = git_show(root, BASE_COMMIT, "SPEC.md")
    if base_spec is None:
        return [f"SPEC.md: cannot read SPEC.md at {BASE_COMMIT[:12]}; the requirement set cannot be "
                f"shown unmoved and this case will not claim it was"]
    current = (root / "SPEC.md").read_text(encoding="utf-8")
    now, then = requirement_rows(current), requirement_rows(base_spec)
    if not then:
        return [f"SPEC.md at {BASE_COMMIT[:12]}: no requirement rows parsed; the comparison measured "
                f"nothing and this case will not pass on it"]
    bad: list[str] = list(measure_spec_section4(root))
    gone = sorted(set(then) - set(now))
    new = sorted(set(now) - set(then))
    if gone:
        bad.append(f"SPEC.md: requirement(s) {gone} are gone; a release that changes no requirement may "
                   f"not remove one")
    if new:
        bad.append(f"SPEC.md: requirement(s) {new} are new; a new id is a requirement change")
    for rid in sorted(set(then) & set(now)):
        if then[rid] != now[rid]:
            bad.append(f"SPEC.md: requirement {rid}'s text changed, and this release changes no "
                       f"requirement: base {then[rid][:110]!r} -> now {now[rid][:110]!r}")
    now_body, then_body = _spec_body_without_header(current), _spec_body_without_header(base_spec)
    if now_body != then_body:
        a, b = now_body.splitlines(), then_body.splitlines()
        first = next((i for i in range(min(len(a), len(b))) if a[i] != b[i]), min(len(a), len(b)))
        bad.append(f"SPEC.md: text outside the header and the section-4 example changed at body line "
                   f"{first + 1}: {(a[first] if first < len(a) else '<end of file>')[:140]!r}")
    return bad


# -- 06 ---------------------------------------------------------------------------------------
def _changelog_entry(text: str, version: str) -> str:
    """The entry for `version`, up to the next version heading."""
    m = re.search(rf"^#{{0,3}}\s*{re.escape(version)}\b.*$", text, flags=re.M)
    if m is None:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^#{1,3}\s*\d+\.\d+\.\d+", rest, flags=re.M)
    return rest[:nxt.start()] if nxt else rest


def _releases_section(text: str) -> str:
    m = re.search(r"^## Releases\s*$(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    return m.group(1) if m else ""


def carried_verbatim(haystack: str, needle: str) -> bool:
    """Is `needle` carried verbatim, however the document WRAPPED it across lines?

    Two readings, and the amendment passes if either holds: the text as typed, and the text with
    markdown's own wrap points restored to spaces. A sentence wrapped for a 100-column document is
    the same sentence, so this measurement may not depend on where the author's line broke. A
    wrapped word joins with a space, which is what the ``-`` arm below undoes.

    A paraphrase still fails: the words are compared as a sequence, and a reworded run of them does
    not appear in either reading.
    """
    if needle in " ".join(haystack.split()):
        return True
    joined = re.sub(r"[\s\u2014-]*\n\s*", " ", haystack)
    joined = " ".join(joined.split())
    return needle in joined


def _wrap_in_two(sentence: str) -> str:
    """The sentence the way a document wrapped for a narrow column writes it: broken at the middle
    word boundary, with the rest on the next line. Used by test_06 to write the wrapped form itself."""
    words = sentence.split()
    mid = len(words) // 2
    return " ".join(words[:mid]) + "\n" + " ".join(words[mid:])


def _wrap_all_matching(text: str, sentence: str) -> str:
    """`text` with EVERY copy of `sentence` wrapped across a line. Every copy, because a tree may
    already carry the sentence once (a conforming release) and the plant inserts a second — wrapping
    one and leaving the other leaves a valid sentence in place for the removal plant to find."""
    return text.replace(sentence, _wrap_in_two(sentence))


def _wrap_clean(text: str) -> str:
    """The text with its line wraps normalised away, so "is the sentence still in there, wrapped or
    not" is one comparison. Used to prove a removal plant actually removed the sentence."""
    return " ".join(text.replace("\n", " ").split())


def _remove_wrapped(text: str, sentence: str) -> str:
    """`text` with the sentence removed, whether or not it was wrapped.

    The span is located on a whitespace-flattened copy of the text, then mapped back to the original
    by character offset, so every line the sentence touches is cut — including the second half of a
    sentence that wrapped. ``str.replace`` cannot do this on wrapped text: it looks for the whole
    sentence on one line, finds nothing, and returns the text unchanged, which is how the old removal
    plant came to compare a tree to itself and report a bite it had not made.
    """
    # Flatten with an index map: flat[i] came from text[pos[i]].
    flat, pos = _flatten_with_map(text)
    target = " ".join(sentence.split())
    out = text
    # Every occurrence, not just the first: a conforming tree may carry the sentence once and the
    # plant inserts a second, and removing one of two would leave the measurement satisfied.
    while True:
        at = flat.find(target)
        if at < 0:
            return out
        start_in_text = pos[at]
        end_in_text = pos[at + len(target) - 1] + 1
        out = out[:start_in_text] + out[end_in_text:]
        flat, pos = _flatten_with_map(out)


def _flatten_with_map(text: str) -> tuple[str, list[int]]:
    """`text` with runs of whitespace collapsed to one space, and for each flat index the index in
    `text` it came from. The map is what lets a span found on the flat text be cut out of the
    original, wrap points and all."""
    chars: list[str] = []
    pos: list[int] = []
    prev_space = False
    for i, ch in enumerate(text):
        if ch.isspace():
            if prev_space:
                continue
            chars.append(" ")
            pos.append(i)
            prev_space = True
        else:
            chars.append(ch)
            pos.append(i)
            prev_space = False
    return "".join(chars), pos


def measure_cadence(root: Path) -> list[str]:
    """A5/A7. The Owner's amendment, in the Owner's words, inside CONTRIBUTING.md's Releases section;
    the release's own changelog entry saying it changed no requirement; and no entry claiming one did.

    The amendment is matched against the section with its line wraps restored, so a sentence the
    document wrapped across a line is read as the sentence it is — see ``carried_verbatim``. Before
    that, a conforming release whose cadence sentence happened to wrap was failed here for the wrap,
    and the plant that was supposed to prove this measurement bites did not bite at all: it removed a
    contiguous run of the amendment's words from the file, and a wrapped amendment does not carry
    that run on one line, so ``str.replace`` changed nothing and the case compared a tree to itself.
    test_06 now also asserts the removal plant CHANGED the text before asking whether it reddens.

    Tested as CLAIMS, so a paraphrase passes and a bare citation of CHANGELOG.md does not.
    """
    bad: list[str] = []
    version = release_version(root)
    contributing = (root / "CONTRIBUTING.md").read_text(encoding="utf-8")
    releases = _releases_section(contributing)
    if not releases:
        bad.append("CONTRIBUTING.md: no `## Releases` section, so the cadence rule has no home")
    elif not carried_verbatim(releases, CADENCE_AMENDMENT):
        bad.append(f"CONTRIBUTING.md: the Releases section does not carry the Owner's amendment "
                   f"verbatim: {CADENCE_AMENDMENT!r}")
    raw_entry = _changelog_entry((root / "CHANGELOG.md").read_text(encoding="utf-8"), version)
    entry = " ".join(raw_entry.split())
    if not entry:
        bad.append(f"CHANGELOG.md: there is no entry for {version}, so the release states nothing "
                   f"about requirements")
    elif not any(p.search(entry) for p in CADENCE_CLAIM_PATTERNS):
        bad.append(f"CHANGELOG.md: the {version} entry does not say the release changed no "
                   f"requirement. Citing CHANGELOG.md is not the claim; the entry must make it.")
    elif CADENCE_CONTRADICTION_RE.search(raw_entry):
        bad.append(f"CHANGELOG.md: the {version} entry names a requirement under **Breaking**, so it "
                   f"says a requirement changed and contradicts itself")
    return bad


def measure_cadence_claim_only(root: Path) -> list[str]:
    """The changelog half on its own, so a case can say which of the two claims failed."""
    version = release_version(root)
    raw_entry = _changelog_entry((root / "CHANGELOG.md").read_text(encoding="utf-8"), version)
    entry = " ".join(raw_entry.split())
    if not entry:
        return [f"CHANGELOG.md: no entry for {version}"]
    if not any(p.search(entry) for p in CADENCE_CLAIM_PATTERNS):
        return [f"CHANGELOG.md: the {version} entry does not say the release changed no requirement"]
    if CADENCE_CONTRADICTION_RE.search(raw_entry):
        return [f"CHANGELOG.md: the {version} entry names a requirement under **Breaking**"]
    return []


# -- 07 ---------------------------------------------------------------------------------------
def sentences(text: str) -> list[str]:
    """One unit per sentence-ish span, with the hard-wrap of markdown joined back up.

    A closing hyphen at end of line means the word continues on the next line ("count.py" wraps at a
    period but "RECORD-GAP-v0.9.8.md" and ``—`` do not), so that line joins with no space; any other
    line joins with one space. Paragraphs break at a blank line, a heading, a table row, a list item,
    or a fence. Joining is what lets a sentence be compared after a reflow — which is exactly what a
    Maker rewriting a wrapped sentence does to it."""
    out: list[str] = []
    buf = ""

    def flush():
        nonlocal buf
        if buf:
            out.append(buf)
            buf = ""

    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith(("|", "-", "*", "#", ">", "```")) or re.match(r"^\d+\.\s", s):
            flush()
            if s:
                out.append(s)
            continue
        if buf.endswith("-") or buf.endswith("—"):
            buf += s
        elif buf:
            buf += " " + s
        else:
            buf = s
    flush()
    return out


def carries_version_fact(sentence: str, exception_version: str = GAP_EXCEPTION_VERSION) -> bool:
    """Does this sentence still state the gap fact? Three halves, none of which may be dropped:

      * it reports that a release shipped with no record,
      * it names WHICH release — cited, or in words — and
      * it names where the note that explains it is, so a reader can open it.

    Never the version. The version in the sentence is the defect test_07 is about: count.py refuses
    any 0.x.y token in a current document (tools/count.py:142-151), so the reference cannot keep its
    number and the release has to be named in words. What may not happen is the claim losing the
    release it is about, or the note losing its address.
    """
    flat = " ".join(sentence.split())
    claims = re.search(r"(?i)\bshipped without (one|it|a record|its record)\b|\bno record\b", flat)
    names = re.search(r"(?i)\b(the (previous|last|preceding|prior) release|release before (this|it))"
                      r"\b|\b0\.9\.[0-9]+\b", flat)
    where = re.search(r"`?record/`?|`?RECORD-GAP", flat, re.I)
    return bool(claims and names and where)


def _squash_code_ticks(text: str) -> str:
    """The text with markdown backticks removed, so ``record/`` and record/ read the same. Used where a
    measurement cares about the words a document carries, not about how it typeset them."""
    return text.replace("`", "")


GAP_NOTE_CLAIM_RE = re.compile(r"(?i)\bshipped without (one|it|a record|its record)\b|\bno record\b")
# The clause that names the release a gap sentence is about, if it names one at all.
GAP_RELEASE_NAMED_RE = re.compile(r"(?i)\b(the (previous|last|preceding|prior) release|release before "
                                  r"(this|it))\b|\b0\.9\.[0-9]+\b")
# The clause that names the note a reader can open, if it names one at all.
GAP_NOTE_NAMED_RE = re.compile(r"`?record/`?|`?RECORD-GAP", re.I)


def measure_stale_stamp(root: Path) -> list[str]:
    """CONTRIBUTING.md:16's problem, in both directions, AND the claim the sentence makes.

    Three things are measured, all of them against the BASE commit's own text so the subject exists
    on an un-cut tree and on a cut one alike:

      (a) TOKEN. count.py's scanner (tools/count.py:142-151) reads every current document for a bare
          ``0.x.y`` and refuses any that is not the release's. On the un-cut tree the sentence's
          token is a non-release number; on the cut tree it names the older release. Either way it
          cannot be left as typed. Red on: a token count.py reads.

      (b) FACT, both directions. The base commit's sentence states a fact a reader needs: one release
          shipped without a record, and a note in ``record/`` says why. The rewritten sentence must
          still state it — a claim with no release in it, or a note with no address, is a sentence
          about nothing — and it must not drop the note's location. Red on: the paragraph removed; the
          claim reworded so no release is named; the note left without a place a reader can look.

      (c) THE CLAIM, which is the defect this revision repairs. The old rule only asked whether the
          sentence's VERSION token differed from the release's, so a sentence naming the release
          itself — a sentence naming the current release — was accepted. That
          sentence is false: this release does not ship without a record. A sentence that asserts a
          bare release shipped without a record is refused; a sentence that attributes the absence to
          some other release is accepted; and if this tree ships a gap note of its own, the absence is
          attributed to THIS release and the sentence must name it. Red on: the false sentence, in
          both of the ways a Maker can write it.

    The subject of (c) is located by clause, not by sentence: the claim, the release it names, and the
    note it cites are each searched for separately, so moving the amendment out of the sentence that
    carries the claim does not take the claim with it.
    """
    bad: list[str] = []
    version = release_version(root)
    p = root / "CONTRIBUTING.md"
    if not p.is_file():
        return ["CONTRIBUTING.md: missing"]
    text = p.read_text(encoding="utf-8")
    base = git_show(root, BASE_COMMIT, "CONTRIBUTING.md")
    if base is None:
        return [f"CONTRIBUTING.md: cannot read CONTRIBUTING.md at {BASE_COMMIT[:12]}; this "
                f"comparison has no subject and this case will not pass on it"]
    # (a) the scanner's reading.
    survivors = sorted({v for v in version_tokens(text) if v != version})
    if survivors:
        where = [s for s in sentences(text) if any(v in survivors for v in version_tokens(s))]
        bad.append(f"CONTRIBUTING.md: still carries {survivors}, which tools/count.py refuses in a "
                   f"current document. The sentence was not rewritten; it was left in the form the "
                   f"scanner reads. First: {where[0][:200]!r}" if where else
                   f"CONTRIBUTING.md: still carries {survivors}")
    # (b) the fact survives, with its release and its note's address.
    base_fact = [s for s in sentences(base) if carries_version_fact(s)]
    if not base_fact:
        return bad + [f"CONTRIBUTING.md at {BASE_COMMIT[:12]}: no sentence states the gap fact, so "
                      f"this comparison has no subject and this case will not pass on it"]
    now_units = sentences(text)
    now_fact = [s for s in now_units if carries_version_fact(s)]
    base_units = sentences(base)
    base_fact_units = set(base_fact)
    if not now_fact:
        bad.append(f"CONTRIBUTING.md: the sentence that explained the missing record is gone. "
                   f"Rewriting it is the fix; deleting it leaves a reader with a rule and no "
                   f"reason, and count.py at {BASE_COMMIT[:12]} cited the fact the sentence "
                   f"carries ({len(base_fact)} sentence(s))")
    else:
        flat_now = " ".join(now_fact)
        if not GAP_RELEASE_NAMED_RE.search(flat_now):
            bad.append(f"CONTRIBUTING.md: the rewritten sentence does not say WHICH release shipped "
                       f"without a record, so a reader cannot tell what the exception covers")
        if not GAP_NOTE_NAMED_RE.search(flat_now):
            bad.append(f"CONTRIBUTING.md: the rewritten sentence does not say where the note that "
                       f"explains the missing record is kept, so a reader cannot open it")
    # (c) THE CLAIM. The clause that asserts an absence, and the clause that names a release, are each
    # taken from the flat text so a reflow or an insertion cannot hide either from this measurement.
    flat = " ".join(_squash_code_ticks(text).split())
    claim = GAP_NOTE_CLAIM_RE.search(flat)
    if claim is not None:
        after = flat[claim.end():]
        before = flat[:claim.start()]
        # Clause boundaries, nearest first. `.` is one only when it ends a sentence, so
        # `record/…v<version>.md` and `count.py` do not cut a clause in half.
        opens = [i + 1 for i in (before.rfind(","), before.rfind(";"), before.rfind("—")) if i >= 0]
        for m in re.finditer(r"\.(?=\s|$)", before):
            opens.append(m.end())
        closes = [i for i in (after.find(","), after.find(";"), after.find("—")) if i >= 0]
        closes += [m.start() for m in re.finditer(r"\.(?=\s|$)", after)]
        clause_start = max([0] + opens)
        clause_end = min([len(after)] + closes)
        clause = (before[clause_start:] + claim.group(0) + after[:clause_end]).strip()
        named = GAP_RELEASE_NAMED_RE.search(clause)
        own_note = (root / "record" / f"RECORD-GAP-v{version}.md").is_file()
        names_this_release = named is not None and named.group(0).find(version) >= 0
        if named is None:
            # An absence attributed to no release at all: the reader cannot tell whose absence it
            # is, and the sentence is refused. The base commit's own sentence names one.
            if own_note:
                bad.append(f"CONTRIBUTING.md: this release ships record/RECORD-GAP-v{version}.md, but "
                           f"the sentence that explains the missing record does not name it: "
                           f"{clause[:160]!r}")
        elif names_this_release and not own_note:
            bad.append(f"CONTRIBUTING.md: the sentence says {clause[:160]!r} — that is, this release, "
                       f"{version}, shipped without a record — and this tree ships no "
                       f"record/RECORD-GAP-v{version}.md. The sentence is false: the claim must test "
                       f"whether this release ships a record, not which release the sentence names")
        # When this tree ships a note of its own, the sentence naming it is the correct sentence —
        # that is what (b) requires, and what the tree that declares the exception's release carries.
        # Nothing further is measured here: a second rule would refuse the fix this case asks for.
    # (d) every sentence of the base file that did not carry the fact still has a successor, compared
    # with version tokens masked. This is what stops a Maker from clearing the token by deleting the
    # paragraph around it. A base sentence that CONTAINS a fact-carrying unit is exempt too: an
    # insertion into the cadence paragraph (the Owner's amendment, which this release adds)
    # legitimately re-cuts the unit it was inserted into, and that is a rewrite, not a deletion. The
    # fact's own sentence is exempted by identity for the same reason.
    masked_now = {_body_without_versions(s) for s in now_units}
    lost = []
    for s in base_units:
        if s in base_fact_units or _body_without_versions(s) in masked_now:
            continue
        if any(f in s for f in base_fact_units):
            continue
        if any(s.startswith(u) for u in UNSTABLE_PREFIXES):
            # the sentence the amendment is inserted into: it must still be there in some form
            head = " ".join(s.split()[:8])
            if not any(head in _body_without_versions(n) for n in now_units):
                lost.append(s)
            continue
        lost.append(s)
    if lost:
        bad.append(f"CONTRIBUTING.md: {len(lost)} sentence(s) of the base commit are gone, which is "
                   f"not a rewrite of one sentence: {lost[0][:180]!r}")
    return bad


# -- 08 ---------------------------------------------------------------------------------------
def measure_document_consistency(root: Path) -> list[str]:
    """README, CONTRIBUTING and DRAFT-NOTE agree with the release and with each other, and each still
    states the phrases it stated at the base commit. Deleting a paragraph is not consistency."""
    bad: list[str] = []
    version = release_version(root)
    for name, patterns in (("CONTRIBUTING.md", CONTRIBUTING_REQUIRED_PHRASES),
                           ("README.md", README_REQUIRED_PHRASES),
                           ("DRAFT-NOTE.md", DRAFT_NOTE_REQUIRED_PHRASES)):
        p = root / name
        if not p.is_file():
            bad.append(f"{name}: missing")
            continue
        text = p.read_text(encoding="utf-8")
        flat = " ".join(text.split())
        for _, pat, what in patterns:
            # Every required phrase is prose, so it is matched against the flattened text: a reflow is
            # not a deletion, and the sentence-level cases (07, 08's DRAFT-NOTE arm) separately prove
            # that a deletion is caught.
            if not pat.search(flat):
                bad.append(f"{name}: no longer says {what} ({pat.pattern!r})")
    readme = (root / "README.md")
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        m = re.search(r"\*\*Status:\s*v?(\d+\.\d+\.\d+)", text)
        if m is None:
            bad.append("README.md: no `**Status: vX.Y.Z ...**` line")
        elif m.group(1) != version:
            bad.append(f"README.md: status says {m.group(1)} but SPEC.md declares {version}")
    draft = root / "DRAFT-NOTE.md"
    if draft.is_file():
        text = draft.read_text(encoding="utf-8")
        first = next((ln for ln in text.splitlines() if ln.strip().startswith("#")), "")
        shown = version_tokens(first)
        if shown and shown[0] != version:
            bad.append(f"DRAFT-NOTE.md: its title names {shown[0]} but SPEC.md declares {version}")
        stale = sorted({v for v in version_tokens(text) if v != version})
        if stale:
            bad.append(f"DRAFT-NOTE.md: still names {stale}; the draft note describes THIS release "
                       f"and a token it carries is read by tools/count.py")
        bad.extend(measure_draft_note_claims_frozen(root, text))
    return bad


# -- 08: DRAFT-NOTE.md may not claim a frozen path changed ---------------------------------------
# The hunk inventory is a LIST OF FILES THE RELEASE TOUCHED. This release freezes the checker, the
# count/verdict tools, the schema, the fixtures and this bar file (the packet's `artifact.frozen`).
# A draft note that lists a hunk in one of them is claiming a change the release did not make, and
# the note is the document a reviewer reads to decide what to look at.
#
# THE VERDICT ON A CUT TREE IS ZERO CLAIMS. An earlier revision only required that the claims be
# REPORTED — the case passed when ``measure_draft_note_claims_frozen`` returned 41 problems and
# ``measure_document_consistency`` reported the same 41, so a DRAFT-NOTE bumped in its version line
# and left carrying the base tree's whole 41-claim frozen inventory passed. Reporting a claim is not
# correcting it. ``CI_FROZEN_PATH_CLAIMS`` below is the reading; ``measure_draft_note_claims_frozen``
# and the case that calls it now require it to be zero on a cut tree.
#
# WHERE THE ZERO APPLIES. On a cut tree — the subject this bar measures, once it declares a release
# later than the base commit's — zero. On the BASE TREE the answer is not zero and is not required to
# be: the base DRAFT-NOTE.md does carry the 41 claims, and a reading taken before the release is cut
# must report that fact rather than fail on it. The base tree's GREEN comes from the "the note is
# unchanged from the base" arm, which is a measurement of the tree, not a pass on the claims.
#
# The frozen paths, and the two ways a document names one. A backticked path is how the inventory
# writes them; a bare repo-relative path is how prose writes one. The regexes are built from these
# paths so the list has one home.
FROZEN_PATHS = ("checker/check.py", "tools/count.py", "tools/check_verdicts.py",
                "schema/custody-v1.schema.json", "fixtures/expected.json",
                "tests/example_version_check.py")
# The directories the job freezes whole, as well as by path. A file under one of them that is not
# FROZEN_PATHS is still a file this job does not let anyone change (fixtures/, tests/). Named
# separately so a claim about `fixtures/generate.py` is read as a claim about a frozen tree even
# though only `fixtures/expected.json` is listed above.
FROZEN_DIRECTORIES = ("checker/", "fixtures/", "schema/", "tools/")
# Paths under a frozen directory that this release DOES move: the two examples the Owner put in the
# editable set ("Include", ruling 1) and the documents themselves. Everything else under a frozen
# directory is frozen. A path named here is not read as a frozen claim.
FROZEN_DIRECTORY_EXCEPTIONS = ("examples/minimal/inputs.json", "examples/minimal/record.json")


def _frozen_in(line: str) -> list[str]:
    """Every frozen path this line names, as typed. A backticked token is read as a path; so is a
    bare token that names a frozen directory. Returns the tokens as found, so a failure can quote what
    the document actually said. Deduplicated within the line, and nowhere else: a measurement holds no
    state between lines or between calls."""
    hits: list[str] = []

    def add(tok: str) -> None:
        if tok not in hits:
            hits.append(tok)

    tokens = re.findall(r"`([^`]+)`", line) + re.findall(
        r"(?<![\w/.-])((?:checker|fixtures|schema|tools|tests)/[\w./-]+)", line)
    for tok in tokens:
        tok = tok.strip()
        if tok in FROZEN_PATHS:
            add(tok)
            continue
        if any(tok.startswith(d) for d in FROZEN_DIRECTORIES) \
                and not any(tok == e for e in FROZEN_DIRECTORY_EXCEPTIONS):
            add(tok)
    return hits


# Verbs that assert a path was CHANGED by this release. A draft note may DISCUSS a frozen path — the
# base commit touched it, and reasoning about that is what a draft note is for — but it may not claim
# this release moved it. The claim is what is measured, so the rule looks for the pairing.
CHANGE_VERB_RE = re.compile(r"(?i)\b(chang(?:e[sd]?|ing)|bump(?:s|ed)?|mov(?:e[sd]?|ing)|"
                            r"edit(?:s|ed)?|rewr(?:ote|ite|ites|itten)|modif(?:y|ies|ied)|"
                            r"updat(?:e[sd]?|ing)|regenerat(?:e[sd]?|ing)|total|hunk)\b")
# The hunk-map table: | `path` | n | item | — every row is a file the release touched, by definition.
HUNK_MAP_ROW_RE = re.compile(r"^\|\s*`(?P<path>[^`]+)`\s*\|\s*\d+\s*\|")


def measure_draft_note_claims_frozen(root: Path, text: str | None = None) -> list[str]:
    """Every line of a draft note that CLAIMS this release touched a frozen path.

    Three shapes, because a draft note makes the claim three ways:

      * an inventory line — `1. `path` (+n -m) — ...` — every numbered entry is a file the release
        touched, so naming a frozen path there is the claim, whatever verb follows;
      * a hunk-map row — `| `path` | 3 | item |` — the same, in table form;
      * a sentence in the prose that names a frozen path AND a change verb. A sentence that names a
        frozen path while reasoning about the base commit makes no claim about this release and is not
        reported.

    A glob (`fixtures/cl1-fail-*`) is not a path: it names a family the note is describing, not a
    file the release moved.

    Measured on the document as it stands, not against the base: the draft note describes the
    release, so every path it claims to have touched is a claim about this release, whoever typed it.
    Green on a note that DISCUSSES a frozen path without claiming the release moved it.

    WHAT A GREEN MEANS IS ``[]``. This function is the reading a case compares to zero on a cut tree;
    it reports every claim and says nothing when the note makes none. It does NOT report a claim as
    "acceptable" or "expected" — an earlier revision's caller did, and a note that carried the base
    tree's 41 claims while its version line had been bumped passed on that. See the block above.
    """
    if text is None:
        p = root / "DRAFT-NOTE.md"
        if not p.is_file():
            return ["DRAFT-NOTE.md: missing"]
        text = p.read_text(encoding="utf-8")
    bad: list[str] = []
    for n, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        inventory = re.match(r"^\d+\.\s+`[^`]+`", stripped) is not None
        hunk_row = HUNK_MAP_ROW_RE.match(stripped) is not None
        hits = [h for h in _frozen_in(line) if "*" not in h]
        if not hits:
            continue
        if inventory or hunk_row:
            bad.append(f"DRAFT-NOTE.md:{n}: the hunk inventory lists {hits}, which this job freezes. "
                       f"The inventory is what the release touched, and this release does not touch "
                       f"them. Line: {stripped[:180]!r}")
        elif CHANGE_VERB_RE.search(line):
            bad.append(f"DRAFT-NOTE.md:{n}: the draft note claims this release changed {hits}, which "
                       f"this job freezes. Line: {stripped[:180]!r}")
    return bad


# ---------------------------------------------------------------------------------------------
# 09b: THE EXAMPLES' DIGESTS, CHECKED AGAINST SOMETHING ------------------------------------------
# record.json carries digests. A digest is a claim about bytes, and a claim nobody compares to bytes is
# decoration: an earlier revision said the examples' digests "are what count.py and the checker read",
# and measured neither, so `examples/minimal/record.json` with `/subject/0/digest/sha256` set to
# sixty-four zeros returned [] from measure_documents_clean. Nothing reported it.
#
# WHAT THE CHECK IS, and why it needs no custody record. Every digest in examples/minimal/record.json
# names a file in examples/minimal/, and examples/minimal/inputs.json — a document in this tree, not a
# record — names which file each digest is about (`"file"`, `"evidenceFile"`). So the tree carries both
# halves: the digest, and the file it is a digest of. The check is a direct digest comparison, resolved
# through inputs.json. It reads no custody record, no log, and no verdict row. (A record's `subject`
# entries carry their own `name`, so those resolve without inputs.json; the rest are resolved by
# walking inputs.json and the record together, in the same order.)
#
# THE FROZEN CHECKER IS ALSO RUN where it applies. tools/check_verdicts.py re-runs checker/check.py over
# examples/minimal/record.json and requires the frozen verdict. It is run here and its exit code is
# required to be 0. It is NOT the whole check: measured, setting the rubric or method digest to zeros
# still exits 0 from check_verdicts.py (the checker does not compare those digests), so the direct
# comparison above is what covers them. Both are run; each catches what the other does not.
EXAMPLE_DIGEST_DIR = "examples/minimal"
EXAMPLE_RECORD = "examples/minimal/record.json"
EXAMPLE_INPUTS = "examples/minimal/inputs.json"


def _example_digest_pairs(root: Path) -> tuple[list[tuple[str, str, str]], list[str]]:
    """(label, digest, path relative to examples/minimal/), and the problems that stop it resolving.

    Every digest in the record is paired with the file inputs.json names for it. Where inputs.json
    does not name a file — the record's own `subject` entries, which carry a `name` — the record's
    name is used. A digest with no resolvable file is reported as a problem, because a digest that
    names nothing is a claim nobody can check.
    """
    base = root / EXAMPLE_DIGEST_DIR
    rec_p, inp_p = root / EXAMPLE_RECORD, root / EXAMPLE_INPUTS
    problems: list[str] = []
    pairs: list[tuple[str, str, str]] = []
    for p in (rec_p, inp_p):
        if not p.is_file():
            return [], [f"{p.relative_to(root)}: missing, so its digests cannot be checked"]
    try:
        rec = json.loads(rec_p.read_text(encoding="utf-8"))
        inp = json.loads(inp_p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [], [f"{EXAMPLE_RECORD} or {EXAMPLE_INPUTS}: not JSON ({e})"]

    pred = rec.get("predicate") or {}

    def add(label: str, dig, rel) -> None:
        if not isinstance(dig, str) or not dig:
            problems.append(f"{EXAMPLE_RECORD}: {label} carries no sha256 digest")
            return
        if not rel:
            problems.append(f"{EXAMPLE_RECORD}: {label} has a digest but {EXAMPLE_INPUTS} names no "
                            f"file for it, so the digest is a claim about nothing this tree holds")
            return
        pairs.append((label, dig, str(rel)))

    for i, s in enumerate(rec.get("subject") or []):
        add(f"subject[{i}]", (s.get("digest") or {}).get("sha256"), s.get("name"))
    subj_files = (inp.get("subject") or {}).get("files") or []
    for i, s in enumerate(rec.get("subject") or []):
        if not s.get("name") and i < len(subj_files):
            pairs[:] = [x for x in pairs if x[0] != f"subject[{i}]"]
            add(f"subject[{i}]", (s.get("digest") or {}).get("sha256"), subj_files[i])
    bar, inp_bar = pred.get("bar") or {}, inp.get("bar") or {}
    add("predicate.bar.digest", (bar.get("digest") or {}).get("sha256"),
        (inp_bar.get("digest") or {}).get("file"))
    for i, a in enumerate(bar.get("approvals") or []):
        src = (inp_bar.get("approvals") or [])
        add(f"predicate.bar.approvals[{i}].barDigest", (a.get("barDigest") or {}).get("sha256"),
            ((src[i].get("barDigest") or {}).get("file") if i < len(src) else None))
    maker, inp_maker = pred.get("maker") or {}, inp.get("maker") or {}
    add("predicate.maker.method", (maker.get("method") or {}).get("sha256"),
        (inp_maker.get("method") or {}).get("file"))
    inst, inp_inst = pred.get("instrument") or {}, inp.get("instrument") or {}
    for name in ("rubric", "runner"):
        add(f"predicate.instrument.{name}", (inst.get(name) or {}).get("sha256"),
            (inp_inst.get(name) or {}).get("file"))
    inp_checks = inp.get("checks") or []
    for i, c in enumerate(pred.get("checks") or []):
        src = inp_checks[i] if i < len(inp_checks) else {}
        add(f"predicate.checks[{i}].evidence", (c.get("evidence") or {}).get("sha256"),
            (src.get("evidence") or {}).get("evidenceFile"))
    inp_controls = inp.get("controls") or []
    for i, c in enumerate(pred.get("controls") or []):
        src = inp_controls[i] if i < len(inp_controls) else {}
        add(f"predicate.controls[{i}].case", (c.get("case") or {}).get("sha256"),
            (src.get("case") or {}).get("file"))
    return pairs, problems


def measure_example_digests(root: Path) -> list[str]:
    """Every digest in examples/minimal/record.json, compared to the bytes of the file it names.

    A doctored digest — the Owner's `/subject/0/digest/sha256` set to sixty-four zeros — must be
    reported here. So must a digest whose file is missing, and a digest whose file has the right
    digest for the wrong content. The comparison is sha256 of the file's bytes, resolved relative to
    examples/minimal/, which is where inputs.json's relative paths point.

    The frozen checker is run as well, over the example record, and a non-zero exit is reported:
    tools/check_verdicts.py is the tree's own statement of what that record must read, and a record
    whose verdict drifted is a record whose content moved. Its exit 1 on a doctored subject digest is
    the same defect as the direct comparison catches, from the other side.
    """
    bad: list[str] = []
    pairs, unresolved = _example_digest_pairs(root)
    bad.extend(unresolved)
    base = root / EXAMPLE_DIGEST_DIR
    if not pairs:
        bad.append(f"{EXAMPLE_RECORD}: no digests resolved, so this case measured nothing")
    for label, dig, rel in pairs:
        p = base / rel
        if not p.is_file():
            bad.append(f"{EXAMPLE_RECORD}: {label} names {rel!r}, which does not exist under "
                       f"{EXAMPLE_DIGEST_DIR}/")
            continue
        got = sha256_file(p)
        if got != dig:
            bad.append(f"{EXAMPLE_RECORD}: {label} says sha256 {dig}, but {EXAMPLE_DIGEST_DIR}/{rel} "
                       f"hashes to {got}. The digest is a claim about those bytes and it is false.")
    cv = root / "tools" / "check_verdicts.py"
    if cv.is_file():
        r = run([sys.executable, "tools/check_verdicts.py"], root)
        if r.returncode != 0:
            body = (r.stdout or "").strip() or (r.stderr or "").strip()
            bad.append(f"tools/check_verdicts.py exited {r.returncode} over {EXAMPLE_RECORD}: "
                       f"{body.splitlines()[-1][:300] if body else 'no output'}")
    return bad


# -- 09 ---------------------------------------------------------------------------------------
LICENSE_NAMES = {
    "CC BY 4.0": re.compile(r"CC[ -]BY[ -]4\.0|Creative Commons Attribution 4\.0"),
    "Apache-2.0": re.compile(r"Apache[ -](?:License,? Version )?2\.0|Apache License"),
    "MIT": re.compile(r"\bMIT\b"), "GPL": re.compile(r"\bA?GPL"), "BSD": re.compile(r"\bBSD\b"),
    "MPL": re.compile(r"\bMPL\b"), "CC0": re.compile(r"\bCC0\b"),
    "CC BY-SA": re.compile(r"CC[ -]BY[ -]SA|Attribution-ShareAlike"),
    "CC BY-NC": re.compile(r"CC[ -]BY[ -]NC|NonCommercial"),
    "Unlicense": re.compile(r"\bUnlicense\b"),
}


def measure_documents_clean(root: Path) -> list[str]:
    """No current document, NOTICE or example carries a version token that is not the release's; the
    license names are the two this repository carries and no other; and the examples' DIGESTS are
    checked against the bytes of the files they name.

    The digest arm is ``measure_example_digests``. An earlier revision claimed here that the examples'
    digests "are what count.py and the checker read" and measured nothing of the kind — a record with
    ``/subject/0/digest/sha256`` set to sixty-four zeros returned [] from this function. A digest
    nobody compares to bytes is decoration, and this function now compares every one of them.
    """
    bad: list[str] = []
    version = release_version(root)
    allowed = {"CC BY 4.0", "Apache-2.0"}
    for name in CURRENT_DOCUMENTS + EXAMPLES:
        p = root / name
        if not p.is_file():
            bad.append(f"{name}: missing")
            continue
        text = p.read_text(encoding="utf-8")
        if name.endswith(".json"):
            # A JSON example's version lives in its `specVersion` field, not in prose; read that
            # field rather than scanning the whole file for a token.
            found_sv = set(re.findall(r'"specVersion"\s*:\s*"(\d+\.\d+\.\d+)"', text))
            stale = sorted(v for v in found_sv if v != version)
        else:
            stale = sorted({v for v in version_tokens(text) if v != version})
        if stale:
            bad.append(f"{name}: names {stale}, which is not the release ({version})")
        if name != "SPEC.md":
            for lic, pat in LICENSE_NAMES.items():
                if lic not in allowed and pat.search(text):
                    bad.append(f"{name}: names license {lic}; this repository carries CC BY 4.0 (text) "
                               f"and Apache-2.0 (code)")
    notice = root / "NOTICE"
    if notice.is_file():
        body = notice.read_text(encoding="utf-8")
        if not LICENSE_NAMES["Apache-2.0"].search(body):
            bad.append("NOTICE: does not say the code is Apache-2.0")
        if not re.search(r"(?is)(text|SPEC\.md|documentation).{0,150}?"
                         r"(CC[ -]BY[ -]4\.0|Creative Commons Attribution 4\.0)", body):
            bad.append("NOTICE: does not say the text is CC BY 4.0")
    bad.extend(measure_example_digests(root))
    return bad


# ---------------------------------------------------------------------------------------------
# The one write gate. Anything this bar writes goes through here and lands in a private temp root.
# ---------------------------------------------------------------------------------------------
class WriteGate:
    """A write primitive that refuses any destination outside the root it was made for."""

    def __init__(self, root: Path):
        self.root = Path(root).resolve()
        self.written: list[Path] = []

    def write_file(self, path: Path, data: str | bytes) -> Path:
        target = Path(path).resolve()
        if target != self.root and self.root not in target.parents:
            raise PermissionError(f"the bar tried to write outside its temp root: {target}")
        body = data.encode("utf-8") if isinstance(data, str) else bytes(data)
        # The whole write is checked, not just the first filesystem call: a destination that fails
        # only part-way must not leave bytes behind, and the caller must see the refusal.
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
        except OSError as e:
            raise PermissionError(f"{target}: the write failed ({e}) and no bytes were kept") from e
        self.written.append(target)
        return target


class BarBase(unittest.TestCase):
    """The subject tree, and planting helpers that go through the gate."""

    @classmethod
    def setUpClass(cls):
        # The checkout this file lives in. No environment variable decides this: a clone runs the bar
        # on itself, which is what D2 asks for.
        cls.subject = Path(__file__).resolve().parents[1]

    def setUp(self):
        if not (self.subject / "SPEC.md").is_file():
            self.skipTest(f"no subject tree at {self.subject}")

    def planted_copy(self) -> tuple[Path, WriteGate]:
        """A copy of the subject, excluding nothing (`.git` travels with it, so measure_spec_change and
        the base-commit comparisons work on it) and excluding only ``__pycache__``. Returns (root, gate)."""
        tmp = Path(tempfile.mkdtemp(prefix="job35-bar-"))
        root = tmp / "tree"
        shutil.copytree(self.subject, root, ignore=shutil.ignore_patterns("__pycache__"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        return root, WriteGate(tmp)

    def _plant(self, rel: str, data: str | bytes) -> Path:
        """A copy with one file replaced, through the gate."""
        root, gate = self.planted_copy()
        gate.write_file(root / rel, data)
        return root

    def _plant_text(self, rel: str, text: str) -> Path:
        return self._plant(rel, text)

    def _edit(self, rel: str, fn) -> Path:
        """A copy with one file's text passed through `fn`. On a tree where `fn` is a no-op — the
        tree's header already IS the base release — the copy is returned unchanged and the caller's
        bite assertion is what fails, with the reason."""
        text = (self.subject / rel).read_text(encoding="utf-8")
        new = fn(text)
        if new == text:
            root, _ = self.planted_copy()
            return root
        return self._plant_text(rel, new)

    # -- the shared bite helper: every GREEN-at-base case proves its plant reddens the SAME function --
    def assert_bites(self, fn, root: Path, needle: str, label: str):
        problems = fn(root)
        hits = [p for p in problems if needle in p]
        self.assertTrue(hits, f"{label}: the plant did not bite — {fn.__name__} returned "
                              f"{problems!r}, none containing {needle!r}")


# ---------------------------------------------------------------------------------------------
# 00-09: what the release documents must be
# ---------------------------------------------------------------------------------------------
class TestReleaseDocuments(BarBase):

    def test_00_the_release_lands(self):
        """RED at base. THE RELEASE GATE: a tree that has not been released must not pass this.

        The case asserts the subject is CLEAN and the gate is SENSITIVE, and neither half is
        optional:

          * the subject — ``measure_release_lands(self.subject)`` must return zero problems. On the
            un-released base tree it reports exactly three: the header's version is not later than
            ``git show 534d873:SPEC.md``'s, the header's date is not later than that header's, and
            ``record/RECORD-GAP-v0.9.8.md`` carries the release's own name. Those three are the
            base reading; they are not filtered or named away.
          * the plant — the base commit's own SPEC.md, written over a copy of the subject, must be
            reported as un-released. Without it the assertion above could go green on a
            ``measure_release_lands`` that had stopped measuring anything.

        The remaining bites are crafted so each fires on the DECLARED release, whatever it is, and
        does not depend on the version being a particular number:

          * bite 1 — a copy whose SPEC.md is the base commit's SPEC.md: the header reverts to the
            base release, so the "not later than base" check must fire.
          * bite 2 — a copy whose newest CHANGELOG entry is re-headed to a version the header does
            not declare: the changelog-agrreement check must fire.
          * bite 3 — a copy whose header date is set to the base header's date: the date check must
            fire.
        """
        version = release_version(self.subject)
        problems = measure_release_lands(self.subject)
        # THE GATE ASSERTS THE SUBJECT IS CLEAN. This is the only polarity a release gate can have:
        # the instrument's sensitivity is what the five bites below prove, on planted copies; the
        # subject is required to have LANDED. The earlier revision asserted `assertTrue(problems)` and
        # was therefore green on an un-released tree and red on a released one — it measured the
        # instrument's ability to complain instead of the tree's conformance, which is the opposite
        # of a gate.
        self.assertEqual(problems, [], "\n".join(problems))

        # THE PLANT that makes this a gate and not a tautology: the base commit's own SPEC.md written
        # over the working one is an un-released tree, copied byte for byte from this tree's history,
        # independent of which release this tree declares. The gate MUST report it. If this plant is
        # green, measure_release_lands() has stopped measuring and the case above certifies nothing.
        base_spec = git_show(self.subject, BASE_COMMIT, "SPEC.md")
        if base_spec is not None:
            unreleased = self._plant_text("SPEC.md", base_spec)
            planted = measure_release_lands(unreleased)
            self.assertTrue(planted,
                            f"PLANTED UN-RELEASED COPY PASSED THE GATE: SPEC.md was replaced with "
                            f"{BASE_COMMIT[:12]}'s own bytes and measure_release_lands() returned []")
            self.assertTrue(any("not later than the base" in p or "has not been cut" in p
                                for p in planted),
                            f"the planted un-released copy was reported, but not as un-released: "
                            f"{planted}")
        else:
            # No history to read: the tree cannot pin its base, so the gate must say so rather than
            # pass by default. This is not a skip; a gate with nothing to compare is red.
            self.assertTrue(any("cannot be derived" in p for p in problems),
                            f"there is no git history to read and the gate returned {problems}, which "
                            f"does not report that the base cannot be derived")
        base_spec = git_show(self.subject, BASE_COMMIT, "SPEC.md")
        if base_spec is not None:
            self.assert_bites(measure_release_lands, self._plant_text("SPEC.md", base_spec),
                              "not later than the base", "test_00 bite 1")
        # bite 2: the newest CHANGELOG entry re-headed to a version the header does not declare.
        other = f"{version.rsplit('.', 1)[0]}.{int(version.rsplit('.', 1)[1]) + 5}"

        def rehead_changelog(t: str) -> str:
            return re.sub(rf"^(#{{0,3}}\s*){re.escape(version)}\b", rf"\g<1>{other}", t,
                          count=1, flags=re.M)

        self.assert_bites(measure_release_lands, self._edit("CHANGELOG.md", rehead_changelog),
                          "the newest entry is", "test_00 bite 2")
        # bite 3: the header dated exactly as the base header -> "not strictly later" fires.
        base_date, _ = base_header_date(self.subject)
        self.assertIsNotNone(base_date, "the base header's date cannot be derived")
        base_date = str(base_date)
        self.assert_bites(measure_release_lands, self._edit("SPEC.md", lambda t: HEADER_RE.sub(
            lambda m: m.group(0).replace(m.group("date"), base_date), t, count=1)),
            "not strictly later than the base header's date", "test_00 bite 3")
        # bite 4: an example left at a version the header does not declare -> "not the release" fires.
        # The base example carries the base version; on an un-released tree that IS the declared
        # version, so planting the base file is an identity and would not bite. Plant a version the
        # header definitely does not name instead, so the example stratum is exercised on any tree.
        stale_example = f"{version.rsplit('.', 1)[0]}.{int(version.rsplit('.', 1)[1]) + 3}"
        self.assert_bites(measure_release_lands,
                          self._edit("examples/minimal/record.json", lambda t: re.sub(
                              r'("specVersion"\s*:\s*")[^"]+(")',
                              rf"\g<1>{stale_example}\g<2>", t, count=1)),
                          "not the release", "test_00 bite 4")
        # bite 5: a gap note carrying the release's name is refused.
        gaproot, gate = self.planted_copy()
        gate.write_file(gaproot / "record" / f"RECORD-GAP-v{version}.md", "# a gap\n")
        self.assert_bites(measure_release_lands, gaproot, "a gap note carries the release's name",
                          "test_00 bite 5")

    def test_01_spec_header_is_the_release_with_a_real_past_date(self):
        """GREEN at base: the base header is a real past date, it is not later than the header it
        replaces on the base's own terms, and section 4's example names the base release. The clauses
        holding that up are conditional (§ the tree IS the base release below), so the case is green
        rather than red — measured GREEN at base, and every docstring here is checked against the
        module's measured list.

        The bites are green-side, so they hold whether or not the tree is cut: a header dated in the
        future must redden the date check, and section 4's example set to a number the header does not
        declare must redden the example check. Both are written against the tree's own declared
        version, so neither depends on which release that is.
        """
        problems = measure_header(self.subject)
        version = release_version(self.subject)
        base = git_show(self.subject, BASE_COMMIT, "SPEC.md")
        self.assertIsNotNone(base, "the subject cannot read its base commit, so this case's subject "
                                   "check cannot run")
        base_v = HEADER_RE.search(base).group("v")
        if version == base_v:
            # The tree IS the base release. The release has not landed, and the case's fact is
            # measured here rather than pretended: the header must be reported as not later than the
            # header it replaces. Its bites are the green-side plants below, which hold either way.
            self.assertTrue(any("not strictly later" in p for p in problems),
                            f"the header is the base release's and measure_header() did not say so: "
                            f"{problems}")
        else:
            self.assertEqual(problems, [], "\n".join(problems))
        future = "2999-01-01"
        self.assert_bites(measure_header, self._edit("SPEC.md", lambda t: HEADER_RE.sub(
            lambda m: m.group(0).replace(m.group("date"), future), t, count=1)),
            "is in the future", "test_01 bite 1")
        other = f"{version.rsplit('.', 1)[0]}.{int(version.rsplit('.', 1)[1]) + 7}"
        self.assert_bites(measure_header, self._edit("SPEC.md", lambda t: SPEC_VERSION_ROW_RE.sub(
            lambda m: vrow_with(m.group(0), other), t, count=1)),
            "section 4's specVersion example", "test_01 bite 2")

    def test_02_count_py_green_except_the_record(self):
        """The Maker's count.py gate. GREEN at base.

        At base the tree IS the base release, so count.py exits 0 through the GAP_EXCEPTIONS release
        itself and there is no record problem to carry; the case's base clause is written for that
        state. On a cut tree it requires zero count.py problems other than the release's missing
        record, and requires that problem to be present and named rather than filtered away by a
        predicate that matches nothing. Bites: a planted gap note, and a planted stale token.

        This case is GREEN once the documents are cut, whether or not Instrument 2's record exists —
        it is the Maker's gate, and the record problem is Instrument 2's, carried and named in
        test_12b rather than required here."""
        version = release_version(self.subject)
        # the case's own fact, measured on the tree as it is
        problems = measure_count_except_record(self.subject)
        base = git_show(self.subject, BASE_COMMIT, "SPEC.md")
        self.assertIsNotNone(base, "the subject cannot read its base commit")
        base_v = HEADER_RE.search(base).group("v")
        if version == base_v:
            # un-cut: count.py exits 0 because the tree is the base release, so this case's fact is
            # the ABSENCE of a missing-record problem — which is exactly what makes a zero exit here
            # unremarkable and why the release has to move for this case to mean anything.
            self.assertEqual(problems, [],
                             f"the tree IS the base release and measure_count_except_record() "
                             f"reported {problems}")
        else:
            self.assertEqual(problems, [], "\n".join(problems))
        # bite 1: a gap note for a release count.py's GAP_EXCEPTIONS does NOT name is refused. On the
        # base tree the declared release IS the exception, so the plant targets a cut tree's release;
        # on a cut tree it targets a release nobody declared. Either way the function must report it.
        gap_v = next(f"{VERSION_LINE_PREFIX}{n}" for n in range(1, 40)
                     if f"{VERSION_LINE_PREFIX}{n}" != version)
        if version != GAP_EXCEPTION_VERSION:
            gap_v = version
        gaproot, gap_gate = self.planted_copy()
        if gap_v != version:
            gate_spec = (gaproot / "SPEC.md").read_text(encoding="utf-8")
            gap_gate.write_file(gaproot / "SPEC.md", HEADER_RE.sub(
                lambda m: m.group(0).replace(m.group("v"), gap_v), gate_spec, count=1))
        gap_gate.write_file(gaproot / "record" / f"RECORD-GAP-v{gap_v}.md", "# a gap\n")
        gap_problems = measure_count_maker_problems(gaproot)
        self.assertTrue(any("declares a gap" in p for p in gap_problems),
                        f"a gap note for {gap_v} was planted and measure_count_maker_problems() "
                        f"did not report it: {gap_problems}")
        # bite 2: a stale token planted into a document count.py reads reddens the same function.
        stale = next(f"{VERSION_LINE_PREFIX}{n}" for n in range(1, 40)
                     if f"{VERSION_LINE_PREFIX}{n}" != version)
        stale_root = self._edit("README.md", lambda t: t + f"\n\nEarlier: {stale}.\n")
        self.assert_bites(measure_count_except_record, stale_root, f"version {stale}", "test_02 bite 2")

    def test_03_count_py_maker_problems_are_gone(self):
        """The Maker's own count.py problems — the stale token and any gap note — measured beside
        test_02 so a failure names which half failed."""
        problems = measure_count_maker_problems(self.subject)
        self.assertEqual(problems, [], "\n".join(problems))

    def test_04_every_example_declares_the_release(self):
        problems = measure_examples(self.subject)
        self.assertEqual(problems, [], "\n".join(problems))

    def test_05_no_requirement_changed(self):
        """GREEN at base: the base tree's section 4 is its own, so nothing is reported. The weight is
        in the bites:

          * a section-5 requirement row's text changed -> reported.
          * SECTION 4's ``specVersion`` required cell flipped from its base answer to the other one
            -> reported. This is reason 3: the row used to be masked whole, so a flip from required to
            not-required — a requirement change — compared equal to the base and passed.
          * section 4's example value left at a version that is not the release -> reported, because
            that is the one cell of the row that may move and it must move to the release.
          * a type cell changed -> reported.
        """
        problems = measure_spec_change(self.subject)
        self.assertEqual(problems, [], "\n".join(problems))
        version = release_version(self.subject)
        base_spec = git_show(self.subject, BASE_COMMIT, "SPEC.md")
        self.assertIsNotNone(base_spec, "the subject cannot read its base commit, so the section-4 "
                                        "bites cannot be built")
        base_cells = spec_field_rows(base_spec)
        self.assertIn("specVersion", base_cells, "section 4 has no `specVersion` row to plant against")
        base_required = base_cells["specVersion"][SPEC_FIELD_REQUIRED_COLUMN]

        def flip_required(t: str) -> str:
            """The `specVersion` row's required cell set to the other answer."""
            def one(m: re.Match) -> str:
                cells = m.group(0).strip().strip("|").split("|")
                col = SPEC_FIELD_REQUIRED_COLUMN
                cell = cells[col].strip()
                cells[col] = " no " if _required_cell_normalised(cell) == "required" else " yes "
                return "|" + "|".join(cells) + "|"
            return SPEC_VERSION_ROW_RE.sub(one, t, count=1)

        flipped = self._edit("SPEC.md", flip_required)
        flipped_text = (flipped / "SPEC.md").read_text(encoding="utf-8")
        self.assertNotEqual(SPEC_VERSION_ROW_RE.search(flipped_text).group(0).strip(),
                            SPEC_VERSION_ROW_RE.search(
                                (self.subject / "SPEC.md").read_text(encoding="utf-8")).group(0).strip(),
                            f"the required-cell plant did not change the row (base cell "
                            f"{base_required!r}), so it would prove nothing")
        self.assert_bites(measure_spec_change, flipped, "requirement change",
                          "test_05 bite 1 (required cell)")
        # BITE 1b — the example cell's PROSE reworded while a valid version token survives. This is
        # the Owner's plant: "This document's version, e.g. `0.9.8`" rewritten to "The version this
        # document declares, for example `0.9.8`". Both arms used to skip this cell whole, so it
        # passed although the row defines a requirement and this release changes none. Measured on
        # both the per-cell comparison and the masked whole-body diff, because each has to catch it.
        def reword_example(t: str) -> str:
            def one(m: re.Match) -> str:
                cells = m.group(0).strip().strip("|").split("|")
                shown = version_tokens(cells[-1])
                cells[-1] = (f" The version this document declares, for example `{shown[0]}` "
                             if shown else cells[-1])
                return "|" + "|".join(cells) + "|"
            return SPEC_VERSION_ROW_RE.sub(one, t, count=1)

        reworded = self._edit("SPEC.md", reword_example)
        reworded_text = (reworded / "SPEC.md").read_text(encoding="utf-8")
        now_row = SPEC_VERSION_ROW_RE.search(reworded_text)
        self.assertIsNotNone(now_row, "the reword plant removed the specVersion row entirely")
        assert now_row is not None
        subj_row = SPEC_VERSION_ROW_RE.search(
            (self.subject / "SPEC.md").read_text(encoding="utf-8"))
        self.assertIsNotNone(subj_row, "the subject has no specVersion row to compare against")
        assert subj_row is not None
        self.assertNotEqual(now_row.group(0), subj_row.group(0),
                            "the reword plant did not change the specVersion row")
        self.assertTrue(version_tokens(now_row.group(0)),
                        "precondition: the reworded cell still carries a version token, so only the "
                        "prose moved and the fix the case asks for is not what is being tested")
        self.assert_bites(measure_spec_section4, reworded, "changed in column 4",
                          "test_05 bite 1b (reworded example cell, per cell)")
        self.assert_bites(measure_spec_change, reworded, "section 4's `specVersion` row changed",
                          "test_05 bite 1b (reworded example cell, whole body)")
        # the same flip must also be caught by the section-4 comparison on its own, so the report
        # comes from the cell comparison and not from the masked whole-body diff.
        self.assertTrue([p for p in measure_spec_section4(flipped) if "specVersion" in p],
                        f"measure_spec_section4 did not report the required-cell flip: "
                        f"{measure_spec_section4(flipped)}")
        # BITE 2 — a type cell changed.
        def retype(t: str) -> str:
            def one(m: re.Match) -> str:
                cells = m.group(0).strip().strip("|").split("|")
                cells[1] = " list of strings " if cells[1].strip() != "list of strings" else " string "
                return "|" + "|".join(cells) + "|"
            return SPEC_VERSION_ROW_RE.sub(one, t, count=1)

        retyped = self._edit("SPEC.md", retype)
        self.assert_bites(measure_spec_section4, retyped, "changed in column 2",
                          "test_05 bite 2 (type cell)")
        # BITE 3 — section 5: one requirement row's text changed, which no section-4 comparison sees.
        def weaken(t: str) -> str:
            return re.sub(r"^(\|\s*CL1-10\s*\|)(.*?)(\|)",
                          lambda m: m.group(1) + m.group(2) + " (weakened) " + m.group(3), t,
                          count=1, flags=re.M)

        weakened = self._edit("SPEC.md", weaken)
        self.assert_bites(measure_spec_change, weakened, "CL1-10's text changed",
                          "test_05 bite 3 (requirement row)")
        # and the tree is still accepted when the example value is the release: the case is
        # satisfiable by the change it asks for. Measured on a copy whose example names the release,
        # on a subject that may or may not be cut.
        example_ok, gate = self.planted_copy()
        spec_now = (example_ok / "SPEC.md").read_text(encoding="utf-8")
        gate.write_file(example_ok / "SPEC.md", SPEC_VERSION_ROW_RE.sub(
            lambda m: vrow_with(m.group(0), version), spec_now, count=1))
        self.assertEqual([p for p in measure_spec_section4(example_ok) if "specVersion" in p], [],
                         f"a section-4 example naming the release was refused: "
                         f"{measure_spec_section4(example_ok)}")

    def test_06_cadence_amendment_and_the_no_requirement_claim(self):
        """GREEN at base: the base tree's newest CHANGELOG entry is the base release's own, and the
        case's base clause is written for that state. Once the release is cut, the entry must say the
        release changed no requirement and the Releases section must carry the Owner's amendment.

        The bites: the amendment REMOVED from a copy that has it, the same removal done on a WRAPPED
        copy where a contiguous `str.replace` cannot find it, and the changelog entry made to claim a
        requirement moved. The wrap bite is what proves the amendment is measured as the sentence it
        is: before it, a conforming release whose cadence sentence wrapped was failed for the wrap and
        the removal plant found nothing to remove.
        """
        problems = measure_cadence(self.subject)
        version = release_version(self.subject)
        base = git_show(self.subject, BASE_COMMIT, "CHANGELOG.md")
        self.assertIsNotNone(base, "the subject cannot read its base commit, so this case cannot tell "
                                   "whether the entry is the base's")
        newest_base = re.search(r"^#{0,3}\s*(\d+\.\d+\.\d+)", base, flags=re.M)
        uncut = newest_base is not None and newest_base.group(1) == version
        if uncut:
            # The newest changelog entry is the base commit's: the release has not landed, so the
            # entry cannot yet make the claim. Both problems the case measures are present by fact.
            self.assertTrue(any("no entry for" in p or "does not say the release changed no" in p
                                for p in problems),
                            f"the newest entry is the base commit's and measure_cadence() did not "
                            f"report it: {problems}")
        else:
            self.assertEqual(problems, [], "\n".join(problems))
        # a copy of the subject with the amendment inserted, so the removal plant has something to
        # remove on every tree and does not depend on the subject's own state. On a tree that already
        # carries the amendment (a conforming release) this insert ADDS A SECOND COPY, which is
        # harmless for the plant below — that plant removes every copy — and is why the plant does not
        # use str.replace, which would leave the second copy standing and report a bite it did not make.
        with_rule = self._edit("CONTRIBUTING.md", lambda t: t.replace(
            "At most one release a month while the version starts with 0",
            "At most one release a month while the version starts with 0; " + CADENCE_AMENDMENT, 1))
        self.assertEqual([p for p in measure_cadence(with_rule) if "amendment" in p], [],
                         f"the amendment was planted and measure_cadence() still misses it: "
                         f"{measure_cadence(with_rule)}")
        # THE WRAP, MEASURED. The amendment is one sentence; a maker may wrap it across a line. The
        # case writes the wrapped form itself and requires the measurement to read it as the sentence
        # it is. Before this, a conforming release whose cadence sentence wrapped was FAILED here —
        # and the removal plant below did not bite on it either, because it removed a contiguous run
        # of words that a wrapped sentence does not carry on one line.
        with_rule_text = (with_rule / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn(CADENCE_AMENDMENT, with_rule_text,
                      "precondition: the inserted amendment is on one line")
        wrapped_text = _wrap_all_matching(with_rule_text, CADENCE_AMENDMENT)
        self.assertNotIn(CADENCE_AMENDMENT, wrapped_text,
                         "precondition: every copy of the amendment was wrapped")
        wrapped_root, wrapped_gate = self.planted_copy()
        wrapped_gate.write_file(wrapped_root / "CONTRIBUTING.md", wrapped_text)
        self.assertEqual([p for p in measure_cadence(wrapped_root) if "amendment" in p], [],
                         f"CONTRIBUTING.md carries the Owner's amendment WRAPPED across a line and "
                         f"measure_cadence() failed it for the wrap: {measure_cadence(wrapped_root)}")
        # and the removal plant bites that wrapped copy: the sentence is gone and the measurement
        # says so. Removal on a wrapped text has to be done by offset — `str.replace` of the
        # amendment finds nothing in a wrapped sentence — which is exactly why the old plant was
        # vacuous.
        wrapped_removed_text = _remove_wrapped(wrapped_text, CADENCE_AMENDMENT)
        self.assertNotEqual(wrapped_removed_text, wrapped_text,
                            "the removal plant did not change the wrapped text, so it proves nothing")
        self.assertNotIn(CADENCE_AMENDMENT, _wrap_clean(wrapped_removed_text),
                         "the removal plant left a copy of the amendment in the wrapped text")
        wrapped_removed, wrapped_rm_gate = self.planted_copy()
        wrapped_rm_gate.write_file(wrapped_removed / "CONTRIBUTING.md", wrapped_removed_text)
        self.assert_bites(measure_cadence, wrapped_removed, "amendment verbatim",
                          "test_06 bite 1 (wrapped)")
        removed_text = _remove_wrapped(with_rule_text, CADENCE_AMENDMENT)
        self.assertNotEqual(removed_text, with_rule_text,
                            "the removal plant did not change the text, so it proves nothing")
        self.assertNotIn(CADENCE_AMENDMENT, " ".join(removed_text.split()),
                         "the removal plant left a copy of the amendment in the text")
        removed = self._plant_text("CONTRIBUTING.md", removed_text)
        self.assert_bites(measure_cadence, removed, "amendment verbatim", "test_06 bite 1")
        # bite 2: the release's own changelog entry claims a requirement moved. This holds whether or
        # not the entry also says it changed none: the contradiction is the defect.
        version = release_version(self.subject)

        def contradicting(t: str) -> str:
            m = re.search(rf"^#{{0,3}}\s*{re.escape(version)}\b", t, flags=re.M)
            entry = ("\n\nNo requirement changed.\n\n"
                     "**Breaking** (what a producer must change)\n- CL1-2: weakened.\n")
            if m is not None:
                # insert into the existing entry, before the next version heading
                rest = t[m.end():]
                nxt = re.search(r"^#{1,3}\s*\d+\.\d+\.\d+", rest, flags=re.M)
                cut = m.end() + (nxt.start() if nxt else len(rest))
                return t[:cut] + entry + t[cut:]
            # no entry yet: open one that both claims no requirement changed and lists one under
            # **Breaking**, so the plant exercises the contradiction rather than the absence
            return t.replace(
                "# Changelog\n",
                f"# Changelog\n\n## {version} (candidate)" + entry, 1)

        contradicted = self._edit("CHANGELOG.md", contradicting)
        self.assert_bites(measure_cadence, contradicted, "names a requirement under **Breaking**",
                          "test_06 bite 2")

    def test_07_contributing_names_v098_and_carries_no_token_count_py_reads(self):
        """GREEN at base: CONTRIBUTING.md at the base commit names the release its gap note explains,
        so no token of it is stale yet. Once the release is cut, that sentence cannot stay as typed if
        its token names another release, and it cannot be deleted either — the plant at the end of
        this case proves that direction bites, and another proves the CLAIM bites: a sentence saying
        THIS release shipped without a record is refused on a tree that has no note for it.
        """
        problems = measure_stale_stamp(self.subject)
        self.assertEqual(problems, [], "\n".join(problems))
        version = release_version(self.subject)

        # bite 1: the token removed by deleting the whole sentence that carries the fact.
        def drop_the_sentence(text: str) -> str:
            units = sentences(text)
            keep = [s for s in units if not carries_version_fact(s)]
            self.assertLess(len(keep), len(units), "the plant found no sentence stating the fact")
            return "\n\n".join(keep)

        deleted = self._edit("CONTRIBUTING.md", drop_the_sentence)
        self.assert_bites(measure_stale_stamp, deleted, "is gone", "test_07 bite 1")
        # bite 2: the paragraph DELETED rather than rewritten — the fact sentence goes with its
        # neighbours, which is a deletion of more than one sentence and must redden as one.
        def delete_the_paragraph(text: str) -> str:
            paras = text.split("\n\n")
            keep = [p for p in paras if not carries_version_fact(p)]
            self.assertLess(len(keep), len(paras), "the plant found no paragraph stating the fact")
            return "\n\n".join(keep)

        dropped = self._edit("CONTRIBUTING.md", delete_the_paragraph)
        self.assert_bites(measure_stale_stamp, dropped, "the sentence that explained", "test_07 bite 2")
        # bite 4: an HONEST rewrite — the token dropped, the fact and its citation kept, the release
        # named in words — must CLEAR the problem. Without this, a measurement that never returns []
        # would still satisfy every bite above and the case would be unsatisfiable by the fix it asks
        # for. The rewrite here is one a Maker could write: it is not the bar's private property.
        def honest_rewrite(text: str) -> str:
            out = []
            for para in text.split("\n\n"):
                if carries_version_fact(para):
                    # The sentence carries TWO bare tokens count.py reads: "Version 0.9.8" and the
                    # citation "RECORD-GAP-v0.9.8.md". The finding the brief names is exactly that
                    # neither can stay, so this rewrite removes both and keeps the fact and its
                    # reference, naming the release in words. It is the fix the case asks for, written
                    # the way a Maker would have to write it to satisfy count.py.
                    para = para.replace(f"Version {GAP_EXCEPTION_VERSION} shipped without one",
                                        "The release before this one shipped without one")
                    para = para.replace(
                        f"`record/RECORD-GAP-v{GAP_EXCEPTION_VERSION}.md`",
                        "the gap note in `record/`")
                out.append(para)
            return "\n\n".join(out)

        cleared = self._edit("CONTRIBUTING.md", honest_rewrite)
        self.assertEqual(measure_stale_stamp(cleared), [],
                         f"an honest rewrite — token dropped, fact and citation kept — still reddens "
                         f"this case: {measure_stale_stamp(cleared)}")
        # bite 5: and the same honest rewrite with a count.py-refused token put back reddens on the
        # token, which proves the token half of the case is alive on a tree that otherwise passes.
        planted_token = next(f"{VERSION_LINE_PREFIX}{n}" for n in range(1, 40)
                             if f"{VERSION_LINE_PREFIX}{n}" != version)
        restamped = self._plant_text("CONTRIBUTING.md",
                                     (cleared / "CONTRIBUTING.md").read_text(encoding="utf-8")
                                     + f"\n\nSee {planted_token}.\n")
        self.assert_bites(measure_stale_stamp, restamped, "still carries", "test_07 bite 5")

        # bite 5b — REASON 1, THE SPECIALIST'S SENTENCE. On a tree released PAST the exception, with
        # no gap note for that release, a sentence naming the release itself as the one that shipped
        # without a record is FALSE: this release ships a record. The old rule compared the sentence's
        # version token to the release's, so that exact sentence passed. Both spellings are planted —
        # with the version as a token, and with the release named in words — and both must be refused,
        # because count.py's token scanner is not what decides this claim.
        cut_v = f"{version.rsplit('.', 1)[0]}.{int(version.rsplit('.', 1)[1]) + 1}"
        claim_root, claim_gate = self.planted_copy()
        (claim_root / "SPEC.md").write_text(HEADER_RE.sub(
            lambda mm: mm.group(0).replace(mm.group("v"), cut_v),
            (claim_root / "SPEC.md").read_text(encoding="utf-8"), count=1), encoding="utf-8")
        self.assertFalse((claim_root / "record" / f"RECORD-GAP-v{cut_v}.md").exists(),
                         "precondition: no gap note for the planted release")
        # The substrate is the base commit's CONTRIBUTING.md, which ALWAYS carries the typed sentence
        # (the subject may already have been rewritten by the Maker, and then this plant would have
        # nothing to replace). The claim sentence is located by its own shape, not by its wording.
        base_claim_text = git_show(claim_root, BASE_COMMIT, "CONTRIBUTING.md")
        self.assertIsNotNone(base_claim_text, "cannot read the base CONTRIBUTING.md to plant against")
        assert base_claim_text is not None
        for label, sentence in (
                ("token", f"Version {cut_v} shipped without one — "
                          f"`record/RECORD-GAP-v{cut_v}.md` says why — and"),
                ("words", "This release shipped without one — the gap note in `record/` says why — and")):
            def plant(text: str, sentence=sentence) -> str:
                """The base text with its gap clause replaced by the false sentence."""
                m = re.search(r"[^.\n]*\bshipped without one\b[^\n]*?— and", text)
                self.assertIsNotNone(m, "the base sentence the claim lives in was not found")
                assert m is not None
                return text[:m.start()] + sentence + text[m.end():]
            claim_gate.write_file(claim_root / "CONTRIBUTING.md", plant(base_claim_text))
            planted_claim = (claim_root / "CONTRIBUTING.md").read_text(encoding="utf-8")
            self.assertIn(sentence, planted_claim,
                          f"precondition ({label}): the false sentence was not planted")
            got = measure_stale_stamp(claim_root)
            self.assertTrue(got,
                            f"on a tree declaring {cut_v} with no gap note, a sentence saying this "
                            f"release shipped without a record ({label}) was accepted: {got}. "
                            f"That sentence is false; a rule that accepts it measures the version in "
                            f"the sentence instead of the claim it makes")
            # Both plants name the release as the one that shipped without a record. The token plant
            # is caught by the token arm AND the claim arm; the words plant names the release with
            # no "Version X" phrase at all, so the arm that must catch it is the claim arm and not
            # count.py's scanner, which reads no bare token as "this release" in either spelling.
        # and the true form of the same sentence — the release BEFORE this one — is accepted, so the
        # case is satisfiable by the fix it asks for.
        claim_gate.write_file(claim_root / "CONTRIBUTING.md", honest_rewrite(base_claim_text))
        self.assertFalse([p for p in measure_stale_stamp(claim_root)
                          if "shipped without a record" in p],
                         f"the honest sentence was refused on a cut tree: "
                         f"{measure_stale_stamp(claim_root)}")

        # bite 6 — THE FINDING, MADE TO BITE. The brief's finding is that CONTRIBUTING.md:16's
        # sentence cannot be left as typed once the release is cut, because count.py reads ANY bare
        # 0.x.y in a current document and refuses it unless it equals the DECLARED release. On the
        # base tree the declared release IS the token's number, so measure_stale_stamp() correctly
        # returns [] here — the token is not stale yet. The finding only bites on a CUT tree. So cut
        # one: bump the header to a version the token does not equal, leave CONTRIBUTING.md exactly
        # as typed, and require BOTH the bar and count.py to refuse it. This is measured, not stated.
        next_v = f"{version.rsplit('.', 1)[0]}.{int(version.rsplit('.', 1)[1]) + 1}"
        cut_root, cut_gate = self.planted_copy()
        spec_text = (cut_root / "SPEC.md").read_text(encoding="utf-8")
        cut_gate.write_file(cut_root / "SPEC.md", HEADER_RE.sub(
            lambda mm: mm.group(0).replace(mm.group("v"), next_v), spec_text, count=1))
        # The sentence must be present AS TYPED for this plant to mean anything. It is present on the
        # un-cut tree, where the fact still carries the exception's version token. On a tree the Maker
        # has ALREADY cut that sentence correctly, there is nothing typed to leave alone — so the
        # plant puts the base commit's own sentence back, which is the same text the finding is about
        # and the same edit a Maker who had not done the work would have left on disk.
        left_as_typed = (cut_root / "CONTRIBUTING.md").read_text(encoding="utf-8")
        if f"v{GAP_EXCEPTION_VERSION}" not in left_as_typed:
            base_ct = git_show(cut_root, BASE_COMMIT, "CONTRIBUTING.md")
            if base_ct is None:
                self.fail("cannot read the base CONTRIBUTING.md, so the plant that restores the "
                          "typed sentence cannot be built")
            cut_gate.write_file(cut_root / "CONTRIBUTING.md", base_ct)
            left_as_typed = (cut_root / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn(f"v{GAP_EXCEPTION_VERSION}", left_as_typed,
                      "precondition: the sentence under test carries the exception's token")
        stale_after_cut = measure_stale_stamp(cut_root)
        self.assertTrue(any("still carries" in p for p in stale_after_cut),
                        f"on a tree declaring {next_v}, CONTRIBUTING.md left exactly as typed did "
                        f"not redden measure_stale_stamp(): {stale_after_cut}. The sentence's bare "
                        f"token is refused by count.py once it disagrees with SPEC.md, and this case "
                        f"must measure that, or the finding is only a sentence in a brief")
        # and count.py agrees: on the cut tree, left as typed, it reports the stale version token.
        code_cut, problems_cut, _ = count_problems(cut_root)
        stale_reports = [p for p in problems_cut if "in CONTRIBUTING.md disagrees with SPEC.md" in p]
        self.assertTrue(stale_reports,
                        f"count.py did not report CONTRIBUTING.md's stale token on the cut tree "
                        f"(declared {next_v}, exit {code_cut}): {problems_cut[:6]}. The bar's finding "
                        f"stands on count.py's scanner; if count.py does not report it, the finding "
                        f"is wrong and must be restated, not shipped")
        # bite 7 — the fix count.py accepts: rewrite the token out, and count.py's stale-token
        # report for CONTRIBUTING.md disappears. This proves the case asks for a reachable fix, not
        # an impossible one (the honest_rewrite above clears the bar; here count.py agrees).
        cut_gate.write_file(cut_root / "CONTRIBUTING.md", honest_rewrite(left_as_typed))
        _, problems_fixed, _ = count_problems(cut_root)
        self.assertFalse([p for p in problems_fixed
                          if "in CONTRIBUTING.md disagrees with SPEC.md" in p],
                         f"after the honest rewrite, count.py still reports CONTRIBUTING.md's token: "
                         f"{[p for p in problems_fixed if 'CONTRIBUTING' in p]}")

    def test_08_readme_contributing_draft_note_are_consistent(self):
        """GREEN at base. The cross-document arm, and what the base draft note's inventory looks like.

        DRAFT-NOTE.md is the hunk inventory of what THIS release touched. At the base commit it
        inventories the checker, the fixtures and the tools — paths this job freezes — so
        ``measure_draft_note_claims_frozen`` returns 41 claims on the untouched base tree. THE VERDICT
        ON A CUT TREE IS ZERO: once the release is cut, a note that still names a frozen path in its
        inventory is claiming a change this release did not make, and this case fails. Reporting a
        claim is not correcting it. An earlier revision accepted the report — it required the 41 to be
        reported and to agree between two measurements, so a DRAFT-NOTE bumped only in its version
        line, still carrying the base's whole 41-claim inventory, passed. That arm is gone.

        TWO SUBJECT STATES, BOTH MEASURED, NEITHER ASSUMED:

          * THE BASE TREE (this checkout before the release is cut). The note still carries the base's
            claims, so the case does NOT ask for zero here — it asks the opposite, and measures it:
            the note is byte-identical to ``git show <base>:DRAFT-NOTE.md``, the claims are reported,
            and the two measurements agree on how many. This is GREEN and is a reading of the base
            tree, not a verdict that a claim is acceptable: the same note on a cut tree fails below.
          * A CUT TREE (``release_version`` later than the base's). ``measure_draft_note_claims_frozen``
            must return ``[]`` and ``measure_document_consistency`` must report nothing at all. This
            is the verdict the Owner asked for, and the plant at the end of this case is the bump that
            used to pass.

        Bites, proved on copies of the subject: an inventory line naming a frozen path is reported; the
        same claim in prose (with a change verb) is reported; and a note that carries neither is
        accepted, so the hits are the claims and not the existence of the file.
        """
        version = release_version(self.subject)
        base_v, _ = base_version(self.subject)
        problems = measure_document_consistency(self.subject)
        claims_frozen = measure_draft_note_claims_frozen(self.subject)
        note_text = (self.subject / "DRAFT-NOTE.md").read_text(encoding="utf-8")
        self.assertTrue(note_text, "precondition: the draft note exists")
        if base_v is not None and version == base_v:
            # THE BASE TREE. The release has not been cut, so the note legitimately still describes
            # the base commit's change and carries its frozen-path inventory. The reading is measured
            # rather than skipped: the note is unchanged from the base, the claims are reported, and
            # the two measurements agree. A cut tree is required to carry none (below).
            base_note = git_show(self.subject, BASE_COMMIT, "DRAFT-NOTE.md")
            self.assertIsNotNone(base_note, "the subject cannot read its base DRAFT-NOTE.md, so this "
                                            "case cannot show the note is the base commit's")
            self.assertEqual(note_text, base_note,
                             "the note differs from the base commit's DRAFT-NOTE.md while the tree "
                             "still declares the base release; this arm measures an unchanged note")
            self.assertTrue(claims_frozen,
                            "the base DRAFT-NOTE.md is expected to carry the base commit's frozen-path "
                            "inventory, and measure_draft_note_claims_frozen() reported none: the "
                            "measurement is not reading the inventory it is pointed at")
            frozen = [p for p in problems
                      if "hunk inventory lists" in p or "claims this release changed" in p]
            self.assertEqual(len(frozen), len(claims_frozen),
                             f"the consistency measurement reported {len(frozen)} frozen claims "
                             f"where the note carries {len(claims_frozen)}")
        else:
            # A CUT TREE. THE VERDICT: ZERO.
            self.assertEqual(claims_frozen, [],
                             f"DRAFT-NOTE.md still claims this release touched "
                             f"{len(claims_frozen)} frozen path(s), and this release touches none of "
                             f"them. Reporting the claims is not correcting them. First: "
                             f"{claims_frozen[0] if claims_frozen else ''}")
            self.assertEqual(problems, [], "\n".join(problems))
        # BITE 1 — a hunk-inventory line naming a frozen path, added to the subject's own note. The
        # bite is proved on the same document the subject check reads: the appended line is the only
        # thing that changed, so a hit carries that line and nothing else could have produced it.
        clean = self.planted_copy()[0]
        note_text = (clean / "DRAFT-NOTE.md").read_text(encoding="utf-8")
        bled_note = note_text + "\n99. `" + FROZEN_PATHS[0] + "` (+3 -1) — a change this release did " \
                               "not make\n"
        (clean / "DRAFT-NOTE.md").write_text(bled_note, encoding="utf-8")
        hits = measure_draft_note_claims_frozen(clean)
        self.assertTrue(any(FROZEN_PATHS[0] in h and "a change this release did not make" in h
                            for h in hits),
                        f"a draft note claiming a hunk in {FROZEN_PATHS[0]} was not reported: {hits}")
        # BITE 2 — the same claim in PROSE rather than as an inventory row, and unbackticked: a note
        # that says in a sentence that it moved the checker is making the same claim.
        (clean / "DRAFT-NOTE.md").write_text(
            note_text + f"\nThis release also changes {FROZEN_PATHS[0]} and the fixtures.\n",
            encoding="utf-8")
        hits = measure_draft_note_claims_frozen(clean)
        self.assertTrue(any(FROZEN_PATHS[0] in h and "in prose" not in h for h in hits),
                        f"a draft note claiming a change to {FROZEN_PATHS[0]} in prose was not "
                        f"reported: {hits}")
        # and the measurement is not a constant: a note that carries none of these claims reports
        # none, so the hits above are the claims and not the fact that a file exists.
        self.assertEqual(measure_draft_note_claims_frozen(
            clean, text="# Draft Note — the release\n\nNothing under `record/` moved.\n"
                        "Only the documents named in the changelog moved.\n"), [])
        # BITE 3 — THE DEFECT, MADE TO BITE. A note bumped ONLY in its version line, still carrying
        # the whole frozen inventory, must fail on a cut tree. This is the plant the Owner measured:
        # on the earlier revision it passed, because the arm accepted "the claims are reported".
        # The plant is built by cutting the header (so the tree is a cut tree whatever the base is)
        # and rewriting only the note's TITLE line to the cut release, leaving the inventory as typed.
        cut_v = f"{version.rsplit('.', 1)[0]}.{int(version.rsplit('.', 1)[1]) + 1}"
        bump_root, bump_gate = self.planted_copy()
        spec_text = (bump_root / "SPEC.md").read_text(encoding="utf-8")
        bump_gate.write_file(bump_root / "SPEC.md", HEADER_RE.sub(
            lambda mm: mm.group(0).replace(mm.group("v"), cut_v), spec_text, count=1))
        bumped_note = re.sub(r"^#\s+Draft Note[^\n]*",
                             f"# Draft Note — v{cut_v} (candidate)",
                             git_show(self.subject, BASE_COMMIT, "DRAFT-NOTE.md"),
                             count=1, flags=re.M)
        self.assertNotEqual(bumped_note,
                            (bump_root / "DRAFT-NOTE.md").read_text(encoding="utf-8"),
                            "precondition: the note's title line was bumped")
        bump_gate.write_file(bump_root / "DRAFT-NOTE.md", bumped_note)
        bumped_claims = measure_draft_note_claims_frozen(bump_root)
        self.assertTrue(bumped_claims,
                        f"the bump-only note on a tree declaring {cut_v} reported no frozen claim, so "
                        f"this plant cannot show the zero verdict bites")
        self.assertTrue(measure_document_consistency(bump_root),
                        f"a DRAFT-NOTE bumped only in its version line, still carrying the base "
                        f"commit's frozen inventory, was accepted on a tree declaring {cut_v}: "
                        f"measure_document_consistency() returned []. Reporting a claim is not "
                        f"correcting it — the note must claim none.")
        # and the fix the case asks for is reachable: the same cut tree with a note that inventories
        # only what this release touches clears the frozen claim. Proved, so the case is satisfiable.
        cleared_note = ("# Draft Note — v" + cut_v + " (candidate)\n\n"
                        "## 1. Hunk inventory (N6)\n\n"
                        "1. `SPEC.md` (+1 -1) — the release's header\n"
                        "2. `CHANGELOG.md` (+4 -0) — the release's entry\n"
                        "3. `DRAFT-NOTE.md` (+2 -2) — this note\n")
        bump_gate.write_file(bump_root / "DRAFT-NOTE.md", cleared_note)
        self.assertEqual(measure_draft_note_claims_frozen(bump_root), [],
                         f"a note inventorying only the documents this release touches was refused: "
                         f"{measure_draft_note_claims_frozen(bump_root)}")

    def test_09_every_current_document_is_clean(self):
        """GREEN at base: no current document carries a non-release version token at the base commit
        beyond CONTRIBUTING.md's, which test_02 and test_07 measure, and every digest in
        ``examples/minimal/record.json`` matches the bytes of the file it names.

        Bites: a stale token planted into README.md; a second license name planted into NOTICE; and —
        the Owner's own plant — ``/subject/0/digest/sha256`` set to sixty-four zeros, which must be
        reported. Before this, that plant returned [] from ``measure_documents_clean``: the digests
        were named in prose and compared to nothing. The bar and the frozen checker are both required
        to catch it, and a digest naming a file that does not exist is required to be caught too.
        """
        problems = measure_documents_clean(self.subject)
        self.assertEqual(problems, [], "\n".join(problems))
        stale = f"{VERSION_LINE_PREFIX}q".replace("q", "1")
        planted = self._edit("README.md", lambda t: t + f"\n\nEarlier: {stale}.\n")
        self.assert_bites(measure_documents_clean, planted, f"names ['{stale}']",
                          "test_09 bite 1")
        licroot, gate = self.planted_copy()
        gate.write_file(licroot / "NOTICE", (licroot / "NOTICE").read_text(encoding="utf-8")
                        + "\nReleased under the MIT License.\n")
        self.assert_bites(measure_documents_clean, licroot, "names license MIT", "test_09 bite 2")
        # BITE 3 — a doctored subject digest. The plant is the Owner's: sixty-four zeros in
        # /subject/0/digest/sha256, and nothing else changed. It must be reported, and by BOTH the
        # direct comparison and the frozen checker.
        def zero_subject_digest(t: str) -> str:
            doc = json.loads(t)
            self.assertTrue(doc.get("subject"), "precondition: the example carries a subject")
            doc["subject"][0].setdefault("digest", {})["sha256"] = "0" * 64
            return json.dumps(doc, indent=2) + "\n"

        doctored = self._edit(EXAMPLE_RECORD, zero_subject_digest)
        self.assertEqual(json.loads((doctored / EXAMPLE_RECORD).read_text(encoding="utf-8"))
                         ["subject"][0]["digest"]["sha256"], "0" * 64,
                         "precondition: the doctored digest is on disk")
        digest_problems = measure_example_digests(doctored)
        self.assertTrue(any("subject[0]" in p and "00000000" in p for p in digest_problems),
                        f"a doctored /subject/0/digest/sha256 was not reported by the direct digest "
                        f"comparison: {digest_problems}. A digest nobody compares to bytes is "
                        f"decoration.")
        self.assert_bites(measure_documents_clean, doctored, "subject[0]", "test_09 bite 3")
        # the frozen checker, run over the same doctored record, must exit non-zero. This is the
        # other half: check_verdicts.py re-runs checker/check.py and the verdict drifts.
        dr = run([sys.executable, "tools/check_verdicts.py"], doctored)
        self.assertNotEqual(dr.returncode, 0,
                            f"tools/check_verdicts.py exited 0 on a record whose subject digest is "
                            f"sixty-four zeros; the frozen checker does not compare it: "
                            f"{(dr.stdout or '')[-300:]}")
        # BITE 4 — a digest whose file does not exist is a claim about nothing, and is reported.
        def name_a_missing_file(t: str) -> str:
            doc = json.loads(t)
            doc["subject"][0]["name"] = "no-such-file.md"
            return json.dumps(doc, indent=2) + "\n"

        missing = self._edit(EXAMPLE_RECORD, name_a_missing_file)
        self.assert_bites(measure_example_digests, missing, "does not exist",
                          "test_09 bite 4")


# ---------------------------------------------------------------------------------------------
# 10, 11, 13, 14: the Maker bar's controls. Each is GREEN at base and proves its own bite inside
# its own body. 12 and 12b are NOT here: they are the Instrument 2 arm, below, because a Maker
# cannot make them green and a bar no Maker can satisfy is not a Maker bar.
# ---------------------------------------------------------------------------------------------
class TestControls(BarBase):

    def test_10_footprint_the_bar_writes_only_inside_its_own_temp_root(self):
        """FOOTPRINT. A copy carries every file at identical bytes; a write through the gate lands and
        is recorded; a write to the SUBJECT is refused AND the subject's bytes do not move. The refused
        target is the subject on purpose: a gate that only refuses a path under its own parent proves
        nothing about the tree under measurement.

        This case is GREEN, and the plant that proves it is the permitted-write side: the gate's own
        write lands, the subject's does not."""
        tests_dir = self.subject / "tests"
        self.assertTrue(tests_dir.is_dir(), f"{tests_dir} is not a directory")
        tmp = Path(tempfile.mkdtemp(prefix="job35-foot-"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        # a gate rooted deep inside temp, whose root cannot contain the subject
        gate = WriteGate(tmp / "root" / "deep")
        (tmp / "root" / "deep").mkdir(parents=True)
        allowed = gate.write_file(tmp / "root" / "deep" / "planted.txt", "the bar wrote this\n")
        self.assertTrue(allowed.is_file(), "the gate's own write did not land")
        self.assertIn(allowed.resolve(), [p.resolve() for p in gate.written])
        target = tests_dir / "job35-footprint-plant.txt"
        self.assertFalse(target.exists(), f"{target} already exists; the control cannot prove a "
                                          f"refusal for a path that was already there")
        with self.assertRaises(PermissionError, msg=f"the gate did not refuse a write to the subject "
                                                    f"({target})"):
            gate.write_file(target, "must not land\n")
        self.assertFalse(target.exists(),
                         f"the gate raised, but {target} exists anyway: the refusal is a message with "
                         f"no effect behind it")
        self.assertNotIn(target.resolve(), [p.resolve() for p in gate.written],
                         "the gate recorded a write it refused")
        # and the copy's bytes are untouched by the control's own writes
        root, copy_gate = self.planted_copy()
        before = {p: sha256_file(p) for p in root.rglob("*")
                  if p.is_file() and "__pycache__" not in p.parts}
        self.assertTrue(before, "the copy is empty, so the footprint control measures nothing")
        copy_gate.write_file(root / "planted.txt", "the bar wrote this\n")
        moved = [str(p.relative_to(root)) for p, h in before.items() if sha256_file(p) != h]
        self.assertEqual(moved, [], f"the bar changed the copy's own files: {moved}")

    def test_11_bytes_move_no_stored_record_changes_while_the_bar_runs(self):
        """BYTES-MOVE. Every stored record under record/ has the same digest before and after a full
        pass of this bar; and a plant that rewrites one is caught by the same comparison."""
        recs = sorted((self.subject / "record").glob("*.json"))
        self.assertTrue(recs, "no stored records to measure: this control measured nothing")
        before = {p: sha256_file(p) for p in recs}
        for fn in (measure_release_lands, measure_header, measure_count_except_record,
                   measure_count_maker_problems, measure_examples, measure_spec_change,
                   measure_cadence, measure_cadence_claim_only, measure_stale_stamp,
                   measure_document_consistency, measure_documents_clean):
            fn(self.subject)
        moved = [str(p.relative_to(self.subject)) for p, h in before.items() if sha256_file(p) != h]
        self.assertEqual(moved, [], f"a stored record's bytes moved while the bar ran: {moved}")
        root, gate = self.planted_copy()
        planted = sorted((root / "record").glob("*.json"))
        digest = sha256_file(planted[0])
        gate.write_file(planted[0], planted[0].read_text(encoding="utf-8") + " ")
        self.assertNotEqual(sha256_file(planted[0]), digest,
                            "case 11 did not bite: a rewritten record hashed the same")


    def test_13_every_green_at_base_case_bites(self):
        """GREEN at base. The controls that remain GREEN at base are run here against a plant, and the
        plant must redden the very function that case calls. A green case whose plant stops biting
        fails this case. (test_00 is the release gate and is the one case that is RED at base, so it
        is not in this set; its bites are asserted inside test_00 itself.)"""
        # 09 -> two bites, asserted in test_09.
        # 10 -> footprint, asserted in test_10.
        # 11 -> bytes-move, asserted in test_11.
        # 14 -> version-from-document, asserted in test_14.
        # This case's own added bite, and it is the one that catches a green case gone vacuous: every
        # measurement function must NAME a tree that is not the subject. A function that returns []
        # for an empty directory, or raises on a missing file, is not measuring the tree it is given.
        tmp = Path(tempfile.mkdtemp(prefix="job35-empty-"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        empty = tmp / "tree"
        empty.mkdir()
        (empty / "SPEC.md").write_text("nothing here\n", encoding="utf-8")
        (empty / "CONTRIBUTING.md").write_text("", encoding="utf-8")
        (empty / "README.md").write_text("", encoding="utf-8")
        (empty / "DRAFT-NOTE.md").write_text("", encoding="utf-8")
        (empty / "CHANGELOG.md").write_text("", encoding="utf-8")
        for fn, needle, raises in ((measure_release_lands, "no `**Version X.Y.Z", AssertionError),
                                   (measure_header, "no `**Version", AssertionError),
                                   (measure_examples, "missing", AssertionError),
                                   (measure_documents_clean, "missing", AssertionError)):
            with self.subTest(fn=fn.__name__):
                try:
                    out = fn(empty)
                except raises:
                    continue  # a measurement that refuses an unusable tree is measuring it
                self.assertTrue(any(needle in p for p in out),
                                f"{fn.__name__} on a tree with no content returned {out!r}, which "
                                f"does not name {needle!r}: it does not measure the tree it is given")
        # count_problems() must not report "no problems" for a tree with no count.py in it.
        code, problems, err = count_problems(empty)
        self.assertNotEqual(code, 0, "count.py on a tree that has no count.py exited 0")
        self.assertTrue(err.strip(), "count.py on a tree that has no count.py produced no error to "
                                     "report, so count_problems() cannot tell 'no problems' from "
                                     "'no run'")
        # the live plants for the greens, asserted through the same helper every case uses
        stale = f"{VERSION_LINE_PREFIX}v".replace("v", "7")
        self.assert_bites(measure_documents_clean,
                          self._edit("README.md", lambda t: t + f"\n\nEarlier: {stale}.\n"),
                          f"names ['{stale}']", "test_13 :: 09")

    def test_14_the_version_is_read_from_the_document_and_never_from_a_flag(self):
        """D2/E1. GREEN. This file carries no version-shaped literal outside its docstring prose and no
        spec-version flag; release_version() follows a planted header."""
        source = Path(__file__).read_text(encoding="utf-8")
        body = source.split('"""', 2)[2]           # skip the module docstring
        stamps = sorted({m for m in re.findall(r"\b0\.\d+\.\d+\b", body)
                     if m != GAP_EXCEPTION_VERSION})
        self.assertEqual(stamps, [], f"this bar carries version literals {stamps}; the release's "
                                 f"version must come from SPEC.md")
        # The flag check reads the source's CODE, not its prose: `#` comments are stripped, the module
        # docstring is already excluded (it is `body`), and run()'s one pass-through of os.environ is
        # whitelisted by its exact line because it chooses nothing that is measured. Every other
        # environment or argv read is a finding.
        code_only = "\n".join(re.sub(r"#.*$", "", ln) for ln in body.splitlines())
        flag_uses = [ln for ln in re.findall(
        r"^[^\n]*?(?:os\.environ|\benviron\s*[\[(]|\bsys\.argv\b|\bargv\b\s*\[)[^\n]*$",
        code_only, flags=re.M) if 'PYTHONDONTWRITEBYTECODE="1")' not in ln]
        self.assertEqual(flag_uses, [],
                     f"this bar reads the environment or argv: {flag_uses[:2]}")
        other = "9.8.7"
        planted = self._edit("SPEC.md", lambda t: HEADER_RE.sub(
        f"**Version {other} · candidate · 2026-12-01**", t, count=1))
        self.assertEqual(release_version(planted), other,
                     "case 14 did not bite: release_version() ignored the planted header")


# ---------------------------------------------------------------------------------------------
# INSTRUMENT 2 — the record arm. NOT part of the Maker bar.
#
# THE RUN, performed by the Orchestrator's release gate and NOT by a Maker. It is run from inside
# `tests/`, by MODULE name, because `tests/` has no `__init__.py` and so is not importable as a
# package from the repository root. Measured 2026-11-11:
#
#     cd tests && python3 -m unittest test_v099_instrument1.Instrument2Sequencing -v
#       -> Ran 2 tests, FAILED (failures=2)
#
# (`python3 -m unittest tests.test_v099_instrument1.Instrument2Sequencing -v` from the root does NOT
# run it: `No module named 'tests.test_v099_instrument1'`. Nor does `-m unittest
# tests/test_v099_instrument1.py`, which runs 1 test and errors. The command above is the one that
# works, and it is the one stated.)
#
# It cannot be collected by accident: the class is `Instrument2Sequencing`, which does not begin with
# `Test`, so neither `discover` nor `python3 tests/test_v099_instrument1.py` picks it up, and
# `load_tests` below drops it a second time for runners that ignore the naming rule. Measured: the
# Maker command runs 14 cases and neither case here.
#
# THE MOVE, AND WHY IT IS A MOVE AND NOT A DELETION. tests 12/12b asserted the sequencing — a
# documents-only tree past GAP_EXCEPTIONS cannot be count.py green, and the record problem is
# Instrument 2's. That sequencing is an Orchestrator's gate over a record that EXISTS; it is not a
# property of the release documents. In the Maker bar it was red at base and red after the work,
# which is a bar no Maker can turn green. So it is carried here, on the release gate each artifact
# is judged under, and the Maker bar is satisfiable by the Maker alone.
#
# The two cases keep their names (`test_12`, `test_12b`): that is what the packet's controls and the
# earlier readings call them, and renaming them would make an old reading name a case that no longer
# exists. They are not prefixed `instrument2_` — nothing in this file is, and the name is not what
# keeps them out of the Maker's run; the class name and `load_tests` are.
#
# VERDICT AT BASE, measured 2026-11-11 by the command above: 2 cases, both FAIL, `FAILED (failures=2)`.
# Both fail on the same opening assertion, because SPEC.md declares 0.9.8, which IS count.py's
# GAP_EXCEPTIONS release, so neither has a subject yet. That is "not applicable yet", not "the release
# is unfinished", and neither case is skipped — a skip in a gate reads as a pass. Once SPEC.md declares
# a release outside GAP_EXCEPTIONS, each case measures the subject rather than the assertion, and each
# has a stated reason it can be red or green.
# ---------------------------------------------------------------------------------------------

class Instrument2Sequencing(BarBase):
    """Instrument 2. Run explicitly by name; never collected by the Maker bar.

    `load_tests` below drops this class from the default suite and the class name does not begin with
    `Test`, so neither ``python3 -m unittest discover`` nor ``python3 tests/test_v099_instrument1.py``
    can pick up its two cases: ``test_12`` and ``test_12b``. The Orchestrator runs them by name with
    the command in the block above.
    """

    def test_12_a_documents_only_tree_cannot_be_count_py_green(self):
        """RED at base, and NOT IN THE MAKER SUITE: this case is not collected by ``load_tests``.

        VERDICT, measured: RED at base, when run by name —
        ``python3 -m unittest test_v099_instrument1.Instrument2Sequencing`` (from ``tests/``)
        runs 2 cases and reports ``FAILED (failures=2)``. This case is one of the two. It is
        NOT collected by ``python3 tests/test_v099_instrument1.py`` or by ``discover``: the
        class is ``Instrument2Sequencing`` and ``load_tests`` below drops it, so a reader of the
        Maker's run sees 14 cases and neither this one nor 12b.

        THE RED IS "NOT APPLICABLE YET", NOT "THE RELEASE IS UNFINISHED". The case opens with
        ``assertNotEqual(version, GAP_EXCEPTION_VERSION)``. At base SPEC.md declares 0.9.8,
        which IS ``GAP_EXCEPTIONS`` (tools/count.py:44), so the assertion fires on
        ``'0.9.8' == '0.9.8'`` and none of the four measurements below runs. A release that is
        merely un-cut does not turn this case green: only a declared version OUTSIDE
        ``GAP_EXCEPTIONS`` does, and then the plants below become the subject.

        What it still measures once that version has moved (the reason it is kept, and the
        reason it is not a skip — a skip in a gate reads as a pass): on planted copies of the
        subject at that version,

          * a copy for a release PAST ``GAP_EXCEPTIONS`` with no record and no gap note ->
            count.py reports the record problem. No edit to the documents closes it, because the
            only documents-only way to a green (a gap note) is refused for that version.
          * the same copy WITH a gap note -> count.py reports gap-not-permitted. A gap note is not
            a way out either.
          * a record AND a gap note -> the gap is still refused (tools/count.py:124's glob is not
            gated on the record's absence).
          * the record present -> the record problem is gone. This is Instrument 2's own file.

        Which of those it reports depends on the version, and this docstring does not claim a
        verdict it has not measured: at base all four are unreachable because the first
        assertion fires. Once SPEC.md declares a version outside ``GAP_EXCEPTIONS``, the cases
        above are the subject's own release and this case is expected GREEN — but that has not
        been observed, because no such tree exists in this job yet.
        """
        version = release_version(self.subject)
        self.assertNotEqual(version, GAP_EXCEPTION_VERSION,
                            f"NOT APPLICABLE YET — SPEC.md declares {version}, which is count.py's own "
                            f"GAP_EXCEPTIONS release (tools/count.py:44). A documents-only tree for "
                            f"this release is count.py green through the exception, not through a "
                            f"record, so there is no crux here to measure. This arm is red until the "
                            f"release has moved past the exception; it is not skipped, because a skip "
                            f"in a gate reads as a pass.")
        rec_rel = Path("record") / f"custody-v{version}.json"
        gap_rel = Path("record") / f"RECORD-GAP-v{version}.md"
        # A — documents only, no record and no gap note.
        a_root, _ = self.planted_copy()
        for rel in (rec_rel, gap_rel):
            if (a_root / rel).exists():
                (a_root / rel).unlink()
        code_a, problems_a, _ = count_problems(a_root)
        parts_a = partition_count(problems_a, version)
        self.assertNotEqual(code_a, 0,
                            f"a documents-only copy declaring {version} exited 0; the sequencing this "
                            f"arm asserts is not what count.py does")
        self.assertEqual(len(parts_a["record"]), 1,
                         f"a documents-only copy declaring {version} did not report the record "
                         f"problem: {parts_a}")
        # B — a gap note alone: refused, so a gap note is not a documents-only way out.
        b_root, b_gate = self.planted_copy()
        if (b_root / rec_rel).exists():
            (b_root / rec_rel).unlink()
        b_gate.write_file(b_root / gap_rel, "# a gap\n\nplanted by the release gate\n")
        code_b, problems_b, _ = count_problems(b_root)
        self.assertNotEqual(code_b, 0, f"a copy declaring {version} with a gap note exited 0")
        self.assertTrue(partition_count(problems_b, version)["gap"],
                        f"the gap note for {version} was not refused: {problems_b}")
        # C — record AND gap note: the gap is still refused.
        c_root, c_gate = self.planted_copy()
        c_gate.write_file(c_root / rec_rel, json.dumps(
            {"_type": "https://in-toto.io/Statement/v1",
             "predicateType": "https://evaluatordriven.com/custody/v1",
             "predicate": {"specVersion": version}}))
        c_gate.write_file(c_root / gap_rel, "# a gap\n\nplanted by the release gate\n")
        code_c, problems_c, _ = count_problems(c_root)
        self.assertNotEqual(code_c, 0, "a copy with a record AND a gap note exited 0")
        self.assertTrue(partition_count(problems_c, version)["gap"],
                        f"count.py admits a gap note even when a record is present: {problems_c}. "
                        f"tools/count.py:124's glob is not gated on the record's absence, and this "
                        f"plant says so.")
        # D — the record present: the record problem is gone. This is Instrument 2's own file.
        d_root, d_gate = self.planted_copy()
        d_gate.write_file(d_root / rec_rel, json.dumps(
            {"_type": "https://in-toto.io/Statement/v1",
             "predicateType": "https://evaluatordriven.com/custody/v1",
             "predicate": {"specVersion": version}}))
        _, problems_d, _ = count_problems(d_root)
        self.assertEqual(partition_count(problems_d, version)["record"], [],
                         f"a copy carrying record/{rec_rel.name} still reported the record problem: "
                         f"{problems_d}")

    def test_12b_the_release_gate_the_record_closes(self):
        """RED at base, and NOT IN THE MAKER SUITE: this case is not collected by ``load_tests``.

        VERDICT, measured: RED at base, when run by name — the same
        ``test_v099_instrument1.Instrument2Sequencing`` run that reports
        ``FAILED (failures=2)`` over 2 cases. It is not collected by
        ``python3 tests/test_v099_instrument1.py``, so the Maker's 14-case run does not include
        it and this case cannot turn that run red or green.

        THE RED IS "NOT APPLICABLE YET". The case opens with
        ``assertNotEqual(version, GAP_EXCEPTION_VERSION)``; at base SPEC.md declares 0.9.8, which
        IS ``GAP_EXCEPTIONS`` (tools/count.py:44), so it fires on ``'0.9.8' == '0.9.8'`` before the
        record is ever read. It is therefore NOT "red until the record exists": a subject that
        has a record but still declares a ``GAP_EXCEPTIONS`` version stays red here, and a
        subject that declares a later version with no record is green on the version check and
        then fails further down. Both readings are distinct from the claim this docstring used
        to make.

        What it still measures once the declared version is outside ``GAP_EXCEPTIONS`` — the
        Instrument 2 gate, and not a Maker failure: Instrument 1's own count.py gate
        (test_02/test_03) already requires that no problem the MAKER owns remains. What is left
        after the Maker is done, if anything, is the record problem, and that is this arm's
        subject: it fails naming that problem as Instrument 2's gate while the record is missing,
        and passes when `kit/emit_custody.py`'s record is on disk.
        """
        version = release_version(self.subject)
        self.assertNotEqual(version, GAP_EXCEPTION_VERSION,
                            f"NOT APPLICABLE YET — SPEC.md declares {version}, the GAP_EXCEPTIONS "
                            f"release (tools/count.py:44); count.py is green on it through the "
                            f"exception, so the record gate has nothing to close. Red until the "
                            f"release moves past the exception; not skipped, because a skip in a "
                            f"gate reads as a pass.")
        code, problems, err = count_problems(self.subject)
        if not problems and code != 0:
            self.fail(f"tools/count.py exited {code} with no parseable problem list: {err[:300]}")
        parts = partition_count(problems, version)
        maker = parts["stale"] + parts["gap"] + parts["rest"]
        self.assertEqual(maker, [],
                         f"INSTRUMENT 1 HAS NOT PASSED — these are Maker problems, and this arm "
                         f"does not stand in for the Maker bar: {maker}")
        if parts["record"]:
            self.fail(
                f"INSTRUMENT 2 GATE (not a Maker failure): count.py reports "
                f"{parts['record'][0]!r}. On a frozen count.py (tools/count.py:44 "
                f"GAP_EXCEPTIONS = {{\"{GAP_EXCEPTION_VERSION}\"}}) this release cannot be "
                f"count.py green until record/custody-v{version}.json exists, and that "
                f"record is Instrument 2's output — the Orchestrator's kit/emit_custody.py "
                f"over the job's log. No edit to the documents closes it, and a RECORD-GAP "
                f"note for {version} is refused by tools/count.py:124-128.")
        self.assertEqual(code, 0, "count.py still reports problems this arm did not classify")
        rec = self.subject / "record" / f"custody-v{version}.json"
        self.assertTrue(rec.is_file(),
                        f"count.py is green but record/{rec.name} does not exist, so the green did "
                        f"not come from a record")


def load_tests(loader, standard_tests, pattern):
    """The Maker's suite: everything except Instrument 2.

    unittest.main() defaults ``pattern`` to ``test*.py`` and collects every ``TestCase`` subclass in
    this module, which would sweep the Instrument 2 arm into the Maker's command. This function
    removes it explicitly, so the split does not depend on which runner is used. Instrument 2 is run
    by name (see its class docstring); a run of it by name goes through the class, not through here.
    """
    standard_tests = standard_tests or loader.loadTestsFromModule(sys.modules[__name__])
    keep = unittest.TestSuite()
    for group in standard_tests:
        cases = [t for t in group if type(t).__name__ != "Instrument2Sequencing"]
        if not cases:
            continue
        if isinstance(group, unittest.TestSuite):
            # keep the suite's own type so its cases still run (a bespoke suite class may filter,
            # and re-wrapping with a plain constructor drops them silently)
            group._tests = cases
            keep.addTest(group)
        else:
            keep.addTest(cases[0])
    return keep


if __name__ == "__main__":
    unittest.main(verbosity=2)
