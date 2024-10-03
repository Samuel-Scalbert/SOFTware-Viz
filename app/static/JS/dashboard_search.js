// Helper function to format institution types
function affi_type(str) {
    const typeMap = {
        "department": "Department",
        "institution": "Institution",
        "laboratory": "Laboratory",
        "regroupinstitution": "Regroup Institution",
        "regrouplaboratory": "Regroup Laboratory",
        "researchteam": "Research Team"
    };
    return typeMap[str] || str;
}

// Load structures and setup event listeners
document.addEventListener('DOMContentLoaded', () => {
    const searchDiv = document.querySelector('.structures');
    const currentPath = window.location.pathname;

    // Check if the URL ends with /dashboard or a specific structure ID
    const isSpecificStructure = currentPath.startsWith('/dashboard/struct-');
    const specificStructId = isSpecificStructure ? currentPath.split('/').pop() : null; // Extract structure ID if it exists

    // Fetch the list of institution types from the API
    fetch(`/api/list_type_institution`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {

            // Define the desired order of institution types
            const typeOrder = [
                "researchteam",        // Highest priority (appears at the top)
                "laboratory",
                "department",
                "institution",
                "regrouplaboratory",
                "regroupinstitution"   // Lowest priority (appears at the bottom)
            ];

            // Sort the institution types according to the desired order
            const sortedData = data.sort((a, b) => {
                return typeOrder.indexOf(a) - typeOrder.indexOf(b);
            });

            // Depending on the URL, fetch either all structures or the specific structure
            const contentPromises = sortedData.map(type_institution => {
                const url = isSpecificStructure
                    ? `/api/list_institution/${type_institution}/${specificStructId}`
                    : `/api/list_institution/${type_institution}`;

                return fetch(url)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then(data_insti => {

                        // Check if data_insti is empty
                        if (data_insti.length === 0) {
                            return '';  // Return an empty string if no institutions
                        }

                        // Sort institutions alphabetically by their name
                        data_insti.sort((a, b) => a.name.localeCompare(b.name));

                        // Generate HTML for each institution
                        const listStructure = data_insti.map(insti =>
                           `<div class="structure" ref="${insti.ref}" acro="${insti.acronym ? `${insti.acronym}` : ''}">
                                <div class="monitor-icon">
                                    <a href="/dashboard/${insti.ref}">
                                        <span class="material-symbols-outlined">monitoring</span>
                                    </a>
                                </div>
                                <span class="structure-text">
                                    ${insti.name} (<span class="${insti.status}">${insti.status}</span>${insti.acronym ? ` - <span style="font-weight:bold">${insti.acronym}</span>` : ''})
                                </span>
                            </div>
                        `
                        ).join('');

                        const sanitizedType = affi_type(type_institution);
                        return `<div class="institution_div">
                                    <h2 class="toggle-title">${sanitizedType} 
                                    <div class="button_insti">
                                    <span class="material-symbols-outlined">keyboard_arrow_down</span></div>
                                    </h2>
                                    <div class="institution-list">${listStructure}</div>
                                </div>`;
                    });
            });

            // Once all content is fetched and processed, update the DOM
            Promise.all(contentPromises).then(contents => {
                // Filter out empty strings from the contents
                const filteredContents = contents.filter(content => content !== '');
                searchDiv.innerHTML = '<h1>Structures</h1>' + filteredContents.join('');

                // Set up event listeners for the toggle titles
                const titles = document.querySelectorAll('.toggle-title');
                titles.forEach(title => {
                    title.addEventListener('click', () => {
                        const institutionList = title.nextElementSibling;
                        institutionList.classList.toggle('expanded');

                        const button = title.querySelector('.material-symbols-outlined');
                        button.innerHTML = (button.innerHTML === "keyboard_arrow_down") ? "keyboard_arrow_up" : "keyboard_arrow_down";
                    });
                });

                // After content is added, set up event listeners for structure elements
                setupStructureClickEvents();
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
});




// Setup event listeners for structure elements
function setupStructureClickEvents() {
    let last_clicked_structure = null;

    document.querySelectorAll('.structure').forEach(item => {
        item.addEventListener('click', event => {
            if (last_clicked_structure) {
                last_clicked_structure.style.color = 'black';
            }
            if (event.target.tagName === 'SPAN' && event.target.classList.contains('material-symbols-outlined')) {
                event.stopPropagation();
                return;
            }
            if (event.target.tagName === 'A') {
                event.stopPropagation();
                return;
            }
            last_clicked_structure = item;
            item.style.color = 'red';
            updateRecap(item.getAttribute('ref'));

            // Reset other UI elements
            const elements = document.querySelectorAll('.mention_doc_id');
            elements.forEach(element => {
                var dropdownBtn = element.querySelector('.dropbtn');
                var dropdownContent = element.querySelector('.dropdown-content');
                dropdownBtn.style.color = '';
                dropdownContent.style.display = 'none';
            });

            // Fetch data for the clicked item
            const ref = item.getAttribute('ref');
            fetch(`/api/id_struc/${ref}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    // Process the fetched data
                    if (data.length == 0) {
                        alert("No software for this structure\n" +
                            "If you have a better idea on how to display this message feel free to open an issue")
                    }
                    else {
                        processFetchedData(data);}
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        });
    });
}

// Process fetched data and update the UI
function processFetchedData(data) {
    function chunkArray(array, chunkSize) {
        const chunks = [];
        for (let i = 0; i < array.length; i += chunkSize) {
            chunks.push(array.slice(i, i + chunkSize));
        }
        return chunks;
    }

    const dataChunks = chunkArray(data, 50);

    function processChunk(chunkIndex) {
        if (chunkIndex >= dataChunks.length) {
            reorderSoftwareMentions();
            return;
        }

        const chunk = dataChunks[chunkIndex];

        chunk.forEach(software_name => {
            const software = software_name ? software_name
                .replace(/\s/g, '')  // Remove all whitespace
                .replace(/\./g, '')  // Remove all periods
                .replace(/@/g, '')  // Escape '@'
                .replace(/\(/g, '')  // Escape '('
                .replace(/\)/g, '')  // Escape ')'
                .replace(/\*/g, '')  // Escape '*'
                .replace(/[0-9]/g, '')  // Escape [0,9]
                .replace(/\//g, '')  // Escape \
                .replace(/\+/g, '')  // Escape '+'
                .replace(/\'/g, '')  // Escape '
                .replace(/\"/g, '')  // Escape "
                : '';

            document.querySelectorAll(`#${software}.mention_doc_id`).forEach(element => {
                var dropdownBtn = element.querySelector('.dropbtn');
                dropdownBtn.style.color = 'red';
                element.parentNode.prepend(element);
            });
        });

        processChunk(chunkIndex + 1);
    }

    processChunk(0);
}

// Reorder software mentions based on their color and number
function reorderSoftwareMentions() {
    const listSoftwareContainers = document.querySelectorAll(".list-software");

    listSoftwareContainers.forEach(container => {
        const softwareDivs = Array.from(container.getElementsByClassName("mention_doc_id"));

        const redSoftware = [];
        const otherSoftware = [];

        softwareDivs.forEach(div => {
            const isRed = window.getComputedStyle(div.querySelector('button')).color === 'rgb(255, 0, 0)';
            if (isRed) {
                redSoftware.push(div);
            } else {
                otherSoftware.push(div);
            }
        });

        const sortByNumberDesc = (a, b) => {
            const aNumber = parseInt(a.querySelector(".dropbtn").getAttribute("number"));
            const bNumber = parseInt(b.querySelector(".dropbtn").getAttribute("number"));
            return bNumber - aNumber;
        };

        redSoftware.sort(sortByNumberDesc);
        otherSoftware.sort(sortByNumberDesc);

        redSoftware.forEach(div => container.appendChild(div));
        otherSoftware.forEach(div => container.appendChild(div));
    });
}
