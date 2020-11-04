window.addEventListener('load', function() {

    const svg = d3.create("svg")
        .attr("viewBox", [0, 0, 900, 900])
        .attr("font-size", 10)
        .attr("font-family", "sans-serif")
        .attr("text-anchor", "middle");
    d3.csv("data.csv", function(row) {
        console.log(row)

        const elt = svg.selectAll('g')
            .data(row)

    });

    d3.select("#rootNode").append(svg)
})