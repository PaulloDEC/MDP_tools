# Define the path to the directory
$directoryPath = "X:\Queensland Parks 2024\MAY Byfield and Blackdown\Trip 3\rename and reorganise\processed"

# Function to remove all spaces from a filename
function Remove-SpacesFromFileName {
    param (
        [string]$fileName
    )

    # Remove all spaces from the filename
    $newFileName = $fileName -replace " ", ""
    return $newFileName
}

# Get all files in the specified directory and its subdirectories
$files = Get-ChildItem -Path $directoryPath -Recurse -File

foreach ($file in $files) {
    $oldFileName = $file.Name
    $newFileName = Remove-SpacesFromFileName -fileName $oldFileName

    # If the filename was changed, rename the file
    if ($newFileName -ne $oldFileName) {
        $newFilePath = Join-Path -Path $file.DirectoryName -ChildPath $newFileName
        Rename-Item -Path $file.FullName -NewName $newFilePath
        Write-Output "Renamed '$oldFileName' to '$newFileName'"
    }
}
