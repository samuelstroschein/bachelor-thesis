import { retractionTemplate } from './retraction_template'


export interface SegmentVariables {
    retractionDistance: number
    retractionSpeed: number
    extraRestartDistance: number
    prime: number
    zHop: number
}


export function gcodeAsBlob(gcode: string): Blob {
    return new Blob([gcode], { type: 'text/plain' });
}

export function downloadGcode(document: Document, blob: Blob, fileName: string) {
    var a = document.createElement('a');
    a.download = fileName;
    a.href = URL.createObjectURL(blob);
    a.dataset.downloadurl = ['text/plain', a.download, a.href].join(':');
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () {
        URL.revokeObjectURL(a.href);
    }, 1500);
}


// partially adjusted from https://github.com/teachingtechYT/teachingtechYT.github.io
export function generateRetractionGcode(
    bedDimensions: [number, number],
    hotEndTemperature: number,
    bedTemperature: number,
    segments: Array<SegmentVariables>
) {
    // centre is for delta printers
    var centre = false;
    var bedX = Math.round((bedDimensions[0] - 100) / 2);
    var bedY = Math.round((bedDimensions[1] - 100) / 2);
    var abl = 0
    var pc = "0"
    var pcResume = 255;
    var a1 = segments[0].retractionDistance
    var a2 = segments[0].retractionSpeed * 60
    var a3 = segments[0].extraRestartDistance
    var a4 = segments[0].prime * 60;
    var a5 = segments[0].zHop;
    var b1 = segments[1].retractionDistance
    var b2 = segments[1].retractionSpeed * 60
    var b3 = segments[1].extraRestartDistance
    var b4 = segments[1].prime * 60;
    var b5 = segments[1].zHop;
    var c1 = segments[2].retractionDistance
    var c2 = segments[2].retractionSpeed * 60
    var c3 = segments[2].extraRestartDistance
    var c4 = segments[2].prime * 60;
    var c5 = segments[2].zHop;
    var d1 = segments[3].retractionDistance
    var d2 = segments[3].retractionSpeed * 60
    var d3 = segments[3].extraRestartDistance
    var d4 = segments[3].prime * 60;
    var d5 = segments[3].zHop;
    var e1 = segments[4].retractionDistance
    var e2 = segments[4].retractionSpeed * 60
    var e3 = segments[4].extraRestartDistance
    var e4 = segments[4].prime * 60;
    var e5 = segments[4].zHop;
    var f1 = segments[5].retractionDistance
    var f2 = segments[5].retractionSpeed * 60
    var f3 = segments[5].extraRestartDistance
    var f4 = segments[5].prime * 60;
    var f5 = segments[5].zHop;
    var customStart = ""
    var retraction = retractionTemplate;
    switch (pc) {
        case '0':
            retraction = retraction.replace(/;fan2/, "M106 S255 ; custom fan 100% from layer 2");
            break;
        case '1':
            retraction = retraction.replace(/;fan3/, "M106 S255 ; custom fan 100% from layer 3");
            break;
        case '2':
            retraction = retraction.replace(/;fan5/, "M106 S255 ; custom fan 100% from layer 5");
            break;
        case '3':
            retraction = retraction.replace(/;fan2/, "M106 S130 ; custom fan 50% from layer 2");
            pcResume = 130;
            break;
        case '4':
            retraction = retraction.replace(/;fan3/, "M106 S130 ; custom fan 50% from layer 3");
            pcResume = 130;
            break;
        case '5':
            retraction = retraction.replace(/;fan5/, "M106 S130 ; custom fan 50% from layer 5");
            pcResume = 130;
            break;
        case '6':
            retraction = retraction.replace(/;fan2/, "; custom fan off");
            pcResume = 0;
            break;
    }
    retraction = retraction.replace(/M140 S60/g, "M140 S" + bedTemperature + " ; custom bed temp");
    retraction = retraction.replace(/M190 S60/g, "M190 S" + bedTemperature + " ; custom bed temp");
    if (abl != 4) {
        retraction = retraction.replace(/M104 S210 T0/g, "M104 S" + hotEndTemperature + " T0 ; custom hot end temp");
        retraction = retraction.replace(/M109 S210 T0/g, "M109 S" + hotEndTemperature + " T0 ; custom hot end temp");
    } else {
        retraction = retraction.replace(/M104 S210/g, "; Prusa Mini");
        retraction = retraction.replace(/M109 S210/g, "; Prusa Mini");
    }
    if (abl == 1) {
        retraction = retraction.replace(/;G29 ; probe ABL/, "G29 ; probe ABL");
    }
    if (abl == 2) {
        retraction = retraction.replace(/;M420 S1 ; restore ABL mesh/, "M420 S1 ; restore ABL mesh");
    }
    if (abl == 3) {
        retraction = retraction.replace(/G28 ; home all axes/, "G28 W ; home all without mesh bed level")
        retraction = retraction.replace(/;G29 ; probe ABL/, "G80 ; mesh bed leveling")
    }
    if (abl == 4) {
        retraction = retraction.replace(/G28 ; home all axes/, "M109 S170 T0 ; probing temperature\nG28 ; home all");
        retraction = retraction.replace(/;G29 ; probe ABL/, "G29 ; probe ABL");
        retraction = retraction.replace(/;M420 S1 ; restore ABL mesh/, "M109 S" + hotEndTemperature + " T0 ; custom hot end temp");
    }
    if (abl == 5) {
        retraction = retraction.replace(/;G29 ; probe ABL/, "G29 L1 ; Load the mesh stored in slot 1\nG29 J ; Probe 3 points to tilt mesh");
    }
    //@ts-ignore
    if (centre == true) {
        var retractionArray = retraction.split(/\n/g);
        var regexp = /X[0-9\.]+/;
        retractionArray.forEach(function (index, item) {
            if (retractionArray[item].search(/X/) > -1) {
                var value = parseFloat(retractionArray[item].match(regexp)[0].substring(1)) - 50;
                retractionArray[item] = retractionArray[item].replace(regexp, "X" + String(value));
            }
        });
        var regexp = /Y[0-9\.]+/;
        retractionArray.forEach(function (index, item) {
            if (retractionArray[item].search(/Y/) > -1) {
                var value = parseFloat(retractionArray[item].match(regexp)[0].substring(1)) - 50;
                retractionArray[item] = retractionArray[item].replace(regexp, "Y" + String(value))
            }
        });
        retraction = retractionArray.join("\n");
    } else {
        if (bedX > 0) {
            var retractionArray = retraction.split(/\n/g);
            var regexp = /X[0-9\.]+/;
            retractionArray.forEach(function (index, item) {
                if (retractionArray[item].search(/X/) > -1) {
                    var value = parseFloat(retractionArray[item].match(regexp)[0].substring(1)) + bedX;
                    retractionArray[item] = retractionArray[item].replace(regexp, "X" + String(value));
                }
            });
            retraction = retractionArray.join("\n");
        }
        if (bedY > 0) {
            var retractionArray = retraction.split(/\n/g);
            var regexp = /Y[0-9\.]+/;
            retractionArray.forEach(function (index, item) {
                if (retractionArray[item].search(/Y/) > -1) {
                    var value = parseFloat(retractionArray[item].match(regexp)[0].substring(1)) + bedY;
                    retractionArray[item] = retractionArray[item].replace(regexp, "Y" + String(value))
                }
            });
            retraction = retractionArray.join("\n");
        }
    }
    // A section
    retraction = retraction.replace(/;retractionA/g, "G1 E-" + a1 + " F" + a2 + " ; custom retraction - A");
    retraction = retraction.replace(/;unretractionA/g, "G1 E" + a3 + " F" + a4 + " ; custom un-retraction/prime - A");
    if (a5 > 0) {
        retraction = retraction.replace(/;zhopupA/g, "G91\nG1 Z" + a5 + " F1200 ; custom z hop - A\nG90");
    }
    // B section
    retraction = retraction.replace(/;retractionB/g, "G1 E-" + b1 + " F" + b2 + " ; custom retraction - B");
    retraction = retraction.replace(/;unretractionB/g, "G1 E" + b3 + " F" + b4 + " ; custom un-retraction/prime - B");
    if (b5 > 0) {
        retraction = retraction.replace(/;zhopupB/g, "G91\nG1 Z" + b5 + " F1200 ; custom z hop - B\nG90");
    }
    // C section
    retraction = retraction.replace(/;retractionC/g, "G1 E-" + c1 + " F" + c2 + " ; custom retraction - C");
    retraction = retraction.replace(/;unretractionC/g, "G1 E" + c3 + " F" + c4 + " ; custom un-retraction/prime - C");
    if (c5 > 0) {
        retraction = retraction.replace(/;zhopupC/g, "G91\nG1 Z" + c5 + " F1200 ; custom z hop - C\nG90");
    }
    // D section
    retraction = retraction.replace(/;retractionD/g, "G1 E-" + d1 + " F" + d2 + " ; custom retraction - D");
    retraction = retraction.replace(/;unretractionD/g, "G1 E" + d3 + " F" + d4 + " ; custom un-retraction/prime - D");
    if (d5 > 0) {
        retraction = retraction.replace(/;zhopupD/g, "G91\nG1 Z" + d5 + " F1200 ; custom z hop - D\nG90");
    }
    // E section
    retraction = retraction.replace(/;retractionE/g, "G1 E-" + e1 + " F" + e2 + " ; custom retraction - E");
    retraction = retraction.replace(/;unretractionE/g, "G1 E" + e3 + " F" + e4 + " ; custom un-retraction/prime - E");
    if (e5 > 0) {
        retraction = retraction.replace(/;zhopupE/g, "G91\nG1 Z" + e5 + " F1200 ; custom z hop - E\nG90");
    }
    // F section
    retraction = retraction.replace(/;retractionF/g, "G1 E-" + f1 + " F" + f2 + " ; custom retraction - F");
    retraction = retraction.replace(/;unretractionF/g, "G1 E" + f3 + " F" + f4 + " ; custom un-retraction/prime - F");
    if (f5 > 0) {
        retraction = retraction.replace(/;zhopupF/g, "G91\nG1 Z" + f5 + " F1200 ; custom z hop - F\nG90");
    }
    // if (document.retractionForm.psuon.checked == true) {
    //     retraction = retraction.replace(/;M80/, "M80");
    // }
    // if (document.retractionForm.removet0.checked == true) {
    //     retraction = retraction.replace(/T0\n/, ";T0\n");
    // }
    // if (document.retractionForm.start.checked == true) {
    //     retraction = retraction.replace(/;customstart/, "; custom start gcode\n" + customStart);
    // }
    return retraction
}