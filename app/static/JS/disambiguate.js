function software_dup_displayer(software_name){
    fetch(`/api/disambiguate/${software_name}`, {
        method: "GET"
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        console.log(response.json());
       return response.json();
    })
}

document.addEventListener('DOMContentLoaded', (event) => {
    fetch(`/api/disambiguate/list_software`, {
        method: "GET"
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Assuming `data` is an array of software names
        const availableSoftware = data;
        const availableSoftwareND = Array.from(availableSoftware);
        const resultBox = document.getElementById("result-box-dis");
        const inputBox = document.getElementById("input-box-dis");
        const resultBox_dup = document.getElementById("result-dup");

        // Event delegation for resultBox
        resultBox.addEventListener('click', async function(event) {
            if (event.target && event.target.classList.contains('mention_search_doc_id')) {
                resultBox.style.display = 'none';
                console.log("Target", event.target.id);
                try {
                    const possible_software_dup = await software_displayer(event.target.id);
                    console.log("Result", possible_software_dup);

                    if (Array.isArray(possible_software_dup)) {
                        const content_dup = possible_software_dup.map(software_dup => {
                            return `<div>${software_dup}</div>`;
                        }).join('');
                        resultBox_dup.innerHTML = content_dup;
                    } else {
                        resultBox_dup.innerHTML = 'No details available.';
                    }
                } catch (error) {
                    console.error('Error fetching software details:', error);
                    resultBox_dup.innerHTML = 'Error fetching details.';
                }
            }
        });

        inputBox.onkeyup = function() {
            let result = [];
            let input = inputBox.value;
            if (input.length) {
                result = availableSoftwareND.filter((keyword) => {
                    return keyword.toLowerCase().includes(input.toLowerCase());
                });
                const content = result.map((list) => {
                    return `<div class='mention_search_doc_id' id="${list}">${list}</div>`;
                }).join(''); // Join the array elements into a single string without any separator
                resultBox.innerHTML = `<div class='dropdown-content-search'>${content}</div>`;
            } else {
                resultBox.innerHTML = ""; // Clear the result box if the input is empty
            }
        }
    })
    .catch(error => {
        console.error('Error fetching the software list:', error);
    });
});

