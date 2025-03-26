
//Using bb from billbord.js, which is loaded in body_end.html
function createChart(id, data = {}) {
    console.log(typeof data)
    console.log(typeof data[0])
    console.log(typeof data[1])
    console.log(data)
    bb.generate({
        data: {
            x: "x",
            columns: [
                data[0],
                data[1],
            ],
            type: "line",
            color: function (color, d) {
                return "#f97e28";
            }
        },
        axis: {
            x: {
                type: "timeseries",
                tick: {
                    format: "%Y-%m-%d %H:%M"
                }
            }
        },
        point: {
            type: "rectangle",
            r: 3,
        },
        bindto: "#" + id
    });
}