"""Order 2026-11-02 Task 38 item 5: print the PDF's page count and whether its text holds "Annex A" and "Limits and
next steps"; Task 41: and "Annex F". Called by scripts/report_pdf.ps1.

    uv run python scripts/check_pdf.py docs/report.pdf
"""

import sys

from pypdf import PdfReader

reader = PdfReader(sys.argv[1])
flat = " ".join(" ".join(page.extract_text() or "" for page in reader.pages).split())
print(f"pdf pages: {len(reader.pages)}")
for needle in ("Annex A", "Limits and next steps", "Annex F"):  # Annex F: Task 41
    print(f"pdf finds {needle!r}: {needle in flat}")
