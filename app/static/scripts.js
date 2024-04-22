function generateCircleChart(selector, value1, value2, value3) {
  const chartConfig = {
    type: 'pie',
    data: {
      labels: ["Used", "Created", "Shared"],
      datasets: [{
        backgroundColor: ["#6C9BCF", "#363949","#677483"],
        data: [value1, value2,value3],
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
document.addEventListener('DOMContentLoaded', (event) => {
    let previousElement = null;

    function handleClick(idValue) {
        if (previousElement) {
            const elements = document.querySelectorAll(`#${previousElement}`);
            elements.forEach(element => {
                console.log(element);
                element.style.color = '';
            });
        }
        // Now set the color of the clicked elements to red
        const elements = document.querySelectorAll(`#${idValue}`);
        elements.forEach(element => {
            console.log(element);
            element.style.color = 'red';
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
        previousElement = idValue; // Update the previousElement variable
    }

    // This function will be executed when the DOMContentLoaded event is fired,
    // indicating that the HTML content of the page is fully loaded and parsed.
    // Add your event listener setup code here
    document.querySelectorAll('.mention_doc_id').forEach(item => {
        item.addEventListener('click', event => {
            // Retrieve the value of the id attribute of the element
            const idValue = item.getAttribute('id');
            // Now you can use the idValue variable as needed
            handleClick(idValue);
        });
    });
});





