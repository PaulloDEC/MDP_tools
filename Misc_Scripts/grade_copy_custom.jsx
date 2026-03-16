app.beginUndoGroup("Auto-Transfer Effects via Clipboard");

var targetComps = app.project.selection;

// --- NEW SELECTION UI ---
function getSourceComp() {
    var compNames = [];
    var compObjects = [];

    // Collect all comps in the project
    for (var i = 1; i <= app.project.numItems; i++) {
        if (app.project.item(i) instanceof CompItem) {
            compNames.push(app.project.item(i).name);
            compObjects.push(app.project.item(i));
        }
    }

    if (compNames.length === 0) {
        alert("No compositions found in the project.");
        return null;
    }

    // Create a simple Dialog
    var win = new Window("dialog", "Select Source Composition");
    win.orientation = "column";
    win.alignChildren = ["fill", "top"];

    win.add("statictext", undefined, "Pick the comp to copy effects FROM:");
    var dropdown = win.add("dropdownlist", undefined, compNames);
    dropdown.selection = 0; // Default to first item

    var btnGroup = win.add("group");
    btnGroup.alignment = "center";
    var okBtn = btnGroup.add("button", undefined, "OK");
    var cancelBtn = btnGroup.add("button", undefined, "Cancel");

    if (win.show() === 1) {
        return compObjects[dropdown.selection.index];
    } else {
        return null; // User cancelled
    }
}

// 1. Prompt the user to select the Master Comp
var masterComp = getSourceComp();

if (masterComp === null) {
    // If user hits cancel or no comps exist, stop the script
    alert("Script cancelled. No source composition selected.");
} else {
    var matchCount = 0;

    for (var i = 0; i < targetComps.length; i++) {
        var currComp = targetComps[i];
        
        // Safety check: ensure item is a comp and not the master itself
        if (!(currComp instanceof CompItem) || currComp === masterComp) continue;

        for (var j = 1; j <= currComp.numLayers; j++) {
            var targetLayer = currComp.layer(j);
            var targetName = targetLayer.name.toLowerCase();
            var targetSrcName = (targetLayer.source !== null) ? targetLayer.source.name.toLowerCase() : "";

            for (var k = 1; k <= masterComp.numLayers; k++) {
                var masterLayer = masterComp.layer(k);
                var masterName = masterLayer.name.toLowerCase();
                var masterSrcName = (masterLayer.source !== null) ? masterLayer.source.name.toLowerCase() : "";

                // MATCHING LOGIC
                if (targetName === masterName || (targetSrcName !== "" && targetSrcName === masterSrcName)) {
                    var masterEffects = masterLayer.property("ADBE Effect Parade");
                    
                    if (masterEffects !== null && masterEffects.numProperties > 0) {
                        
                        // A. Clear existing effects on target layer
                        var targetEffects = targetLayer.property("ADBE Effect Parade");
                        while (targetEffects.numProperties > 0) {
                            targetEffects.property(1).remove();
                        }

                        // B. Deselect everything to ensure clean copy/paste
                        deselectAllLayers(masterComp);
                        deselectAllLayers(currComp);

                        // C. Focus Master Comp and select effects
                        masterComp.openInViewer();
                        masterLayer.selected = true;
                        for (var e = 1; e <= masterEffects.numProperties; e++) {
                            masterEffects.property(e).selected = true;
                        }

                        // D. Native Copy
                        app.executeCommand(19); // 19 = Copy

                        // E. Focus Target Comp and Paste
                        currComp.openInViewer();
                        targetLayer.selected = true;
                        app.executeCommand(20); // 20 = Paste

                        // Cleanup for next iteration
                        masterLayer.selected = false;
                        targetLayer.selected = false;

                        matchCount++;
                        break; 
                    }
                }
            }
        }
    }
    alert("Success! Matched and fully graded " + matchCount + " layers.");
}

app.endUndoGroup();

function deselectAllLayers(comp) {
    for (var l = 1; l <= comp.numLayers; l++) {
        comp.layer(l).selected = false;
    }
}