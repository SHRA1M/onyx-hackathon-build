"""Task 8 live-run order (2026-10-21), Part A: token accounting, the spend guard, the "obligation proxy" label.
No test makes a model call: the live model's HTTP call is replaced, and every run is written under tmp_path."""

from pathlib import Path
from statistics import median

import pytest

from onyx import cost, data, eval as onyx_eval, model, runs, scripted

ROOT = Path(__file__).resolve().parents[1]
SCRIPTED = ROOT / "runs" / "scripted"


def _env(tmp_path, model_id="claude-opus-5-5", key="test-key"):
    env = tmp_path / ".env"
    env.write_text(f"ONYX_MODEL_BASE_URL=https://example.invalid/v1/\nONYX_MODEL={model_id}\n"
                   f"ONYX_MODEL_API_KEY={key}\n", encoding="utf-8")
    return env


def _clear_env(monkeypatch):
    for name in model.ENV_NAMES:
        monkeypatch.delenv(name, raising=False)


def _with_usage(model_id, prompt=1000, completion=500):
    """A stand-in for the live HTTP call: the scripted reply in the chat-completions shape, with usage."""
    calls = []

    def complete(self, request_id, messages):
        sid, lang = request_id.split("-")[0], "ar" if any("(Arabic)" in m["content"] for m in messages) else "en"
        raw = scripted.model(sid, lang).complete(request_id, messages).raw
        calls.append(request_id)
        return model.ModelResponse(request_id, {**raw, "model": model_id, "usage": {
            "prompt_tokens": prompt, "completion_tokens": completion, "total_tokens": prompt + completion}})
    return complete, calls


# --- prices -----------------------------------------------------------------------------------------------

def test_price_table_quotes_the_pricing_page():
    prices = cost.load_prices()
    assert prices["source"].startswith("https://platform.claude.com/docs/en/about-claude/pricing")
    assert prices["read"] == "2026-10-21"
    for model_id in ("claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5"):
        assert model_id in prices["models"]
    assert cost.check_prices() == []


def test_a_price_not_in_its_quote_fails_check(monkeypatch):
    prices = cost.load_prices()
    prices["models"]["claude-opus-5-5"] = {**prices["models"]["claude-opus-5-5"], "usd_per_mtok_out": 25}
    monkeypatch.setattr(cost, "load_prices", lambda: prices)
    assert any("claude-opus-5-5" in p for p in cost.check_prices())


def test_cost_in_usd_and_price_unknown():
    assert cost.cost_usd("claude-opus-5-5", 1_000_000, 100_000) == pytest.approx(4 + 2)
    assert cost.cost_usd("scripted-mock", 1000, 1000) is None
    assert cost.cost_usd("claude-haiku-5-5", 100_001, 10) is None  # over the row's prompt-length limit


# --- token accounting in eval -------------------------------------------------------------------------------

def test_eval_reports_calls_tokens_and_cost_per_run(tmp_path, monkeypatch):
    _clear_env(monkeypatch)
    complete, _ = _with_usage("claude-opus-5-5", prompt=1000, completion=500)
    monkeypatch.setattr(model.OpenAICompatibleModel, "complete", complete)
    root = tmp_path / "runs"
    runs.record("live", root, scenarios=("S1",), runs=1, langs=("en",), modes=("governed",),
                env=_env(tmp_path), retriever=scripted.retriever("S1"), max_usd=5, spend_root=root, out=lambda s: None)
    results = onyx_eval.evaluate(root, tmp_path / "eval")
    (row,) = results["runs"]
    assert row["path"] == "S1/run1.jsonl" and row["model"] == "claude-opus-5-5"
    assert row["calls"] > 0
    assert row["prompt_tokens"] == 1000 * row["calls"] and row["completion_tokens"] == 500 * row["calls"]
    assert row["cost_usd"] == pytest.approx(row["calls"] * (1000 * 4 + 500 * 20) / 1e6)
    md = (tmp_path / "eval" / "results.md").read_text(encoding="utf-8")
    assert "## Tokens and cost" in md and "S1/run1.jsonl" in md


def test_a_model_with_no_price_row_reports_price_unknown(tmp_path, monkeypatch):
    results = onyx_eval.evaluate(SCRIPTED, tmp_path / "eval")
    assert results["runs"] and all(r["cost_usd"] is None for r in results["runs"])
    md = (tmp_path / "eval" / "results.md").read_text(encoding="utf-8")
    assert "price unknown" in md and "$0.00" not in md


def test_obligation_recall_is_labelled_obligation_proxy(tmp_path):
    results = onyx_eval.evaluate(SCRIPTED, tmp_path / "eval")
    md = (tmp_path / "eval" / "results.md").read_text(encoding="utf-8")
    assert "Obligation proxy" in md and "obligation recall" not in md.lower()
    assert "obligation_proxy" in results["scenarios"]["S1"]["governed"]["en"]


# --- spend guard --------------------------------------------------------------------------------------------

def test_live_shape_prompt_estimate():
    plan = cost.plan(("S1",), ("en",), ("governed",), 1, retriever=scripted.retriever("S1"))
    assert plan.calls == len(plan.prompt_bytes) > 0
    assert plan.prompt_tokens == round(median(plan.prompt_bytes) / cost.BYTES_PER_TOKEN)
    assert cost.BYTES_PER_TOKEN == 4  # pricing page: "Average web page (10 kB): ~2,500 tokens"


def test_guard_refuses_over_the_cap_before_any_call(tmp_path, monkeypatch):
    _clear_env(monkeypatch)
    complete, calls = _with_usage("claude-opus-5-5")
    monkeypatch.setattr(model.OpenAICompatibleModel, "complete", complete)
    printed = []
    with pytest.raises(cost.SpendRefused):
        runs.record("live", tmp_path / "runs", scenarios=("S1",), runs=1, langs=("en",), modes=("governed",),
                    env=_env(tmp_path), retriever=scripted.retriever("S1"), max_usd=0.000001,
                    spend_root=tmp_path / "runs", out=printed.append)
    assert calls == [] and not (tmp_path / "runs" / "S1").exists()
    assert printed and "estimate" in printed[0].lower() and "USD" in printed[0]


def test_guard_default_cap_is_five_usd():
    assert cost.DEFAULT_MAX_USD == 5 and cost.TOTAL_CAP_USD == 15


def test_estimate_is_printed_before_the_first_call(tmp_path, monkeypatch):
    _clear_env(monkeypatch)
    complete, calls = _with_usage("claude-opus-5-5")
    order = []
    monkeypatch.setattr(model.OpenAICompatibleModel, "complete",
                        lambda self, rid, msgs: (order.append("call"), complete(self, rid, msgs))[1])
    runs.record("live", tmp_path / "runs", scenarios=("S1",), runs=1, langs=("en",), modes=("governed",),
                env=_env(tmp_path), retriever=scripted.retriever("S1"), max_usd=5, spend_root=tmp_path / "runs",
                out=lambda line: order.append("print"))
    assert order[0] == "print" and "call" in order


def test_guard_refuses_a_model_with_no_price(tmp_path, monkeypatch):
    _clear_env(monkeypatch)
    with pytest.raises(cost.SpendRefused, match="price unknown"):
        runs.record("live", tmp_path / "runs", scenarios=("S1",), runs=1, langs=("en",), modes=("governed",),
                    env=_env(tmp_path, model_id="no-such-model"), retriever=scripted.retriever("S1"), max_usd=5,
                    spend_root=tmp_path / "runs", out=lambda s: None)


def test_guard_uses_recorded_tokens_and_counts_output_once_measured(tmp_path, monkeypatch):
    _clear_env(monkeypatch)
    complete, _ = _with_usage("claude-opus-5-5", prompt=2000, completion=3000)
    monkeypatch.setattr(model.OpenAICompatibleModel, "complete", complete)
    root = tmp_path / "runs"
    runs.record("live", root / "a", scenarios=("S1",), runs=1, langs=("en",), modes=("governed",), env=_env(tmp_path),
                retriever=scripted.retriever("S1"), max_usd=5, spend_root=root, out=lambda s: None)
    plan = cost.plan(("S1",), ("en",), ("governed",), 1, retriever=scripted.retriever("S1"))
    est = cost.estimate("claude-opus-5-5", plan, spend_root=root)
    assert est.prompt_tokens == 2000 and est.completion_tokens == 3000
    assert est.usd == pytest.approx(plan.calls * (2000 * 4 + 3000 * 20) / 1e6)
    assert est.spent_usd == pytest.approx(est.usd)  # the first run's actual spend, same calls and tokens


def test_guard_refuses_when_total_spend_would_pass_fifteen(tmp_path, monkeypatch):
    _clear_env(monkeypatch)
    complete, calls = _with_usage("claude-opus-5-5")
    monkeypatch.setattr(model.OpenAICompatibleModel, "complete", complete)
    monkeypatch.setattr(cost, "spent_usd", lambda root: 15.0)
    with pytest.raises(cost.SpendRefused, match="would pass USD 15"):
        runs.record("live", tmp_path / "runs", scenarios=("S1",), runs=1, langs=("en",), modes=("governed",),
                    env=_env(tmp_path), retriever=scripted.retriever("S1"), max_usd=5, spend_root=tmp_path / "runs",
                    out=lambda s: None)
    assert calls == []


def test_live_record_without_a_key_still_stops_first(tmp_path, monkeypatch):
    _clear_env(monkeypatch)
    with pytest.raises(model.MissingModelKey):
        runs.record("live", tmp_path / "runs", env=_env(tmp_path, key=""), out=lambda s: None)
    assert not (tmp_path / "runs").exists()


def test_check_data_includes_the_price_table(capsys):
    assert data.check_data() == 0
    assert "prices" in capsys.readouterr().out
