"""README order 2026-11-08 (readme-top): the short top part a judge reads first, copied word for word."""
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
README = (REPO / "README.md").read_text(encoding="utf-8")
TOP = README.split("## For the reviewer", 1)[0]

BLOCK = [
    "Mizan is a consumer-care AI for a phone company, tested on written scenarios with a fictional UAE operator, not on "
    "live customers. The AI proposes each step of a conversation; code written from binding UAE law (the gates) allows "
    "it, holds it for a staff member or blocks it, in Arabic and English, and every step goes into a log that anyone "
    "can replay.",
    "Five agents: the care agent talks to the customer, the adviser checks the law, and two agents play the regulators, "
    "TDRA and the Data Office. These four are AI. The fifth, the coordinator, is plain code that routes each step.",
    "![The runs page: scenario S1, step 3, held for a staff member, with the gate's reason]"
    "(docs/site/screenshots/runs-S1-step3-held.png)",
    "Watch the 7-minute film: [https://youtu.be/_hSZLOfSAs0](https://youtu.be/_hSZLOfSAs0) (in YouTube, set Quality to 1080p HD)",
    "See the runs: [https://shra1m.github.io/onyx-hackathon-build/site/runs.html]"
    "(https://shra1m.github.io/onyx-hackathon-build/site/runs.html)",
    "Read the report: [docs/report.pdf](docs/report.pdf)",
    "In each of the five scored scenarios, one move was written into the test by the team, not proposed by the AI, to "
    "check the gate: S1 step 6, S2 step 5, S3 step 3, S4 step 5, S5 step 4. The runs page marks each one; the report's "
    "annex lists them.",
]


def test_top_block_is_in_order_above_the_reviewer_section():
    at = [TOP.index(line + "\n") for line in BLOCK]
    assert at == sorted(at)
    assert "synthetic UAE operator:" not in README
    assert (REPO / "docs/site/screenshots/runs-S1-step3-held.png").is_file()
    assert (REPO / "docs/site/runs.html").is_file() and (REPO / "docs/report.pdf").is_file()
