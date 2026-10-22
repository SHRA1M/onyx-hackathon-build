"""Figure 1 (order 2026-10-22-task-17-figures item 1): Mizan on the Y.3172 nodes, black and white, 8 cm wide.

Each box carries the node as the README mapping table names it and one short line from its "in Mizan" column
(tests/test_figures.py checks every label against the table). Writes docs/fig/fig1-architecture.png and .svg;
a second run writes the same bytes.

    uv run python scripts/fig_architecture.py [--out docs/fig]
"""

import argparse
import io
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
STEM = "fig1-architecture"

NODES = {
    "MLFO": "the coordinator's staged release of steps",
    "SRC": "the scenario injects",
    "C": "each agent's inbox",
    "PP": "mandate-scoped retrieval",
    "M": "it proposes, never decides",
    "P": "the gates, plain code",
    "D": "the human hand-over",
    "SINK": "the hash-chained audit log",
    "ML sandbox": "the governed-versus-ungoverned run",
}
CHAIN = ["SRC", "C", "PP", "M", "P", "D", "SINK"]
HANDOVER = "hand-over to a human (gap-8)"
CAPTION = "Mizan on the Y.3172 nodes; the model proposes, the P node decides, D hands a complaint to a person."

WIDTH_IN = 8 / 2.54
FONT = 6.5


def _box(ax, x, y, w, h, node, *, dashed=False, bold_edge=False):
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor="black", linewidth=1.4 if bold_edge else 0.8,
                           linestyle=(0, (3, 2)) if dashed else "solid"))
    label = "\n".join(textwrap.wrap(NODES[node], 22 if w < 4 else 60))
    ax.text(x + w / 2, y + h - 0.28, node, ha="center", va="top", fontsize=FONT, fontweight="bold")
    ax.text(x + w / 2, y + 0.22, label, ha="center", va="bottom", fontsize=FONT - 0.5, linespacing=1.1)


def _arrow(ax, start, end, *, dashed=False):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=7, color="black", linewidth=0.8,
                                 linestyle=(0, (3, 2)) if dashed else "solid", shrinkA=0, shrinkB=0))


def draw() -> plt.Figure:
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.hashsalt": "mizan-fig1", "svg.fonttype": "none"})
    fig = plt.figure(figsize=(WIDTH_IN, 5.0))
    ax = fig.add_axes((0.02, 0.10, 0.96, 0.89))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 17.6)
    ax.axis("off")

    cx, cw, bh, gap = 0.2, 5.6, 1.45, 0.55
    top = 14.4

    _box(ax, 0.2, top + 1.6, 9.6, bh, "MLFO")
    ys = {}
    for i, node in enumerate(CHAIN):
        y = top - (i + 1) * (bh + gap) + gap
        ys[node] = y
        _box(ax, cx, y, cw, bh, node, bold_edge=node == "P")
        if i:
            _arrow(ax, (cx + cw / 2, ys[CHAIN[i - 1]]), (cx + cw / 2, y + bh))
    _arrow(ax, (cx + cw / 2, top + 1.6), (cx + cw / 2, ys["SRC"] + bh), dashed=True)

    sx, sw = 6.4, 3.4
    sy = ys["M"] + (ys["PP"] - ys["M"]) / 2
    _box(ax, sx, sy, sw, bh + 0.3, "ML sandbox", dashed=True)
    _arrow(ax, (sx + sw / 2, top + 1.6), (sx + sw / 2, sy + bh + 0.3), dashed=True)

    d_mid = ys["D"] + bh / 2
    _arrow(ax, (cx + cw, d_mid), (9.8, d_mid))
    ax.text(cx + cw + 0.2, d_mid + 0.15, "\n".join(textwrap.wrap(HANDOVER, 20)), ha="left", va="bottom",
            fontsize=FONT - 0.5, fontstyle="italic", linespacing=1.1)

    fig.text(0.5, 0.015, "\n".join(textwrap.wrap(CAPTION, 62)), ha="center", va="bottom", fontsize=FONT,
             linespacing=1.2)
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=REPO / "docs" / "fig")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    fig = draw()
    fig.savefig(args.out / f"{STEM}.png", dpi=300, metadata={"Software": None})
    svg = io.BytesIO()
    fig.savefig(svg, format="svg", metadata={"Date": None, "Creator": None})
    (args.out / f"{STEM}.svg").write_bytes(svg.getvalue().replace(b"\r\n", b"\n"))  # LF on every machine
    plt.close(fig)
    print(f"wrote {args.out / STEM}.png and .svg")


if __name__ == "__main__":
    main()
