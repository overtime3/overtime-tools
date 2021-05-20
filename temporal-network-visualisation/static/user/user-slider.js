// Initialise the time range slider
function updateSlider(startTime, endTime) {
    d3.select("#sliderStartValue").text(startTime);
    d3.select("#sliderStart")
        .attr("min", startTime)
        .attr("max", endTime)
        .attr("value", startTime);
    d3.select("#sliderEndValue").text(endTime);
    d3.select("#sliderEnd")
        .attr("min", startTime)
        .attr("max", endTime)
        .attr("value", endTime);
}