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

    const mentionDocElements = document.querySelectorAll('.mention_doc_id');
    const availableSoftware = new Set();
    mentionDocElements.forEach(item => {
        const value = item.getAttribute('id');
        availableSoftware.add(value);
    });

    let previousElement = null;
    const availableSoftwareND = Array.from(availableSoftware);
    const resultBox = document.getElementById("result-box");
    const inputBox = document.getElementById("input-box");
    inputBox.onkeyup = function (){
        let result = []
        let input = inputBox.value;
        if(input.length){
            result = availableSoftwareND.filter((keyword)=>{return keyword.toLowerCase().includes(input.toLowerCase());
            });
        displayResult(result);
        let previousClickedElement = null;

        document.querySelectorAll('.mention_search_doc_id').forEach(item => {
            item.addEventListener('click', event => {
                // Reset the color of the previously clicked element
                if (previousClickedElement !== null) {
                    previousClickedElement.style.backgroundColor = ''; // Reset to default
                }

                // Set the background color of the current clicked element
                item.style.backgroundColor = 'red';

                // Set the current clicked element as the previous clicked element
                previousClickedElement = item;

                const idValue = item.getAttribute('id');
                handleClick(idValue);
    });
    });
        }
    }
    function displayResult(result){
    const content = result.map((list)=> {
        return "<div class='mention_search_doc_id' id=" + list + ">" + list + "</div>";
    }).join(''); // Join the array elements into a single string without any separator
    resultBox.innerHTML = "<div class='dropdown-content-search'>" + content + "</div>";
    };

    function handleClick(idValue) {
        if (previousElement) {
            const elements = document.querySelectorAll(`#${previousElement}.mention_doc_id`);
            console.log(elements)
            elements.forEach(element => {
                var dropdownBtn = element.querySelector('.dropbtn');
                var dropdownContent = element.querySelector('.dropdown-content');
                dropdownBtn.style.color = '';
                dropdownContent.style.display = 'None';
            });
        }
        const sanitizedId = idValue.replace(/\s/g, '').replace(".", ''); // Remove spaces and "." from the ID
        console.log(document.querySelectorAll(`#${sanitizedId}`))
        const elements = document.querySelectorAll(`#${sanitizedId}.mention_doc_id`);
        elements.forEach(element => {
            var dropdownBtn = element.querySelector('.dropbtn');
            var dropdownContent = element.querySelector('.dropdown-content');
            dropdownBtn.style.color = 'red';
            dropdownContent.style.display = 'block';
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
        previousElement = sanitizedId;
    }

    document.querySelectorAll('.mention_doc_id').forEach(item => {
        item.addEventListener('click', event => {
            const idValue = item.getAttribute('id');
            handleClick(idValue);
        });
    });
});






