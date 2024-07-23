document.addEventListener('DOMContentLoaded', async (event) => {
    try {
        const response = await fetch(`/api/disambiguate/list_software`, {
            method: "GET"
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const availableSoftware = await response.json(); // Assuming `data` is an array of software names
        const resultBox = document.getElementById("result-box-dis");
        const inputBox = document.getElementById("input-box-dis");
        const resultBoxDup = document.getElementById("result-dup");
        const noDupBox = document.getElementById("nodup-box");
        const cardBox = document.getElementById("card-box");
        const titleNoDup = document.getElementById("nb-sofwnodup");
        const titleDup = document.getElementById("nb-sofwdup");

        const availableSoftware_sliced = availableSoftware.slice(0, 10);

        let list_dup_software = []

        // Display for each card
        for (const item of availableSoftware_sliced) {
            try {
                if (!list_dup_software.includes(item)){
                    const possibleSoftwareDup = await software_dup_displayer(item);
                    if (Array.isArray(possibleSoftwareDup)) {
                            const contentDup = possibleSoftwareDup.map(softwareDup => {
                                return `<div>${softwareDup}</div>`;
                            }).join('');
                            const software_target = `<div>${item}</div>`;
                            if (contentDup) {
                                possibleSoftwareDup.forEach(software => {list_dup_software.push(software)});
                                list_dup_software.push(item);
                                cardBox.innerHTML += "<div id='software_card'>" + software_target + contentDup + "<div class='button_dup'>More Info</div></div>";
                                let currentNumber = parseInt(titleDup.textContent);
                                currentNumber += 1;
                                titleDup.textContent = currentNumber;
                            } else {
                                noDupBox.innerHTML += `<li>${item}</li>`;
                                let currentNumber = parseInt(titleNoDup.textContent);
                                currentNumber += 1;
                                titleNoDup.textContent = currentNumber;
                            }
                        }}
            } catch (error) {
                console.error('Error fetching software details:', error);
                cardBox.innerHTML += 'Error fetching details.';
            }
        }

        // Event delegation for resultBox
        resultBox.addEventListener('click', async function(event) {
            if (event.target && event.target.classList.contains('mention_search_doc_id')) {
                resultBox.style.display = 'none';
                const nodupBox = document.getElementById('nodup-box');
                const title_nodup = document.getElementById('nodup-title-box');
                if (nodupBox) {
                    const childDivs = nodupBox.querySelectorAll('li');

                    childDivs.forEach(div => {
                        if (div.innerText === event.target.id) {
                        title_nodup.classList.add('animate-bounce');
                        nodupBox.classList.add('animate-bounce');
                        return;
                    }
                    });
                };
                const cardBox = document.getElementById('card-box');
                const cardBox_title = document.getElementById('card-title-box');
                if (cardBox) {
                    const childDivs = cardBox.querySelectorAll('div');
                    childDivs.forEach(div => {
                        if (div.innerText === event.target.id) {
                        div.scrollIntoView({behavior: 'smooth', block: 'center'});
                        const parent = div.closest('#software_card');
                        if (parent) {
                            parent.classList.add('animate-bounce');
                            cardBox_title.classList.add('animate-bounce');
                        }
                        return;
                    }
                    });
                } else {
                    console.error("Element with ID 'card-box' not found.");
                }
            }
        });

        // button for duplicates

        const buttons = document.querySelectorAll('.button_dup');

        buttons.forEach(button => {
            button.addEventListener('click', function() {
                let listSoftwareToSend = [];
                const parent = button.closest('#software_card');
                parent.querySelectorAll('div:not(.button_dup)').forEach(software => {
                    listSoftwareToSend.push(software.innerText);
                });

                // Send the list to the Flask route
                fetch('/receive_list', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ list: listSoftwareToSend })  // Send the list as JSON
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            });
        });

        inputBox.onkeyup = function() {
            let result = [];
            let input = inputBox.value;
            if (input.length) {
                result = availableSoftware.filter((keyword) => {
                    return keyword.toLowerCase().includes(input.toLowerCase());
                });
                const content = result.map((list) => {
                    return `<div class='mention_search_doc_id' id="${list}">${list}</div>`;
                }).join('');
                resultBox.innerHTML = `<div class='dropdown-content-search'>${content}</div>`;
                resultBox.style.height = '150px';
                resultBox.style.overflowY = 'scroll';
                resultBox.style.display = 'block'; // Ensure resultBox is displayed
            } else {
                resultBox.innerHTML = ""; // Clear the result box if the input is empty
                resultBox.style.display = 'none'; // Hide resultBox when there's no input
            }
        };
    } catch (error) {
        console.error('Error fetching the software list:', error);
    }
});

// Function to fetch software details
async function software_dup_displayer(software_name) {
    try {
        const response = await fetch(`/api/disambiguate/${software_name}`, {
            method: "GET"
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    } catch (error) {
        console.error('Error fetching software details:', error);
    }
}
