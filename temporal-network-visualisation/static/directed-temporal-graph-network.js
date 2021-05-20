const width = windowWidth()*0.9;
const height = windowHeight()*0.9;   
const pageTitle = "Temporal Network Example";

let vertices;
let edges;
let startTime;
let endTime;

const defaultCircleRadius = 9;
const largerCircleRadius = defaultCircleRadius*2;
const defaultVertexFontSize = defaultCircleRadius*2;
const largerVertexFontSize = defaultVertexFontSize*2;

const labelFontSize = defaultVertexFontSize * 0.5;
const markerWidth = 4;
const markerHeight = 4;

let verticeLabelSwitch = true;
let edgeLabelSwitch = true;

const updateGraphNetworkTitle = d3.select("#temporal-graph-network-title").text(pageTitle)

function temporalGraphNetwork(vertices, edges, enableVerticeLabel, enableEdgeLabel) {
    // Initialise the SVG canvas for d3.js
    const svg = d3.select("#visualisation")
        .append("svg")
                .attr("width", width)
                .attr("height", height)

    userDashboard(svg, startTime, endTime, vertices.length, edges.length)

        // Create the arrow head
    svg.append("defs").selectAll("marker")
        .data(["end"])      // Different link/path types can be defined here
        .enter()
        .append("svg:marker")  
                .attr("id", String)
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 20)
                .attr("refY", -1)
                .attr("markerWidth", markerWidth)
                .attr("markerHeight", markerHeight)
                .attr("orient", "auto")
                .attr("fill", "black")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5");

    const simulation = d3.forceSimulation(vertices)
        .force('link', d3.forceLink()
        .links(edges)
        .distance(d => 50) // The length of the edges or links
        .strength(0.1))     
        .force('charge', d3.forceManyBody().strength(-50)) // strength() attraction (+) or repulsion (-)
        .force('overlap', d3.forceCollide()) // prevent vertex overlap one another
        .force('center', d3.forceCenter(width/2, height/2)) // center the graph 
        .on('tick', tick);    // add vertices and edges elements to canvas

    let addEdges = svg.append("g")
        .attr("id", "edges")
        .selectAll("path")
        .data(edges)
        .enter()
        .append("path")
        .attr("class","edge")
        .attr("id", d => d.source.name + " to " + d.target.name + ":" + d.start + "-" + d.end)
        .attr("marker-end", "url(#end)");

    let addVertices = svg.selectAll(".vertex")
        .data(vertices)
        .enter()
        .append("g")
        .attr("class", "vertex")
        .on("mouseover", mouseoverVertex) // trigger mouse hover over events
        .on("mouseout", mouseoutVertex)
        .call(drag(simulation)) // iInvokes callback function on the selection

    addVertices.append("circle")   // Append circle elem for each data
        .attr("r", defaultCircleRadius) // This needs to be scalable depending on network size

    addVertices.append("text") // Append text elem for each data
        .attr("dx", 10) // Position text off from circle
        .attr("dy", ".30em")
        .attr("font-size", defaultVertexFontSize)
        .attr("font-weight", 400)
        .attr("opacity", 0.5)
        .text(d => enableVerticeLabel ? d.name : "")

    let addLabels = svg.append("g")
        .attr("id", "labels")
        .style("fill", "black")
        .selectAll("text")
        .data(edges)
        .enter()
        .append("text")
        .attr("class", "label")
        .attr("dy", -2)
        .attr("font-size", labelFontSize)
                .append("textPath")

    function tick() {
        addEdges 
                .attr("stroke", function(d){
                    if (d.start >= (startTime + endTime) / 2) {
                        return "#191919"
                    }
                    return "#C0C0C0"
                })
                .attr("", function(d) {
                    let neightbour1 = d.source.name + d.target.name;
                    let neightbour2 = d.target.name + d.source.name;
                    if (!centralityDegreeTracker.has(neightbour1) && !centralityDegreeTracker.has(neightbour2)) {
                        centralityDegreeTracker.add(neightbour1);
                        centralityDegreeTracker.add(neightbour2);
                        vertices[verticesNameIndex[d.source.name]].degree += 1;
                        vertices[verticesNameIndex[d.target.name]].degree += 1;
                    }
                })
                .attr("d", function(d) {
                var dr = 75/d.linknum; 
                return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
                });
        addLabels
                .attr("xlink:href", d => "#" + d.source.name + " to " + d.target.name + ":" + d.start + "-" + d.end)
                .attr("startOffset", "40%")	
                .text(d => enableEdgeLabel ? d.start : "")

        addVertices
                .attr("id", d => d.name)
                .attr("fill", d => d.color)
                .attr("transform", d => "translate(" + d.x + "," + d.y + ")")
     }
}

function initialiseTemporalGraphNetwork(startTime, endTime) {
        let updatedLinks = edges.filter(link => link.start >= startTime && link.end <= endTime)
        centralityDegreeTracker = new Set();
        temporalGraphNetwork(vertices, updatedLinks, verticeLabelSwitch, edgeLabelSwitch) 
}

