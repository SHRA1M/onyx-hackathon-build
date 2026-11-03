# Order 2026-11-02 Task 38 item 5: export docs/report.docx to docs/report.pdf from Word (COM ExportAsFixedFormat,
# PDF, optimise for print), then check with pypdf that the PDF's page count equals Word's and that its text holds
# "Annex A" and "Limits and next steps". Prints Word's pages, the PDF's pages, the two finds and the file size.
# Word must be installed, so CI does not run this. The PDF is what ITU receives.
#
#     powershell -ExecutionPolicy Bypass -File scripts/report_pdf.ps1 [-Path docs/report.docx] [-Out docs/report.pdf]
param([string]$Path = (Join-Path $PSScriptRoot "..\docs\report.docx"),
      [string]$Out = (Join-Path $PSScriptRoot "..\docs\report.pdf"))

$full = (Resolve-Path $Path).Path
$pdf = [System.IO.Path]::GetFullPath($Out)
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($full, $false, $true)  # ConfirmConversions false, ReadOnly true
    $doc.Repaginate()
    $wordPages = $doc.ComputeStatistics(2)
    $doc.ExportAsFixedFormat($pdf, 17, $false, 0)  # wdExportFormatPDF, OpenAfterExport false, wdExportOptimizeForPrint
    $doc.Close(0)
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
Write-Output "word pages: $wordPages"
$pdfPages = $null
uv run python (Join-Path $PSScriptRoot "check_pdf.py") $pdf | ForEach-Object { Write-Output $_; if ($_ -match '^pdf pages: (\d+)') { $pdfPages = [int]$Matches[1] } }
Write-Output "pdf bytes: $((Get-Item $pdf).Length)"
if ($pdfPages -ne $wordPages) { Write-Output "STOP: the PDF has $pdfPages pages, Word has $wordPages"; exit 1 }
