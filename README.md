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

![Capture d’écran du 2024-06-03 16-39-41](https://github.com/Samuel-Scalbert/SOFTware-Viz/assets/32683708/6be2a593-0508-4e52-a7cb-2cf28b768f00)

![Capture d’écran du 2024-10-18 10-44-19](https://github.com/user-attachments/assets/e8d7bcea-9881-49af-abfc-d92f536b9233)

## Presentation of the project

### DB of PDF
The process begins with a Database of PDF files. These PDFs are scholarly PDFs that need to be extracted and processed.

### GROBID
The PDFs are sent to GROBID, a tool used to extract structured data (like bibliographic information) from scholarly PDFs. GROBID processes the PDFs and outputs XML files. This is a crucial step in extracting machine-readable information from the documents.

### SOFTCITE
After GROBID, the extracted data (likely enriched or supplemented data) is passed to SOFTCITE, which generates JSON outputs. SOFTCITE analyzes citations, software mentions, or related information in the PDF files like references.

### SOFTware-Sync
The extracted data (XML and JSON) is then passed to SOFTware-Sync, which is a tool that synchronizes the data into one single XML.

### SOFTware-Viz
SOFTware-Viz is responsible for visualizing the processed data. It likely takes the synchronized data from SOFTware-Sync and transforms it into visual outputs or dashboards.

### ArangoDB
The processed data is stored in ArangoDB, a multi-model NoSQL database, to manage both structured data. This database serves as the main storage for the extracted information/mentions.

### Flask
Flask is a web framework used for developing web applications. Flask interacts with both SOFTware-Viz (for visualizations) and ArangoDB (for retrieving data).



##  Repository Structure

```sh
├── app
│   ├── app.py
│   ├── __init__.py
│   ├── routes
│   │   ├── api_route.py
│   │   ├── dashboard_route.py
│   │   ├── doc.py
│   │   ├── __init__.py
│   │   ├── reset_db.py
│   │   ├── software_count_route.py
│   │   └── software_mentions_route.py
│   ├── static
│   │   ├── charts.js
│   │   ├── css
│   │   │   └── styles.css
│   │   ├── data
│   │   │   ├── json_files
│   │   │   ├── pdf_files
│   │   │   ├── xml_files
│   │   │   └── xml_meta
│   │   ├── result
│   │   │   ├── CSV_software
│   │   │   ├── XML_meta_software
│   │   │   └── XML_software
│   │   └── scripts.js
│   └── templates
│       ├── pages
│       │   ├── dashboard.html
│       │   ├── doc_wsoftware.html
│       │   ├── software_counts.html
│       │   └── software_mentions.html
│       └── partials
│           └── conteneur.html
├── README.md
├── requirement.txt
├── run.py
└── Utils
    ├── dashboard.py
    ├── doc_info.py
    ├── __init__.py
    ├── insert_json_db.py
    └── software_mentions.py

```

---
##  Getting Started

**System Requirements:**

* **Python**: `version 3.`

###  Installation

<h4>From <code>source</code></h4>

> 1. Clone the  repository:
>
> ```console
> git clone ../
> ```
>
> 2. Change to the project directory:
> ```console
> cd ./SOFTware-viz
> ```
>
> 3. Create a virtualenv:
> ```console
> python -m venv env
> ```
>
> 4. Install docker image
> ```console
> docker pull arangodb/arangodb:3.11.6
> ```
>
> 5. Launch docker container
> ```console
> docker run -p 8529:8529 -e ARANGO_NO_AUTH=1 arangodb/arangodb:3.11.6
> ```
>
> 6. Create the database "SOF-viz"
>```
> go to the port http://localhost:8529/ and create mannualy the database named "SOF-viz"
>```
>
> 7. Launch the virtualenv
> ```console
> source env/bin/activate
> ```
>
> 8. Install the dependencies:
> ```console
> pip install -r requirement.txt
> ```
> 
> 9. Launch the app
> ```console
> python run.py
> ```
>
###  Usage

<h4>From <code>source</code></h4>

> Run  using the command below:
> ```console
> (env) python run.py
> ```

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
