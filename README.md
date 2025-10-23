<p align="center">
    <h1 align="center">SOFTware-Viz</h1>
</p>
<div align="center">
  <img src="https://github.com/user-attachments/assets/43b01db2-450e-4d9d-a805-cb37f861bdb2" alt="logo_full_HUB" width="250" />
</div>

<div style="text-align: center; margin-bottom: 20px;" align="center">
	<img src="https://img.shields.io/github/last-commit/Samuel-Scalbert/SOFTware-Viz?style=default&logo=git&logoColor=white&color=44a7e4" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/Samuel-Scalbert/SOFTware-Viz?style=default&color=6598ef" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/Samuel-Scalbert/SOFTware-Viz?style=default&color=9283ec" alt="repo-language-count">
	<img src="https://badgen.net/github/commits/Samuel-Scalbert/SOFTware-Viz/main?style=default&color=bd67d6" alt="repo-commits-count">
    <img src="https://img.shields.io/github/issues/Samuel-Scalbert/SOFTware-Viz?style=default&color=de42af" alt="open-issues">
    <img src="https://img.shields.io/github/issues-closed/Samuel-Scalbert/SOFTware-Viz?style=default&color=ee0979" alt="closed-issues">
</div>

## Présentation du projet

🛑 Cette application est conçue pour interagir avec **HAL** et récolter des métadonnées liées à la base de données.

🛑 Une version plus légère de l’application est en cours de développement, permettant à chacun de créer sa propre application sans nécessiter de connexion à **HAL**.

-> [SOFTware-Viz-Light](https://github.com/Samuel-Scalbert/SOFTware-Viz-Light)

### Base de données de PDF
Le processus commence avec une base de données de fichiers **PDF** académiques qui doivent être extraits et traités.

### GROBID
Les fichiers **PDF** sont envoyés à **GROBID**, un outil permettant d’extraire des données structurées (comme des informations bibliographiques) à partir de **PDF** académiques. **GROBID** génère en sortie des fichiers **XML**, rendant l’information lisible par machine.

### SOFTCITE
Après **GROBID**, les données extraites sont transmises à **SOFTCITE**, qui génère des fichiers **JSON**. **SOFTCITE** analyse les citations, les mentions de logiciels ou d’autres informations de référence présentes dans les **PDF**.

### SOFTware-Sync
Les fichiers **XML** et **JSON** extraits sont ensuite traités par **SOFTware-Sync**, un outil qui synchronise ces données dans un fichier **XML** unique.

### SOFTware-Viz
**SOFTware-Viz** est chargé de la visualisation des données traitées. Il prend les données synchronisées par **SOFTware-Sync** et les transforme en **tableaux de bord** ou autres représentations graphiques.

### ArangoDB
Les données traitées sont stockées dans **ArangoDB**, une base de données **NoSQL multi-modèle**, permettant la gestion des données structurées. Elle sert de stockage principal pour les informations et mentions extraites.

### Flask
**Flask** est un framework web utilisé pour développer des applications web. Il interagit avec **SOFTware-Viz** (pour la visualisation) et **ArangoDB** (pour la récupération des données).

---

## Installation

#### Depuis `la source`

* Clonez le dépôt :<br>
```console
git clone ../
```
* Accédez au répertoire du projet :<br>
```console
cd ./SOFTware-viz
```
* Créez un environnement virtuel :<br>
```console
python -m venv env
```
* Installez l’image **Docker** :<br>
```console
docker pull arangodb/arangodb:3.11.6
```
* Lancez un conteneur **Docker** :<br>
```console
docker run -p 8529:8529 -e ARANGO_NO_AUTH=1 arangodb/arangodb:3.11.6
```
* Installez l’image **Elasticsearch** :<br>
```console
docker pull docker.elastic.co/elasticsearch/elasticsearch:9.0.2
```
* Lancez un conteneur **Docker** :<br>
```console
sudo docker run -d \
  --name elasticsearch \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" \
  -e "xpack.security.enabled=false" \
  --memory="2g" \
  docker.elastic.co/elasticsearch/elasticsearch:9.0.2
```
* Activez l’environnement virtuel :<br>
```console
source env/bin/activate
```
* Installez les dépendances :<br>
```console
pip install -r requirement.txt
```
* Lancez l’application :    
```console
python run.py
```
---

## Utilisation

#### Depuis `la source`

Exécutez l’application avec la commande suivante (**la base de données se créera automatiquement lors du premier lancement**) :

```
python run.py
```
