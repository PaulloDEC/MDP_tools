// Target Illustrator
if (app.documents.length > 0) {
    var doc = app.activeDocument;
    var items = doc.pathItems;
    
    // Iterate backwards when deleting to avoid skipping items
    for (var i = items.length - 1; i >= 0; i--) {
        var item = items[i];
        var shouldDelete = false;

        // Check Fill Color
        if (item.filled) {
            if (isColor(item.fillColor)) {
                shouldDelete = true;
            }
        }

        // Check Stroke Color
        if (item.stroked && !shouldDelete) {
            if (isColor(item.strokeColor)) {
                shouldDelete = true;
            }
        }

        if (shouldDelete) {
            item.remove();
        }
    }
    alert("Cleanup complete! Only greyscale/black objects remain.");
} else {
    alert("No active document found.");
}

// Function to determine if a color has "hue"
function isColor(color) {
    if (color.typename === "RGBColor") {
        // If R, G, and B aren't equal, it's a color
        return !(color.red === color.green && color.green === color.blue);
    } else if (color.typename === "CMYKColor") {
        // If there is any Cyan, Magenta, or Yellow, it's a color
        return (color.cyan > 0 || color.magenta > 0 || color.yellow > 0);
    } else if (color.typename === "GrayColor") {
        // Naturally grey
        return false;
    }
    return false;
}