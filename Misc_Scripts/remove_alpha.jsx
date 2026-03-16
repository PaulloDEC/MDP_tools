function processTGAFiles() {
    var inputFolder = Folder.selectDialog("Select a folder containing TGA files");
    if (!inputFolder) return;
    
    var files = inputFolder.getFiles("*.tga");
    if (files.length === 0) {
        alert("No TGA files found in the selected folder.");
        return;
    }
    
    var outputFolder = Folder.selectDialog("Select a folder to save PNG files");
    if (!outputFolder) return;
    
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        if (file instanceof File) {
            var doc = app.open(file);
            
            // Check if the document has an alpha channel
            if (doc.channels.length > 3) {
                app.activeDocument = doc;
                doc.channels[3].remove(); // Remove the alpha channel
            }
            
            // Save as PNG
            var saveFile = new File(outputFolder + "/" + file.name.replace(/\.tga$/, ".png"));
            var pngOptions = new PNGSaveOptions();
            pngOptions.interlaced = false;
            
            doc.saveAs(saveFile, pngOptions, true, Extension.LOWERCASE);
            doc.close(SaveOptions.DONOTSAVECHANGES);
        }
    }
    alert("Processing complete.");
}

processTGAFiles();
