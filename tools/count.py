#!/usr/bin/env python3
"""Mechanical checks on this repository itself. Standard library only. Exit 1 on any violation.

  sizes        normative words <= 4,500; MUST / MUST NOT / REQUIRED / SHALL / SHALL NOT <= 20;
               terms in SPEC.md section 2 <= 12; checker <= 300 non-blank, non-comment lines,
               none over 100 characters
  keywords     upper-case BCP 14 key words appear only in SPEC.md sections marked (normative)
  one home     no term from the Terms table is defined in a second file
  evidence     every requirement row in SPEC.md section 5 has the class structural, semantic or
               external; each structural or semantic requirement is failed by at least one fixture
               in fixtures/expected.json; at most 5 requirements are external (D7)
  agreement    version, levels, outcomes and disposition states agree across SPEC.md, the schema,
               the checker, README.md and every other current document (files under record/ are
               kept records of earlier work, so they may name earlier versions), and any record in
               record/; README.md claims no level that no record in record/ supports; the
               documents' statements of how many reference checkers exist match checker/; LICENSE carries CC BY 4.0
               and LICENSE-CODE carries Apache-2.0, each naming no other license; and every current
               document and NOTICE name only those two

Counting rules. Normative text = SPEC.md sections whose heading carries "(normative)", minus fenced
code blocks; tables count. Words = whitespace-separated tokens. Key words are counted as written,
including the BCP 14 boilerplate sentence; "MUST NOT" counts once, not as MUST plus MUST NOT.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEYS = r"\b(MUST NOT|MUST|REQUIRED|SHALL NOT|SHALL|SHOULD NOT|SHOULD|RECOMMENDED|MAY|OPTIONAL)\b"
STRONG = {"MUST NOT", "MUST", "REQUIRED", "SHALL NOT", "SHALL"}


def sections(text):
    """Yield (heading, body) for each '## ' section, with fenced code removed."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    parts = re.split(r"^(## .*)$", text, flags=re.M)
    return list(zip(parts[1::2], parts[2::2]))


def main():
    problems, report = [], {}
    spec = (ROOT / "SPEC.md").read_text(encoding="utf-8")
    secs = sections(spec)
    normative = [b for h, b in secs if "(normative)" in h]
    words = sum(len(b.split()) for b in normative)
    strong = [k for b in normative for k in re.findall(KEYS, b) if k in STRONG]
    terms_body = next(b for h, b in secs if h.startswith("## 2."))
    terms = re.findall(r"^\| \*\*([a-z ]+)\*\* \|", terms_body, flags=re.M)
    checker = (ROOT / "checker" / "check.py").read_text(encoding="utf-8").splitlines()
    logical = [ln for ln in checker if ln.strip() and not ln.strip().startswith("#")]
    report["sizes"] = {"normative words": words, "strong key words": len(strong),
                       "terms": len(terms), "checker lines": len(logical),
                       "longest checker line": max(map(len, checker))}
    for name, value, limit in (("normative words", words, 4500), ("strong key words", len(strong), 20),
                               ("terms", len(terms), 12), ("checker lines", len(logical), 300),
                               ("longest checker line", max(map(len, checker)), 100)):
        if value > limit:
            problems.append(f"{name}: {value} > {limit}")

    rows = re.findall(r"^\| ((?:CR|CL\d|BL)-\d+) \|.*\| *([^|]*?) *\|\s*$", spec, flags=re.M)
    failed = {v.get("fails") for v in json.loads(
        (ROOT / "fixtures" / "expected.json").read_text())["cases"].values()}
    for rid, cls in rows:
        if cls not in ("structural", "semantic", "external"):
            problems.append(f"{rid} has no valid class ({cls!r}): no evidence path")
        elif cls != "external" and rid not in failed:
            problems.append(f"{rid} is {cls} but no fixture fails for it")
    external = [rid for rid, cls in rows if cls == "external"]
    report["evidence"] = {"requirements": len(rows), "external": len(external)}
    if len(external) > 5:
        problems.append(f"{len(external)} external requirements > 5")

    md = [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]
    for path in md:
        text = path.read_text(encoding="utf-8")
        bodies = [b for h, b in sections(text) if not (path.name == "SPEC.md" and "(normative)" in h)]
        if path.name != "SPEC.md":
            bodies = [re.sub(r"```.*?```", "", text, flags=re.S)]
        for body in bodies:
            for k in set(re.findall(KEYS, body)):
                problems.append(f"keyword {k} outside SPEC.md normative text: {path.relative_to(ROOT)}")
        if path.name != "SPEC.md":
            for t in terms:
                if re.search(rf"^\s*[|*-]*\s*\*\*{re.escape(t)}\*\*\s*[|:—-]", text, flags=re.M | re.I):
                    problems.append(f"term '{t}' defined again in {path.relative_to(ROOT)}")

    version = re.search(r"\*\*Version (\d+\.\d+\.\d+)", spec).group(1)
    schema = json.loads((ROOT / "schema" / "custody-v1.schema.json").read_text())
    pred = schema["$defs"]["predicate"]["properties"]
    want = {"levels": set(pred["levelClaimed"]["enum"]), "outcomes": set(schema["$defs"]["outcome"]["enum"]),
            "states": set(pred["disposition"]["properties"]["state"]["enum"])}
    import importlib.util
    spec_mod = importlib.util.spec_from_file_location("check", ROOT / "checker" / "check.py")
    check = importlib.util.module_from_spec(spec_mod)
    spec_mod.loader.exec_module(check)
    have = {"levels": check.ENUMS["levelClaimed"], "outcomes": check.OUTCOMES,
            "states": check.ENUMS["state"]}
    for key in want:
        if want[key] != set(have[key]):
            problems.append(f"{key} differ between schema and checker: {want[key]} vs {have[key]}")
        missing = [v for v in want[key] if f"`{v}`" not in spec and v not in spec]
        if missing:
            problems.append(f"{key} missing from SPEC.md: {missing}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    current = [p for p in md if "record" not in p.relative_to(ROOT).parts[:1]  # records, and the
               and p.name != "CHANGELOG.md"]  # changelog, are history: they name earlier versions
    for path in current + [ROOT / "schema" / "custody-v1.schema.json"]:
        for v in set(re.findall(r"\b[vV]?(0\.\d+\.\d+)\b", path.read_text(encoding="utf-8"))):
            if v != version:
                problems.append(f"version {v} in {path.relative_to(ROOT)} disagrees with SPEC.md {version}")
    recorded = set()
    for rec in sorted((ROOT / "record").glob("*.json")) if (ROOT / "record").is_dir() else []:
        pred = json.loads(rec.read_text()).get("predicate", {})
        if pred.get("specVersion") != version:
            problems.append(f"{rec.name} specVersion {pred.get('specVersion')} != {version}")
        level = pred.get("levelClaimed")
        recorded.add(level)
        if level and f"claims {level}" not in readme:
            problems.append(f"README.md does not state the record's claimed level ({level})")
    for level in set(re.findall(r"claims (CL[123]|baseline)\b", readme)) - recorded:
        problems.append(f"README.md claims {level} but no record in record/ claims it")

    # Self-state: what the documents say this repository contains must match what it contains.
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
             "nine": 9, "ten": 10}
    checkers = len([f for f in (ROOT / "checker").glob("*.py") if f.name != "__init__.py"])
    for name, text in (("SPEC.md", spec), ("README.md", readme)):
        for n in re.findall(r"\b(\w+) reference checkers? exists?\b", text, flags=re.I):
            claimed = words.get(n.lower(), int(n) if n.isdigit() else None)
            if claimed != checkers:
                problems.append(f"{name} says {n} reference checker(s) exist; checker/ holds "
                                f"{checkers}")

    # Licenses: the license files carry what the documents say, and nothing else (v0.9.3 S5).
    known = {"CC BY 4.0": r"CC[ -]BY[ -]4\.0|Creative Commons Attribution 4\.0",
             "Apache-2.0": r"Apache[ -](?:License,? Version )?2\.0|Apache License",
             "MIT": r"\bMIT\b", "GPL": r"\bA?GPL", "BSD": r"\bBSD\b", "MPL": r"\bMPL",
             "CC0": r"\bCC0\b", "CC BY-SA": r"CC[ -]BY[ -]SA|Attribution-ShareAlike",
             "CC BY-NC": r"CC[ -]BY[ -]NC|NonCommercial", "Unlicense": r"\bUnlicense\b"}
    lic_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    lic_code = (ROOT / "LICENSE-CODE").read_text(encoding="utf-8")
    text_lic, code_lic = "CC BY 4.0", "Apache-2.0"
    for name, body, own, need in (("LICENSE", lic_text, text_lic, (r"Creative Commons Attribution 4\.0",
                                                                     r"CC BY 4\.0")),
                                  ("LICENSE-CODE", lic_code, code_lic, (r"Apache License",
                                                                        r"Version 2\.0"))):
        for pat in need:
            if not re.search(pat, body):
                problems.append(f"{name} does not carry {own} (missing '{pat.replace(chr(92), '')}')")
        for lic, pat in known.items():  # LICENSE may point to the code license, nothing else
            if lic != own and not (name == "LICENSE" and lic == code_lic) and re.search(pat, body):
                problems.append(f"{name} names license {lic}; it should carry only {own}")
    allowed = {text_lic, code_lic}
    for path in current + [ROOT / "NOTICE"]:
        body = path.read_text(encoding="utf-8")
        for lic, pat in known.items():
            if lic not in allowed and re.search(pat, body):
                problems.append(f"{path.relative_to(ROOT)} names license {lic}; this repository "
                                f"carries {text_lic} (text) and {code_lic} (code)")
    for path in (ROOT / "README.md", ROOT / "NOTICE", ROOT / "LICENSE"):
        body = path.read_text(encoding="utf-8")
        if not re.search(r"(?is)code.{0,150}?(?:" + known[code_lic] + ")", body):
            problems.append(f"{path.name} does not say the code is {code_lic}")
        if not re.search(r"(?is)(text|SPEC\.md|documentation).{0,150}?(?:" + known[text_lic] + ")", body):
            problems.append(f"{path.name} does not say the text is {text_lic}")
    report["agreement"] = {"spec version": version, "levels": sorted(want["levels"])}
    print(json.dumps({"report": report, "problems": problems}, indent=2))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
