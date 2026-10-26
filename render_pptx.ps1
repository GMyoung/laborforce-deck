param([string]$Pptx = "E:\Claude\laborforce-deck\LaborForce_CookCountyHealth.pptx", [string]$OutDir = "C:\Users\Harvey\AppData\Local\Temp\claude\E--Claude\03439a39-1f73-415c-8215-fbb7bf35ab8b\scratchpad\render")
if (Test-Path $OutDir) { Remove-Item "$OutDir\*.png" -Force -ErrorAction SilentlyContinue } else { New-Item -ItemType Directory -Force $OutDir | Out-Null }
$app = New-Object -ComObject PowerPoint.Application
try {
  $pres = $app.Presentations.Open($Pptx, $true, $false, $false)  # ReadOnly, Untitled, WithWindow
  $n = $pres.Slides.Count
  for ($i = 1; $i -le $n; $i++) {
    $out = Join-Path $OutDir ("slide-{0:D2}.png" -f $i)
    $pres.Slides.Item($i).Export($out, "PNG", 1920, 1080)
  }
  $pres.Close()
  Write-Output "Rendered $n slides to $OutDir"
} finally {
  $app.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
