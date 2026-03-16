# Prompt for the folder containing the JPG files
$folderPath = Read-Host "Please enter the folder path containing the JPG files"

# Check if the folder exists
if (-Not (Test-Path -Path $folderPath)) {
    Write-Host "The folder path does not exist. Please check the path and try again."
    exit
}

# Prompt for the general location
$generalLocation = Read-Host "What is the general location?"

# Prompt for the specific location
$specificLocation = Read-Host "What is the specific location?"

# Get all JPG files in the folder
$jpgFiles = Get-ChildItem -Path $folderPath -Filter "*.jpg" | Sort-Object Name

# Check if there are any JPG files in the folder
if ($jpgFiles.Count -eq 0) {
    Write-Host "No JPG files found in the specified folder."
    exit
}

# Initialize the counter
$counter = 1
$lastCounter = 0

# Rename the files
foreach ($file in $jpgFiles) {
    if ($file.Name -like "*_no_license_plate.jpg") {
        # Use the same counter as the last image for files with "_no_license_plate"
        $newFileName = "{0}_{1}_{2}_no_license_plate_©QldGovt.jpg" -f $generalLocation, $specificLocation, $lastCounter
    } else {
        # Use the current counter and then increment it
        $newFileName = "{0}_{1}_{2}_©QldGovt.jpg" -f $generalLocation, $specificLocation, $counter
        $lastCounter = $counter
        $counter++
    }
    $newFilePath = Join-Path -Path $folderPath -ChildPath $newFileName

    Rename-Item -Path $file.FullName -NewName $newFileName
}

Write-Host "Files have been renamed successfully."
