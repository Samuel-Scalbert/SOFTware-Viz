Chart.register(ChartDataLabels);

function generateBubbleChart(selector) {
    var labels = [];
    var DATA_COUNT = 3;
    let datamin = 2010;
    let datamax = 2025;

    const chartConfig = {
        type: 'bubble',
        data: {
            datasets: [{
                backgroundColor: "#6C9BCF",
                borderColor: "#6C9BCF",
                data: [
                        {
                            "x": 2012,
                            "y": 22,
                            "v": 22
                        },
                        {
                            "x": 2019,
                            "y": 9,
                            "v": 9
                        },
                        {
                            "x": 2020,
                            "y": 2,
                            "v": 2
                        }
                    ]
            },
            {
                backgroundColor: "#CF0D14",
                borderColor: "#CF0D14",
                data: [
                        {
                            "x": 2021,
                            "y": 15,
                            "v": 15
                        },
                        {
                            "x": 2018,
                            "y": 18,
                            "v": 18
                        },
                        {
                            "x": 2023,
                            "y": 3,
                            "v": 3
                        }
                    ]
            }]
        },
        options: {
            plugins: {
                datalabels: {
                    anchor: function(context) {
                        var value = context.dataset.data[context.dataIndex];
                        return value.v < 50 ? 'end' : 'center';
                    },
                    align: function(context) {
                        var value = context.dataset.data[context.dataIndex];
                        return value.v < 50 ? 'end' : 'center';
                    },
                    color: function(context) {
                        var value = context.dataset.data[context.dataIndex];
                        return value.v < 50 ? context.dataset.backgroundColor : 'white';
                    },
                    font: {
                        weight: 'bold'
                    },
                    formatter: function(value) {
                        return Math.round(value.v);
                    },
                    offset: 2,
                    padding: 0
                }
            },

            // Core options
            aspectRatio: 5 / 3,
            layout: {
                padding: 16
            },
            elements: {
                point: {
                    radius: function(context) {
                        var value = context.dataset.data[context.dataIndex];
                        var size = context.chart.width;
                        var base = Math.abs(value.v) / 100;
                        return (size / 24) * base;
                    }
                }
            },
        }
    };

    const ctx = document.querySelector(selector);

    new Chart(ctx.getContext('2d'), chartConfig);

}




function generateCircleChart(selector, value1, value2, value3) {
    const chartConfig = {
        type: 'pie',
        data: {
            labels: ["Used", "Created", "Shared"],
            datasets: [{
                backgroundColor: ["#6C9BCF", "#363949", "#677483"],
                data: [value1, value2, value3],
                borderWidth: 1,
                cutout: '20%',
            }]
        },
        options: {
            radius: 100,
            rotation: 180,
            hoverOffset: 4,
            responsive: false,
            animation: {
                animateScale: true
            },

            tooltips: {
                enabled: false
            },
            legend: {
                display: false
            }
        },

        plugins: [{
            beforeDraw: function(chart) {
                const width = chart.width;
                const height = chart.height;
                const ctx = chart.ctx;

                ctx.restore();
                ctx.font = 'bold 55px sans-serif';
                ctx.textAlign = 'center';
                chart.ctx.fillStyle = "black";
            },
        }]

    };

    const ctx = document.querySelector(selector);

    new Chart(ctx.getContext('2d'), chartConfig);

}