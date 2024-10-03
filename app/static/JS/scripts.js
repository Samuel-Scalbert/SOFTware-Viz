function updateRecap (item){
    fetch(`/api/line_chart/${item}`, {
                method: "GET"
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Extract datasets from the fetched data
                const usedData = data[0];
                const createdData = data[1];
                const sharedData = data[2];
                const newCircleData = data[3];
                if (window.myLineChart) {
                    window.myLineChart.data.datasets[0].data = usedData;
                    window.myLineChart.data.datasets[1].data = createdData;
                    window.myLineChart.data.datasets[2].data = sharedData;
                    window.myLineChart.update();
                }
                if (window.circleChart){
                    window.circleChart.data.datasets[0].data = newCircleData;
                    window.circleChart.update();
                }
                const recapDwMention = document.querySelector('.recap_dw_mention');
                const recapDwnMention = document.querySelector('.recap_dwn_mention');
                const recapNbMention = document.querySelector('.recap_nb_mention');

                // Update the inner text with the new data
                if (recapDwMention) recapDwMention.textContent = data[4][0];
                if (recapDwnMention) recapDwnMention.textContent = data[4][1];
                if (recapNbMention) recapNbMention.textContent = data[4][2];
                    })
            .catch(error => {
                console.error('Error:', error);
            });
};

document.addEventListener('DOMContentLoaded', (event) => {
    const struc = window.location.pathname.split('/').pop();
    if (struc !== "dashboard") {
        updateRecap(struc);
    };
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
    inputBox.onkeyup = function() {
        let result = []
        let input = inputBox.value;
        if (input.length) {
            result = availableSoftwareND.filter((keyword) => {
                return keyword.toLowerCase().includes(input.toLowerCase());
            });
            displayResult(result);
            let previousClickedElement = null;

            document.querySelectorAll('.mention_search_doc_id').forEach(item => {
                item.addEventListener('click', event => {
                    const elements = document.querySelectorAll('.mention_doc_id');
                    elements.forEach(element => {
                        var dropdownBtn = element.querySelector('.dropbtn');
                        var dropdownContent = element.querySelector('.dropdown-content');
                        dropdownBtn.style.color = '';
                        dropdownContent.style.display = 'none';
                    });
                    // Reset the color of the previously clicked element
                    if (previousClickedElement !== null) {
                        previousClickedElement.style.backgroundColor = ''; // Reset to default
                    }

                    // Set the background color of the current clicked element
                    item.style.backgroundColor = 'red';

                    // Set the current clicked element as the previous clicked element
                    previousClickedElement = item;

                    const idValue = item.getAttribute('id');
                    handleClick(idValue, 1);
                    resultBox.style.display = 'none'
                    resultBox.innerHTML = "<div class='dropdown-content-search'></div>";
                });
            });
        }
    }

    function displayResult(result) {
        const content = result.map((list) => {
            return "<div class='mention_search_doc_id' id=" + list + ">" + list + "</div>";
        }).join(''); // Join the array elements into a single string without any separator
        resultBox.style.display = 'block'
        resultBox.innerHTML = "<div class='dropdown-content-search'>" + content + "</div>";
    };

    function handleClick(idValue, value) {
    if (previousElement) {
        const elements = document.querySelectorAll(`#${previousElement}.mention_doc_id`);
        elements.forEach(element => {
            var dropdownBtn = element.querySelector('.dropbtn');
            var dropdownContent = element.querySelector('.dropdown-content');
            if (dropdownBtn) dropdownBtn.style.color = '';
            if (dropdownContent) dropdownContent.style.display = 'none';
        });
    }

    const sanitizedId = idValue ? idValue
        .replace(/\s/g, '')  // Remove all whitespace
        .replace(/\./g, '')  // Remove all periods
        .replace(/@/g, '\\@')  // Escape '@'
        .replace(/\+/g, '\\+')  // Escape '+'
        : '';

    const csssanitizedId = CSS.escape(sanitizedId);
    const elements = document.querySelectorAll(`#${csssanitizedId}.mention_doc_id`);

    if (elements.length === 0) {
        console.log('No elements found for ID:', csssanitizedId);
        return;
    }

    elements.forEach((element, index) => {
        setTimeout(() => {
            var dropdownBtn = element.querySelector('.dropbtn');
            var dropdownContent = element.querySelector('.dropdown-content');
            if (dropdownBtn) dropdownBtn.style.color = 'red';
            if (dropdownContent) dropdownContent.style.display = 'block';
            const container = element.parentElement.parentElement;
            // Scroll the current element into view smoothly, aligning it to the center
            container.scrollTo({
                top: element.offsetTop - container.offsetTop - (container.clientHeight / 2) + (element.clientHeight / 2),
                behavior: 'smooth'
            });

            // Additional debug to check scroll position
        }, index * 100);  // Adjust the delay (500ms) as needed
    });

    previousElement = csssanitizedId;
}



document.addEventListener('click', function(event) {
    // Selectors to exclude
    const selectors = [
        '.structure',
        '.mention_search_doc_id',
        '.dropbtn',
    ];

    // Check if the click occurred on any of the excluded elements
    const clickedExcludedElement = selectors.some(selector => event.target.closest(selector));

    if (!clickedExcludedElement) {
        // Handle clicks outside the specified elements
        const elements = document.querySelectorAll('.mention_doc_id');
        const elements_search = document.querySelectorAll('.dropdown-content-search');

        elements.forEach(element => {
            var dropdownBtn = element.querySelector('.dropbtn');
            var dropdownContent = element.querySelector('.dropdown-content');
            dropdownBtn.style.color = '';
            dropdownContent.style.display = 'none';
        });

        elements_search.forEach(searchElement => {
            searchElement.style.display = 'none';
        });

        // Reset search dropdown visibility
        const elements_search_soft = document.querySelector('.search');
        const elements_search_soft_table = elements_search_soft.querySelector('#result-box');
        elements_search_soft_table.style.display = 'none';

        // Reset structure color only if click is outside excluded elements
        const structure_reset = document.querySelectorAll('.structure');
        structure_reset.forEach(stru => {
            stru.style.color = 'black'; // Reset color
        });
    }
});

// Add event listeners for .mention_doc_id items
document.querySelectorAll('.mention_doc_id').forEach(item => {
    item.addEventListener('click', event => {
        event.stopPropagation(); // Prevent the global click event from being triggered
        const elements = document.querySelectorAll('.mention_doc_id');

        // Reset all dropdowns
        elements.forEach(element => {
            var dropdownBtn = element.querySelector('.dropbtn');
            var dropdownContent = element.querySelector('.dropdown-content');
            dropdownBtn.style.color = '';
            dropdownContent.style.display = 'none';
        });

        // Handle the specific click
        const idValue = item.getAttribute('id');
        handleClick(idValue, 2);
    });
});

});