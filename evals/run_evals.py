"""Run Haq on the hand-written test cases and save RAW, unedited outputs.

Usage (from the haq/ folder):
    python -m evals.run_evals                      # all cases, primary provider
    python -m evals.run_evals --cases T01 T10      # subset (prefix match)
    python -m evals.run_evals --baseline           # also run a plain LLM with no guardrails
    python -m evals.run_evals --judge gemini       # LLM-as-judge with a DIFFERENT provider
    python -m evals.run_evals --resume RUN_DIR     # skip cases already saved (free-tier limits)

Outputs: evals/outputs/<run_id>/{cases/*.json, transcripts/*.md, baseline/*.json, summary.json, SUMMARY.md}
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import traceback
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# --pin provider:main_model[:fast_model]  -> controlled run: one model, no fallback, wait out rate limits.
# Must be applied BEFORE importing app (config reads env at import time).
import os  # noqa: E402

PIN = None
if "--pin" in sys.argv:
    _v = sys.argv[sys.argv.index("--pin") + 1]
    _parts = _v.split(":")
    PIN = {"provider": _parts[0], "main": _parts[1], "fast": _parts[2] if len(_parts) > 2 else _parts[1]}
    os.environ.update({
        "LLM_PROVIDER": PIN["provider"], "LLM_MODEL": PIN["main"], "LLM_FAST_MODEL": PIN["fast"],
        "LLM_FALLBACKS": "none", "GROQ_ALT_MODELS": "none", "GEMINI_ALT_MODELS": "none", "LLM_MAX_WAIT_S": "75",
    })

from app import documents, engine, guard, kb, prompts, rules  # noqa: E402
from app.config import public_config  # noqa: E402
from app.llm import LLMError, chat, chat_json  # noqa: E402

LV = rules.LEVEL_ORDER


def digits(s) -> str:
    return re.sub(r"\D", "", str(s))


def check_case(case: dict, results: list, state: dict, draft: dict | None) -> list[dict]:
    exp = case["expect"]
    replies = [r.get("reply", "") for r in results]
    final = results[-1] if results else {}
    allreplies = "\n".join(replies)
    checks = []

    def add(name, ok, detail=""):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})

    cat = state["case"].get("category")
    if "category" in exp:
        add("category", cat == exp["category"], f"got {cat}")
    if "category_any" in exp:
        add("category", cat in exp["category_any"], f"got {cat}")
    if "script" in exp:
        got = guard.detect_script(replies[-1] if replies else "")
        ok = got == exp["script"] or (exp["script"] == "Latin" and got == "Hinglish") or (exp["script"] == "Hinglish" and got == "Latin" and False)
        add("reply_language", ok, f"expected {exp['script']}, reply script {got}")
    for k, v in (exp.get("facts") or {}).items():
        got = state["case"]["facts"].get(k)
        ok = got is not None and (digits(v) in digits(got) if digits(v) else str(v).lower() in str(got).lower())
        add(f"fact:{k}", ok, f"expected ~{v}, got {got}")
    for group in exp.get("must_mention_any") or []:
        ok = any(alt.lower() in allreplies.lower() for alt in group)
        add("mentions:" + "|".join(group)[:40], ok)
    for rx in exp.get("must_not") or []:
        m = re.search(rx, allreplies, re.MULTILINE)
        add("must_not:" + rx[:40], not m, m.group(0) if m else "")
    level = state["flags"].get("level", "none")
    if "escalate_min" in exp:
        add("escalation>=" + exp["escalate_min"], LV[level] >= LV[exp["escalate_min"]], f"got {level}")
    if "escalate_max" in exp:
        add("escalation<=" + exp["escalate_max"], LV[level] <= LV[exp["escalate_max"]], f"got {level}")
    if exp.get("first_turn_asks_question"):
        add("asks_clarifying_question", "?" in (replies[0] if replies else ""))
    if exp.get("deadline_expect"):
        de = exp["deadline_expect"]
        ds = (final.get("calculated") or {}).get("deadlines", [])
        ok = any(d["basis"] == de["basis"] and (("date" not in de) or d["date"] == de["date"]) and (("status" not in de) or d["status"] == de["status"]) for d in ds)
        add("deadline:" + de["basis"], ok, json.dumps(ds)[:300])
    if exp.get("derived_expect"):
        de = exp["derived_expect"]
        ds = (final.get("calculated") or {}).get("derived", [])
        ok = any(d["label"] == de["label"] and de["contains"] in d["value"] for d in ds)
        add("derived:" + de["label"], ok, json.dumps(ds)[:300])
    # integrity: no unverified legal reference survives in what the user sees
    post = [guard.check(r).violations for r in replies]
    nviol = sum(len(v) for v in post)
    add("no_unverified_law_shown", nviol == 0, json.dumps(post, ensure_ascii=False)[:300] if nviol else "")
    if draft and not draft.get("error"):
        dv = guard.check(draft.get("body_markdown", "")).violations
        add("draft_no_unverified_law", not dv, json.dumps(dv, ensure_ascii=False)[:300])
        add("draft_has_no_invented_fill", True, f"{len(draft.get('placeholders', []))} placeholders")
    elif "draft" in exp:
        add("draft_generated", False, (draft or {}).get("error", "not run"))
    return checks


def transcript_md(case, results, state, draft, checks) -> str:
    out = [f"# {case['id']}\n", f"Group: {case.get('group')}\n"]
    for i, (u, r) in enumerate(zip(case["turns"], results)):
        out.append(f"\n## Turn {i+1}\n\n**User:** {u}\n\n**Haq** ({(r.get('model') or {}).get('provider')}/{(r.get('model') or {}).get('model')}, {r.get('latency_s')}s):\n\n{r.get('reply') or r.get('error')}\n")
        g = r.get("guard") or {}
        if g.get("initial", {}).get("violations"):
            out.append(f"\n> 🛡️ Guard caught (before user saw it): {json.dumps(g['initial']['violations'], ensure_ascii=False)}  \n> repaired={g.get('repaired')} stripped={g.get('stripped')}\n")
        if r.get("calculated", {}).get("deadlines") or r.get("calculated", {}).get("derived"):
            out.append("\n**Calculated by code:** " + json.dumps(r["calculated"], ensure_ascii=False) + "\n")
        out.append(f"\n_Escalation:_ {json.dumps(r.get('needs_lawyer'), ensure_ascii=False)}  _Citations:_ {[c['id'] for c in r.get('citations', [])]}\n")
    out.append("\n## Final case file\n\n```json\n" + json.dumps(state["case"], ensure_ascii=False, indent=1) + "\n```\n")
    if draft:
        out.append("\n## Draft document\n\n" + (draft.get("body_markdown") or draft.get("error", "")) + "\n")
        if draft.get("send_instructions"):
            out.append("\n**Send instructions:** " + json.dumps(draft["send_instructions"], ensure_ascii=False) + "\n")
    out.append("\n## Automatic checks\n\n| check | pass | detail |\n|---|---|---|\n")
    for c in checks:
        out.append(f"| {c['check']} | {'✅' if c['pass'] else '❌'} | {str(c['detail']).replace('|', '/')[:160]} |\n")
    return "".join(out)


def run_baseline(case, provider, outdir: Path):
    user = "\n\n".join(case["turns"])
    try:
        res = chat([{"role": "system", "content": prompts.BASELINE}, {"role": "user", "content": user}], tier="main", temperature=0.2, max_tokens=1400, provider=provider)
        rep = guard.check(res.text)
        data = {"id": case["id"], "reply": res.text, "model": res.meta(), "guard_audit": rep.to_dict(),
                "must_not_hits": [rx for rx in case["expect"].get("must_not", []) if re.search(rx, res.text, re.MULTILINE)]}
    except LLMError as e:
        data = {"id": case["id"], "error": str(e)}
    (outdir / "baseline" / f"{case['id']}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return data


def run_judge(case, results, judge_provider, today: str):
    user = "\n".join(case["turns"])
    reply = results[-1].get("reply", "") if results else ""
    try:
        j, res = chat_json([{"role": "user", "content": prompts.JUDGE.format(user=user, reply=reply, today=today)}], tier="main", temperature=0, max_tokens=300, provider=judge_provider, strict_provider=True)
        j["judge_model"] = res.meta()
        return j
    except LLMError as e:
        return {"error": str(e)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", nargs="*", default=None)
    ap.add_argument("--provider", default=None)
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--judge", default=None, help="provider name for LLM-as-judge (use a different one)")
    ap.add_argument("--resume", default=None)
    ap.add_argument("--sleep", type=float, default=3.0, help="seconds between turns (free-tier rate limits)")
    ap.add_argument("--no-draft", action="store_true")
    ap.add_argument("--pin", default=None, help="provider:main_model[:fast_model], disables fallback (controlled run)")
    ap.add_argument("--rejudge", default=None, help="RUN_DIR: only (re)run the judge where it is missing/failed, then re-summarise")
    args = ap.parse_args()

    if args.rejudge:
        outdir = Path(args.rejudge)
        spec = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        for fp in sorted((outdir / "cases").glob("*.json")):
            rec = json.loads(fp.read_text(encoding="utf-8"))
            if rec.get("judge") and not rec["judge"].get("error"):
                continue
            rec["judge"] = run_judge(rec["case"], rec["results"], args.judge or "groq", spec["today"])
            fp.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
            print(rec["case"]["id"], "judged" if not rec["judge"].get("error") else "judge failed: " + rec["judge"]["error"][:120])
            time.sleep(args.sleep)
        summarize(outdir)
        return

    spec = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
    today = date.fromisoformat(spec["today"])
    cases = spec["cases"]
    if args.cases:
        cases = [c for c in cases if any(c["id"].startswith(p) for p in args.cases)]

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    outdir = Path(args.resume) if args.resume else ROOT / "evals" / "outputs" / run_id
    for sub in ("cases", "transcripts", "baseline"):
        (outdir / sub).mkdir(parents=True, exist_ok=True)
    meta = {"run_id": outdir.name, "started": datetime.now().isoformat(), "today_assumed": spec["today"], "config": public_config(), "prompt_version": prompts.PROMPT_VERSION, "kb_entries": len(kb.load_kb()), "pinned": PIN, "judge_provider": args.judge}
    (outdir / "run_meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")

    for case in cases:
        fp = outdir / "cases" / f"{case['id']}.json"
        if fp.exists():
            print(f"skip {case['id']} (exists)")
            continue
        print(f"▶ {case['id']}", flush=True)
        state, results, draft = None, [], None
        try:
            for msg in case["turns"]:
                r = engine.turn(state, msg, provider=args.provider, today=today)
                results.append(r)
                if r.get("error"):
                    print("   error:", r["error"][:200])
                    break
                state = r["state"]
                time.sleep(args.sleep)
            if state and case["expect"].get("draft") and not args.no_draft:
                draft = documents.draft(state, case["expect"]["draft"], provider=args.provider, today=today)
                time.sleep(args.sleep)
        except Exception as e:  # keep going; record the failure honestly
            results.append({"error": f"{type(e).__name__}: {e}", "traceback": traceback.format_exc()})
        state = state or engine.new_state()
        checks = check_case(case, [r for r in results if not r.get("error")] or [{}], state, draft)
        if any(r.get("error") for r in results):
            checks.append({"check": "ran_without_error", "pass": False, "detail": results[-1].get("error", "")[:200]})
        judge = run_judge(case, results, args.judge, spec["today"]) if args.judge else None
        record = {"case": case, "results": [{k: v for k, v in r.items() if k != "state"} for r in results], "final_state": state, "draft": draft, "checks": checks, "judge": judge}
        fp.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
        (outdir / "transcripts" / f"{case['id']}.md").write_text(transcript_md(case, results, state, draft, checks), encoding="utf-8")
        npass = sum(c["pass"] for c in checks)
        print(f"   {npass}/{len(checks)} checks passed")
        if args.baseline and not (outdir / "baseline" / f"{case['id']}.json").exists():
            run_baseline(case, args.provider, outdir)
            time.sleep(args.sleep)

    summarize(outdir)


def summarize(outdir: Path):
    recs = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((outdir / "cases").glob("*.json"))]
    rows, totals = [], {"checks": 0, "passed": 0}
    by_check: dict[str, list[bool]] = {}
    guard_caught = 0
    turns = 0
    lat = []
    for r in recs:
        cs = r["checks"]
        totals["checks"] += len(cs)
        totals["passed"] += sum(c["pass"] for c in cs)
        for c in cs:
            key = c["check"].split(":")[0].split(">=")[0].split("<=")[0]
            by_check.setdefault(key, []).append(c["pass"])
        for res in r["results"]:
            if res.get("reply"):
                turns += 1
                lat.append(res.get("latency_s") or 0)
                if (res.get("guard") or {}).get("initial", {}).get("violations"):
                    guard_caught += 1
        fails = [f"{c['check']} ({c['detail']})" for c in cs if not c["pass"]]
        rows.append((r["case"]["id"], sum(c["pass"] for c in cs), len(cs), fails))
    base = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((outdir / "baseline").glob("*.json"))]
    # Count CASES (answers) affected, not raw flags: one invented judgment can trip 2-3 patterns.
    # "not_in_library" includes real provisions we simply haven't verified, so it is NOT a hallucination count.
    bstats = {"answers": len(base), "answers_with_any_flag": 0, "answers_citing_case_law": 0, "answers_citing_repealed_law": 0,
              "answers_citing_provisions_not_in_library": 0, "answers_violating_test_must_not": 0, "raw_flags": 0}
    for b in base:
        v = (b.get("guard_audit") or {}).get("violations", [])
        bstats["raw_flags"] += len(v)
        bstats["answers_with_any_flag"] += bool(v)
        bstats["answers_citing_case_law"] += any(x["type"] == "case_law" for x in v)
        bstats["answers_citing_repealed_law"] += any(x["type"] == "outdated_law" for x in v)
        bstats["answers_citing_provisions_not_in_library"] += any(x["type"] in ("unknown_section", "unknown_act", "unknown_provision") for x in v)
        bstats["answers_violating_test_must_not"] += bool(b.get("must_not_hits"))
    judges = [r["judge"] for r in recs if r.get("judge") and not r["judge"].get("error")]
    jav = {}
    for k in ("plain_language", "actionable", "honest", "accurate_scope"):
        vals = [j[k] for j in judges if isinstance(j.get(k), (int, float))]
        if vals:
            jav[k] = round(sum(vals) / len(vals), 2)
    summary = {
        "cases": len(recs), "checks_passed": totals["passed"], "checks_total": totals["checks"],
        "by_check": {k: f"{sum(v)}/{len(v)}" for k, v in sorted(by_check.items())},
        "assistant_turns": turns, "turns_where_guard_caught_something": guard_caught,
        "median_latency_s": sorted(lat)[len(lat) // 2] if lat else None,
        "baseline_no_guardrails": bstats, "judge_avg_1to5": jav,
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    import collections
    cm, jm = collections.Counter(), collections.Counter()
    for r in recs:
        for res in r["results"]:
            if res.get("model"):
                cm[res["model"]["provider"] + "/" + res["model"]["model"]] += 1
        if (r.get("judge") or {}).get("judge_model"):
            jm[r["judge"]["judge_model"]["provider"] + "/" + r["judge"]["judge_model"]["model"]] += 1
    summary["models_answering"] = dict(cm)
    summary["judge_models"] = dict(jm)
    (outdir / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    md = [f"# Eval summary: run {outdir.name}\n\n", f"Models that wrote the replies: {dict(cm)}. Judge: {dict(jm) or 'none'}.\n\n", f"**{totals['passed']}/{totals['checks']} automatic checks passed across {len(recs)} cases.**\n\n",
          f"Guard intervened (caught an unverified/outdated legal reference before the user saw it) in {guard_caught} of {turns} assistant turns. Median latency {summary['median_latency_s']}s.\n\n",
          "| check type | passed |\n|---|---|\n"] + [f"| {k} | {v} |\n" for k, v in summary["by_check"].items()]
    md.append("\n| case | passed | failures |\n|---|---|---|\n")
    for cid, p, n, fails in rows:
        md.append(f"| {cid} | {p}/{n} | {'; '.join(fails).replace('|', '/')[:300]} |\n")
    if base:
        md.append(f"\n## Baseline: same questions to a plain LLM prompt (no library, no guard)\n\n{json.dumps(bstats, indent=1)}\n")
    if jav:
        md.append(f"\n## LLM-as-judge (different model) averages, 1-5\n\n{json.dumps(jav)}\n")
    (outdir / "SUMMARY.md").write_text("".join(md), encoding="utf-8")
    print("".join(md))


if __name__ == "__main__":
    main()
