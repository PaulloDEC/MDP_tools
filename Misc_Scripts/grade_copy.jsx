{
    app.beginUndoGroup("Auto-Transfer Effects via Clipboard");

    var targetComps = app.project.selection;
    var masterCompName = "FSC Sports Bar Video"; 
    
    var masterComp = null;

    // 1. Find the Master Comp in the project
    for (var i = 1; i <= app.project.numItems; i++) {
        if (app.project.item(i) instanceof CompItem && app.project.item(i).name === masterCompName) {
            masterComp = app.project.item(i);
            break;
        }
    }

    if (masterComp === null) {
        alert("Error: Could not find master comp: " + masterCompName);
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
                            break; // Move to the next target layer
                        }
                    }
                }
            }
        }
        alert("Success! Matched and fully graded " + matchCount + " layers.");
    }

    app.endUndoGroup();

    // Helper function to deselect all layers in a comp
    function deselectAllLayers(comp) {
        for (var l = 1; l <= comp.numLayers; l++) {
            comp.layer(l).selected = false;
        }
    }
}