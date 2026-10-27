param(
  [string]$Pptx = "E:\Claude\laborforce-deck\LaborForce_CookCountyHealth.pptx",
  [string]$OutDir = "C:\Users\Harvey\AppData\Local\Temp\claude\E--Claude\03439a39-1f73-415c-8215-fbb7bf35ab8b\scratchpad\render",
  [string]$Pdf = "E:\Claude\laborforce-deck\LaborForce_CookCountyHealth.pdf"
)
# 1) exports every slide to PNG (1920 x 1080) for the visual check
# 2) exports the deck to PDF next to the PPTX: slides only (no notes), hidden slides excluded,
#    print-quality intent, fonts embedded by PowerPoint's PDF writer
if (Test-Path $OutDir) { Remove-Item "$OutDir\*.png" -Force -ErrorAction SilentlyContinue } else { New-Item -ItemType Directory -Force $OutDir | Out-Null }
$app = New-Object -ComObject PowerPoint.Application
try {
  $pres = $app.Presentations.Open($Pptx, $true, $false, $false)  # ReadOnly, Untitled, WithWindow
  $n = $pres.Slides.Count
  $shown = 0
  for ($i = 1; $i -le $n; $i++) {
    $sl = $pres.Slides.Item($i)
    if ($sl.SlideShowTransition.Hidden -eq -1) { continue }   # hidden scenario pages are not rendered
    $shown++
    $out = Join-Path $OutDir ("slide-{0:D2}.png" -f $shown)
    $sl.Export($out, "PNG", 1920, 1080)
  }
  Write-Output "Rendered $shown visible slides (of $n) to $OutDir"
  if ($Pdf) {
    if (Test-Path $Pdf) { Remove-Item $Pdf -Force }
    $pres.PrintOptions.PrintHiddenSlides = 0   # PDF = visible slides only
    # ExportAsFixedFormat(Path, FixedFormatType=ppFixedFormatTypePDF(2), Intent=ppFixedFormatIntentPrint(2),
    #   FrameSlides=0, HandoutOrder=1, OutputType=ppPrintOutputSlides(1), PrintHiddenSlides=0, PrintRange=[Type]::Missing,
    #   RangeType=ppPrintAll(1), SlideShowName="", IncludeDocProperties, KeepIRMSettings, DocStructureTags,
    #   BitmapMissingFonts, UseISO19005_1)
    $missing = [Type]::Missing
    try {
      $pres.ExportAsFixedFormat($Pdf, 2, 2, 0, 1, 1, 0, $missing, 1, "", $true, $true, $true, $true, $false)
    } catch {
      Write-Output ("ExportAsFixedFormat failed (" + $_.Exception.Message.Trim() + "); falling back to SaveAs ppSaveAsPDF")
      $pres.SaveAs($Pdf, 32)   # ppSaveAsPDF
    }
    $size = (Get-Item $Pdf).Length
    Write-Output ("PDF: {0} ({1:N0} bytes)" -f $Pdf, $size)
  }
  $pres.Close()
} finally {
  $app.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
