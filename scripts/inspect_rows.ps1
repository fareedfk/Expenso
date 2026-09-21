Add-Type -AssemblyName System.Drawing
$imgSrc = "C:/Users/samee/.gemini/antigravity-ide/brain/c6f55c58-5974-4893-85ed-148af2bc9e2b/.user_uploaded/media_1789994591146.png"
$bmp = New-Object System.Drawing.Bitmap($imgSrc)

# Notice A.I.E.T.M ribbon ends around y = 226
# Let's verify each row from 210 to 240
for ($y = 210; $y -lt 240; $y++) {
    $colored = 0
    for ($x = 350; $x -lt 670; $x++) {
        $c = $bmp.GetPixel($x, $y)
        if ($c.R -lt 240 -or $c.G -lt 240 -or $c.B -lt 240) {
            $colored++
        }
    }
    Write-Host "Row $y has $colored colored pixels"
}
