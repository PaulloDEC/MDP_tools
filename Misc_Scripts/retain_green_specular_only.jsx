function processTGAFiles() {
    var inputFolder = Folder.selectDialog("Select a folder containing TGA files");
    if (!inputFolder) return;
    
    var files = inputFolder.getFiles("*.tga");
    if (files.length === 0) {
        alert("No TGA files found in the selected folder.");
        return;
    }
    
    var outputFolder = Folder.selectDialog("Select a folder to save processed PNG files");
    if (!outputFolder) return;
    
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        if (file instanceof File) {
            var doc = app.open(file);
            
            // Check if the document has at least three channels (RGB)
            if (doc.channels.length >= 3) {
                app.activeDocument = doc;
                
                // Select the green channel
                var greenChannel = doc.channels[1];
                app.activeDocument.activeChannels = [greenChannel];
                
                // Copy the green channel
                app.activeDocument.selection.selectAll();
                app.activeDocument.selection.copy();
                
                // Create a new document with the same dimensions
                var newDoc = app.documents.add(doc.width, doc.height, doc.resolution, file.name.replace(/\.tga$/, "_green"), NewDocumentMode.GRAYSCALE);
                app.activeDocument = newDoc;
                
                // Paste the green channel as the new image
                newDoc.paste();
                
                // Flatten the image to remove transparency
                newDoc.flatten();
                
                // Save as PNG
                var saveFile = new File(outputFolder + "/" + file.name.replace(/\.tga$/, "_green.png"));
                var pngOptions = new PNGSaveOptions();
                pngOptions.interlaced = false;
                
                newDoc.saveAs(saveFile, pngOptions, true, Extension.LOWERCASE);
                newDoc.close(SaveOptions.DONOTSAVECHANGES);
            }
            
            doc.close(SaveOptions.DONOTSAVECHANGES);
        }
    }
    alert("Processing complete.");
}

processTGAFiles();