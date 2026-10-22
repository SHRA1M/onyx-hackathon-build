"""Selftest (order 2026-10-17, Task 10): S1 through the agents and the gate with the scripted MockModel, no key and
no model call, its chain verified and replayed, then the headline figures from eval/results.json. Until live results
exist it reads eval/scripted/results.json and says so. Writes only to a temporary folder."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from onyx import audit, coordinator, data, runs, scripted
from onyx.eval import _cell, evaluate

ROOT = Path(__file__).resolve().parents[1]
RESULTS = (ROOT / "eval" / "results.json", ROOT / "eval" / "scripted" / "results.json")
RUNS_OF = {RESULTS[0]: ROOT / "runs", RESULTS[1]: ROOT / "runs" / "scripted"}
HEADLINE = (("Action recall", "action_recall"), ("Citation validity", "citation_validity"),
            ("Obligation proxy", "obligation_proxy"), ("Gap recall", "gap_recall"), ("Abstention", "abstention"),
            ("Hand-over latency", "handover_latency_steps"))


def headline(results: dict) -> list[str]:
    """With a C5 run set in results (order 2026-10-22, hq ruling on the C5 report): the C5 governed figures per
    scenario, the run set named, then C3's ungoverned claims as the baseline line. Without it: every scenario's
    governed figures and ungoverned claims, as before. Every figure is read from results, never typed."""
    if "c5" in results:
        c5 = results["c5"]
        runs_of = {lang: c5["C5"]["all"][lang]["runs"] for lang in runs.LANGS}
        lines = [f"C5 governed, {', '.join(results['models'])}: runs/c5, prompt {', '.join(c5['prompts']['governed'])}, "
                 f"{runs_of['en']} / {runs_of['ar']} runs (en / ar); chains ok: "
                 f"{'yes' if results['all_chains_ok'] else 'NO'}; key hashes match: "
                 f"{'yes' if results['all_keys_match'] else 'NO'}",
                 "  Governed     " + " | ".join(name for name, _ in HEADLINE)]
        for sid, by_lang in c5["C5"]["by_scenario"].items():
            for lang in runs.LANGS:
                cells = ["n/a" if by_lang[lang][m] is None else f"{by_lang[lang][m]:.2f}" for _, m in HEADLINE]
                lines.append(f"  {sid} {lang}        " + " | ".join(cells))
        claims = [f"{sid} {lang} {_cell(modes['ungoverned'][lang]['ungoverned_claims_allowed'])}"
                  for sid, modes in results["scenarios"].items() for lang in runs.LANGS]
        ungoverned = sum(modes["ungoverned"][lang]["runs"] for modes in results["scenarios"].values()
                         for lang in runs.LANGS)
        return lines + [f"Ungoverned baseline: C3, runs/ungoverned ({ungoverned} runs), ungoverned claims allowed per "
                        "run: " + ", ".join(claims)]
    label = "SCRIPTED (no model call)" if results["scripted"] else ", ".join(results["models"])
    lines = [f"{label}; {results['runs_read']} runs; chains ok: {'yes' if results['all_chains_ok'] else 'NO'}; "
             f"key hashes match: {'yes' if results['all_keys_match'] else 'NO'}",
             "  Governed     " + " | ".join(name for name, _ in HEADLINE) + " | Ungoverned claims allowed"]
    for sid, modes in results["scenarios"].items():
        for lang in runs.LANGS:
            cells = [_cell(modes["governed"][lang][m]) for _, m in HEADLINE]
            claims = _cell(modes["ungoverned"][lang]["ungoverned_claims_allowed"])
            lines.append(f"  {sid} {lang}        " + " | ".join(cells) + f" | {claims}")
    return lines


def selftest() -> int:
    scenario = data.load_scenario("S1")
    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "S1-en-governed.jsonl"
        run = coordinator.Coordinator(scenario, scripted.model("S1", "en"), scripted.retriever("S1"), log_path=log,
                                      gaps_dir=Path(tmp) / "gaps", lang="en", governed=True)
        print(f"Selftest: S1 {scenario['title_en']} (en, governed). SYNTHETIC operator and subscriber.")
        print("Model: scripted-mock (MockModel, no key, no model call). Retrieval: scripted.")
        run.start(source="selftest", model="scripted-mock")
        for r in run.run():
            verdicts = ", ".join(f"{p.verb}: {v.verdict}" for p, v in r.verdicts) or (r.answer or "no proposal")
            print(f"  {r.inject:<6} {r.agent:<12} {verdicts}")
        chain = audit.verify(log)
        recorded, replayed = runs.replay(log)
        same = bool(recorded) and recorded == replayed
        print(f"log: {'chain ok' if chain else 'CHAIN BROKEN'}; replay {'matches' if same else 'DIFFERS'} "
              f"({len(recorded)} decisions)")
    path = next((p for p in RESULTS if p.exists()), None)
    if path is None:
        print("Headline figures: no results.json yet (run `python -m onyx eval`).")
        return 1
    print(f"Headline figures from {path.relative_to(ROOT).as_posix()}:")
    for line in headline(json.loads(path.read_text(encoding="utf-8"))):
        print(line)
    # the figures are recomputed from the committed logs, never trusted as written (addendum, order 2026-10-21)
    with tempfile.TemporaryDirectory() as tmp:
        evaluate(RUNS_OF[path], tmp)
        match = (Path(tmp) / "results.json").read_bytes() == path.read_bytes()
    print(f"{'figures match a fresh eval' if match else 'FIGURES DIFFER from a fresh eval'} of "
          f"{RUNS_OF[path].relative_to(ROOT).as_posix()}/")
    return 0 if chain and same and match else 1


def register(subparsers) -> None:
    parser = subparsers.add_parser("selftest", help="run S1 offline (no key, no model call) and print the headline "
                                                    "figures")
    parser.set_defaults(func=lambda args: selftest())
