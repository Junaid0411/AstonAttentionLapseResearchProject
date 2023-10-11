# Start recording in Pupil Capture
$recordCommand = "C:\Users\scrim\AppData\Local\Programs\Python\Python311\python.exe"
$recordScript = "record_capture.py"
$recordProcess = Start-Process -NoNewWindow -PassThru -FilePath $recordCommand -ArgumentList $recordScript

$duration = 300

$durationString = $duration.ToString("F2")  # Format the duration as a float with 2 decimal places
Write-Host "Recording duration: $durationString seconds"

# Wait for the specified duration
Start-Sleep -Seconds $duration

# Stop recording in Pupil Capture
$stopCommand = "C:\Users\scrim\AppData\Local\Programs\Python\Python311\python.exe"
$stopScript = "stop_record_capture.py"
Start-Process -NoNewWindow -FilePath $stopCommand -ArgumentList $stopScript

# Check if the sound recording process is still running before waiting for it
if ($soundRecordingProcess -ne $null -and !$soundRecordingProcess.HasExited) {
    Wait-Process -Id $soundRecordingProcess.Id | Out-Null
}
