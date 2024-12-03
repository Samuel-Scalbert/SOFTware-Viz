document.addEventListener('DOMContentLoaded', (event) => {

    const url_info = window.location.pathname.split('/').pop();
    const div_block = document.getElementsByClassName("software_canva_info");

    // Ensure div_block is not empty
    if (div_block.length > 0) {
        if (url_info.startsWith('struct-')) {
            fetch(`/api/soft/${url_info}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const title_block = document.createElement('div');
                title_block.className = "titre-block";
                title_block.innerHTML = `<h2 style="padding: 5px">${window.location.pathname.split('/', 2).pop()}/${data}</h2>`;
                // Insert at the top of the div
                div_block[0].insertBefore(title_block, div_block[0].firstChild);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
        } else {
            const title_block = document.createElement('div');
            title_block.className = "titre-block";
            title_block.innerHTML = `<h2 style="padding: 5px">${url_info}</h2>`;
            // Insert at the top of the div
            div_block[0].insertBefore(title_block, div_block[0].firstChild);
        }
    };

    async function setupSoftwareSearch() {
        try {
            const response = await fetch(`/api/disambiguate/list_software`, { method: "GET" });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const availableSoftwareND = await response.json();
            console.log(availableSoftwareND);

            const resultBox = document.getElementById("result-box-software");
            const inputBox = document.getElementById("input-box-software");

            // Debounce function to delay input handling
            function debounce(func, wait) {
                let timeout;
                return function (...args) {
                    clearTimeout(timeout);
                    timeout = setTimeout(() => func.apply(this, args), wait);
                };
            }

            function displayResult(results) {
                const content = results.map(keyword =>
                    `<div class='mention_search_doc_id' id="${keyword}">${keyword}</div>`
                ).join('');
                resultBox.style.display = results.length ? 'block' : 'none';
                resultBox.innerHTML = `<div class='dropdown-content-search'>${content}</div>`;

                // Add event listeners for new result items
                document.querySelectorAll('.mention_search_doc_id').forEach(item => {
                    item.addEventListener('click', function () {
                        const idValue = this.getAttribute('id');
                        handleClick(idValue);
                        resultBox.style.display = 'none';
                        resultBox.innerHTML = ""; // Clear results
                    });
                });
            }

            inputBox.onkeyup = debounce(function () {
                const input = inputBox.value.trim();
                if (input.length) {
                    const results = availableSoftwareND.filter(keyword =>
                        keyword.toLowerCase().includes(input.toLowerCase())
                    );
                    displayResult(results);
                } else {
                    resultBox.style.display = 'none';
                    resultBox.innerHTML = "";
                }
            }, 300); // Debounce delay of 300ms
        } catch (error) {
            console.error('Error fetching software list:', error);
        }
    }

    // Call the setup function on page load
    setupSoftwareSearch();

    function handleClick(softwareName) {
    // Navigate to a new URL, passing the software name as part of the path or query string
    const url = `/${softwareName}`;
    window.location.href = url;
}



});
