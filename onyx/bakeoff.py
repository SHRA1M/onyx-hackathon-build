"""Bake-off (Task 8 live order, 2026-10-21, Part B): three Claude models through the same adapter, one governed run
per scenario in English and in Arabic each, under runs/bakeoff/<model id>/. One table, eval/bakeoff.md, and hq's
decision rule. Recomputed from the run logs like eval; running it twice writes the same bytes.

Rows, per model and language, over the five scenarios (one run each):
- the Task 8 metrics from onyx/eval.py, as the mean of the five runs (a run where a metric does not apply is left
  out); abstention is the share of the five runs that abstained on the key's step;
- JSON parse failures: replies parse_output could not read, out of the model calls;
- of which stopped by the endpoint: replies whose finish_reason is content_filter (empty or cut short);
- quote failures: gated proposals whose quote is not 20+ characters verbatim in a cited clause (English or Arabic
  text), out of the gated proposals; the gate's own quote check, without its other checks;
- model_ms median and max, prompt and completion tokens, and cost in USD from onyx/data/model_prices.json.
Per model: Arabic versus English agreement on decisions and clause ids (mean over the five scenario pairs).

Decision rule (hq): Opus 5.5 is the main model unless Sonnet 5.5 equals or beats it on every row, in which case
Sonnet; Haiku is a comparator only. If Opus has a JSON parse or quote failure in Arabic, stop: hq decides whether
Fable 5.1 is tried. Rows with no better direction (gate rejection rate, tokens, calls) are shown, not compared.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from statistics import mean, median
from typing import Any

from onyx import cost, data, gate
from onyx import eval as onyx_eval
from onyx.coordinator import _rules_by_chunk
from onyx.runs import LANGS, SCENARIOS, run_path

ROOT = Path(__file__).resolve().parents[1]
BAKEOFF_DIR = ROOT / "runs" / "bakeoff"
# (prompt, runs root, commit of the prompt the runs used): v1 Part B; v2 Part C2 (order 2026-10-21-task-8-part-c)
VERSIONS = (("v1", BAKEOFF_DIR, "d7bb264"), ("v2", ROOT / "runs" / "bakeoff-v2", "a85a448"))
# a line under a version's table, written by hq's order (2026-10-21-task-8-part-c2b item 3)
NOTES = {"v2": "Arabic gap ids present in notes in 10 of 10 runs; scored 0 under v2 parsing; see C2b."}
MODELS = ("claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5")
OPUS, SONNET, _ = MODELS
UNPARSEABLE = "unparseable model response"
HIGHER, LOWER, SHOWN = 1, -1, 0

# (label, key, per language or per model, direction)
ROWS = (
    ("Runs read", "runs", "lang", SHOWN),
    ("Gate rejection rate", "gate_rejection_rate", "lang", SHOWN),
    ("Citation validity", "citation_validity", "lang", HIGHER),
    ("Action recall", "action_recall", "lang", HIGHER),
    ("Obligation proxy", "obligation_proxy", "lang", HIGHER),
    ("Gap recall", "gap_recall", "lang", HIGHER),
    ("Abstention (share of runs)", "abstention", "lang", HIGHER),
    ("Hand-over latency (steps)", "handover_latency_steps", "lang", LOWER),
    ("Arabic versus English agreement", "ar_en_agreement", "model", HIGHER),
    ("JSON parse failures", "parse_failures", "lang", LOWER),
    ("Replies stopped by the endpoint (content_filter)", "filter_stops", "lang", SHOWN),
    ("Quote failures", "quote_failures", "lang", LOWER),
    ("model_ms median", "model_ms_median", "lang", LOWER),
    ("model_ms max", "model_ms_max", "lang", LOWER),
    ("Model calls", "calls", "lang", SHOWN),
    ("Prompt tokens", "prompt_tokens", "lang", SHOWN),
    ("Completion tokens", "completion_tokens", "lang", SHOWN),
    ("Cost (USD)", "cost_usd", "model", LOWER),
)
MEANS = ("gate_rejection_rate", "citation_validity", "action_recall", "obligation_proxy", "gap_recall", "abstention",
         "handover_latency_steps")


def parse_failures(events: list[dict[str, Any]]) -> int:
    return sum(1 for e in events if e["action"] == "propose"
               and str((e["new_value"].get("reasoning_chain") or [""])[0]).startswith(UNPARSEABLE))


def filter_stops(events: list[dict[str, Any]]) -> int:
    return sum(1 for e in events if e["action"] == "propose"
               and e["model_response"]["choices"][0].get("finish_reason") == "content_filter")


def quote_failures(events: list[dict[str, Any]], kb: gate.Knowledge) -> int:
    def found(p: dict[str, Any]) -> bool:
        texts = [re.sub(r"\s+", " ", (kb.chunk(c) or {}).get(f) or "").strip()
                 for c in p.get("clause_ids") or [] for f in ("text_en", "text_ar")]
        quote = re.sub(r"\s+", " ", p.get("quote", "")).strip()
        return len(quote) >= data.MIN_QUOTE and any(quote in t for t in texts if t)
    return sum(not found(e["old_value"]) for e in onyx_eval._gates(events, pending=False))


def _mean(values: list[Any]) -> float | None:
    present = [v for v in values if v is not None]
    return round(mean(present), 4) if present else None


def _sum(values: list[Any]) -> Any:
    return None if not values or None in values else round(sum(values), 6)


def _language(paths: list[tuple[str, Path]], keys: dict, scenarios: dict, kb: gate.Knowledge, by_chunk: dict) -> tuple[dict, list]:
    metrics, row = [], {"runs": len(paths), "chains_ok": True}
    calls = proposals = parse = quotes = stops = 0
    model_ms: list[float] = []
    for sid, path in paths:
        m = onyx_eval.run_metrics(path, keys[sid], scenarios[sid], kb, by_chunk, earlier_addressee=True,
                                     resolve=False)
        events = onyx_eval._events(path)
        metrics.append(m)
        row["chains_ok"] &= m["chain_ok"] and m["keys_match"]
        model_ms += m["model_ms"]
        parse += parse_failures(events)
        stops += filter_stops(events)
        quotes += quote_failures(events, kb)
        calls += m["usage"]["calls"]
        proposals += len(onyx_eval._gates(events, pending=False))
    row.update({k: _mean([m[k] for m in metrics]) for k in MEANS})
    # the bake-off was scored on every proposal; hq's later citation rule does not rescore it
    row["citation_validity"] = _mean([m["citation_validity_all"] for m in metrics])
    row.update({"parse_failures": parse, "filter_stops": stops, "calls": calls, "quote_failures": quotes, "proposals": proposals,
                "model_ms_median": round(median(model_ms), 1) if model_ms else None,
                "model_ms_max": round(max(model_ms), 1) if model_ms else None,
                "prompt_tokens": _sum([m["usage"]["prompt_tokens"] for m in metrics]),
                "completion_tokens": _sum([m["usage"]["completion_tokens"] for m in metrics]),
                "cost_usd": _sum([m["usage"]["cost_usd"] for m in metrics])})
    return row, metrics


def build(root: str | Path = BAKEOFF_DIR) -> dict[str, Any]:
    root = Path(root)
    kb, by_chunk = gate.Knowledge.load(), _rules_by_chunk()
    keys = {sid: data.load_key(sid) for sid in SCENARIOS}
    scenarios = {sid: data.load_scenario(sid) for sid in SCENARIOS}
    models = []
    for model_id in (m for m in MODELS if (root / m).is_dir()):
        entry: dict[str, Any] = {"model": model_id}
        per_lang = {}
        for lang in LANGS:
            paths = [(sid, p) for sid in SCENARIOS if (p := run_path(root / model_id, sid, 1, lang)).exists()]
            entry[lang], per_lang[lang] = _language(paths, keys, scenarios, kb, by_chunk)
        pairs = []
        for en, ar in zip(per_lang["en"], per_lang["ar"]):
            steps = set(en["signature"]) | set(ar["signature"])
            pairs.append(onyx_eval._ratio(sum(en["signature"].get(s) == ar["signature"].get(s) for s in steps),
                                          len(steps)))
        entry["ar_en_agreement"] = _mean(pairs)
        entry["cost_usd"] = _sum([entry[lang]["cost_usd"] for lang in LANGS])
        models.append(entry)
    return {"models": models, "decision": decide(models)}


def build_all(versions: tuple[tuple[str, Path, str], ...] = VERSIONS) -> list[dict[str, Any]]:
    """One table per prompt version. Only v1 is decided by hq's rule; from v2 on the model is hq's decision."""
    tables = []
    for label, root, commit in versions:
        if Path(root).is_dir():
            table = {"prompt": label, "prompt_commit": commit, **build(root)}
            if label != "v1":
                table["decision"] = {"model": SONNET, "stop": False, "sonnet_behind": [], "decided_by": "hq",
                                     "reason": f"{SONNET} is the main model (hq, order 2026-10-21-task-8-part-c, "
                                               "decision 1); the Part B rule is not re-applied"}
            tables.append(table)
    return tables


def _at_least(sonnet: Any, opus: Any, direction: int) -> bool:
    if opus is None:
        return True
    if sonnet is None:
        return False
    return sonnet * direction >= opus * direction


def decide(models: list[dict[str, Any]]) -> dict[str, Any]:
    by = {m["model"]: m for m in models}
    if OPUS not in by or SONNET not in by:
        return {"model": None, "stop": True, "sonnet_behind": [], "reason": "Opus or Sonnet runs missing"}
    opus, sonnet = by[OPUS], by[SONNET]
    failed = [f"{key} ar {opus['ar'][key]}" for key in ("parse_failures", "quote_failures") if opus["ar"][key]]
    if failed:
        return {"model": None, "stop": True, "sonnet_behind": [],
                "reason": f"Opus fails in Arabic ({', '.join(failed)}): stop, hq decides whether Fable 5.1 is tried"}
    behind = []
    for _, key, scope, direction in ROWS:
        if direction == SHOWN:
            continue
        pairs = ([(sonnet[lang][key], opus[lang][key], f"{key} {lang}") for lang in LANGS] if scope == "lang"
                 else [(sonnet[key], opus[key], key)])
        behind += [name for s, o, name in pairs if not _at_least(s, o, direction)]
    if behind:
        return {"model": OPUS, "stop": False, "sonnet_behind": behind,
                "reason": f"Sonnet is behind Opus on {len(behind)} row(s): {', '.join(behind)}"}
    return {"model": SONNET, "stop": False, "sonnet_behind": [],
            "reason": "Sonnet equals or beats Opus on every compared row"}


def _fmt(value: Any, key: str) -> str:
    if value is None:
        return "price unknown" if key == "cost_usd" else "n/a"
    if key == "cost_usd":
        return f"{value:.4f}"
    if key in ("model_ms_median", "model_ms_max"):
        return f"{value:,.0f}"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def _cell(entry: dict[str, Any], key: str, scope: str) -> str:
    if scope == "model":
        return _fmt(entry[key], key)
    parts = []
    for lang in LANGS:
        value = _fmt(entry[lang][key], key)
        if key in ("parse_failures", "filter_stops"):
            value += f" of {entry[lang]['calls']}"
        elif key == "quote_failures":
            value += f" of {entry[lang]['proposals']}"
        parts.append(f"{lang} {value}")
    return " / ".join(parts)


def _section(table: dict[str, Any]) -> list[str]:
    models = table["models"]
    chains = all(m[lang]["chains_ok"] for m in models for lang in LANGS)
    lines = [f"## Prompt {table['prompt']}, commit {table['prompt_commit']}", "",
             f"All hash chains verify and every run_start carries the current key hashes: {'yes' if chains else 'NO'}.",
             "", "| Row | " + " | ".join(m["model"] for m in models) + " | Compared |",
             "|---|" + "---|" * len(models) + "---|"]
    for label, key, scope, direction in ROWS:
        compared = {HIGHER: "higher is better", LOWER: "lower is better", SHOWN: "shown only"}[direction]
        lines.append(f"| {label} | " + " | ".join(_cell(m, key, scope) for m in models) + f" | {compared} |")
    if table["prompt"] in NOTES:
        lines += ["", NOTES[table["prompt"]]]
    decision = table["decision"]
    if decision.get("decided_by") == "hq":
        lines += ["", f"### Decision ({table['prompt']})", "", f"{decision['reason']}.", ""]
    else:
        lines += ["", f"### Decision ({table['prompt']})", "",
                  "hq's rule: Opus 5.5 is the main model unless Sonnet 5.5 equals or beats it on every compared row, "
                  "in which case Sonnet. Haiku 5.5 is a comparator only. If Opus fails the JSON or quote rows in "
                  "Arabic, stop and report.", "",
                  f"Result: {'STOP. ' if decision['stop'] else ''}"
                  f"{decision['model'] or 'no model chosen'}. {decision['reason']}.", ""]
    return lines


def markdown(tables: list[dict[str, Any]]) -> str:
    prices = cost.load_prices()
    lines = ["# Bake-off: Opus 5.5, Sonnet 5.5, Haiku 5.5 (Task 8 live order, Part B; Part C2)", "",
             "Generated by `python -m onyx bakeoff` from the run logs under runs/bakeoff/<model id>/ (prompt v1) and "
             "runs/bakeoff-v2/<model id>/ (prompt v2): one governed run per scenario (S1 to S5) in English and in "
             "Arabic per model, live calls through Anthropic's OpenAI-compatible endpoint, the same adapter, prompts "
             "and retrieval for every model of a table. Synthetic operator and subscribers. Each cell is English / "
             "Arabic unless the row is per model.", "",
             f"Cost priced from {prices['source']} (read {prices['read']}).", ""]
    for table in tables:
        lines += _section(table)
    lines += ["## Definitions", "", *[line.strip() for line in __doc__.split("Rows,", 1)[1].split("Decision rule")[0]
                                      .splitlines()[1:] if line.strip()]]
    return "\n".join(lines) + "\n"


def write(tables: list[dict[str, Any]], out: str | Path) -> None:
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "bakeoff.json").write_text(json.dumps(tables, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                                      encoding="utf-8", newline="\n")
    (out / "bakeoff.md").write_text(markdown(tables), encoding="utf-8", newline="\n")


def _cli(args) -> int:
    tables = build_all()
    write(tables, args.out)
    for table in tables:
        decision = table["decision"]
        print(f"prompt {table['prompt']} ({table['prompt_commit']}): {len(table['models'])} models; decision: "
              f"{'STOP, ' if decision['stop'] else ''}{decision['model'] or 'none'} ({decision['reason']}).")
    print(f"table in {args.out}/bakeoff.md")
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser("bakeoff", help="the model bake-off tables, prompt v1 and v2 (Task 8 Parts B, C2)")
    parser.add_argument("--out", default="eval", help="where bakeoff.md and bakeoff.json go")
    parser.set_defaults(func=_cli)
