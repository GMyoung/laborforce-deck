param([string]$Pptx = "E:\Claude\laborforce-deck\LaborForce_CookCountyHealth.pptx")
# Adds a native entrance sequence to slide 4: each slab fades in together with its function row,
# layer 01 on click, layers 02-05 after the previous one. Everything stays editable in PowerPoint.
$msoAnimEffectFade = 10
$OnClick = 1; $WithPrevious = 2; $AfterPrevious = 3
$app = New-Object -ComObject PowerPoint.Application
try {
  $pres = $app.Presentations.Open($Pptx, $false, $false, $false)
  $slide = $pres.Slides.Item(4)
  $seq = $slide.TimeLine.MainSequence
  while ($seq.Count -gt 0) { $seq.Item(1).Delete() }
  $byName = @{}
  foreach ($sh in $slide.Shapes) { $byName[$sh.Name] = $sh }
  for ($n = 1; $n -le 5; $n++) {
    $names = @("slab-$n-left", "slab-$n-right", "slab-$n-top", "slab-$n-num", "fn-$n-card", "fn-$n-badge", "fn-$n-badgenum", "fn-$n-title", "fn-$n-desc")
    if ($n -lt 5) { $names += @("slab-$n-link", "slab-$n-drop") }
    $first = $true
    foreach ($nm in $names) {
      if (-not $byName.ContainsKey($nm)) { Write-Output "missing shape $nm"; continue }
      $trigger = if ($first) { if ($n -eq 1) { $OnClick } else { $AfterPrevious } } else { $WithPrevious }
      $eff = $seq.AddEffect($byName[$nm], $msoAnimEffectFade, 0, $trigger)
      $eff.Timing.Duration = 0.5
      if ($first -and $n -gt 1) { $eff.Timing.TriggerDelayTime = 0.15 }
      $first = $false
    }
  }
  Write-Output ("effects on slide 4: " + $seq.Count)
  $pres.Save()
  $pres.Close()
} finally {
  $app.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
