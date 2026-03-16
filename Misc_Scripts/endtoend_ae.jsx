// Arrange selected layers end-to-end
// Each layer assumed to be 4 seconds long
(function() {
    var comp = app.project.activeItem;
    if (!(comp && comp instanceof CompItem)) {
        alert("Please select a composition.");
        return;
    }

    var layers = comp.selectedLayers;
    if (layers.length === 0) {
        alert("Please select the layers to arrange.");
        return;
    }

    app.beginUndoGroup("Arrange Layers End-to-End");

    var duration = 4; // seconds per layer
    for (var i = 0; i < layers.length; i++) {
        layers[i].startTime = i * duration;
    }

    app.endUndoGroup();
})();
