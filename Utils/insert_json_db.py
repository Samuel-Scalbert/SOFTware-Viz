import os
import json
from tqdm import tqdm
import xml.etree.ElementTree as ET
import requests
import time

def insert_json_db (data_path_json,data_path_xml,db):

    if db.hasCollection('documents'):
        documents_collection = db['documents']
    else:
        db.createCollection('Collection', name='documents')
        documents_collection = db['documents']

    if db.hasCollection('softwares'):
        softwares_collection = db['softwares']
    else:
        db.createCollection('Collection', name='softwares')
        softwares_collection = db['softwares']

    if db.hasCollection('references'):
        references_collection = db['references']
    else:
        db.createCollection('Collection', name='references')
        references_collection = db['references']

    if db.hasCollection('edge_software'):
        doc_soft_edge = db['edge_software']
    else:
        db.createCollection('Edges', name='edge_software')
        doc_soft_edge = db['edge_software']

    if db.hasCollection('edge_reference'):
        doc_ref_edge = db['edge_reference']
    else:
        db.createCollection('Edges', name='edge_reference')
        doc_ref_edge = db['edge_reference']


    data_json_files = os.listdir(data_path_json)
    data_xml_list = os.listdir(data_path_xml)
    files_list_registered = db.AQLQuery('FOR hal_id in documents RETURN hal_id.file_hal_id', rawResults=True)

    for data_file_xml in tqdm(data_xml_list):
        file_path = f'{data_path_xml}/{data_file_xml}'
        file_name = os.path.basename(file_path)
        while "." in file_name:
            file_name, extension = os.path.splitext(file_name)

        if file_name in files_list_registered:
            continue
        time.sleep(0.2)
        url = "https://api.archives-ouvertes.fr/search/"
        params = {
            "q": f"halId_id:{file_name}",
            "rows": 10,
            "fl": "citationFull_s"
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            try:
                citations = data["response"]["docs"][0]["citationFull_s"]
            except IndexError:
                citations = None
        else:
            print("Error:", response.status_code)

        with open(file_path, 'r', encoding='utf-8') as xml_file:
            data_json_get_document = {}
            tree = ET.parse(xml_file)
            root = tree.getroot()
            ns = {"tei": "http://www.tei-c.org/ns/1.0"}

            title = tree.find(".//tei:listBibl//tei:titleStmt//tei:title", ns)
            title = title.text

            structures = tree.find(".//tei:back//tei:listOrg", ns)
            list_org = []
            for org in structures:
                if org.attrib['type'] in ['regrouplaboratory','regroupinstitution','institution']:
                    for org_child_tags in list(org):
                        try:
                            if org_child_tags.attrib['type'] == 'acronym':
                                list_org.append(org_child_tags.text)
                        except KeyError:
                            continue
            data_json_get_document['structures'] = list_org

            doc_type = tree.findall(".//tei:listBibl//tei:biblFull//tei:profileDesc//tei:textClass//tei:classCode", ns)
            for tag in doc_type:
                if tag.attrib.get('n') == 'COMM':
                    production_date = tree.find(".//tei:listBibl//tei:biblFull//tei:sourceDesc//tei:biblStruct//tei:monogr//tei:meeting//tei:date[@type='start']", ns)
                    if production_date is not None:
                        data_json_get_document['date'] = production_date.text[:4]
                else:
                    production_date = tree.find(
                        ".//tei:listBibl//tei:biblFull//tei:sourceDesc//tei:biblStruct//tei:monogr//tei:imprint//tei:date[@type='datePub']",
                        ns)
                    if production_date is not None:
                        data_json_get_document['date'] = production_date.text[:4]
                    else:
                        production_date = tree.find(
                            ".//tei:listBibl//tei:biblFull//tei:editionStmt//tei:edition[@type='current']//tei:date[@type='whenProduced']",
                            ns)
                        if production_date is not None:
                            data_json_get_document['date'] = production_date.text[:4]
                        else:
                            print(f'problem : {file_name}')
            author_list = tree.findall(".//tei:listBibl//tei:titleStmt//tei:author", ns)
            list_author = []
            for elm in author_list:
                author = {}
                persName = elm.find("{http://www.tei-c.org/ns/1.0}persName")
                author['role'] = elm.attrib['role']
                for name in persName:
                    author[name.tag.split('}')[1]] =  name.text
                list_author.append(author)

            abstract = tree.find(".//{http://www.tei-c.org/ns/1.0}abstract")
            if abstract:
                tag_text = list(abstract)[0]
                if tag_text.tag == '{http://www.tei-c.org/ns/1.0}p':
                    abstract = "".join(tag_text.itertext())
                    data_json_get_document['abstract'] = ['HAL' , abstract]
                if tag_text.tag == '{http://www.tei-c.org/ns/1.0}div':
                    for p_tag in list(tag_text):
                        text = "".join(p_tag.itertext())
                    data_json_get_document['abstract'] = ['GROBID' , abstract]

            data_json_get_document['file_hal_id'] = file_name
            data_json_get_document['citation'] = citations
            data_json_get_document['title'] = title
            data_json_get_document['author'] = list_author

            document_document = documents_collection.createDocument(data_json_get_document)
            document_document.save()
            if f"{file_name}.software.json" in data_json_files:
                with open(f'{data_path_json}/{file_name}.software.json', 'r') as json_file:
                    data_json = json.load(json_file)

                    data_json_get_mentions = data_json.get("mentions")
                    for data_json_get_mention in data_json_get_mentions:
                        data_json_get_mention['software_name'] = data_json_get_mention['software-name']
                        data_json_get_mention.pop('software-name')
                        data_json_get_mention['software_type'] = data_json_get_mention['software-type']
                        data_json_get_mention.pop('software-type')
                        software_document = softwares_collection.createDocument(data_json_get_mention)
                        software_document.save()

                        edge = doc_soft_edge.createEdge()
                        edge['_from'] = document_document._id
                        edge['_to'] = software_document._id
                        edge.save()

                    data_json_get_references = data_json.get("references")
                    for data_json_get_reference in data_json_get_references:
                        references_document = references_collection.createDocument(data_json_get_reference)
                        references_document.save()

                        edge = doc_ref_edge.createEdge()
                        edge['_from'] = document_document._id
                        edge['_to'] = references_document._id
                        edge.save()
