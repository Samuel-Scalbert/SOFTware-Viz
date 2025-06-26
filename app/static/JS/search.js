document.addEventListener('DOMContentLoaded', () => {
  const searchBar = document.getElementById('es-searchBar');
  const filterButtons = document.querySelectorAll('.filter-buttons button');
  const resultsContainer = document.getElementById('results'); // Assuming you have a div to show results

  function activateFilter(filterValue) {
    filterButtons.forEach(btn => {
      if (btn.getAttribute('data-filter') === filterValue) {
        btn.classList.add('active-filter');
      } else {
        btn.classList.remove('active-filter');
      }
    });

    searchBar.disabled = false;
    searchBar.placeholder = "Search metadata...";
    searchBar.dataset.filter = filterValue;
  }

  async function search(query, filter) {
  if (!query) {
    resultsContainer.innerHTML = ''; // Clear results if empty query
    return;
  }
  try {
    const response = await fetch(`/api/search_${filter}?q=${encodeURIComponent(query)}`);
    if (!response.ok) throw new Error("Network response was not ok");
    const results = await response.json();
    console.log('ss',filter)
    if (results.length === 0) {
      resultsContainer.innerHTML = '<a href="#" class="no-result">No results found</a>';
      return;
    }

    else if (filter === 'software') {
      resultsContainer.innerHTML = results.map(r => `<a href="/software/${r.name}">${r.name}</a>`).join('');
    }

    else if (filter === 'document') {
      resultsContainer.innerHTML = results.map(r =>
        `<a href="/doc/${r.doc_id}" class="${r.doc_id}">
           <div>${r.title}</div>
         </a>`
      ).join('');
    }

    else if (filter === 'author') {
      resultsContainer.innerHTML = results.map(r =>
        `<a href="/author?author-id=${r.author_id}">${r.first_name} ${r.last_name}</a>`
      ).join('');
    }

    else if (filter === 'structure') {
  resultsContainer.innerHTML = results.map(r =>
        `<a href="/dashboard/${r.structure_id}">${r.structure}${r.struct_acronym ? ` (${r.struct_acronym})` : ''}</a>`
      ).join('');
    }


    // You can add more if blocks here for other filters

  } catch (err) {
    resultsContainer.innerHTML = `<div>Error: ${err.message}</div>`;
  }
}


  filterButtons.forEach(button => {
    button.addEventListener('click', () => {
      const filter = button.getAttribute('data-filter');
      resultsContainer.innerHTML = '';
      console.log("Filter selected:", filter);
      activateFilter(filter);
      searchBar.focus();
    });
  });

  searchBar.addEventListener('input', () => {
    const query = searchBar.value;
    const filter = searchBar.dataset.filter;
    console.log("Searching for:", query, "with filter:", filter);

    if (filter === "software") {
      search(query, filter);
    }
    if (filter === "document") {
      search(query, filter);
    }
    if (filter === "author") {
      search(query, filter);
    }
    if (filter === "structure") {
      search(query, filter);
    }
    // You can add else if for other filters here if you want
  });

  activateFilter("software");
});
