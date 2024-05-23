<p align="center">
    <h1 align="center">SOFTware-Viz</h1>
</p>
<p align="center">
	<!-- local repository, no metadata badges. -->
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/HTML5-E34F26.svg?style=default&logo=HTML5&logoColor=white" alt="HTML5">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=default&logo=Python&logoColor=white" alt="Python">
</p>

<br><!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary><br>

- [ Overview](#-overview)
- [ Features](#-features)
- [ Repository Structure](#-repository-structure)
- [ Modules](#-modules)
- [ Getting Started](#-getting-started)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Tests](#-tests)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)
</details>
<hr>

##  Overview

<code>► INSERT-TEXT-HERE</code>

---

##  Features

<code>► INSERT-TEXT-HERE</code>

---

##  Repository Structure

```sh
└── /
    ├── README.md
    ├── Utils
    │   ├── __init__.py
    │   ├── dashboard.py
    │   ├── doc_info.py
    │   ├── insert_json_db.py
    │   └── software_mentions.py
    ├── app
    │   ├── __init__.py
    │   ├── app.py
    │   ├── routes
    │   ├── static
    │   └── templates
    ├── requirement.txt
    └── run.py
```

---

##  Modules

<details closed><summary>.</summary>

| File                               | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ---                                | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [run.py](run.py)                   | The run script launches the main application, acting as an entry point. It initializes and runs our web application, ensuring seamless operation of various routes, templates, and static assets housed within the app directory, while leveraging utilities such as dashboard functionality, data insertion into the database, software mention analysis, and documentation tools defined in the Utils folder. This orchestration brings our dynamic web solution to life. |
| [requirement.txt](requirement.txt) | This `requirement.txt` file serves as a list of necessary libraries for the software project, ensuring smooth functioning within its ecosystem. Libraries like Flask, Werkzeug, and pyArango, among others, facilitate the building and deployment of web applications and database management tasks in this project.                                                                                                                                                       |

</details>

<details closed><summary>app</summary>

| File                 | Summary                                                                                                                                                                                                                                                                                                                                                  |
| ---                  | ---                                                                                                                                                                                                                                                                                                                                                      |
| [app.py](app/app.py) | Inits ArangoDB connection and imports necessary modules for managing and visualizing software data. Initializes the database using static files located under json_files and saves the results to result. Provides default landing page and sets up routes for documentation, dashboard, reset, count, mentions, and API functions in the Flask web app. |

</details>

<details closed><summary>app.templates.partials</summary>

| File                                                    | Summary                                                                                                                                                                                                                                                           |
| ---                                                     | ---                                                                                                                                                                                                                                                               |
| [conteneur.html](app/templates/partials/conteneur.html) | App/templates/partials/conteneur.html`. This template serves as the basic layout for SOFtware-Vizs pages, structuring headers, footers, and main content sections, ensuring consistent navigation to different routes like Dashboard', software_count, and more." |

</details>

<details closed><summary>app.templates.pages</summary>

| File                                                                 | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ---                                                                  | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| [software_mentions.html](app/templates/pages/software_mentions.html) | Showcases an HTML template for visualizing software mentions data within a dynamic dashboard. This file integrates Chart.js library to display software mentions in a bubble chart format. The template receives data in the form of dictionary, providing a visually engaging representation for easier understanding and analysis of the data structure, source, container, and author information.                                                                                                                              |
| [software_counts.html](app/templates/pages/software_counts.html)     | Displays software count recap on dashboard, this template leverages data from the `software_mentions.py` module within the repositorys Utils folder, enhancing the visual presentation of analyzed software statistics within the application.                                                                                                                                                                                                                                                                                     |
| [doc_wsoftware.html](app/templates/pages/doc_wsoftware.html)         | Displays structured documentation for a software within the platforms dashboard, highlighting key contexts, abstract, source details, associated files, and links to related software. Utilizes template inheritance and Jinja2 syntax to dynamically generate content, enhancing usability and consistency across multiple document views.                                                                                                                                                                                        |
| [dashboard.html](app/templates/pages/dashboard.html)                 | HTML template for dashboard pageFunctionality: Renders the DashBoard, showcasing key performance indicators (KPIs) related to software mentions in documents stored in the database. This includes number of docs with/without mentions, total mentions, as well as breakdown per individual software, showing shared, created and used mentions for each. Additionally, a search bar allows users to look up specific documents efficiently. A circular chart visually summarizes KPIs using data passed from the backend server. |

</details>

<details closed><summary>app.routes</summary>

| File                                                                | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---                                                                 | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| [software_mentions_route.py](app/routes/software_mentions_route.py) | The `software_mentions_route.py` file serves as a routing mechanism in this repository, directing the web application to display data on software mentions when a specific software is specified in the URL. The function `software_all_mentions`, found within the `Utils` module, collects and processes the required data from the database, while `dataset_creator` formats it for visualization in HTML templates.                                                                                                                                                                                    |
| [software_count_route.py](app/routes/software_count_route.py)       | In this repository, the provided `software_count_route.py` file contributes by generating and delivering software count statistics to an HTML template within the Flask application. This enables the user interface (UI) to display detailed data about multiple instances of software across documents stored in the database. The collected data is only shown if there are more than one instance to ensure data relevance for users.                                                                                                                                                                  |
| [reset_db.py](app/routes/reset_db.py)                               | This module, `app/routes/reset_db.py`, is a part of the application that offers database reset functionality. When invoked via /resett endpoint, it initiates a full reset of all collections stored within the application database. This operation prepares the system for fresh operations and data manipulations, ensuring a clean slate for proper application functioning.                                                                                                                                                                                                                           |
| [doc.py](app/routes/doc.py)                                         | Generates web-accessible links to document pages for a given application, pulling data from an ArangoDB database using utilities provided in the Utils' module. Each generated link leads to the respective document page, and can optionally filter documents by associated software."                                                                                                                                                                                                                                                                                                                    |
| [dashboard_route.py](app/routes/dashboard_route.py)                 | In this Flask web application, `dashboard_route.py` handles user requests to /dashboard and /dashboard/<structure>. It fetches data from the Utils.dashboard module, which presumably aggregates and analyzes project data based on the database and provided structure, before rendering a tailored HTML dashboard. This streamlines the process of monitoring key metrics, enhancing usability and efficiency within our open-source platform.                                                                                                                                                           |
| [api_route.py](app/routes/api_route.py)                             | This code module (`app/routes/api_route.py`) within our repository serves APIs that fetch data from the database. By employing functions like `links_structures()` and `links_authors()`, it delivers JSON representations of the structures associated with a given document, as well as a list of the documents author names. It communicates seamlessly with our `Utils/software_mentions` module to leverage its functionality in serving the requested data. This enables real-time analysis of documents and offers efficient access to crucial metadata for users interacting with our application. |

</details>

<details closed><summary>Utils</summary>

| File                                               | Summary                         |
| ---                                                | ---                             |
| [software_mentions.py](Utils/software_mentions.py) | <code>► INSERT-TEXT-HERE</code> |
| [insert_json_db.py](Utils/insert_json_db.py)       | <code>► INSERT-TEXT-HERE</code> |
| [doc_info.py](Utils/doc_info.py)                   | <code>► INSERT-TEXT-HERE</code> |
| [dashboard.py](Utils/dashboard.py)                 | <code>► INSERT-TEXT-HERE</code> |

</details>

---

##  Getting Started

**System Requirements:**

* **Python**: `version x.y.z`

###  Installation

<h4>From <code>source</code></h4>

> 1. Clone the  repository:
>
> ```console
> $ git clone ../
> ```
>
> 2. Change to the project directory:
> ```console
> $ cd 
> ```
>
> 3. Install the dependencies:
> ```console
> $ pip install -r requirements.txt
> ```

###  Usage

<h4>From <code>source</code></h4>

> Run  using the command below:
> ```console
> $ python main.py
> ```

###  Tests

> Run the test suite using the command below:
> ```console
> $ pytest
> ```

---

##  Project Roadmap

- [X] `► INSERT-TASK-1`
- [ ] `► INSERT-TASK-2`
- [ ] `► ...`

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://local/SOFTware-Viz/issues)**: Submit bugs found or log feature requests for the `` project.
- **[Submit Pull Requests](https://local/SOFTware-Viz/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://local/SOFTware-Viz/discussions)**: Share your insights, provide feedback, or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your local account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone ../
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to local**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="center">
   <a href="https://local{/SOFTware-Viz/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=SOFTware-Viz">
   </a>
</p>
</details>

---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-overview)

---
