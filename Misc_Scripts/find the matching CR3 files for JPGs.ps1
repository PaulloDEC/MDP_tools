# Prompt user for input folder path, list file path, and output folder path
$inputFolderPath = Read-Host "Enter the input folder path"
$listFilePath = Read-Host "Enter the path of the file containing the list of filenames"
$outputFolderPath = Read-Host "Enter the output folder path"

# Check if input and output folder paths are valid
if (-not (Test-Path -Path $inputFolderPath -PathType Container)) {
    Write-Host "Invalid input folder path. Exiting script."
    Exit
}
if (-not (Test-Path -Path $outputFolderPath -PathType Container)) {
    Write-Host "Invalid output folder path. Exiting script."
    Exit
}

# Check if list file path is valid
if (-not (Test-Path -Path $listFilePath -PathType Leaf)) {
    Write-Host "Invalid list file path. Exiting script."
    Exit
}

# Read list of filenames from the list file
$filenames = Get-Content -Path $listFilePath

# Iterate through each filename in the list
foreach ($filename in $filenames) {
    $filename = $filename.Trim()  # Trim whitespace from filename
    Write-Host "Searching for file: $filename"
    
    # Search for files matching the filename pattern in the input folder
    $matchingFiles = Get-ChildItem -Path $inputFolderPath -Filter $filename -File
    
    if ($matchingFiles.Count -eq 0) {
        Write-Host "No matching file found for: $filename"
    }
    
    # Copy matching files to the output folder
    foreach ($file in $matchingFiles) {
        $destinationPath = Join-Path -Path $outputFolderPath -ChildPath $file.Name
        Copy-Item -Path $file.FullName -Destination $destinationPath -Force
        Write-Host "Copied $($file.Name) to $($destinationPath)"
    }
}

Write-Host "File copying process completed."
