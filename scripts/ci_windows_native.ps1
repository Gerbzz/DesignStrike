param(
    [Parameter(Mandatory)][string]$Executable,
    [Parameter(Mandatory)][string]$Output
)

$ErrorActionPreference = 'Stop'
$binary = [System.IO.Path]::GetFullPath($Executable)
$directory = [System.IO.Path]::GetFullPath($Output)
New-Item -ItemType Directory -Force -Path $directory | Out-Null
if (!(Test-Path -LiteralPath $binary)) { throw 'The native editor must be built first.' }

$start = [System.Diagnostics.ProcessStartInfo]::new($binary)
$start.ArgumentList.Add('--control')
$start.ArgumentList.Add('18950')
$start.UseShellExecute = $false
$start.Environment['DESIGNCRAFT_CONFIG_DIR'] = (Join-Path $directory 'profile')
$process = [System.Diagnostics.Process]::Start($start)
if ($null -eq $process) { throw 'Windows did not start the publication editor.' }

try {
    python scripts/ci_designstrike_native.py $directory $process.Id
    if ($LASTEXITCODE -ne 0) { throw 'Native publication creation and screenshot workflow failed.' }
    $process.Refresh()
    if ($process.HasExited) { throw "Editor exited after the native workflow: $($process.ExitCode)." }
    [ordered]@{
        platform = 'windows-2025'
        process_running = $true
        native_control_workflow = 'passed'
        screenshots = 'running app ui.screenshot'
        main_window_handle = $process.MainWindowHandle.ToInt64()
    } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $directory 'desktop-status.json')
}
catch {
    [ordered]@{
        platform = 'windows-2025'
        process_running = !$process.HasExited
        native_control_workflow = 'failed'
        error = $_.Exception.Message
        main_window_handle = $process.MainWindowHandle.ToInt64()
    } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $directory 'desktop-status.json')
    throw
}
finally {
    if (!$process.HasExited) { $process.Kill() }
    $process.Dispose()
}
