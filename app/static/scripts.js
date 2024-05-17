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
                    console.log(item)
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
                    console.log(element)
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

    function handleClick(idValue) {
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
        console.log(document.querySelectorAll(`#${sanitizedId}`))
        const elements = document.querySelectorAll(`#${sanitizedId}.mention_doc_id`);
        elements.forEach(element => {
            var dropdownBtn = element.querySelector('.dropbtn');
            var dropdownContent = element.querySelector('.dropdown-content');
            dropdownBtn.style.color = 'red';
            dropdownContent.style.display = 'block';
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
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