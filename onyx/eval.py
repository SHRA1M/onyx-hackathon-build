"""Eval (order Task 8): every figure recomputed from the run logs against the frozen keys. Running it twice writes
the same bytes (no clock, sorted keys), so `git diff` stays empty.

Metrics, per run, then min and max over the three runs of each scenario, mode and language:
- gate rejection rate: share of gate verdicts that are not allow.
- citation validity: share of proposals (pending proposals excluded: they cite nothing) whose every cited chunk is
  VERIFIED and whose quote is 20+ characters verbatim in a cited chunk.
- action recall: share of key steps with a proposal by the key's agent whose verb is the key's verb and whose
  addressee, the subscriber side or a human, matches: where the key answers a step sent by a human with a reply
  (draft_reply), the reply is addressed to that human (args.recipient 'human' or a 'Human agent' target); every
  other step expects a non-human addressee (blind keys review, 2026-10-21: S2 steps 3 and 4).
  On the abstention step the verb is flag_gap; the pending proposal's verb is never counted (addendum 29).
- obligation proxy (addendum item 27 wording): share of key obligations on steps that reached the key's verdict
  (gate_outcome on the abstention step) with every must_cite clause on the step's record (verdict, proposal or
  clauses searched).
- gap recall: share of the key's gaps_expected flagged in the run (flag_gap proposals and the abstention's gaps).
- abstention: the key's abstain_step answered INSUFFICIENT_EVIDENCE by the adviser (addendum 29).
- hand-over latency in steps: from the key's handover_step to the first step that passes to a human: a hold (held
  for a human), an allowed proposal addressed to a human or asking for one, or a complaint_gate hand-over duty.
- ungoverned baseline: steps where the ungoverned run allowed what the key says the gate holds or blocks.
- Arabic versus English agreement: share of steps whose decision and clause ids are the same in the two languages.
- gate_ms and model_ms: median and max (addendum 18).
- tokens and cost, per run: model calls, prompt and completion tokens from each reply's usage, and USD priced from
  onyx/data/model_prices.json; "price unknown" where the model has no price row or a reply carries no usage.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from statistics import median
from typing import Any

from onyx import audit, cost, data, gate
from onyx.coordinator import _rules_by_chunk
from onyx.runs import LANGS, RUNS, SCENARIOS, run_path

MODES = {"governed": True, "ungoverned": False}
METRICS = ("gate_rejection_rate", "citation_validity", "action_recall", "obligation_proxy", "gap_recall",
           "abstention", "handover_latency_steps", "ungoverned_claims_allowed")
HUMAN_VERBS = {"escalate_to_human", "request_human_review"}


def _events(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _step(entity_id: str) -> int:
    return int(entity_id.split("-")[1])


def _gates(events: list[dict[str, Any]], pending: bool | None = None) -> list[dict[str, Any]]:
    return [e for e in events if e["action"] == "gate"
            and (pending is None or bool(e["new_value"].get("pending")) == pending)]


def _to_human(proposal: dict[str, Any]) -> bool:
    return (proposal.get("args") or {}).get("recipient") == "human" or str(proposal.get("target", "")).startswith(
        "Human agent")


def _ratio(hit: int, total: int) -> float | None:
    return round(hit / total, 4) if total else None


def action_hits(events: list[dict[str, Any]], key: dict[str, Any], scenario: dict[str, Any]) -> dict[int, bool]:
    senders = {s["n"]: s["from"] for s in scenario["steps"]}
    hits = {}
    for step in key["steps"]:
        n, entity = step["n"], f"{key['scenario']}-{step['n']}-{step['agent']}"
        expect_human = senders[n] == "human" and step["verb"] == "draft_reply"
        hits[n] = any(e["old_value"]["verb"] == step["verb"] and _to_human(e["old_value"]) == expect_human
                      for e in _gates(events, pending=False) if e["entity_id"] == entity)
    return hits


def _citation_valid(proposal: dict[str, Any], kb: gate.Knowledge) -> bool:
    texts = []
    for cid in proposal.get("clause_ids") or []:
        chunk = kb.chunk(cid)
        if chunk is None or chunk.get("status") != "VERIFIED":
            return False
        texts += [re.sub(r"\s+", " ", chunk.get(f, "") or "").strip() for f in ("text_en", "text_ar")]
    quote = re.sub(r"\s+", " ", proposal.get("quote", "")).strip()
    return len(quote) >= data.MIN_QUOTE and any(quote in t for t in texts if t)


def _signature(events: list[dict[str, Any]]) -> dict[str, tuple[Any, ...]]:
    return {f"{e['entity_id']}:{e['action']}": (e["verdict"], tuple(sorted(e["clause_ids"]))) for e in events
            if e["action"] in {"gate", "abstain"}}


def run_metrics(path: Path, key: dict[str, Any], scenario: dict[str, Any], kb: gate.Knowledge,
                by_chunk: dict[str, list[str]]) -> dict[str, Any]:
    events = _events(path)
    sid, governed = key["scenario"], events[0]["new_value"].get("mode") != "ungoverned"
    gates, proposals = _gates(events), _gates(events, pending=False)
    by_step: dict[int, list[dict[str, Any]]] = {}
    for e in gates:
        by_step.setdefault(_step(e["entity_id"]), []).append(e)
    abstains = {_step(e["entity_id"]): e for e in events if e["action"] == "abstain" and e["actor"] == "adviser"}
    steps = {s["n"]: s for s in key["steps"]}

    def judged(n: int) -> list[dict[str, Any]]:
        """The gate events the key's verdict is about: the pending proposal on the abstention step (gate_outcome),
        the agents' proposals elsewhere."""
        abstain = bool(steps[n].get("abstain"))
        return [e for e in by_step.get(n, []) if bool(e["new_value"].get("pending")) == abstain]

    def expected(n: int) -> str:
        return steps[n].get("gate_outcome", steps[n]["verdict"])

    # obligation proxy: the step reached the key's verdict and every must_cite clause is on its record
    met = total = 0
    for n, step in steps.items():
        on_record = {c for e in by_step.get(n, []) for c in e["clause_ids"]}
        on_record |= {r for e in by_step.get(n, []) for c in e["old_value"].get("clause_ids", [])
                      for r in by_chunk.get(c, [])}
        on_record |= set(abstains[n]["clause_ids"]) if n in abstains else set()
        reached = expected(n) in {e["verdict"] for e in judged(n)}
        total += len(step["obligations"])
        met += len(step["obligations"]) if reached and set(step["must_cite"]) <= on_record else 0

    flagged = {str(e["old_value"]["args"].get("gap") or e["old_value"]["target"]) for e in proposals
               if e["old_value"]["verb"] == "flag_gap"} | {g for e in abstains.values() for g in e["new_value"]["gaps"]}
    handover = None
    if key.get("handover_step"):
        for n in sorted(by_step):
            if n < key["handover_step"]:
                continue
            if any(e["verdict"] == gate.HOLD or (e["verdict"] == gate.ALLOW and (
                    _to_human(e["old_value"]) or e["old_value"]["verb"] in HUMAN_VERBS)) or any(
                    r.get("gate") == "complaint_gate" and r.get("kind") == "obligation" and "hand" in r.get("text", "")
                    for r in e["new_value"]["reasons"]) for e in by_step[n]):
                handover = n - key["handover_step"]
                break
    claims = [n for n in steps if expected(n) in {gate.HOLD, gate.BLOCK}
              and any(e["verdict"] == gate.ALLOW for e in judged(n))]
    hits = action_hits(events, key, scenario)
    return {
        "chain_ok": audit.verify(path),
        "keys_match": events[0]["new_value"]["answer_keys"] == audit.key_hashes(),
        "model": events[0]["new_value"].get("model", ""),
        "gate_rejection_rate": _ratio(sum(e["verdict"] != gate.ALLOW for e in gates), len(gates)),
        "citation_validity": _ratio(sum(_citation_valid(e["old_value"], kb) for e in proposals), len(proposals)),
        "action_recall": _ratio(sum(hits.values()), len(hits)),
        "obligation_proxy": _ratio(met, total),
        "gap_recall": _ratio(len(set(key["gaps_expected"]) & flagged), len(key["gaps_expected"])),
        "abstention": int(abstains.get(key["abstain_step"], {}).get("verdict") == gate.INSUFFICIENT),
        "handover_latency_steps": handover,
        "ungoverned_claims_allowed": None if governed else len(claims),
        "gate_ms": [e["gate_ms"] for e in gates if e.get("gate_ms") is not None],
        "model_ms": [e["model_ms"] for e in events if e["action"] == "propose" and e.get("model_ms") is not None],
        "signature": _signature(events),
        "usage": cost.run_usage(events),
    }


def _span(values: list[Any]) -> dict[str, Any]:
    present = [v for v in values if v is not None]
    return {"min": min(present), "max": max(present)} if present else {"min": None, "max": None}


def _latency(values: list[float]) -> dict[str, Any]:
    return {"median_ms": round(median(values), 3), "max_ms": round(max(values), 3), "n": len(values)} if values else {
        "median_ms": None, "max_ms": None, "n": 0}


def evaluate(root: str | Path, out: str | Path) -> dict[str, Any]:
    root, out = Path(root), Path(out)
    kb, by_chunk = gate.Knowledge.load(), _rules_by_chunk()
    repo = Path(__file__).resolve().parents[1]
    shown = root.resolve().relative_to(repo) if root.resolve().is_relative_to(repo) else root
    results: dict[str, Any] = {"runs_root": shown.as_posix(), "scenarios": {}, "latency": {}, "models": [],
                               "runs_read": 0, "all_chains_ok": True, "all_keys_match": True, "runs": []}
    timings: dict[str, dict[str, list[float]]] = {m: {"gate_ms": [], "model_ms": []} for m in MODES}
    models = set()
    for sid in SCENARIOS:
        key, scenario = data.load_key(sid), data.load_scenario(sid)
        results["scenarios"][sid] = {}
        for mode, governed in MODES.items():
            per_lang: dict[str, list[dict[str, Any]]] = {}
            for lang in LANGS:
                paths = [p for n in range(1, RUNS + 1) if (p := run_path(root, sid, n, lang, governed)).exists()]
                per_lang[lang] = [run_metrics(p, key, scenario, kb, by_chunk) for p in paths]
                results["runs"] += [{"path": p.relative_to(root).as_posix(), "model": r["model"], **r["usage"]}
                                    for p, r in zip(paths, per_lang[lang])]
            row: dict[str, Any] = {}
            for lang, rows in per_lang.items():
                results["runs_read"] += len(rows)
                for r in rows:
                    models.add(r["model"])
                    results["all_chains_ok"] &= r["chain_ok"]
                    results["all_keys_match"] &= r["keys_match"]
                    timings[mode]["gate_ms"] += r["gate_ms"]
                    timings[mode]["model_ms"] += r["model_ms"]
                row[lang] = {"runs": len(rows), **{m: _span([r[m] for r in rows]) for m in METRICS}}
            agreement = []
            for en, ar in zip(per_lang["en"], per_lang["ar"]):
                steps = set(en["signature"]) | set(ar["signature"])
                agreement.append(_ratio(sum(en["signature"].get(s) == ar["signature"].get(s) for s in steps), len(steps)))
            row["ar_en_clause_agreement"] = _span(agreement)
            results["scenarios"][sid][mode] = row
    results["latency"] = {mode: {name: _latency(values) for name, values in t.items()} for mode, t in timings.items()}
    results["models"] = sorted(models)
    results["scripted"] = results["models"] == ["scripted-mock"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.json").write_text(json.dumps(results, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                                      encoding="utf-8", newline="\n")
    (out / "results.md").write_text(_markdown(results), encoding="utf-8", newline="\n")
    return results


def _cell(span: dict[str, Any]) -> str:
    lo, hi = span["min"], span["max"]
    if lo is None:
        return "n/a"
    fmt = (lambda v: f"{v:.2f}") if isinstance(lo, float) or isinstance(hi, float) else str
    return fmt(lo) if lo == hi else f"{fmt(lo)} to {fmt(hi)}"


def _markdown(results: dict[str, Any]) -> str:
    label = ("SCRIPTED runs (scripted-mock, no model call): these test the coordinator and the gate, never a model"
             if results["scripted"] else f"Live runs, model {', '.join(results['models'])}")
    lines = [f"# Eval results: {label}", "",
             f"Generated by `python -m onyx eval --runs {results['runs_root']}` from {results['runs_read']} run logs "
             "against the frozen keys (onyx/data/keys). Each cell is min to max over the three runs; one figure where "
             "they agree. Synthetic operator and subscribers.", "",
             f"All hash chains verify: {'yes' if results['all_chains_ok'] else 'NO'}. "
             f"Every run_start carries the current key hashes: {'yes' if results['all_keys_match'] else 'NO'}.", ""]
    heads = ["Scenario", "Lang", "Runs", "Gate rejection", "Citation validity", "Action recall", "Obligation proxy",
             "Gap recall", "Abstention", "Hand-over latency (steps)", "Ungoverned claims allowed"]
    for mode in MODES:
        lines += [f"## {mode.capitalize()}", "", "| " + " | ".join(heads) + " |", "|" + "---|" * len(heads)]
        for sid, modes in results["scenarios"].items():
            for lang in LANGS:
                row = modes[mode][lang]
                lines.append("| " + " | ".join([sid, lang, str(row["runs"])] + [_cell(row[m]) for m in METRICS]) + " |")
        lines += ["", "Arabic versus English agreement on decisions and clause ids: " + ", ".join(
            f"{sid} {_cell(modes[mode]['ar_en_clause_agreement'])}" for sid, modes in results["scenarios"].items()), ""]
        lat = results["latency"][mode]
        lines += [f"Latency: gate median {lat['gate_ms']['median_ms']} ms, max {lat['gate_ms']['max_ms']} ms "
                  f"({lat['gate_ms']['n']} decisions); model median {lat['model_ms']['median_ms']} ms, max "
                  f"{lat['model_ms']['max_ms']} ms ({lat['model_ms']['n']} calls).", ""]
    prices = cost.load_prices()
    lines += ["## Tokens and cost", "",
              f"Priced from {prices['source']} (read {prices['read']}), base input and output prices; a model with no "
              "price row, or a reply with no usage, is price unknown.", "",
              "| Run | Model | Calls | Prompt tokens | Completion tokens | Cost |", "|---|---|---|---|---|---|"]
    for r in results["runs"]:
        tokens = [str(r[k]) if r[k] is not None else "not recorded" for k in ("prompt_tokens", "completion_tokens")]
        usd = "price unknown" if r["cost_usd"] is None else f"USD {r['cost_usd']:.4f}"
        lines.append(f"| {r['path']} | {r['model']} | {r['calls']} | {' | '.join(tokens)} | {usd} |")
    total = [r["cost_usd"] for r in results["runs"]]
    lines += ["", "Total: " + ("price unknown" if not total or None in total else f"USD {sum(total):.4f}") +
              f" over {sum(r['calls'] for r in results['runs'])} calls.", ""]
    lines += ["## Definitions", "", *[line.strip() for line in __doc__.split("Metrics,", 1)[1].splitlines()[1:]
                                      if line.strip()]]
    return "\n".join(lines) + "\n"


def _cli(args) -> int:
    results = evaluate(args.runs, args.out)
    print(f"{results['runs_read']} runs read from {args.runs}; results in {args.out}/results.md and results.json "
          f"({'scripted' if results['scripted'] else ', '.join(results['models'])}).")
    return 0 if results["all_chains_ok"] and results["all_keys_match"] else 1


def register(subparsers) -> None:
    parser = subparsers.add_parser("eval", help="recompute every metric from the run logs (Task 8)")
    parser.add_argument("--runs", default="runs", help="runs root (runs/ for live, runs/scripted/ for scripted)")
    parser.add_argument("--out", default="eval", help="where results.md and results.json go")
    parser.set_defaults(func=_cli)
