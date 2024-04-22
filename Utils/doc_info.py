from pyArango.theExceptions import AQLQueryError
from collections import defaultdict

def doc_info_from_id(file_id,db):
    try:
        file_meta = db.AQLQuery("FOR file_meta in documents FILTER file_meta.file_hal_id == '"+ file_id +"'  RETURN file_meta", rawResults=True)
        print(file_meta)
        file_meta_id = file_meta[0]['_id']
    except AQLQueryError:
        file_meta = 'not file'
        return file_meta
    result = []
    for id_software_doc in db['edge_software'].getEdges(file_meta_id):
        to_id = id_software_doc['_to']
        json_software = db.AQLQuery("LET file_meta = DOCUMENT('"+to_id+"') RETURN file_meta", rawResults=True)
        json_software = json_software[0]
        software_name = json_software['software-name']['normalizedForm']
        max_score = float('-inf')
        max_attribute = None

        for attribute, details in json_software["documentContextAttributes"].items():
            if details["score"] > max_score:
                max_score = details["score"]
                max_attribute = attribute
                attr_software = {"ContextAttributes": max_attribute}
        result.append([software_name,attr_software])

    software_counts = defaultdict(lambda: defaultdict(int))

    for software, attributes in result:
        context_attribute = attributes['ContextAttributes']
        software_counts[software][context_attribute] += 1

    software_counts = dict(software_counts)

    return software_counts