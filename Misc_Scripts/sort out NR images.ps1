# Prompt the user for the folder path
$folderPath = Read-Host "Enter the path to the folder containing the JPG files"

# Create the 'originals' folder if it doesn't exist
$originalsFolder = Join-Path -Path $folderPath -ChildPath "originals"
if (-not (Test-Path -Path $originalsFolder)) {
    New-Item -ItemType Directory -Path $originalsFolder
}

# Get all JPG files in the folder
$jpgFiles = Get-ChildItem -Path $folderPath -Filter *.jpg

# Loop through each file
foreach ($file in $jpgFiles) {
    # Check if the file has a noise reduced version
    $enhancedNRFile = $file.FullName.Replace(".jpg", "-Enhanced-NR.jpg")
    if (Test-Path -Path $enhancedNRFile) {
        # Move the original file to the 'originals' folder
        $destinationPath = Join-Path -Path $originalsFolder -ChildPath $file.Name
        Move-Item -Path $file.FullName -Destination $destinationPath
    }
}
