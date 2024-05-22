Chart.register(ChartDataLabels);

function generateBubbleChart(selector, dictionnary_data_raw, minyear, maxyear, maxoccu) {
    var labels = [];
    let xdatamin = minyear - 1;
    let xdatamax = maxyear + 1;
    let ydatamin = 0;
    let ydatamax = maxoccu + 2;

    const chartConfig = {
        type: 'bubble',
        data: {
            datasets: dictionnary_data_raw
        },
        options: {
            hitRadius :  5,
            hoverBorderWidth : 15,
            scales: {
            y: {suggestedMin: ydatamin,
                suggestedMax: ydatamax,
                 ticks:{
                    display: true,
                    font: {size:25}
                    },
                title:{
                display:true,
                    text:'Nb of occurences',
                    font: {size:25}
                }
                },
            x: {suggestedMin: xdatamin,
                suggestedMax: xdatamax,
                ticks:{
                    display: true,
                    font: {size:25}
                    },
                title:{
                display:true,
                    text:'Year',
                    font: {size:25}
                }
                }
            },
            events: ['mouseout', 'click'],
            plugins: {
                legend: {
                              position: 'top',
                              labels: {
                                  font: {
                                    size: 25
                                  }
                             }
                          },
                datalabels: {
                    anchor: function(context) {
                        var value = context.dataset.data[context.dataIndex];
                        return value.v < 50 ? 'end' : 'center';
                    },
                    align: function(context) {
                        var value = context.dataset.data[context.dataIndex];
                        return value.v < 50 ? 'end' : 'center';
                    },
                    color: 'black',
                    font: {weight: 'bold',
                           size: 25,
                    },
                    formatter: function(value) {
                        return Math.round(value.v);
                    },
                    offset: 4,
                    padding: 0
                },
                tooltip:{
                    padding : 20,
                    bodyFont: {
                      size: function(context){
                        return document.body.offsetWidth / 100;
                      },
                    },
                    callbacks: {
                        title: function(context) {
                            return '';
                        },
                        label: function(context) {
                            return context.raw.label;
                        },
                        labelTextColor: function(context) {
                            let color = context.dataset.backgroundColor;
                            return color;
                        },
                    }
                }
            },

            // Core options
            layout: {
                padding: 30
            },
            elements: {
                point: {
                    radius: function(context) {
                        var value = context.dataset.data[context.dataIndex];
                        var size = context.chart.width;
                        var base = Math.abs(value.v) / 15;
                        return (size / 24) * base;
                    }
                }
            },
        }
    };

    const ctx = document.querySelector(selector);

    const chart = new Chart(ctx.getContext('2d'), chartConfig);

    ctx.onclick = (evt) => {
      const points = chart.getElementsAtEventForMode(
        evt,
        'nearest',
        { intersect: true },
        true
      );
      if (points.length) {
          console.log(points)
          const firstPoint = points[0]
          const datasetPoint = firstPoint.datasetIndex;
          const dataPoint = firstPoint.index;
          console.log(chart.data.datasets[datasetPoint].data[dataPoint].label)
      }
    };
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