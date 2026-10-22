"""Figure 2 (order 2026-10-22-task-17-figures item 2, hq ruling 1): results, read from eval/results.md, never typed.

(a) C5 action recall and citation validity per scenario, English and Arabic side by side: the C5 value of each cell
    of the per-scenario table in section "C3, C4 and C5".
(b) C3 gate rejection rate, governed, as a bar over its min-to-max range, against the ungoverned run's claims allowed
    (a count, on its own axis): the Governed and Ungoverned tables, the only governed-against-ungoverned pair on file.

Exits naming the scenario and language when a value it needs is missing. Writes docs/fig/fig2-results.png and .svg;
a second run writes the same bytes.

    uv run python scripts/fig_results.py [--out docs/fig]
"""

import argparse
import re
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "eval" / "results.md"
STEM = "fig2-results"
SCENARIOS = ["S1", "S2", "S3", "S4", "S5"]
LANGS = ["en", "ar"]
CAPTION_A = ("C5, Claude Sonnet 5.5, prompt v5, two runs per scenario per language; figures regenerate from the "
             "committed logs.")
CAPTION_B = "C3, prompt v3, three runs per scenario per language; the only governed-against-ungoverned pair on file."
FONT = 7


def _section(text: str, heading: str) -> str:
    if heading not in text:
        raise SystemExit(f"eval/results.md: section {heading!r} missing")
    start = text.index(heading)
    end = text.find("\n## ", start + len(heading))
    return text[start:] if end == -1 else text[start:end]


def _table(section: str, header_cell: str) -> tuple[list[str], dict]:
    """The first table in the section whose header carries header_cell: its header and rows keyed (scenario, lang)."""
    lines = section.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("|") and header_cell in line:
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            rows = {}
            for row in lines[i + 2:]:
                if not row.startswith("|"):
                    break
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                rows[(cells[0], cells[1])] = dict(zip(header, cells))
            return header, rows
    raise SystemExit(f"eval/results.md: no table with column {header_cell!r}")


def _cell(rows: dict, scenario: str, lang: str, column: str, where: str) -> str:
    value = rows.get((scenario, lang), {}).get(column, "")
    if not value or value == "n/a":
        raise SystemExit(f"eval/results.md: {where}: {scenario} {lang} {column!r} missing")
    return value


def _span(cell: str) -> tuple[float, float]:
    parts = [float(p) for p in cell.split(" to ")]
    return parts[0], parts[-1]


def read_values(path: Path = RESULTS) -> dict:
    text = path.read_text(encoding="utf-8")
    _, c5 = _table(_section(text, "## C3, C4 and C5"), "Citation validity C3 / C4 / C5")
    _, governed = _table(_section(text, "## Governed"), "Gate rejection")
    _, ungoverned = _table(_section(text, "## Ungoverned"), "Ungoverned claims allowed")
    a, b = {}, {}
    for scenario in SCENARIOS:
        for lang in LANGS:
            citation = _cell(c5, scenario, lang, "Citation validity C3 / C4 / C5", "C3, C4 and C5")
            recall = _cell(c5, scenario, lang, "Action recall C3 / C4 / C5 (earlier rule in brackets)",
                           "C3, C4 and C5")
            a[(scenario, lang)] = {
                "citation": float(citation.split(" / ")[2]),
                "recall": float(re.sub(r"\s*\(.*\)", "", recall.split(" / ")[2])),
            }
            b[(scenario, lang)] = {
                "rejection": _span(_cell(governed, scenario, lang, "Gate rejection", "Governed")),
                "claims": _span(_cell(ungoverned, scenario, lang, "Ungoverned claims allowed", "Ungoverned")),
            }
    return {"a": a, "b": b}


def _positions() -> tuple[list[float], list[str]]:
    xs, labels = [], []
    for i, scenario in enumerate(SCENARIOS):
        for j, lang in enumerate(LANGS):
            xs.append(i * 2.6 + j)
            labels.append(f"{scenario}\n{lang}")
    return xs, labels


def draw(values: dict) -> plt.Figure:
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": FONT, "svg.hashsalt": "mizan-fig2",
                         "svg.fonttype": "none", "hatch.linewidth": 0.5})
    fig = plt.figure(figsize=(16 / 2.54, 6.0))
    ax_a = fig.add_axes((0.09, 0.63, 0.80, 0.31))
    ax_b = fig.add_axes((0.09, 0.14, 0.80, 0.29))
    xs, labels = _positions()
    keys = [(s, lang) for s in SCENARIOS for lang in LANGS]
    w = 0.38

    ax_a.bar([x - w / 2 for x in xs], [values["a"][k]["recall"] for k in keys], w, color="0.35", edgecolor="black",
             linewidth=0.5, label="action recall")
    ax_a.bar([x + w / 2 for x in xs], [values["a"][k]["citation"] for k in keys], w, color="white",
             edgecolor="black", linewidth=0.5, hatch="////", label="citation validity")
    ax_a.set_title("(a) Governed, C5", loc="left", fontsize=FONT + 1, pad=14)
    ax_a.legend(loc="lower right", bbox_to_anchor=(1.0, 1.0), ncol=2, frameon=False, fontsize=FONT - 0.5)

    lo = [values["b"][k]["rejection"][0] for k in keys]
    hi = [values["b"][k]["rejection"][1] for k in keys]
    ax_b.bar(xs, lo, 0.6, color="0.35", edgecolor="black", linewidth=0.5, label="gate rejection rate, governed")
    ax_b.bar(xs, [h - l for h, l in zip(hi, lo)], 0.6, bottom=lo, color="white", edgecolor="black", linewidth=0.5,
             hatch="////", label="its range over runs")
    ax_b.set_title("(b) Governed against ungoverned, C3", loc="left", fontsize=FONT + 1, pad=14)
    ax_c = ax_b.twinx()
    c_lo = [values["b"][k]["claims"][0] for k in keys]
    c_hi = [values["b"][k]["claims"][1] for k in keys]
    ax_c.vlines(xs, c_lo, c_hi, color="black", linewidth=1.2)
    ax_c.plot(xs, c_hi, "o", color="black", markersize=3.5, markerfacecolor="white", markeredgewidth=0.8,
              label="claims allowed, ungoverned")
    ax_c.plot(xs, c_lo, "o", color="black", markersize=3.5, markerfacecolor="white", markeredgewidth=0.8)
    ax_c.set_ylim(0, 4)
    ax_c.set_yticks([0, 1, 2, 3, 4])
    ax_c.set_ylabel("claims allowed (count per run)", fontsize=FONT)
    handles = ax_b.get_legend_handles_labels()[0] + ax_c.get_legend_handles_labels()[0][:1]
    ax_b.legend(handles=handles, loc="lower right", bbox_to_anchor=(1.0, 1.0), ncol=3, frameon=False,
                fontsize=FONT - 0.5)

    for ax, ylabel in ((ax_a, "share"), (ax_b, "share")):
        ax.set_ylim(0, 1)
        ax.set_ylabel(ylabel, fontsize=FONT)
        ax.set_xticks(xs, labels, fontsize=FONT - 0.5)
        ax.spines["top"].set_visible(False)
    ax_a.spines["right"].set_visible(False)
    ax_c.spines["top"].set_visible(False)

    fig.text(0.09, 0.535, "\n".join(textwrap.wrap(CAPTION_A, 100)), ha="left", va="top", fontsize=FONT)
    fig.text(0.09, 0.045, "\n".join(textwrap.wrap(CAPTION_B, 100)), ha="left", va="top", fontsize=FONT)
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=REPO / "docs" / "fig")
    args = parser.parse_args()
    values = read_values()
    args.out.mkdir(parents=True, exist_ok=True)
    fig = draw(values)
    fig.savefig(args.out / f"{STEM}.png", dpi=300, metadata={"Software": None})
    fig.savefig(args.out / f"{STEM}.svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)
    print(f"wrote {args.out / STEM}.png and .svg")


if __name__ == "__main__":
    main()
