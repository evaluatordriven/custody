#!/usr/bin/env python3
"""Check a plain-language document against the v0.9.3 reading target (non-normative tooling).

    python3 tools/readability.py [FILE.md ...]        default: docs/REVIEWERS-GUIDE.md

The target, from the Owner's measurement of the site:
  Flesch-Kincaid grade <= 8 · Flesch Reading Ease >= 60 · average sentence <= 15 words ·
  no sentence over 30 words · every listed term explained the first time it appears, and never used
  before that.

Method, so the numbers can be checked:
  - Prose only: headings, code blocks, tables and HTML comments are left out. Paragraphs, list items and
    block quotes are kept, and Markdown markup is removed (links keep their words).
  - Sentences are split on . ! ? WITHIN each paragraph or list item, never across a joined text.
  - Syllables come from textstat 0.7.13 (the measurement's own instrument); the grade and ease formulas
    are the standard Flesch-Kincaid ones, applied to those sentences.
  - A term is explained ("glossed") if, within 40 characters after its first use, there is an em dash, a
    colon, an opening parenthesis, "means", or "is a" (or "is an"): the measurement's own rule. Plurals
    count as uses.
Prints a JSON report; exits 1 if any rule fails.
"""
import json
import pathlib
import re
import sys

import textstat

ROOT = pathlib.Path(__file__).resolve().parent.parent
TERMS = ["artifact", "bar", "buyer", "check", "custody", "delegation", "dimension", "disposition",
         "evaluator", "gate", "handoff", "instrument", "level", "maker", "published", "record",
         "signature", "specialist", "specification", "threshold"]
PLURAL = {t: (t if t in ("published", "custody") else t + "s") for t in TERMS}
GLOSS = re.compile(r"^.{0,40}?(—|:|\(|\bmeans\b|\bis an?\b)", re.S)


def blocks(md):
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    md = re.sub(r"```.*?```", "", md, flags=re.S)
    out, cur = [], []
    for line in md.splitlines() + [""]:
        s = line.strip()
        new_item = re.match(r"^([-*+]|\d+\.)\s+", s)
        if not s or s.startswith("#") or s.startswith("|") or new_item:
            if cur:
                out.append(" ".join(cur))
            cur = [re.sub(r"^([-*+]|\d+\.)\s+", "", s)] if new_item else []
            continue
        cur.append(re.sub(r"^>\s?", "", s))
    return [plain(b) for b in out if b.strip()]


def plain(text):
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return re.sub(r"[*_`]", "", text).strip()


def sentences(block):
    parts = re.split(r"(?<=[.!?])[\"”’)]?\s+(?=[A-Z0-9\"“(])", block)
    return [p for p in (x.strip() for x in parts) if re.search(r"\w", p)]


def words(sentence):
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'’.-]*", sentence)


def check(path):
    md = path.read_text(encoding="utf-8")
    bl = blocks(md)
    sents = [s for b in bl for s in sentences(b)]
    lens = [len(words(s)) for s in sents]
    n_words = sum(lens)
    syll = sum(textstat.syllable_count(w) for s in sents for w in words(s))
    wps, spw = n_words / max(len(sents), 1), syll / max(n_words, 1)
    fk, ease = 0.39 * wps + 11.8 * spw - 15.59, 206.835 - 1.015 * wps - 84.6 * spw
    problems = []
    if fk > 8:
        problems.append(f"Flesch-Kincaid grade {fk:.1f} > 8")
    if ease < 60:
        problems.append(f"Reading Ease {ease:.1f} < 60")
    if wps > 15:
        problems.append(f"average sentence {wps:.1f} words > 15")
    for s, n in zip(sents, lens):
        if n > 30:
            problems.append(f"sentence of {n} words > 30: {s[:70]}…")
    prose = "\n".join(bl)
    unglossed = []
    for t in TERMS:
        m = re.search(rf"\b({re.escape(t)}|{re.escape(PLURAL[t])})\b", prose, flags=re.I)
        if m and not GLOSS.match(prose[m.end():]):
            unglossed.append(t)
            problems.append(f"term '{t}' first used without an explanation: …{prose[m.start():m.end() + 50]}…")
    report = {"file": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
              "fleschKincaid": round(fk, 1), "readingEase": round(ease, 1),
              "averageSentence": round(wps, 1), "longestSentence": max(lens, default=0),
              "sentences": len(sents), "words": n_words,
              "termsUsed": sum(1 for t in TERMS if re.search(rf"\b({t}|{PLURAL[t]})\b", prose, re.I)),
              "termsUnglossed": unglossed}
    return report, problems


def main():
    files = [pathlib.Path(a) for a in sys.argv[1:]] or [ROOT / "docs" / "REVIEWERS-GUIDE.md"]
    out, bad = [], []
    for f in files:
        report, problems = check(f.resolve())
        out.append(dict(report, problems=problems))
        bad += problems
    print(json.dumps(out, indent=2))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
