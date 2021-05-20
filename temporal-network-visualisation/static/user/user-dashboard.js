function userDashboard(svg, startTimeRange, endTimeRange, numVertices, numEdges) {
    let userDisplay = svg.append("g")
        .attr("class", "information")

    userDisplay.append("text")
            .attr("fill", "Black")
            .attr("font-size", 16)
            .attr("font-weight", 400)
            .attr("x", 50)
            .attr("y", 50)
            .text("Show time window from " + startTimeRange + " to " + endTimeRange)

    userDisplay.append("text")
            .attr("fill", "Black")
            .attr("font-size", 16)
            .attr("font-weight", 400)
            .attr("x", 50)
            .attr("y", 70)
            .text("Total vertices: " + numVertices)

    userDisplay.append("text")
            .attr("fill", "Black")
            .attr("font-size", 16)
            .attr("font-weight", 400)
            .attr("x", 50)
            .attr("y", 90)
            .text("Total edges: " + numEdges)
}
