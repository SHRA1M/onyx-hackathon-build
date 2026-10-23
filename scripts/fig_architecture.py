"""Figure 1 (order 2026-10-22-task-17-figures item 1, Task 18 item 3): Mizan on the Y.3172 nodes, black and white,
landscape, 16 cm wide by 4.5 cm tall; the caption is the Word caption under it, not drawn here.

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

# the drawing works in centimetres, one data unit per cm
WIDTH_CM, HEIGHT_CM = 16, 4.5
FONT = 6.5


def _box(ax, x, y, w, h, node, *, dashed=False, bold_edge=False, inline=False):
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor="black", linewidth=1.4 if bold_edge else 0.8,
                           linestyle=(0, (3, 2)) if dashed else "solid"))
    if inline:
        # a wide box: the node name at the left, its line after it
        ax.text(x + 0.15, y + h / 2, node, ha="left", va="center", fontsize=FONT, fontweight="bold")
        ax.text(x + 0.3 + 0.17 * len(node), y + h / 2, NODES[node], ha="left", va="center", fontsize=FONT)
        return
    ax.text(x + w / 2, y + h - 0.12, node, ha="center", va="top", fontsize=FONT, fontweight="bold")
    ax.text(x + w / 2, y + 0.1, "\n".join(textwrap.wrap(NODES[node], 14, break_on_hyphens=False)), ha="center", va="bottom",
            fontsize=FONT, linespacing=1.05)


def _arrow(ax, start, end, *, dashed=False, style="arc3"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=7, color="black", linewidth=0.8,
                                 linestyle=(0, (3, 2)) if dashed else "solid", shrinkA=0, shrinkB=0,
                                 connectionstyle=style))


def draw() -> plt.Figure:
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.hashsalt": "mizan-fig1", "svg.fonttype": "none"})
    fig = plt.figure(figsize=(WIDTH_CM / 2.54, HEIGHT_CM / 2.54))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, WIDTH_CM)
    ax.set_ylim(0, HEIGHT_CM)
    ax.axis("off")

    left, right, gap = 0.7, 15.95, 0.25
    bw = (right - left - gap * (len(CHAIN) - 1)) / len(CHAIN)
    cy, ch = 1.4, 1.35
    xs = {node: left + i * (bw + gap) for i, node in enumerate(CHAIN)}

    mlfo_y = 3.65
    _box(ax, 0.1, mlfo_y, right - 0.1, 0.75, "MLFO", inline=True)
    for i, node in enumerate(CHAIN):
        _box(ax, xs[node], cy, bw, ch, node, bold_edge=node == "P")
        if i:
            _arrow(ax, (xs[CHAIN[i - 1]] + bw, cy + ch / 2), (xs[node], cy + ch / 2))
    _arrow(ax, (xs["SRC"] + bw / 2, mlfo_y), (xs["SRC"] + bw / 2, cy + ch), dashed=True)

    sx, sy, sh = xs["C"], 0.1, 0.7
    _box(ax, sx, sy, xs["M"] + bw - sx, sh, "ML sandbox", dashed=True, inline=True)
    _arrow(ax, (0.4, mlfo_y), (sx, sy + sh / 2), dashed=True, style="angle,angleA=-90,angleB=180,rad=0")

    d_mid = xs["D"] + bw / 2
    _arrow(ax, (d_mid, cy), (d_mid, 0.2))
    ax.text(d_mid + 0.12, 0.2, "\n".join(textwrap.wrap(HANDOVER, 16, break_on_hyphens=False)), ha="left", va="bottom", fontsize=FONT,
            fontstyle="italic", linespacing=1.05)
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
