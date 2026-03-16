# Define the directory containing the files
$directory = "X:\Queensland Parks 2024\MAY Byfield and Blackdown\Trip 3\rename and reorganise\processed"

# Check if the directory exists
if (-not (Test-Path -Path $directory -PathType Container)) {
    Write-Host "The specified directory does not exist."
    exit
}

# Prompt for the first filename (without .jpg)
$filename1 = Read-Host "Enter the first filename (without .jpg)"

# Prompt for the second filename (without .jpg)
$filename2 = Read-Host "Enter the second filename (without .jpg)"

# Append .jpg to the filenames
$filename1 = "$filename1.jpg"
$filename2 = "$filename2.jpg"

# Prompt for the new folder name
$newFolder = Read-Host "Enter the name for the new folder"

# Create the full path for the new folder
$newFolderPath = Join-Path -Path $directory -ChildPath $newFolder

# Create the new folder if it doesn't exist
if (-not (Test-Path -Path $newFolderPath -PathType Container)) {
    New-Item -Path $newFolderPath -ItemType Directory | Out-Null
}

# Get all .jpg files in the specified directory
$files = Get-ChildItem -Path $directory -Filter "*.jpg" -File

# Sort filenames in alphabetical order
$sortedFiles = $files | Sort-Object Name

# Determine the range based on the provided filenames
$startMoving = $false

foreach ($file in $sortedFiles) {
    if ($file.Name -ge $filename1 -and $file.Name -le $filename2) {
        $startMoving = $true
    }
    
    if ($startMoving) {
        if ($file.Name -ge $filename1 -and $file.Name -le $filename2) {
            Move-Item -Path $file.FullName -Destination $newFolderPath
        } else {
            break
        }
    }
}
