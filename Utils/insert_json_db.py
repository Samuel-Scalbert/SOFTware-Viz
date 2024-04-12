import os
import json
from tqdm import tqdm

def insert_json_db (data_path,db):

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


    data_files = os.listdir(data_path)
    files_list_registered = db.AQLQuery('FOR hal_id in documents RETURN hal_id.md5', rawResults=True)


    for data_file in tqdm(data_files, colour='white'):
        if data_file.endswith('.software.json'):
            with open(data_path + '/' + data_file, 'r') as json_file:
                data_json = json.load(json_file)
                data_md5 = data_json.get("md5")

                if data_md5 in files_list_registered:
                    continue

                data_json_get_document = {key: value for key, value in data_json.items() if key not in ['references', 'mentions', 'original_file_path']}
                data_file = data_file.replace('.software.json','')
                data_json_get_document['file_id'] = data_file
                document_document = documents_collection.createDocument(data_json_get_document)
                document_document.save()

                data_json_get_mentions = data_json.get("mentions")
                for data_json_get_mention in data_json_get_mentions:
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
