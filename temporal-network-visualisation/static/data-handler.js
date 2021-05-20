var vertices;
var edges;
var verticesNameIndex = {};
var centralityDegreeTracker = new Set();

// Get the Overtime temporal directed graph object as JSON 
async function getDataset() {
    let response = await fetch("http://localhost:5000/dataset");
    let result = await response.json();
    edges = result.edges;
    vertices = result.nodes;
    return result;
}

async function initialiseData() {
    console.log("Initialising dataset");
    const data = await getDataset();
    console.log("Dataset has been initialised");
    console.log(data);
    
    let verticeMap = {}
    for (var i = 0; i < vertices.length; i++) {
        verticeMap[vertices[i]] = i
    }

    for (var i = 0; i < edges.length; i++) {
        edges[i].source = verticeMap[edges[i].source];
        edges[i].target = verticeMap[edges[i].target];
    }

    tempVertices = []
    for (var i = 0; i < vertices.length; i++) {
        tempVertices.push({"name": vertices[i]});
    }
    vertices = tempVertices;

    edges.sort(function(a,b) {
        if (a.source > b.source) {return 1;}
        else if (a.source < b.source) {return -1;}
        else {
            if (a.target > b.target) {return 1;}
            if (a.target < b.target) {return -1;}
            else {return 0;}
        }
    });
    
    for (var i=0; i < edges.length; i++) {
        if (i != 0 &&
            edges[i].source == edges[i-1].source &&
            edges[i].target == edges[i-1].target) {
                edges[i].linknum = edges[i-1].linknum + 1;
            }
        else {edges[i].linknum = 1;};
    };

    totalColor = COLOURS.length - 1;
    indexColor = 0;
    for (var i = 0; i < vertices.length; i++) {
        if (indexColor == totalColor) {
            indexColor = 0;
        }
        vertices[i].color = COLOURS[indexColor];
        vertices[i].degree = 0;
        verticesNameIndex[vertices[i].name] = i;
        indexColor += 1;
    }
    console.log(vertices)
    return true;
}

