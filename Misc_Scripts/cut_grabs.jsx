// Adobe Premiere ExtendScript for Automating Clip Extraction
(function extractClips() {
    var timecodes = [
        [0.31, 0.38], [1.00, 1.13], [2.22, 2.29], [6.16, 6.26], [7.00, 7.13], [7.33, 7.37], [8.10, 8.19], [9.24, 9.28],
        [13.49, 14.00], [17.41, 17.48], [17.53, 18.05], [18.47, 18.55], [20.18, 20.21], [23.40, 23.59],
        [26.22, 26.32], [27.20, 27.36], [28.05, 28.07], [28.13, 28.20], [29.15, 29.30], [29.30, 29.43],
        [29.55, 30.09], [31.20, 31.39], [31.58, 32.11], [37.02, 37.04], [40.00, 40.11], [42.12, 42.24],
        [42.50, 42.59], [46.26, 46.30], [52.03, 52.10], [59.19, 59.32], [60.14, 60.26], [60.33, 60.45], [64.01, 64.10]
    ];

    function getSequenceByName(name) {
        for (var i = 0; i < app.project.sequences.length; i++) {
            if (app.project.sequences[i].name === name) {
                return app.project.sequences[i];
            }
        }
        return null;
    }

    function timecodeToSeconds(tc) {
        var parts = tc.toString().split(".");
        var minutes = parseInt(parts[0], 10);
        var seconds = parseFloat("0." + parts[1]) * 60;
        return (minutes * 60) + seconds;
    }

    var sourceSeq = getSequenceByName("INTERVIEW complete ALL ORIGINAL");
    var targetSeq = getSequenceByName("INTERVIEW selects");

    if (!sourceSeq || !targetSeq) {
        alert("Error: One or both sequences not found!");
        return;
    }

    var track = sourceSeq.videoTracks[0]; // Assumes first video track
    
    for (var i = 0; i < timecodes.length; i++) {
        var inPoint = timecodeToSeconds(timecodes[i][0]);
        var outPoint = timecodeToSeconds(timecodes[i][1]);

        app.enableQE();
        var qeSeq = qe.project.getActiveSequence();
        qeSeq.setInPoint(inPoint);
        qeSeq.setOutPoint(outPoint);
        qeSeq.addToClipboard();
    }

    targetSeq.videoTracks[0].overwriteFromClipboard();
    alert("Clips copied and pasted successfully!");
})();
