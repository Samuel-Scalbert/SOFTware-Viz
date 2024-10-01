document.addEventListener('DOMContentLoaded', async (event) => {

    function affi_type(str) {
        const typeMap = {
            "department": "Department",
            "institution": "Institution",
            "laboratory": "Laboratory",
            "regroupinstitution": "Regroup Institution",
            "regrouplaboratory": "Regroup Laboratory",
            "researchteam": "Research Team"
        };

        // Return the formatted string if it exists in the map, otherwise return the original string
        return typeMap[str] || str;
    }

    try {
        // Fetch the list of authors from the API
        const response = await fetch(`/api/author/list_authors`, {
            method: "GET"
        });

        // Check if the response is OK (status code 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the response as JSON
        const Author_list = await response.json();

        // Example of using the Author_list
        const resultBox = document.getElementById("result-box-dis");
        const inputBox = document.getElementById("input-box-dis");
        const authorBox = document.getElementById("author-box");

        inputBox.onkeyup = function() {
            let result = [];
            let input = inputBox.value;

            if (input.length) {
                // Filter the authors based on the input
                result = Author_list.filter((author) => {
                    // author[0] is the name and author[1] is the ID
                    return author[0].toLowerCase().includes(input.toLowerCase());
                });

                // Create HTML content with IDs set to author IDs
                const content = result.map((author) => {
                    return `<div class='mention_search_auth_id' id="${author[1]}">${author[0]}</div>`;
                }).join('');

                // Display the results
                resultBox.innerHTML = `<div class='dropdown-content-search'>${content}</div>`;
                resultBox.style.height = '150px';
                resultBox.style.overflowY = 'scroll';
                resultBox.style.display = 'block'; // Ensure resultBox is displayed
            } else {
                resultBox.innerHTML = ""; // Clear the result box if the input is empty
                resultBox.style.display = 'none'; // Hide resultBox when there's no input
            }
        };

        resultBox.addEventListener('click', async function(event) {
            if (event.target && event.target.classList.contains('mention_search_auth_id')) {
                resultBox.style.display = 'none';
                const auth_id = event.target.id;
                console.log(`/api/author/${auth_id}`)
                try {
                    // Fetch the author details using the ID
                    const response = await fetch(`/api/author/${auth_id}`, {
                        method: "GET"
                    });

                    // Check if the response is OK (status code 200-299)
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    // Parse the response JSON
                    const auth_info = await response.json();
                    console.log("full info:",auth_info[0]);
                    const soft_info = auth_info[0].software_names;

                    // Create a new author card
                    const authorCard = document.createElement('div');
                    authorCard.classList.add('author_card');
                    authorCard.id = auth_id;

                    let documentsList = '<ul>';
                    auth_info[0].author.documents.forEach(dict_doc=> {
                        documentsList += `<li class="${dict_doc.role}"><a href="/doc/${dict_doc.document_halid}">${dict_doc.document_halid}</a></li>`;
                    });
                    documentsList += '</ul>';


                    let affiList = '<ul>';
            auth_info[0].structures.forEach(affi => {
                const affi_type_cleaned = affi_type(affi.struc.type);  // Ensure affi_type is defined
                let affi_card;
                if (affi.struc.acronym) {
                    affi_card = `<h4>${affi.struc.acronym} (${affi_type_cleaned})</h4>`;
                } else {
                    affi_card = `<h4>${affi_type_cleaned}</h4>`;
                }
                if (affi.struc.status) {
                    affi_card += `<p class="status">Status: <span class="${affi.struc.status}">${affi.struc.status}</span></p>`;
                }

                if (affi.struc.url_team) {
                    affi_card += `<p>${affi.struc.name} (<a href='${affi.struc.url_team}'>url</a>)</p>`;
                } else {
                    affi_card += `<p>${affi.struc.name}</p>`;
                }

                affi_card += `<p>AureHAL ID: <a href='https://aurehal.archives-ouvertes.fr/structure/read/id/${affi.struc.id_haureal}'>${affi.struc.id_haureal}</a></p>`;

                affiList += `<li>${affi_card}</li>`;  // Add the affi_card to the list
            });
            affiList += '</ul>';
                    let software_list = '<ul>';
                    soft_info.forEach(soft_list => {
                            let soft_tag = `<li><a href="/doc/${soft_list[1]}/${soft_list[0]}">${soft_list[0]}</a>(${soft_list[1]})</li>`
                            software_list += soft_tag
                        });
                    software_list += '</ul>';
                    console.log(software_list)
                    // Assuming auth_info is an object, format it for display
                    authorCard.innerHTML = `
                        <h2>${auth_info[0].author.name.surname} ${auth_info[0].author.name.forename} </h2>
                        <p>Hal ID: ${auth_info[0].author.id.halauthorid}</p>
                        <p>Documents: ${documentsList}</p>
                    `;

                    if (auth_info[0].structures.length > 0){
                        authorCard.innerHTML += `<p>Affiliations: ${affiList}</p>`;
                    }
                    else {authorCard.innerHTML += `<p>We found no affiliations for this author</p>`;}

                    if (soft_info.length > 0) {
                        authorCard.innerHTML += `<p>Softwares: ${software_list}</p>`;
                    }
                    else {authorCard.innerHTML += `<p>No softwares associated with this author</p>`;}
                    // Prepend the new card to the top of the author box
                    authorBox.prepend(authorCard);

                } catch (error) {
                    // Handle any errors that occurred during the fetch
                    console.error('Error fetching the author details:', error);
                }
            }
        });

    } catch (error) {
        // Handle any errors that occurred during the fetch
        console.error('Error fetching the author list:', error);
    }
});
