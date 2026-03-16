# Prompt user for folder path
$folderPath = Read-Host "Enter the folder path"

# Check if folder path is valid
if (-not (Test-Path -Path $folderPath -PathType Container)) {
    Write-Host "Invalid folder path. Exiting script."
    Exit
}

# Get list of files in the folder
$files = Get-ChildItem -Path $folderPath | Where-Object { -not $_.PSIsContainer }

# Create a new .txt file to store the list of files
$outputFilePath = "$folderPath\FilesList.txt"

# Modify filenames to change ".jpg" extensions to ".CR3" extensions
$modifiedFilenames = $files.Name -replace '\.jpg$', '.CR3'

# Write modified list of filenames to the .txt file
$modifiedFilenames | Out-File -FilePath $outputFilePath

Write-Host "List of filenames with modified extensions has been saved to: $outputFilePath"
