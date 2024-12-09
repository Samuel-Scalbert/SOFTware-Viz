Chart.register(ChartDataLabels);

document.addEventListener('DOMContentLoaded', async (event) => {reorderSoftwareMentions()})

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

async function generateBubbleChart(selector) {
    // Get the current URL
    let url = window.location.href;
    let parts = url.split('/');
    let software_hash;

    if (parts.slice(-1)[0].startsWith("struct-")) {
        software_hash = parts.slice(-2)[0];
    } else {
        software_hash = parts.slice(-1)[0];
    }

    async function getChartData(software_hash) {
        try {
            const response = await fetch(`/chart/${software_hash}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data_chart = await response.json();
            return data_chart;  // Return the data
        } catch (error) {
            console.error('Error fetching chart data:', error);
            return null;  // Return null if there was an error
        }
    }

    // Fetch the chart data
    let full_dataset = await getChartData(software_hash);

    // Check if data is valid
    if (!full_dataset || !Array.isArray(full_dataset) || full_dataset.length === 0) {
        console.error("Invalid chart data:", full_dataset);
        return; // Stop execution if data is invalid
    }

    console.log("full_dataset", full_dataset);

    // Variables to control the chart's axis range
    let xdatamin = full_dataset[1] - 1;
    let xdatamax = full_dataset[2] + 1;
    let ydatamin = 0;
    let ydatamax = full_dataset[3] + 2;

    // Assuming `full_dataset[0]` contains the chart data (datasets)
    let parsedData = full_dataset[0];

    // Make sure parsedData is in the correct format
    if (!Array.isArray(parsedData)) {
        console.error("Invalid data format for chart:", parsedData);
        return; // Stop execution if parsedData is not in the expected format
    }

    console.log('type', typeof parsedData);

    const chartConfig = {
        type: 'bubble',
        data: {
            datasets: parsedData, // Use the fetched dataset
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    suggestedMin: ydatamin,
                    suggestedMax: ydatamax,
                    ticks: {
                        display: true,
                        font: { size: 25 },
                    },
                    title: {
                        display: false,
                        text: 'Nb of occurrences',
                        font: { size: 25 }
                    }
                },
                x: {
                    suggestedMin: xdatamin,
                    suggestedMax: xdatamax,
                    ticks: {
                        display: true,
                        font: { size: 25 },
                        callback: function(value) {
                            return Math.floor(value);  // Only show whole numbers (years)
                        },
                        stepSize: 1
                    },
                    title: {
                        display: false,
                        text: 'Year',
                        font: { size: 25 }
                    }
                }
            },
            events: ['mouseout'],
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: {
                            size: 25
                        },
                        filter: function(item) {
                            return !item.text.includes('label');
                        }
                    }
                },
                datalabels: {
                    anchor: function(context) {
                        var value = context.dataset.data[context.dataIndex];
                        return value.v < 20 ? 'end' : 'center';
                    },
                    align: function(context) {
                        var value = context.dataset.data[context.dataIndex];
                        return value.v < 20 ? 'end' : 'center';
                    },
                    color: 'black',
                    font: {
                        weight: 'bold',
                        size: 25,
                    },
                    formatter: function(value) {
                        if (value.display_custom && value.display_custom === 'on') {
                            return Math.round(value.v);
                        }
                        return value.display_custom === 'off' ? null : Math.round(value.v);
                    },
                    offset: 1,
                    padding: 0
                },
                tooltip: { enabled: false }
            },
            layout: {
                padding: 30
            },
            elements: {
                point: {
                    radius: function(context) {
                        var value = context.dataset.data[context.dataIndex];
                        var size = context.chart.width;
                        var base = Math.abs(value.v) / 15;
                        return (size / 24) * base ;
                    }
                }
            },
            animation: {
                duration: 0
            },
            hover: {
                animationDuration: 0
            },
            responsiveAnimationDuration: 0
        }
    };

    // Initialize the chart
    const ctx = document.querySelector(selector);
    const chart = new Chart(ctx.getContext('2d'), chartConfig);

    // Handle chart click events
    ctx.onclick = (evt) => {
        const points = chart.getElementsAtEventForMode(
            evt,
            'nearest',
            { intersect: true },
            true
        );
        if (points.length) {
            const firstPoint = points[0];
            const datasetPoint = firstPoint.datasetIndex;
            const dataPoint = firstPoint.index;
            if (chart.data.datasets[datasetPoint].data[dataPoint].label) {
                const software = document.getElementById("software_name");
                showSources(chart.data.datasets[datasetPoint].data[dataPoint].label, software.getAttribute("class"));
                showStructures(chart.data.datasets[datasetPoint].data[dataPoint].label, software.getAttribute("class"));
                showAuthors(chart.data.datasets[datasetPoint].data[dataPoint].label);
            }
        }
    };
}


async function showStructures(hal_id_list, software) {
    const uniqueStructures = new Set();
    let softwareName;
    if (software !== "") {
        softwareName = software;
    } else {
        softwareName = window.location.pathname.split('/').pop();
    }
    try {
        // Fetch the list of institution types once
        const response = await fetch(`/api/list_type_institution`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const institutionTypes = await response.json();

        // Select the target div for displaying structures
        const searchDiv = document.querySelector('.structureContainer_chart');

        // Iterate over each hal_id and institution type
        hal_id_list.forEach(hal_id => {
            institutionTypes.forEach(async (type_institution) => {
                try {
                    // Fetch the list of institutions for the current type and hal_id
                    const response = await fetch(`/api/list_institution/${type_institution}/chart_halid/${hal_id}`);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data_insti = await response.json();
                    console.log(data_insti)
                    // Process and add institutions to the DOM
                    data_insti.forEach(insti => {
                        // Check if the structure with the same 'ref' already exists
                        if (!document.querySelector(`.structure_chart[ref="${insti.ref}"]`)) {
                            const structureHtml = `
                                <div><a style="color:black" class="structure_chart" href="/${softwareName}/${insti.ref}" ref="${insti.ref}" acro="${insti.acronym ? insti.acronym : ''}">
                                    ${insti.name} (<span class="${insti.status}">${insti.status}</span>
                                    ${insti.acronym ? ` - <span style="font-weight:bold">${insti.acronym}</span>` : ''})
                                </a></div>`;
                            const sanitizedType = affi_type(type_institution);

                            // Check if the institution type section already exists
                            let institutionDiv = document.querySelector(`.institution_div[data-type="${sanitizedType}"]`);
                            if (!institutionDiv) {
                                // If not found, create a new section for the institution type
                                institutionDiv = document.createElement('div');
                                institutionDiv.className = 'institution_div';
                                institutionDiv.setAttribute('data-type', sanitizedType);
                                institutionDiv.innerHTML = `
                                    <h2 class="toggle-title">${sanitizedType}
                                        <div class="button_insti">
                                            <span class="material-symbols-outlined">keyboard_arrow_down</span>
                                        </div>
                                    </h2>
                                    <div class="institution-list">${structureHtml}</div>`;
                                searchDiv.appendChild(institutionDiv);

                                // Add event listener for toggling visibility of the institution list
                                const title = institutionDiv.querySelector('.toggle-title');
                                title.addEventListener('click', () => {
                                    const institutionList = title.nextElementSibling;
                                    institutionList.classList.toggle('expanded');

                                    const button = title.querySelector('.material-symbols-outlined');
                                    button.innerHTML = (button.innerHTML === "keyboard_arrow_down") ? "keyboard_arrow_up" : "keyboard_arrow_down";
                                });
                            } else {
                                // If section exists, append the new structure to the institution list
                                const institutionList = institutionDiv.querySelector('.institution-list');
                                institutionList.innerHTML += structureHtml;
                            }
                        }
                    });
                } catch (error) {
                    console.error(`Error fetching institution for ${type_institution} and ${hal_id}:`, error);
                }
            });
        });

    } catch (error) {
        console.error('Error fetching institution types:', error);
    }
}

function showAuthors(hal_id_list) {
    // Clear the container before adding new content
    const container = document.getElementById('authorContainer');
    container.innerHTML = '';

    hal_id_list.forEach(async (hal_id) => {
        try {
            const response = await fetch(`/api/soft_aut/${hal_id}`, {
                method: "GET"
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const uniqueAuthors = new Set(data); // Assuming data is an array of authors

            // Create a section for each hal_id
            const halSection = document.createElement('div');

            const halTitle = document.createElement('h2');
            halTitle.className = "toggle-title"; // Set class to toggle-title
            halTitle.textContent = `${hal_id}`; // Display the hal_id in the title

            // Create the anchor element for hal_id (visually separate but still clickable)
            const halLink = document.createElement('a');
            halLink.href = `/doc/${hal_id}`; // Link to the document
            halLink.textContent = "(link)"; // Display link text

            // Create a toggle button
            const toggleButton = document.createElement('div');
            toggleButton.classList.add('button_insti');
            toggleButton.innerHTML = `<span class="material-symbols-outlined">keyboard_arrow_down</span>`;
            halTitle.appendChild(halLink);
            halTitle.appendChild(toggleButton);
            halSection.appendChild(halTitle); // Add title to hal section

            // Create a nested list for authors
            const authorsNestedList = document.createElement('ul');
            halSection.appendChild(authorsNestedList); // Add nested list to hal section

            // Process and add authors to the nested list
            uniqueAuthors.forEach(author => {
                const liTag = document.createElement('p');
                liTag.textContent = author; // Display author name
                authorsNestedList.appendChild(liTag); // Append to nested list
            });

            // Initially hide the author list
            authorsNestedList.style.display = 'none';

            // Add event listener for toggling visibility of the author list
            halTitle.addEventListener('click', () => {
                const isExpanded = authorsNestedList.style.display === 'block';
                authorsNestedList.style.display = isExpanded ? 'none' : 'block'; // Toggle display
                toggleButton.querySelector('.material-symbols-outlined').innerHTML =
                    isExpanded ? "keyboard_arrow_down" : "keyboard_arrow_up"; // Change icon
            });

            // Append the hal section to the main container
            container.appendChild(halSection);

        } catch (error) {
            console.error('Error fetching authors:', error);
        }
    });
}

function showSources(hal_id_list, software) {
    let softwareName;
    if (software !== "") {
        softwareName = software;
    } else {
        softwareName = window.location.pathname.split('/').pop();
    }
    const container = document.getElementById('sourceContainer');
    container.innerHTML = ''; // Clearing the container before adding new elements

    hal_id_list.forEach(hal_id => {
        const pTag = document.createElement('a');
        pTag.textContent = hal_id;
        pTag.href = `/doc/${hal_id}/${softwareName}`; // Assuming you want the hal_id to link to its corresponding API
        pTag.style.display = "block";
        container.appendChild(pTag);
    });
}



function generateCircleChart(selector, value1, value2, value3) {
    const chartConfig = {
        type: 'pie',
        data: {
            labels: ["Used", "Created", "Shared"],
            datasets: [{
                backgroundColor: ["#6C9BCF", "#363949", "#677483"],
                data: [value1, value2, value3],
                borderWidth: 1,
                cutout: '20%',
            }]
        },
        options: {
            responsive: true,
            animation: {
                animateScale: true, // This enables scaling animation on initial load
                animateRotate: true, // This animates rotation if desired
                duration: 1000, // Adjust the duration of the animation (1 second)
                easing: 'easeOutQuart', // Smooth easing for animation
            },
            plugins: {
                tooltip: {
                    enabled: true, // Enable tooltips
                },
                legend: {
                    display: true, // Display the legend
                },
                datalabels: {
                    display: false, // Disable data labels
                }
            },
            layout: {
                padding: 20 // Add padding around the chart
            },
            elements: {
                arc: {
                    borderWidth: 1 // Set border width of each pie slice
                }
            },
        },
        plugins: [{
            beforeDraw: function(chart) {
                const width = chart.width;
                const height = chart.height;
                const ctx = chart.ctx;

                ctx.restore();
                ctx.font = 'bold 55px sans-serif';
                ctx.textAlign = 'center';
                chart.ctx.fillStyle = "black";
            },
        }]
    };

    const ctx = document.querySelector(selector);
    if (!ctx) {
        console.error("Canvas element not found!");
        return;
    }

    new Chart(ctx.getContext('2d'), chartConfig);
}