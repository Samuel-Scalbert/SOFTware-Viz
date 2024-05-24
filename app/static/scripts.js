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
                    console.log(item)

                    const idValue = item.getAttribute('id');
                    handleClick(idValue, 1);
                    resultBox.innerHTML = "<div class='dropdown-content-search'></div>";
                });
            });
        }
    }
    document.querySelectorAll('.structure').forEach(item => {
        item.addEventListener('click', event => {
            const elements = document.querySelectorAll('.mention_doc_id');
            elements.forEach(element => {
                var dropdownBtn = element.querySelector('.dropbtn');
                var dropdownContent = element.querySelector('.dropdown-content');
                dropdownBtn.style.color = '';
                dropdownContent.style.display = 'none';
            });
            item.querySelectorAll('div').forEach(child_div => {
                // Get all div elements
                const divElements = document.querySelectorAll('.dropdown-content');
                // Iterate over each div element
                divElements.forEach(div => {
                    if (div.textContent.trim() === child_div.className) {
                        const element = div.parentNode.parentNode;
                        var dropdownBtn = element.querySelector('.dropbtn');
                        var dropdownContent = element.querySelector('.dropdown-content');
                        dropdownBtn.style.color = 'red';
                    }
                });
            });
        });
    });

    function displayResult(result) {
        const content = result.map((list) => {
            return "<div class='mention_search_doc_id' id=" + list + ">" + list + "</div>";
        }).join(''); // Join the array elements into a single string without any separator
        resultBox.innerHTML = "<div class='dropdown-content-search'>" + content + "</div>";
    };

    function handleClick(idValue, value) {
        if (previousElement) {
            const elements = document.querySelectorAll(`#${previousElement}.mention_doc_id`);
            elements.forEach(element => {
                var dropdownBtn = element.querySelector('.dropbtn');
                var dropdownContent = element.querySelector('.dropdown-content');
                dropdownBtn.style.color = '';
                dropdownContent.style.display = 'None';
            });
        }
        const sanitizedId = idValue.replace(/\s/g, '').replace(".", ''); // Remove spaces and "." from the ID
        const elements = document.querySelectorAll(`#${sanitizedId}.mention_doc_id`);
        elements.forEach(element => {
            var dropdownBtn = element.querySelector('.dropbtn');
            var dropdownContent = element.querySelector('.dropdown-content');
            dropdownBtn.style.color = 'red';
            if (value == 2) {
                dropdownContent.style.display = 'block';
            }

            // Scroll the current element into view smoothly, aligning it to the center
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        });
        previousElement = sanitizedId;
    }

    document.addEventListener('click', function(event) {
    // Selectors to exclude
    const selectors = [
        '.structure',
        '.mention_search_doc_id',
        '.dropbtn'
    ];

    // Check if the click occurred on any of the excluded elements
    const clickedExcludedElement = selectors.some(selector => event.target.closest(selector));

    if (!clickedExcludedElement) {
        // Handle clicks outside the specified elements
        const elements = document.querySelectorAll('.mention_doc_id');
            elements.forEach(element => {
                var dropdownBtn = element.querySelector('.dropbtn');
                var dropdownContent = element.querySelector('.dropdown-content');
                dropdownBtn.style.color = '';
                dropdownContent.style.display = 'none';
            })
    }
});


    document.querySelectorAll('.mention_doc_id').forEach(item => {
        item.addEventListener('click', event => {
            const elements = document.querySelectorAll('.mention_doc_id');
            elements.forEach(element => {
                var dropdownBtn = element.querySelector('.dropbtn');
                var dropdownContent = element.querySelector('.dropdown-content');
                dropdownBtn.style.color = '';
                dropdownContent.style.display = 'none';
            });
            const idValue = item.getAttribute('id');
            handleClick(idValue, 2);
        });
    });
});