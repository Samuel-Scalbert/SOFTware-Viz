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
        // Reset the dropdowns
        const elements = document.querySelectorAll('.mention_doc_id');
        elements.forEach(element => {
            var dropdownBtn = element.querySelector('.dropbtn');
            var dropdownContent = element.querySelector('.dropdown-content');
            dropdownBtn.style.color = '';
            dropdownContent.style.display = 'none';
        });

        // Fetch data based on the clicked item text content
        fetch(`/api/id_struc/${item.textContent.trim()}`, {
            method: "GET"
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Number of documents:', data.length);

            // Split the data into chunks of 50
            function chunkArray(array, chunkSize) {
                const chunks = [];
                for (let i = 0; i < array.length; i += chunkSize) {
                    chunks.push(array.slice(i, i + chunkSize));
                }
                return chunks;
            }

            const dataChunks = chunkArray(data, 50);

            // Process each chunk sequentially
            function processChunk(chunkIndex) {
                if (chunkIndex >= dataChunks.length) {
                    return;
                }

                console.time(`Process Chunk ${chunkIndex + 1}`);
                const chunk = dataChunks[chunkIndex];

                chunk.forEach(software_name => {
                    software = CSS.escape(software_name).replace(" ", '').replace(".", '')
                    software = CSS.escape(software)
                    console.log("\'",software,"\'")
                    const soft_div = document.querySelectorAll(`#${software}.mention_doc_id`);
                    soft_div.forEach(element => {
                        var dropdownBtn = element.querySelector('.dropbtn');
                        dropdownBtn.style.color = 'red';
                    });
                });

                console.timeEnd(`Process Chunk ${chunkIndex + 1}`);

                // Process the next chunk
                setTimeout(() => processChunk(chunkIndex + 1), 0);
            }

            processChunk(0);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
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
        const sanitizedId = idValue.replace(/\s/g, '').replace(".", '')?.replace("@",'\\@'); // Remove spaces and "." from the ID
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
        const elements_search =document.querySelectorAll('.dropdown-content-search');
            elements.forEach(element => {
                var dropdownBtn = element.querySelector('.dropbtn');
                var dropdownContent = element.querySelector('.dropdown-content');
                dropdownBtn.style.color = '';
                dropdownContent.style.display = 'none';
                elements_search.forEach(searchElement => {searchElement.style.display = 'none';})
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