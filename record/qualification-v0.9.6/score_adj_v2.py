#!/usr/bin/env python3
"""Q1 scoring, v2. Supersedes score_adj.py (pinned sha c03a9eab...).

WHY A NEW SCRIPT: v1 used the count of RESOLVABLE asks as the denominator. The runbook states
absolute counts - "at least 18 of 20 asks correct", "at most 2 asks choose Y" - so an ask that
produced no ruling must count against the 20, not vanish from it. v1 also silently excluded
such asks. This version uses the fixed denominators and reports every unresolved ask.

Nothing else changes: same correct/contradiction/withdrawal rules, same seats and ranking.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import config as C

ROOT = C.ROOT


def load_latest():
    latest = {}
    for line in (ROOT / "results-q1.jsonl").read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        latest[(r["model_slug"], r["case"], r["ask"])] = r
    return latest


def main():
    man = json.loads((ROOT / "cases-q1-manifest.json").read_text())
    kind = {e["case"]: "planted" for e in man["planted"]}
    kind.update({e["case"]: "settled" for e in man["settled"]})
    cases = sorted(kind)
    models = C.ADJUDICATORS
    by = load_latest()

    missing = [(m, c, a) for m in models for c in cases for a in (1, 2) if (m, c, a) not in by]
    print("=== completeness ===")
    print(f"  expected asks={len(models)*len(cases)*2} present={len(by)} missing={len(missing)}")
    if missing:
        print(f"  MISSING: {missing[:10]}")

    withdrawn = []
    for c in cases:
        if kind[c] != "settled":
            continue
        n_y = sum(1 for m in models
                  if by.get((m, c, 1), {}).get("choice") == "Y"
                  and by.get((m, c, 2), {}).get("choice") == "Y")
        if n_y >= 2:
            withdrawn.append(c)
    print(f"\n=== withdrawn settled cases: {len(withdrawn)} {withdrawn}")

    scored = [c for c in cases if c not in withdrawn]
    n_planted = sum(1 for c in scored if kind[c] == "planted")
    n_settled = sum(1 for c in scored if kind[c] == "settled")
    planted_asks, settled_asks = 2 * n_planted, 2 * n_settled
    print(f"  scored: {n_planted} planted ({planted_asks} asks), {n_settled} settled ({settled_asks} asks)")

    print("\n=== per candidate (fixed denominators) ===")
    results = {}
    for m in models:
        planted_correct = settled_y = 0
        contradictions, unresolved = [], []
        for c in scored:
            a1 = by.get((m, c, 1), {}).get("choice")
            a2 = by.get((m, c, 2), {}).get("choice")
            if a1 and a2 and a1 != a2:
                contradictions.append(c)
            for a, ch in ((1, a1), (2, a2)):
                if ch is None:
                    unresolved.append(f"{c}/a{a}")
                if kind[c] == "planted" and ch == "X":
                    planted_correct += 1
                if kind[c] == "settled" and ch == "Y":
                    settled_y += 1
        qualifies = (planted_correct >= 18 and settled_y <= 2 and len(contradictions) <= 1)
        results[m] = {"planted_correct": planted_correct, "planted_asks": planted_asks,
                      "settled_y": settled_y, "settled_asks": settled_asks,
                      "contradictions": contradictions, "unresolved": unresolved,
                      "qualifies": qualifies}
        print(f"  {m:16s} planted {planted_correct}/{planted_asks} (need >=18)  "
              f"settled Y={settled_y}/{settled_asks} (need <=2)  "
              f"contradictions={len(contradictions)}  unresolved={len(unresolved)} "
              f"-> {'QUALIFIES' if qualifies else 'does not qualify'}")

    qual = [m for m in models if results[m]["qualifies"]]
    print(f"\n=== seats ===  qualifiers: {qual}")
    if "gpt-6.1-sol" in qual and "grok-4.7" in qual:
        seats = ["gpt-6.1-sol", "grok-4.7"]
        print("  both GPT 6.1 Sol and Grok 4.7 qualify -> seated as the frame proposes")
    else:
        seats = sorted(qual, key=lambda m: (-results[m]["planted_correct"], results[m]["settled_y"]))[:2]
        print(f"  ranked qualifiers -> {seats}")

    agreement = None
    if len(seats) == 2:
        s1, s2 = seats
        both_clean = same = 0
        for c in scored:
            for a in (1, 2):
                c1 = by.get((s1, c, a), {}).get("choice")
                c2 = by.get((s2, c, a), {}).get("choice")
                if c1 in ("X", "Y") and c2 in ("X", "Y"):
                    both_clean += 1
                    same += c1 == c2
        agreement = same / both_clean if both_clean else 0.0
        print(f"\n=== seated pair agreement === {same}/{both_clean} = {agreement:.1%} (need >=80%) "
              f"-> {'OK' if agreement >= 0.8 else 'STOP: below 80%'}")
        print(f"  asks where the pair both gave a non-ambiguous reading: {both_clean}/{2*len(scored)}")

    out = {"withdrawn": withdrawn, "results": results, "seats": seats, "agreement": agreement,
           "missing": missing, "scored_cases": scored, "planted_asks": planted_asks,
           "settled_asks": settled_asks, "supersedes": "score_adj.py (c03a9eab...)"}
    (ROOT / "score-q1.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"\nstopped_early = {len(seats) < 2 or (agreement is not None and agreement < 0.8)}")


if __name__ == "__main__":
    main()
