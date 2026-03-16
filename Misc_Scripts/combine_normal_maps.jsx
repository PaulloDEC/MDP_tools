/*
Combine X and Y Normal Map Components

This script combines PNG files from two folders, treating them as X and Y components of a normal map, and creates combined normal map images.

How to use:
1. Place the script in your Photoshop Scripts folder.
2. In Photoshop, go to File > Scripts > Combine X and Y Normal Maps.
3. Select the folder containing the X component images.
4. Select the folder containing the Y component images.
5. Choose a destination folder for the combined normal maps.

*/

#target photoshop

function main() {
  var xFolder = Folder.selectDialog("Select the folder containing X component images:");
  if (xFolder == null) return;

  var yFolder = Folder.selectDialog("Select the folder containing Y component images:");
  if (yFolder == null) return;

  var destinationFolder = Folder.selectDialog("Select the destination folder for combined normal maps:");
  if (destinationFolder == null) return;

  var xFiles = xFolder.getFiles("*.png");
  var yFiles = yFolder.getFiles("*.png");

  if (xFiles.length != yFiles.length) {
    alert("The number of X and Y component images must be the same.");
    return;
  }

  for (var i = 0; i < xFiles.length; i++) {
    var xFile = xFiles[i];
    var yFile = yFiles[i];

    var xDoc = open(xFile);
    app.activeDocument = xDoc;

    var yDoc = open(yFile);
    app.activeDocument = yDoc;

    if (xDoc.width != yDoc.width || xDoc.height != yDoc.height) {
      alert("Image dimensions do not match for " + xFile.name + " and " + yFile.name);
      xDoc.close(SaveOptions.DONOTSAVECHANGES);
      yDoc.close(SaveOptions.DONOTSAVECHANGes);
      continue;
    }

    var newDoc = app.documents.add(xDoc.width, xDoc.height, xDoc.resolution, xFile.name.replace(".png", "_normal.png"), NewDocumentMode.RGB, DocumentFill.TRANSPARENT, xDoc.pixelAspectRatio);

    app.activeDocument = xDoc;
    var xLayer = xDoc.layers[0].duplicate(newDoc, ElementPlacement.PLACEATBEGINNING);

    app.activeDocument = yDoc;
    var yLayer = yDoc.layers[0].duplicate(newDoc, ElementPlacement.PLACEATBEGINNING);

    xDoc.close(SaveOptions.DONOTSAVECHANGES);
    yDoc.close(SaveOptions.DONOTSAVECHANGES);

    // Combine channels using applyImage()
    var redChannel = newDoc.channels[0];
    var greenChannel = newDoc.channels[1];

    redChannel.applyImage(xLayer.channels[0]);
    greenChannel.applyImage(yLayer.channels[0]);

    newDoc.layers.removeAll();

    var saveFile = new File(destinationFolder + "/" + xFile.name.replace(".png", "_normal.png"));
    var saveOptions = new PNGSaveOptions();
    saveOptions.compression = 0;
    newDoc.saveAs(saveFile, saveOptions, true, Extension.LOWERCASE);
    newDoc.close(SaveOptions.DONOTSAVECHANGES);
  }

  alert("Normal maps created successfully!");
}

main();