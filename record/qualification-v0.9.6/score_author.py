#!/usr/bin/env python3
"""Q2 scoring. Per case: the author's key against the published checker; mismatches go to both
seated adjudicators through Appendix A (real code, key as Y). Prints every acceptance value.
"""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import config as C
import q1lib as L
import q2lib as Q2

ROOT = C.ROOT
EV = ROOT / "evidence"
FIX = L.FIX


def fails_list(v):
    if v is None:
        return []
    return [v] if isinstance(v, str) else sorted(v)


def norm_key_entry(e):
    """Author key entry -> comparable reading, or a reason it is unusable."""
    if not isinstance(e, dict):
        return None, "not an object"
    if str(e.get("verdict", "")).upper() == "AMBIGUOUS":
        return None, "ambiguous"
    failing = e.get("failing")
    ids = []
    if isinstance(failing, list):
        for item in failing:
            if isinstance(item, dict):
                rid = item.get("id")
                sent = (item.get("sentence") or "").strip()
                if rid:
                    ids.append(str(rid).strip())
                if rid and not sent:
                    return None, f"no SPEC.md sentence for {rid}"
            elif isinstance(item, str):
                ids.append(item.strip())
                return None, f"no SPEC.md sentence for {item}"
    elif failing is None:
        ids = []
    return {"verdict": e.get("verdict"), "level": e.get("levelAchieved"),
            "routing": e.get("routing"), "failing": sorted(set(ids))}, None


def expected_reading(fixture):
    exp = json.loads((FIX / "expected.json").read_text())["cases"][fixture]
    return {"verdict": exp["verdict"], "level": exp["levelAchieved"],
            "routing": exp["routing"], "failing": fails_list(exp["fails"])}


def adj_ask(slug, fixture, X, Y, spec, schema, code, tag):
    """Appendix A, X shown as A, Y shown as B."""
    rec = (FIX / f"{fixture}.json").read_text()
    parts = [L.APPENDIX_A, "", "## SPEC.md", "", spec, "",
             "## JSON schema", "", schema, "",
             "## The record under review", "", f"```json\n{rec}\n```", "",
             L._dir_block("files/", FIX / "files"),
             L._dir_block("evidence/", FIX / "evidence"),
             "## The checker's source code", "", f"```python\n{code}\n```", "",
             "## The two readings", "", L.reading_block("A", X), L.reading_block("B", Y)]
    prompt = "\n".join(parts)
    model, provider, _ = C.PIN[slug]
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 8000,
            "provider": {"order": [provider], "allow_fallbacks": False}}
    st, d = L.post(body, key=C.load_key())
    text = L.content_of(d) if st == 200 else ""
    (EV / f"harness-q2adj-{slug}-{tag}.json").write_text(json.dumps(
        {"label": f"harness-q2adj-{slug}-{tag}", "model_requested": model,
         "provider_requested": provider, "http": st, "request": body, "response": d},
        indent=1) + "\n")
    ruling = L.parse_ruling(text)
    choice = {"A": "X", "B": "Y", "AMBIGUOUS": "ambiguous"}.get(ruling)
    return {"slug": slug, "ruling": ruling, "choice": choice,
            "cost": (d.get("usage") or {}).get("cost") if st == 200 else 0,
            "reply": text[:600]}


def main():
    seats = json.loads((ROOT / "score-q1.json").read_text())["seats"]
    mapping = json.loads((ROOT / "q2-map.json").read_text())
    spec = (L.PUB / "SPEC.md").read_text()
    schema = (L.PUB / "schema" / "custody-v1.schema.json").read_text()
    code = (L.PUB / "checker" / "check.py").read_text()

    results, findings, held = {}, [], []
    total_cost = 0.0
    for slug in C.AUTHORS:
        f = EV / f"harness-author-{slug}.json"
        if not f.exists():
            print(f"{slug}: NO RUN")
            continue
        run = json.loads(f.read_text())
        key = run.get("key") or {}
        correct = wrong = 0
        detail = []
        for neutral, fixture in sorted(mapping.items()):
            want = expected_reading(fixture)
            entry = key.get(neutral)
            got, why = norm_key_entry(entry) if entry is not None else (None, "missing from key")
            if got is None:
                wrong += 1
                detail.append({"case": neutral, "fixture": fixture, "result": "wrong",
                               "why": why})
                continue
            if (got["verdict"], got["level"], got["routing"], got["failing"]) == \
               (want["verdict"], want["level"], want["routing"], want["failing"]):
                correct += 1
                detail.append({"case": neutral, "fixture": fixture, "result": "correct",
                               "why": "matches the checker"})
                continue
            # mismatch -> both seated adjudicators
            votes = []
            for seat in seats:
                r = adj_ask(seat, fixture, want, got, spec, schema, code, f"{slug}-{neutral}")
                total_cost += r["cost"] or 0
                votes.append(r)
            choices = [v["choice"] for v in votes]
            if all(c == "X" for c in choices):
                verdict = "wrong"
                why = "both adjudicators chose the checker"
            elif all(c == "Y" for c in choices):
                verdict = "correct"
                why = "both adjudicators chose the key"
                findings.append({"fixture": fixture, "author": slug,
                                 "note": "checker finding for the v0.9.6 bar"})
            else:
                verdict = "held out"
                why = f"split or ambiguous: {choices}"
                held.append({"fixture": fixture, "author": slug})
            if verdict == "correct":
                correct += 1
            elif verdict == "wrong":
                wrong += 1
            detail.append({"case": neutral, "fixture": fixture, "result": verdict, "why": why,
                           "key": got, "checker": want, "votes": votes})
            print(f"  {slug} {neutral} {fixture[:44]:46s} -> {verdict} ({why})", flush=True)

        denom = correct + wrong
        acc = correct / denom if denom else 0.0
        cost = (run.get("usage") or {}).get("cost") or 0
        results[slug] = {"correct": correct, "wrong": wrong, "held_out": len(held),
                         "accuracy": acc, "cost": cost, "qualifies": acc >= 0.90,
                         "detail": detail}
        print(f"{slug:14s} correct={correct} wrong={wrong} held_out={len(held)} "
              f"accuracy={acc:.1%} (need >=90%) -> {'QUALIFIES' if acc >= 0.90 else 'does not qualify'}")

    qual = [(s, r) for s, r in results.items() if r["qualifies"]]
    qual.sort(key=lambda t: (-t[1]["accuracy"], t[1]["cost"]))
    seat = qual[0][0] if qual else None
    print(f"\n=== Q2 seat === {seat}  (ranked: "
          f"{[(s, round(r['accuracy'],3), round(r['cost'],4)) for s, r in qual]})")
    print(f"=== checker findings === {len(findings)}")
    for fnd in findings:
        print(f"  {fnd['fixture']}  ({fnd['author']})")

    out = {"results": {k: {kk: vv for kk, vv in v.items() if kk != "detail"} for k, v in results.items()},
           "detail": {k: v["detail"] for k, v in results.items()},
           "findings": findings, "held": held, "seat": seat,
           "seats_used": seats, "adjudication_cost": total_cost}
    (ROOT / "score-q2.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
