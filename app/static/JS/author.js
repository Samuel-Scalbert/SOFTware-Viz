document.addEventListener('DOMContentLoaded', async (event) => {
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

        // Log the list of authors to the console for debugging
        console.log(Author_list);

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

                    // Create a new author card
                    const authorCard = document.createElement('div');
                    authorCard.classList.add('author_card');
                    authorCard.id = auth_id;

                    let documentsList = '<ul>';
                        auth_info[0].documents.forEach((doc) => {
                            documentsList += `<li>${doc}</li>`;
                        });
                        documentsList += '</ul>';

                    // Assuming auth_info is an object, format it for display
                    authorCard.innerHTML = `
                        <h2>${auth_info[0].name.surname} ${auth_info[0].name.forename} </h2>
                        <p>Hal ID: ${auth_info[0].id.halauthorid}</p>
                        <p>Documents: ${auth_info[0].documents}</p>
                        <p>Affiliations: ${auth_info[0].affiliation}</p>
                    `;

                    // Prepend the new card to the top of the author box
                    authorBox.prepend(authorCard);

                    console.log(auth_info);
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
