# Order 2026-10-23-task-12-report-build item 4: open docs/report.docx in Word (COM), print its page count
# (ComputeStatistics(2)) and word count (ComputeStatistics(0)); over five pages, also the first sentence on page 6.
# Task 38 item 4: with the annex, "pages" and "words" are the main text's (everything before the "Annex" heading),
# then "annex starts on page", "total pages" and "total words".
# Read only; Word quits at the end. Word must be installed, so CI does not run this.
#
#     powershell -ExecutionPolicy Bypass -File scripts/report_pages.ps1 [-Path docs/report.docx]
param([string]$Path = (Join-Path $PSScriptRoot "..\docs\report.docx"))

$full = (Resolve-Path $Path).Path
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($full, $false, $true)  # ConfirmConversions false, ReadOnly true
    $doc.Repaginate()
    $total = $doc.ComputeStatistics(2)
    $annex = $null
    foreach ($p in $doc.Paragraphs) {
        if ($p.Range.Text.Trim() -eq "Annex") { $annex = $p.Range; break }
    }
    if ($annex) {
        $annexPage = $annex.Information(3)  # wdActiveEndPageNumber
        $main = $doc.Range(0, $annex.Start)
        $pages = $annexPage - 1
        $words = $main.ComputeStatistics(0)
    } else {
        $pages = $total
        $words = $doc.ComputeStatistics(0)
    }
    Write-Output "pages: $pages"
    Write-Output "words: $words"
    if ($annex) {
        Write-Output "annex starts on page: $annexPage"
        Write-Output "total pages: $total"
        Write-Output "total words: $($doc.ComputeStatistics(0))"
    }
    if ($pages -gt 5) {
        $range = $doc.GoTo(1, 1, 6)  # wdGoToPage, wdGoToAbsolute, page 6
        $range.Expand(3) | Out-Null  # wdSentence
        Write-Output "first sentence on page 6: $($range.Text.Trim())"
    }
    $doc.Close(0)
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
