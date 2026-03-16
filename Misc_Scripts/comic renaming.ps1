# Ask for the folder path
$folderPath = Read-Host "Enter the folder path containing the JPG files"

# Validate if the folder path exists
if (-Not (Test-Path -Path $folderPath -PathType Container)) {
    Write-Host "The folder path is not valid." -ForegroundColor Red
    exit
}

# Ask for the string to replace the file names
$newString = Read-Host "Enter the string to replace the filenames (except the three-digit number)"

# Get all JPG files in the folder
$jpgFiles = Get-ChildItem -Path $folderPath -Filter "*.jpg"

# Regular expression pattern to match filenames ending in a space followed by a three-digit number
$pattern = ".* (?<number>\d{3})\.jpg"

# Iterate through each file and rename it
foreach ($file in $jpgFiles) {
    if ($file.Name -match $pattern) {
        $number = $matches['number']
        $newFileName = "$newString $number.jpg"
        $newFilePath = Join-Path -Path $folderPath -ChildPath $newFileName
        Rename-Item -Path $file.FullName -NewName $newFileName
    } else {
        Write-Host "The file '$($file.Name)' does not match the expected pattern." -ForegroundColor Yellow
    }
}

Write-Host "Renaming completed."
