Add-Type -AssemblyName System.Drawing
$imgSrc = "C:/Users/samee/.gemini/antigravity-ide/brain/c6f55c58-5974-4893-85ed-148af2bc9e2b/.user_uploaded/media_1789994591146.png"
$bmp = New-Object System.Drawing.Bitmap($imgSrc)

$minX = 1000
$maxX = 0
$minY = 41
$maxY = 226

for ($y = $minY; $y -le $maxY; $y++) {
    for ($x = 350; $x -lt 670; $x++) {
        $c = $bmp.GetPixel($x, $y)
        if ($c.R -lt 240 -or $c.G -lt 240 -or $c.B -lt 240) {
            if ($x -lt $minX) { $minX = $x }
            if ($x -gt $maxX) { $maxX = $x }
        }
    }
}

$x0 = [Math]::Max(0, $minX - 2)
$y0 = [Math]::Max(0, $minY - 2)
$w = ($maxX - $minX) + 4
$h = ($maxY - $minY) + 4

$rect = New-Object System.Drawing.Rectangle($x0, $y0, $w, $h)
$crop = $bmp.Clone($rect, $bmp.PixelFormat)
$outPath = "c:\Users\samee\Downloads\expenso\scripts\aietm_logo.png"
$crop.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)
$webPath = "c:\Users\samee\Downloads\expenso\apps\web\public\aietm_logo.png"
$crop.Save($webPath, [System.Drawing.Imaging.ImageFormat]::Png)
Write-Host "Perfect crop saved to $outPath and $webPath ($w x $h)"
