param(
    [Parameter(Mandatory = $true)]
    [string]$Source
)

$lines = Get-Content -LiteralPath $Source -Encoding UTF8
$storyStart = [Array]::IndexOf($lines, '# FMA 동양편 — STORYLINE MASTER')
$specStart = [Array]::IndexOf($lines, '# FMA 동양편 — STORY DASHBOARD MASTER SPEC')
$storyEnd = [Array]::IndexOf($lines, 'END.')
$specEnd = [Array]::IndexOf($lines, '```', $specStart)
while ($specEnd -ge 0 -and $specEnd + 1 -lt $lines.Count -and $lines[$specEnd + 1] -match '^\s*$') {
    $nextFence = [Array]::IndexOf($lines, '```', $specEnd + 1)
    if ($nextFence -lt 0) { break }
    $specEnd = $nextFence
}

if ($storyStart -lt 0 -or $specStart -lt 0 -or $storyEnd -lt $storyStart) {
    throw '두 문서의 경계를 찾지 못했습니다.'
}

# 문서 2의 마지막 코드 블록은 파일 끝에 가장 가까운 닫는 펜스다.
$specEnd = ($lines | Select-String '^```$' | Where-Object LineNumber -gt ($specStart + 1) | Select-Object -Last 1).LineNumber - 1

$story = ($lines[$storyStart..$storyEnd] -join "`n").TrimEnd() + "`n"
$spec = ($lines[$specStart..$specEnd] -join "`n").TrimEnd() + "`n"

[System.IO.File]::WriteAllText((Join-Path $PSScriptRoot '..\private\STORYLINE_MASTER_v2.0.md'), $story, [System.Text.UTF8Encoding]::new($false))
[System.IO.File]::WriteAllText((Join-Path $PSScriptRoot '..\private\STORY_DASHBOARD_SPEC_v2.0.md'), $spec, [System.Text.UTF8Encoding]::new($false))

Write-Output "스토리라인 $($story.Length)자, 검증 규칙 $($spec.Length)자를 저장했습니다."
