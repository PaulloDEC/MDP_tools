# Define the path to the directory
$directoryPath = "X:\Queensland Parks 2024\MAY Byfield and Blackdown\Trip 3\rename and reorganise\processed"

# Function to insert space before two consecutive capital letters
function Insert-SpaceBeforeCapitalLetters {
    param (
        [string]$folderName
    )

    # Use regex to find two consecutive capital letters and insert a space before them
    $newFolderName = $folderName -replace "([a-zA-Z])([A-Z]{2})", '$1 $2'
    return $newFolderName
}

# Get all directories in the specified directory and its subdirectories
$directories = Get-ChildItem -Path $directoryPath -Recurse -Directory

foreach ($directory in $directories) {
    $oldFolderName = $directory.Name
    $newFolderName = Insert-SpaceBeforeCapitalLetters -folderName $oldFolderName

    # If the folder name was changed, rename the folder
    if ($newFolderName -ne $oldFolderName) {
        $newFolderPath = Join-Path -Path $directory.Parent.FullName -ChildPath $newFolderName
        Rename-Item -Path $directory.FullName -NewName $newFolderPath
        Write-Output "Renamed '$oldFolderName' to '$newFolderName'"
    }
}
