window.addEventListener('load', function() {

    const svg = d3.select("#svg")
        .attr("viewBox", [0, 0, 900, 900])
        .attr("font-size", 10)
        .attr("font-family", "sans-serif")
        .attr("text-anchor", "middle");
    d3.csv("avgRead.csv").then(data => {

        color = d3.scaleOrdinal(data.map(d => d.attrName), d3.schemeCategory10)

        groups = (data.map(d => d.attrName).filter(distinct))
        numGrp = groups.length

        modNames = []
        for (i = 0; i < numGrp; i++) {
            modNames.push([])
            for (row in data) {
                if (data[row].attrName == groups[i]) {
                    modNames[i].push(data[row].modName)
                }
            }
        }

        xs = d3.scaleBand()
            .domain(groups)
            .range([100, 800])

        ys = n => {
            return d3.scaleBand()
                .domain(modNames[n])
                .range([100, 800])
        }


        gs = d3.select("#svg").selectAll("g")
            .data(data)
            .enter()
            .append("g")
        gs.append("circle")
            .attr('r', d => parseFloat(d.deg) * 30)
            .attr('fill', d => color(d.attrName))
            .attr("cy", d => xs(d.attrName))
            .attr("cx", (d => ys(groups.indexOf(d.attrName))(d.modName)))
        gs.append("text")
            .text(d => (d.attrName + "." + d.modName))
            .attr("y", d => xs(d.attrName))
            .attr("x", (d => ys(groups.indexOf(d.attrName))(d.modName)))
    })

})

function distinct(val, index, self) {
    return self.indexOf(val) === index
}

function submodNames(val, index, self) {
    return (val[0][0] === val[1])
}