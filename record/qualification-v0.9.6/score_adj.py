#!/usr/bin/env python3
"""Q1 scoring. Reads results-q1.jsonl and prints every acceptance value.

Rules (runbook Q1):
- Correct   = the ruling chose X.
- Contradiction = the two asks of a case map to different choices.
- Withdrawn case = a settled case where at least two of the three candidates choose Y on BOTH asks.
  Withdrawn before scoring; reported as a possible text finding.
- Qualifies when all three hold: planted >= 18 of 20 asks correct; settled <= 2 asks choose Y;
  <= 1 contradiction across all 24 cases.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import config as C

ROOT = C.ROOT


def load():
    rows = []
    for line in (ROOT / "results-q1.jsonl").read_text().splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def main():
    man = json.loads((ROOT / "cases-q1-manifest.json").read_text())
    kind = {e["case"]: "planted" for e in man["planted"]}
    kind.update({e["case"]: "settled" for e in man["settled"]})
    cases = sorted(kind)
    models = C.ADJUDICATORS

    by = {}
    for r in load():
        by[(r["model_slug"], r["case"], r["ask"])] = r

    print("=== completeness ===")
    missing = [(m, c, a) for m in models for c in cases for a in (1, 2)
               if (m, c, a) not in by]
    print(f"  expected asks={len(models)*len(cases)*2} present={len(by)} missing={len(missing)}")
    if missing:
        print(f"  MISSING: {missing[:10]}")
    unresolved = [(m, c, a) for (m, c, a), r in by.items() if not r.get("choice")]
    print(f"  unresolved (no parseable ruling): {len(unresolved)} {unresolved[:8]}")

    # ---- withdrawn settled cases: >=2 candidates chose Y on BOTH asks ----
    withdrawn = []
    for c in cases:
        if kind[c] != "settled":
            continue
        n_y = 0
        for m in models:
            a1 = by.get((m, c, 1), {}).get("choice")
            a2 = by.get((m, c, 2), {}).get("choice")
            if a1 == "Y" and a2 == "Y":
                n_y += 1
        if n_y >= 2:
            withdrawn.append(c)
    print(f"\n=== withdrawn settled cases: {len(withdrawn)} {withdrawn}")

    scored_cases = [c for c in cases if c not in withdrawn]

    print("\n=== per candidate ===")
    results = {}
    for m in models:
        planted_total = planted_correct = 0
        settled_total = settled_y = 0
        contradictions = []
        for c in scored_cases:
            a1 = by.get((m, c, 1), {}).get("choice")
            a2 = by.get((m, c, 2), {}).get("choice")
            if a1 and a2 and a1 != a2:
                contradictions.append(c)
            if kind[c] == "planted":
                for ch in (a1, a2):
                    if ch is None:
                        continue
                    planted_total += 1
                    if ch == "X":
                        planted_correct += 1
            else:
                for ch in (a1, a2):
                    if ch is None:
                        continue
                    settled_total += 1
                    if ch == "Y":
                        settled_y += 1
        qualifies = (planted_correct >= 18 and settled_y <= 2 and len(contradictions) <= 1)
        results[m] = {"planted_correct": planted_correct, "planted_total": planted_total,
                      "settled_y": settled_y, "settled_total": settled_total,
                      "contradictions": contradictions, "qualifies": qualifies}
        print(f"  {m:16s} planted {planted_correct}/{planted_total} (need >=18)  "
              f"settled Y={settled_y}/{settled_total} (need <=2)  "
              f"contradictions={len(contradictions)} {contradictions}  "
              f"-> {'QUALIFIES' if qualifies else 'does not qualify'}")

    # ---- seats ----
    qual = [m for m in models if results[m]["qualifies"]]
    print(f"\n=== seats ===  qualifiers: {qual}")
    if "gpt-6.1-sol" in qual and "grok-4.7" in qual:
        seats = ["gpt-6.1-sol", "grok-4.7"]
        print("  both GPT 6.1 Sol and Grok 4.7 qualify -> seated as the frame proposes")
    else:
        seats = sorted(qual, key=lambda m: (-results[m]["planted_correct"],
                                            -results[m]["settled_total"] + results[m]["settled_y"]))[:2]
        print(f"  ranked qualifiers -> {seats}")

    # ---- agreement ----
    agreement = None
    if len(seats) == 2:
        s1, s2 = seats
        both_clean = same = 0
        for c in scored_cases:
            for a in (1, 2):
                c1 = by.get((s1, c, a), {}).get("choice")
                c2 = by.get((s2, c, a), {}).get("choice")
                if c1 in ("X", "Y") and c2 in ("X", "Y"):
                    both_clean += 1
                    if c1 == c2:
                        same += 1
        agreement = same / both_clean if both_clean else 0.0
        print(f"\n=== seated pair agreement === {same}/{both_clean} = {agreement:.1%} "
              f"(need >=80%)  -> {'OK' if agreement >= 0.8 else 'STOP: below 80%'}")

    out = {"withdrawn": withdrawn, "results": results, "seats": seats,
           "agreement": agreement, "missing": missing, "unresolved": unresolved,
           "scored_cases": scored_cases}
    (ROOT / "score-q1.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"\nstopped_early = {len(seats) < 2 or (agreement is not None and agreement < 0.8)}")


if __name__ == "__main__":
    main()
