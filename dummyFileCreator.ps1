param (
[Parameter(Mandatory=$true)][string]$from,
[Parameter(Mandatory=$true)][string]$to,
[Parameter(Mandatory=$true)][string]$size
)

$sw = [Diagnostics.Stopwatch]::StartNew()

Write-Host $from
Write-Host $to
Write-Host $size

$filePath = ((Get-Item -Path $from).FullName)
Write-Host $filePath

DO
{

    $temp = [IO.file]::ReadAllText($filePath)
    DO
    {
    $temp += $temp
    } While ($temp.length -lt 10000)

$temp | Out-File -append $to -NoNewLine
Write-Host -NoNewLine ((Get-Item $to).length/1MB) 'MB' `r

} While ((Get-Item $to).length -lt $size)

$sw.Stop()
Write-Host $sw.Elapsed
