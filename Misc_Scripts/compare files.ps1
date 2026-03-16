# Ask for the first folder path
$folder1 = Read-Host "Enter the path of the first folder"

# Ask for the second folder path
$folder2 = Read-Host "Enter the path of the second folder"

# Get the list of files in the first folder
$filesInFolder1 = Get-ChildItem -Path $folder1 -File

# Get the list of files in the second folder
$filesInFolder2 = Get-ChildItem -Path $folder2 -File

# Find the files that are in the first folder but not in the second
$uniqueFiles = $filesInFolder1 | Where-Object { $_.Name -notin $filesInFolder2.Name }

# Group the unique files by their extension
$groupedFiles = $uniqueFiles | Group-Object Extension | Sort-Object Name

# Output the results
if ($groupedFiles.Count -gt 0) {
    Write-Host "The following files are in $folder1 but not in ${folder2}, ordered by file type:"
    foreach ($group in $groupedFiles) {
        Write-Host "File type: $($group.Name)"
        $group.Group | ForEach-Object { Write-Host "  $_.Name" }
    }
} else {
    Write-Host "All files in $folder1 are also present in ${folder2}."
}
