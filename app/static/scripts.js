function generateCircleChart(selector, value1, value2, value3) {
  const chartConfig = {
    type: 'pie',
    data: {
      labels: ["Used", "Created", "Shared"],
      datasets: [{
        backgroundColor: ["#6C9BCF", "#363949","#677483"],
        data: [7158, 1117,277],
        borderWidth:1,
        cutout:'20%',
      }]
    },
    options:{
      radius:100,
      rotation:180,
      hoverOffset: 4,
      responsive:false,
       animation:{animateScale:true},

      tooltips:{enabled:false},
       legend:{display:false}
    },

   plugins:[{
     beforeDraw:function(chart){
          const width = chart.width;
          const height = chart.height;
        	const ctx = chart.ctx;

        	ctx.restore();
        	ctx.font='bold 55px sans-serif';
      		ctx.textAlign= 'center';
      		chart.ctx.fillStyle="black";
  	 },
   }]

 };

const ctx = document.querySelector(selector);

new Chart(ctx.getContext('2d'),chartConfig);

}