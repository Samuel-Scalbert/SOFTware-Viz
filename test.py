from wikibaseintegrator import WikibaseIntegrator
from app.app import app, db, data_dashboard
import requests

# All softwares
query = """
        for soft in softwares
        return distinct soft.software_name.normalizedForm
"""
software_list = db.AQLQuery(query,rawResults=True, batchSize=10000)

#Ropenscience

'''url = 'https://ropensci.r-universe.dev/api/ls'
request = requests.get(url)

for software in software_list:
    if software in request:
        print(request)'''

# Wikidata
wbi = WikibaseIntegrator()
wikidata_url = "https://query.wikidata.org/sparql"

for software in software_list:
    query = f"""
        SELECT DISTINCT ?software ?softwareLabel WHERE {{
          ?software wdt:P31/wdt:P279* wd:Q7397;
                    rdfs:label ?softwareLabel.
          FILTER(LANG(?softwareLabel) = "en" && CONTAINS(?softwareLabel, "{software}"))
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
        """
    response = requests.get(wikidata_url, params={'query': query, 'format': 'json'})
    if response.status_code == 200:
        data = response.json()
        software_list = [item['softwareLabel']['value'] for item in data['results']['bindings']]
        if len(software_list) == 0:
            continue
        print(f'Searching for: {software} in {software_list}')
        for item in data['results']['bindings']:
            if software == item['softwareLabel']['value']:
                software_id_wkd = item['software']['value'].replace('http://www.wikidata.org/entity/','')
                wikidata_item = wbi.item.get(entity_id=software_id_wkd)
                wikidata_item_json = wikidata_item.get_json()
                wikidata_item_json_fr = {"labels" : wikidata_item_json["labels"]['en'],
                                        "descriptions" : wikidata_item_json["descriptions"]['en'],
                                        "aliases" : wikidata_item_json["aliases"]['en'],
                                        "type" : wikidata_item_json["type"],
                                        "id" : wikidata_item_json["id"],
                                        "wikidata_id" : software_id_wkd}
                print(wikidata_item_json_fr)
                break
    else:
        print(f"Failed to fetch data for {software} from Wikidata: {response.status_code}")


