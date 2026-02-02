# EBS Morning Automation - Windows Task Scheduler Setup
# Run this script as Administrator

$TaskName = "EBS Morning Automation"
$PythonPath = "python"
$ScriptPath = "C:\claude\ebs\tools\morning-automation\main.py"
$WorkingDir = "C:\claude\ebs\tools\morning-automation"

# Arguments: incremental collection + report + notify
$Arguments = "$ScriptPath --notify"

# Remove existing task if exists
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing task: $TaskName"
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create scheduled task
Write-Host "Creating scheduled task: $TaskName"

# Trigger: Daily at 9:00 AM
$Trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM

# Action: Run Python script
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument $Arguments -WorkingDirectory $WorkingDir

# Settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register task
Register-ScheduledTask -TaskName $TaskName -Trigger $Trigger -Action $Action -Settings $Settings -Description "EBS 프로젝트 아침 자동화 - 매일 09:00 Slack/Gmail 수집 및 브리핑 생성"

Write-Host ""
Write-Host "Task created successfully!"
Write-Host "  Name: $TaskName"
Write-Host "  Schedule: Daily at 9:00 AM"
Write-Host "  Script: $ScriptPath"
Write-Host ""
Write-Host "To run manually: schtasks /run /tn `"$TaskName`""
Write-Host "To check status: schtasks /query /tn `"$TaskName`""
