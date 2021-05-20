// Basic settings for the graph
// Such as windows or time range settings

function windowWidth() {
    let width = window.innerWidth
    || document.documentElement.clientWidth
    || document.body.clientWidth;
    return width
}

function windowHeight() {
    let height = window.innerHeight
    || document.documentElement.clientHeight
    || document.body.clientHeight;
    return height
}

function getStartTimeRange(edges) {
    min = Number.MAX_SAFE_INTEGER
    for (var i = 0; i < edges.length; i++) {
        currNum = edges[i].start;
        if (currNum < min) {
            min = currNum;
        }
    }
    return min;
}

function getEndTimeRange(edges) {
    max = Number.MIN_VALUE
    for (var i = 0; i < edges.length; i++) {
        currNum = edges[i].end;
        if (currNum > max) {
            max = currNum;
        }
    }
    return max;
}
