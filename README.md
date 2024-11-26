<p align="center">
    <h1 align="center">SOFTware-Viz</h1>
</p>
<div align="center">
  <img src="https://github.com/user-attachments/assets/43b01db2-450e-4d9d-a805-cb37f861bdb2" alt="logo_full_HUB" width="250" />
</div>

<p align="center">
	<!-- local repository, no metadata badges. -->
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/HTML5-E34F26.svg?style=default&logo=HTML5&logoColor=white" alt="HTML5">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=default&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/github/last-commit/Samuel-Scalbert/SOFTware-Viz?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/Samuel-Scalbert/SOFTware-Viz?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/Samuel-Scalbert/SOFTware-Viz?style=default&color=0080ff" alt="repo-language-count">
</p>

![Capture d’écran du 2024-06-03 16-39-41](https://github.com/Samuel-Scalbert/SOFTware-Viz/assets/32683708/6be2a593-0508-4e52-a7cb-2cf28b768f00)

![Capture d’écran du 2024-10-18 10-44-19](https://github.com/user-attachments/assets/e8d7bcea-9881-49af-abfc-d92f536b9233)

## Presentation of the project

🛑 This application is currently designed to interact with and harvest metadata from HAL linked to the database.

🛑 A lighter version of the application is under development, allowing anyone to create their own application without requiring a connection to HAL.

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

---
##  Installation

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

> Run  using the command below (the database will create itself only on the first launch):
> ```console
> python run.py
> ```

---
##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.
