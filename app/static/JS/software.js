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
    }
});
